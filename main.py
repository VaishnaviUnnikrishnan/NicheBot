import os
from fastapi import FastAPI, Form, File, UploadFile, HTTPException, Request, Depends, BackgroundTasks
from pydantic import BaseModel
from typing import Optional, List
from motor.motor_asyncio import AsyncIOMotorClient
import base64
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets
from datetime import datetime, timedelta
import asyncio
from response import LimelightResponseSystem
import csv
from bson import ObjectId
from bot import generate_response
import pandas as pd
import numpy as np

app = FastAPI()

# Initialize templates
templates = Jinja2Templates(directory="templates")
templates.env.globals.update(enumerate=enumerate)

# Database setup
MONGO_URI = "mongodb://localhost:27017"
client = AsyncIOMotorClient(MONGO_URI)
db = client["niche_community"]
users_collection = db["users"]
posts_collection = db["posts"]
comments_collection = db["comments"]
google_collection = db["Google"]

# Initialize Limelight response system
limelight = LimelightResponseSystem()

security = HTTPBasic()


async def verify_user(username: str, password: str):
    user = await users_collection.find_one({"username": username, "password": password})
    if user:
        return user
    return None


@app.get("/view_response_report", response_class=HTMLResponse)
async def view_response_report(request: Request):
    username = request.cookies.get("username")
    if not username or username != "NicheBot":  # Changed to admin for broader access
        raise HTTPException(status_code=403, detail="Only admin can access this page")

    try:
        df = pd.read_csv("survey_responses.csv")
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="No survey responses found")

    metric_labels = [
        "Relevance", "Accuracy", "Clarity", "Conciseness", "Completeness",
        "Bias", "Grammar", "References", "Human-like", "Specificity",
        "Novelty", "Factual Accuracy", "Offensiveness", "Trustworthiness",
        "Expectation Alignment", "Structure", "Understanding", "Recommendation",
        "Overall Satisfaction"
    ]

    metric_scores = [df[f"Q{i + 1}"].mean() for i in range(19)]
    overall_satisfaction = df["Q20"].mean()

    score_distribution = [
        {"name": "Excellent (5)", "y": len(df[df["Q20"] == 5])},
        {"name": "Good (4)", "y": len(df[df["Q20"] == 4])},
        {"name": "Average (3)", "y": len(df[df["Q20"] == 3])},
        {"name": "Poor (2)", "y": len(df[df["Q20"] == 2])},
        {"name": "Very Poor (1)", "y": len(df[df["Q20"] == 1])}
    ]

    time_labels = ["Day 1", "Day 2", "Day 3", "Day 4", "Day 5"]
    trend_data = [4.2, 4.5, 4.1, 4.3, 4.4]

    recommendations = []
    for i, score in enumerate(metric_scores):
        if score < 3:
            recommendations.append(f"Improve {metric_labels[i]} (Current Score: {score:.2f})")

    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "average_scores": {
            "overall_satisfaction": overall_satisfaction,
            "relevance": metric_scores[0],
            "accuracy": metric_scores[1]
        },
        "metric_labels": metric_labels,
        "metric_scores": metric_scores,
        "score_distribution": score_distribution,
        "time_labels": time_labels,
        "trend_data": trend_data,
        "recommendations": recommendations
    })


@app.get("/limelight_stats", response_class=HTMLResponse)
async def get_limelight_stats(request: Request):
    username = request.cookies.get("username")
    if not username or username != "admin":
        raise HTTPException(status_code=403, detail="Access denied")

    recent_posts = await limelight.get_recent_oracle_posts()
    limelight_comments = await comments_collection.count_documents({"author": "Limelight"})

    return templates.TemplateResponse("limelight_stats.html", {
        "request": request,
        "recent_posts": len(recent_posts),
        "total_responses": limelight_comments,
        "posts": recent_posts[:10]
    })


@app.get("/countries")
async def get_countries():
    countries = ["United States", "India", "Canada", "Germany", "France", "Japan", "United Kingdom", "Australia"]
    return {"countries": countries}


@app.post("/signup")
async def signup(
        username: str = Form(...),
        role: str = Form(...),
        first_name: str = Form(...),
        last_name: str = Form(...),
        areas_of_interest: str = Form(...),
        bio: Optional[str] = Form(None),
        micro_influencer: str = Form(...),
        allow_companies: Optional[str] = Form(None),
        country: str = Form(...),
        stay_informed: str = Form(...),
        profile_picture: Optional[UploadFile] = File(None),
        password: str = Form(...)
):
    try:
        micro_influencer_bool = micro_influencer.lower() == "true"
        allow_companies_bool = allow_companies.lower() == "true" if allow_companies else None
        areas_of_interest_list = [x.strip() for x in areas_of_interest.split(",")]

        profile_pic_base64 = None
        if profile_picture:
            profile_pic_base64 = base64.b64encode(await profile_picture.read()).decode()

        user_data = {
            "username": username,
            "role": role,
            "first_name": first_name,
            "last_name": last_name,
            "areas_of_interest": areas_of_interest_list,
            "bio": bio,
            "micro_influencer": micro_influencer_bool,
            "allow_companies": allow_companies_bool,
            "country": country,
            "stay_informed": stay_informed,
            "profile_picture": profile_pic_base64,
            "password": password
        }

        await users_collection.insert_one(user_data)
        return {"message": "User registered successfully!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/login")
async def login(request: Request, username: str = Form(...), password: str = Form(...)):
    user = await verify_user(username, password)
    if user:
        response = RedirectResponse(url="/home", status_code=303)
        response.set_cookie(key="username", value=username)
        return response
    else:
        return RedirectResponse(url="/", status_code=303)


@app.get("/home", response_class=HTMLResponse)
async def home(request: Request):
    username = request.cookies.get("username")
    if not username:
        return RedirectResponse(url="/", status_code=303)
    return templates.TemplateResponse("home.html", {"request": request, "username": username})


@app.get("/profile", response_class=HTMLResponse)
async def profile(request: Request):
    username = request.cookies.get("username")
    if not username:
        return RedirectResponse(url="/", status_code=303)

    user = await users_collection.find_one({"username": username})
    return templates.TemplateResponse("profile.html", {"request": request, "user": user})


@app.post("/edit_profile")
async def edit_profile(
        request: Request,
        bio: Optional[str] = Form(None),
        areas_of_interest: Optional[str] = Form(None),
        profile_picture: Optional[UploadFile] = File(None)
):
    username = request.cookies.get("username")
    if not username:
        return RedirectResponse(url="/", status_code=303)

    update_data = {}
    if bio:
        update_data["bio"] = bio
    if areas_of_interest:
        update_data["areas_of_interest"] = [x.strip() for x in areas_of_interest.split(",")]
    if profile_picture:
        profile_pic_base64 = base64.b64encode(await profile_picture.read()).decode()
        update_data["profile_picture"] = profile_pic_base64

    if update_data:
        await users_collection.update_one({"username": username}, {"$set": update_data})

    return RedirectResponse(url="/profile", status_code=303)


@app.get("/community", response_class=HTMLResponse)
async def community(request: Request):
    username = request.cookies.get("username")
    if not username:
        return RedirectResponse(url="/", status_code=303)

    posts = await posts_collection.find({}).to_list(100)
    for post in posts:
        post["comments"] = await comments_collection.find({"post_id": str(post["_id"])}).to_list(100)
        post["has_google_reply"] = any(comment["author"].lower() == "google bot" for comment in post["comments"])
        post["has_limelight_reply"] = any(comment["author"].lower() == "limelight" for comment in post["comments"])

    return templates.TemplateResponse("community.html", {
        "request": request,
        "username": username,
        "posts": posts
    })


@app.post("/create_post")
async def create_post(
        request: Request,
        background_tasks: BackgroundTasks,
        title: str = Form(...),
        content: str = Form(...)
):
    username = request.cookies.get("username")
    if not username:
        return RedirectResponse(url="/", status_code=303)

    post_data = {
        "title": title,
        "content": content,
        "author": username,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "limelight_processed": False
    }

    try:
        result = await posts_collection.insert_one(post_data)

        # Check if post is Oracle-related for Limelight response
        if any(keyword.lower() in (title + " " + content).lower()
               for keyword in ["oracle", "database", "sql", "pl/sql"]):
            background_tasks.add_task(limelight.generate_limelight_response, post_data)

        return RedirectResponse(url="/community", status_code=303)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/add_comment")
async def add_comment(request: Request, post_id: str = Form(...), comment: str = Form(...)):
    username = request.cookies.get("username")
    if not username:
        return RedirectResponse(url="/", status_code=303)

    comment_data = {
        "post_id": post_id,
        "comment": comment,
        "author": username,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    await comments_collection.insert_one(comment_data)
    return RedirectResponse(url="/community", status_code=303)


@app.get("/survey/{post_id}/{comment_id}", response_class=HTMLResponse)
async def survey(request: Request, post_id: str, comment_id: str):
    try:
        post_object_id = ObjectId(post_id)
        comment_object_id = ObjectId(comment_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid post or comment ID")

    post = await posts_collection.find_one({"_id": post_object_id})
    comment = await comments_collection.find_one({"_id": comment_object_id})

    if not post or not comment:
        raise HTTPException(status_code=404, detail="Post or comment not found")

    # Allow evaluation of both Limelight and Google Bot responses
    if (comment["author"].lower() not in ["limelight", "google bot"] or
            post["author"] != request.cookies.get("username")):
        raise HTTPException(status_code=403, detail="You can only evaluate bot responses to your own posts")

    questions = [
        "Was the response relevant to the question?",
        "Did the response provide accurate information?",
        "Was the response easy to understand?",
        "Did the response include unnecessary information?",
        "Was the response concise?",
        "Did the response address all parts of the question?",
        "Was the response biased in any way?",
        "Was the response grammatically correct?",
        "Did the response provide sources or references?",
        "Did the response feel human-like?",
        "Was the response too generic?",
        "Did the response provide new information?",
        "Was the response free from factual errors?",
        "Did the response include any offensive content?",
        "Would you trust this response?",
        "Did the response align with your expectations?",
        "Was the response structured well?",
        "Did the response improve your understanding?",
        "Would you recommend this response to someone else?",
        "Overall, how satisfied are you with the response?"
    ]

    return templates.TemplateResponse("survey.html", {
        "request": request,
        "post_id": post_id,
        "comment_id": comment_id,
        "questions": questions,
        "bot_name": comment["author"]
    })


@app.post("/submit_survey")
async def submit_survey(
        request: Request,
        post_id: str = Form(...),
        bot_reply_id: str = Form(...)
):
    form_data = await request.form()
    responses = {f"Q{i + 1}": form_data.get(f"q{i + 1}") for i in range(20)}

    # Create the CSV file if it doesn't exist
    csv_file = "survey_responses.csv"
    file_exists = os.path.exists(csv_file)

    with open(csv_file, mode="a", newline="") as file:
        writer = csv.writer(file)

        # Write headers if file is new
        if not file_exists:
            headers = ["post_id", "bot_reply_id"] + [f"Q{i + 1}" for i in range(20)]
            writer.writerow(headers)

        # Write the data
        writer.writerow([post_id, bot_reply_id] + [responses[f"Q{i + 1}"] for i in range(20)])

    return RedirectResponse(url="/community", status_code=303)


@app.on_event("startup")
async def startup_event():
    asyncio.create_task(limelight.monitor_new_posts())


@app.get("/logout")
async def logout():
    response = RedirectResponse(url="/", status_code=303)
    response.delete_cookie(key="username")
    return response


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)