import praw
import oracledb
import cohere

# Reddit API Configuration
user_agent = 'Scraper 1.0 by /u/hamza'
reddit = praw.Reddit(
    client_id="***",
    client_secret="****",
    user_agent=user_agent
)

# Oracle Database Configuration
conn = oracledb.connect(
    user="HAMZA",
    password="Oracle21c",
    dsn="localhost:1521/orclcdb"
)
cursor = conn.cursor()

# Cohere API Configuration
cohere_api_key = '****'
co = cohere.Client(cohere_api_key)
