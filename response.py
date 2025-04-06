import asyncio
from datetime import datetime
from bson import ObjectId
from bot import generate_response
from typing import List, Dict, Optional
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel


class Post(BaseModel):
    title: str
    content: str
    author: str
    timestamp: str


class Comment(BaseModel):
    post_id: str
    comment: str
    author: str
    timestamp: str


class LimelightResponseSystem:
    def __init__(self, db_uri: str = "mongodb://localhost:27017"):
        self.client = AsyncIOMotorClient(db_uri)
        self.db = self.client["niche_community"]
        self.posts_collection = self.db["posts"]
        self.comments_collection = self.db["comments"]

        # Oracle-related keywords that trigger Limelight responses
        self.oracle_keywords = [
            "oracle", "database", "sql", "pl/sql", "cloud", "oci",
            "autonomous", "ebs", "fusion", "apex", "java", "net",
            "erp", "crm", "hcm", "financials", "supply chain"
        ]

    async def monitor_new_posts(self):
        """Monitor new posts for Oracle-related content"""
        while True:
            try:
                # Get the latest posts (last 5 minutes)
                time_threshold = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                query = {
                    "timestamp": {"$gte": time_threshold},
                    "limelight_processed": {"$exists": False}
                }

                new_posts = await self.posts_collection.find(query).to_list(100)

                for post in new_posts:
                    if self._is_oracle_related(post["title"] + " " + post["content"]):
                        await self.generate_limelight_response(post)
                        # Mark post as processed
                        await self.posts_collection.update_one(
                            {"_id": post["_id"]},
                            {"$set": {"limelight_processed": True}}
                        )

                await asyncio.sleep(300)  # Check every 5 minutes
            except Exception as e:
                print(f"Error in monitor_new_posts: {str(e)}")
                await asyncio.sleep(60)

    def _is_oracle_related(self, text: str) -> bool:
        """Check if text contains Oracle-related keywords"""
        text_lower = text.lower()
        return any(keyword in text_lower for keyword in self.oracle_keywords)

    async def generate_limelight_response(self, post: Dict) -> Optional[Dict]:
        """Generate a response to an Oracle-related post using the bot.py functionality"""
        try:
            # Generate response using the bot's functionality
            query = f"Post title: {post['title']}\nPost content: {post['content']}"
            response_text = generate_response(query)

            # Create and store the comment
            comment = {
                "post_id": str(post["_id"]),
                "comment": response_text,
                "author": "Limelight",
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "is_automated": True
            }

            result = await self.comments_collection.insert_one(comment)
            return {"comment_id": str(result.inserted_id)}
        except Exception as e:
            print(f"Error generating Limelight response: {str(e)}")
            return None

    async def get_recent_oracle_posts(self, hours: int = 24) -> List[Dict]:
        """Get recent Oracle-related posts for analysis"""
        time_threshold = (datetime.now() - timedelta(hours=hours)).strftime("%Y-%m-%d %H:%M:%S")
        posts = await self.posts_collection.find({
            "timestamp": {"$gte": time_threshold}
        }).to_list(100)

        return [post for post in posts if self._is_oracle_related(post["title"] + " " + post["content"])]

    async def close(self):
        """Clean up resources"""
        self.client.close()