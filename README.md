# NicheBot - AI-Powered Conversational Assistant

## Overview
NicheBot is an AI-powered chatbot designed to enhance discussions in niche online communities. Utilizing **Natural Language Processing (NLP) and Machine Learning (ML)**, it identifies relevant conversations, generates insightful responses, and fosters user engagement across various platforms.

## Features
- **Conversation Identification & Response Generation**: Extracts data from **RSS feeds, Q&A platforms (Reddit, Discord, Stack Overflow), and niche blogs** using web scraping.
- **Topic Modeling**: Uses **Latent Dirichlet Allocation (LDA) and Naïve Bayes** to categorize discussions accurately.
- **Sentiment Analysis**: Analyzes emotional tone in conversations using a model trained on Kaggle’s Twitter dataset.
- **Real-Time Processing**: Stores models as **.pkl files**, vectorized using **TF-IDF & Count Vectorizer** for efficient response generation.
- **FastAPI-Powered Backend**: Integrates AI models with **MongoDB**, allowing users to **register, post blogs, and engage in discussions**.
- **Contextual Responses**: Uses **MiniLM-L6-v2** and **Together AI API** to generate relevant, high-quality replies.
- **Slack Integration**: Engages users in workspace communities with real-time discussions.
- **Impact Measurement**: Collects user feedback stored in **CSV format**, visualized in a real-time **Highcharts dashboard**.

## Tech Stack & Concepts
- **Programming Languages**: Python
- **Frameworks & APIs**: FastAPI, Together AI API
- **Databases**: MongoDB
- **NLP & ML Models**: LDA, Naïve Bayes, MiniLM-L6-v2
- **Sentiment Analysis**: Kaggle-based Twitter dataset
- **Vectorization**: TF-IDF, Count Vectorizer
- **Web Scraping**: BeautifulSoup, Scrapy
- **Data Storage & Visualization**: JSON, CSV, Highcharts
- **Deployment & Integration**: Slack Bot API

## Installation & Setup
1. Clone the repository:
   ```sh
   git clone https://github.com/VaishnaviUnnikrishnan/NicheBot.git
   cd NicheBot
   ```
2. Set up a virtual environment:
   ```sh
   python -m venv venv
   source venv/bin/activate  # Mac/Linux
   venv\Scripts\activate  # Windows
   ```
3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
4. Run the application:
   ```sh
   uvicorn main:app --reload
   ```


## Future Enhancements
- Expand chatbot integration to additional platforms like Telegram and Discord.
- Improve topic modeling with transformer-based models.
- Develop an interactive admin dashboard for conversation insights.

## License
This project is licensed under the MIT License.

## Contact
For inquiries, reach out to v.ukrishnan8@gmail.com.


![image](https://github.com/user-attachments/assets/ca7934db-205c-47bb-813c-d4c6b1a3e68d)

![image](https://github.com/user-attachments/assets/6e8ec346-7da9-4a93-bd69-55d851c39d7f)

![image](https://github.com/user-attachments/assets/ea9a6d9e-9c3f-4deb-a0c3-4bf28a9cdda7)

![image](https://github.com/user-attachments/assets/5cd389c1-9974-4523-b16b-5435dee5c91e)

![image](https://github.com/user-attachments/assets/c228c80c-c7fc-4e70-8c6c-a4416a85c69a)

![image](https://github.com/user-attachments/assets/f6c148d7-216b-4114-9446-66b18401900c)
