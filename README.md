# NicheBot
NicheBot is an AI-powered conversational assistant designed to enhance discussions in niche online communities. 

NicheBot is an AI-powered conversational assistant designed to enhance discussions in niche online
communities. By leveraging Natural Language Processing (NLP) and Machine Learning (ML), NicheBot identifies relevant conversations, generates insightful responses, and fosters engagement among users.
The system collects data from RSS feeds, Q&A platforms (Reddit, Discord, Stack Overflow), and niche blog discussions through web scraping. The extracted data is preprocessed and stored in a JSON file for further analysis.Topic modeling is implemented using Latent Dirichlet Allocation (LDA) and Naïve
Bayes, allowing the system to categorize discussions accurately. To analyze sentiment, a Sentiment
Analysis Model trained on Kaggle’s Twitter dataset evaluates the emotional tone behind conversations. These models are stored as .pkl files and vectorized for real-time processing.
A FastAPI-powered backend integrates the AI models with a MongoDB database, enabling users to register, post blogs, and engage in discussions. All comments are monitored by MiniLM-L6-v2, a
transformer-based NLP model that generates contextual responses using Together AI's API. This ensures high-quality, meaningful interactions.If a user posts about technology, NicheBot automatically engages, providing relevant responses and encouraging discussions. The chatbot is also integrated with Slack,
enabling seamless interaction within workspace communities. The system’s accuracy and effectiveness are measured through a user feedback survey, with results stored in a CSV file. The collected metrics power a real-time impact dashboard created using Highcharts.
Tech Stack & Concepts

•	Programming Languages: Python

•	Frameworks & APIs: FastAPI, Together AI API

•	Databases: MongoDB

•	NLP & ML Models: LDA, Naïve Bayes, MiniLM-L6-v2

•	Sentiment Analysis: Kaggle-based Twitter dataset

•	Vectorization: TF-IDF, Count Vectorizer

•	Web Scraping: BeautifulSoup, Scrapy

•	Data Storage & Visualization: JSON, CSV, Highcharts

•	Deployment & Integration: Slack Bot API
![image](https://github.com/user-attachments/assets/ca7934db-205c-47bb-813c-d4c6b1a3e68d)

![image](https://github.com/user-attachments/assets/6e8ec346-7da9-4a93-bd69-55d851c39d7f)

![image](https://github.com/user-attachments/assets/ea9a6d9e-9c3f-4deb-a0c3-4bf28a9cdda7)

![image](https://github.com/user-attachments/assets/5cd389c1-9974-4523-b16b-5435dee5c91e)

![image](https://github.com/user-attachments/assets/c228c80c-c7fc-4e70-8c6c-a4416a85c69a)

![image](https://github.com/user-attachments/assets/f6c148d7-216b-4114-9446-66b18401900c)
