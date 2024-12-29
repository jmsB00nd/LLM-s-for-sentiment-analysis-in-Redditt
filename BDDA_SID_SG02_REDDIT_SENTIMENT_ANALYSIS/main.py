from config import reddit, conn, cursor, co
from scraper import scrape_and_analyze

subreddits = ["storys"]
posts_per_subreddit = 15
comments_per_post = 5

try:
    scrape_and_analyze(cursor, reddit, co, subreddits, posts_per_subreddit, comments_per_post)
    conn.commit()
    print("Data inserted successfully!")
except Exception as e:
    print(f"Error occurred: {e}")
    conn.rollback()
finally:
    cursor.close()
    conn.close()
