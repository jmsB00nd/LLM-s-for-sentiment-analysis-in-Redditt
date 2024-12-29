from utils import analyze_sentiment, generate_prompt, cohere_generate, generate_sentiment_analysis
from database import insert_subreddit, insert_post, insert_comment

def scrape_and_analyze(cursor, reddit, co, subreddits, posts_per_subreddit, comments_per_post):
    for subreddit_name in subreddits:
        print(f"Processing subreddit: {subreddit_name}")
        subreddit = reddit.subreddit(subreddit_name)
        subreddit_data = {
            "subreddit_id": subreddit.id,
            "name": subreddit.display_name,
            "description": subreddit.public_description,
            "subscriber_count": subreddit.subscribers,
            "active_users": subreddit.accounts_active,
            "created_at": subreddit.created_utc
        }
        insert_subreddit(cursor, subreddit_data)

        for post in subreddit.hot(limit=posts_per_subreddit):
            label = analyze_sentiment(post.selftext)
            post_data = {
                "post_id": post.id,
                "title": post.title,
                "content": post.selftext,
                "author": post.author.name if post.author else None,
                "score": post.score,
                "flair": post.link_flair_text,
                "num_comments": post.num_comments,
                "media_url": post.url,
                "subreddit_id": subreddit.id,
                "created_at": post.created_utc,
                "label": label
            }
            insert_post(cursor, post_data)

            post.comments.replace_more(limit=0)
            for comment in post.comments[:comments_per_post]:
                label = analyze_sentiment(comment.body)
                comment_data = {
                    "comment_id": comment.id,
                    "content": comment.body,
                    "author": comment.author.name if comment.author else None,
                    "score": comment.score,
                    "post_id": post.id,
                    "parent_comment_id": comment.parent_id[3:] if comment.parent_id.startswith("t1_") else None,
                    "created_at": comment.created_utc,
                    "label": label
                }
                insert_comment(cursor, comment_data)
        generate_sentiment_analysis(subreddit_data["name"], subreddit_data["subreddit_id"],cursor,co)