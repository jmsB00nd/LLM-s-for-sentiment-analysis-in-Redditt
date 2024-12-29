def insert_subreddit(cursor, subreddit_data):
    cursor.execute("""
        INSERT INTO Subreddit (subreddit_id, name, description, subscriber_count, active_users, created_at)
        VALUES (:subreddit_id, :name, :description, :subscriber_count, :active_users, TO_DATE('1970-01-01', 'YYYY-MM-DD') + (:created_at / 86400))
    """, subreddit_data)

def insert_post(cursor, post_data):
    cursor.execute("""
        INSERT INTO Post (post_id, title, content, author, score, flair, num_comments, media_url, subreddit_id, created_at, label)
        VALUES (:post_id, :title, :content, :author, :score, :flair, :num_comments, :media_url, :subreddit_id, TO_DATE('1970-01-01', 'YYYY-MM-DD') + (:created_at / 86400), :label)
    """, post_data)

def insert_comment(cursor, comment_data):
    cursor.execute("""
        INSERT INTO Comments (comment_id, content, author, score, post_id, parent_comment_id, created_at, label)
        VALUES (:comment_id, :content, :author, :score, :post_id, :parent_comment_id, TO_DATE('1970-01-01', 'YYYY-MM-DD') + (:created_at / 86400), :label)
    """, comment_data)
