from nltk.sentiment import SentimentIntensityAnalyzer
import nltk
import random

# Initialize NLTK VADER sentiment analyzer
nltk.download('vader_lexicon')
sia = SentimentIntensityAnalyzer()

def analyze_sentiment(text):
    sentiment_score = sia.polarity_scores(text)
    compound = sentiment_score["compound"]
    if compound >= 0.05:
        return "positive"
    elif compound <= -0.05:
        return "negative"
    else:
        return "neutral"

def cohere_generate(prompt, co):
    try:
        response = co.generate(
            model='command-xlarge-nightly',
            prompt=prompt,
            max_tokens=200
        )
        return response.generations[0].text.strip()
    except Exception as e:
        return f"Error generating response: {str(e)}"

def generate_prompt(subreddit_name, posts_with_comments):
    prompt = f"The following is a sentiment analysis for the subreddit '{subreddit_name}' based on selected posts and their comments:\n\n"
    for i, post in enumerate(posts_with_comments, 1):
        prompt += f"Post {i}:\nTitle: {post['post_title']}\nContent: {post['post_content']}\nComments:\n"
        for comment in post["comments"]:
            prompt += f"- {comment}\n"
        prompt += "\n"
    prompt += "Please provide a sentiment analysis summarizing the overall tone and themes discussed in this subreddit.\n"
    return prompt


def generate_sentiment_analysis(subreddit_name, subreddit_id, cursor,co):
    cursor.execute("""
        SELECT post_id, title, content
        FROM Post
        WHERE subreddit_id = :subreddit_id
        FETCH FIRST 10 ROWS ONLY
    """, {"subreddit_id": subreddit_id})
    
    posts = cursor.fetchall()
    if not posts:
        print(f"No posts found for subreddit {subreddit_name}")
        return
    
    selected_posts = random.sample(posts, min(5, len(posts)))
    posts_with_comments = []
    
    for post_id, title, content in selected_posts:
        cursor.execute("""
            SELECT content
            FROM Comments
            WHERE post_id = :post_id
            FETCH FIRST 10 ROWS ONLY
        """, {"post_id": post_id})
        
        comments = [row[0] for row in cursor.fetchall()]
        posts_with_comments.append({
            "post_title": title,
            "post_content": content,
            "comments": comments
        })
    
    prompt = generate_prompt(subreddit_name, posts_with_comments)
    
    sentiment_analysis = cohere_generate(prompt,co)
    print("Generated Sentiment Analysis:", sentiment_analysis)
    
    cursor.execute("""
        INSERT INTO SubredditSentiments (subreddit_id, sentiment_analysis)
        VALUES (:subreddit_id, :sentiment_analysis)
    """, {"subreddit_id": subreddit_id, "sentiment_analysis": sentiment_analysis})
    
    print(f"Sentiment analysis for subreddit {subreddit_name} saved successfully!")