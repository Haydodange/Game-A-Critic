from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import os


def database_exists():
    return os.path.exists('database/reviews.db')


def init_db():
    # create database directory if it doesn't exist
    if not os.path.exists('database'):
        os.makedirs('database')
    
     # create tables if database doesn't exist
    if not database_exists():
        db = sqlite3.connect("database/reviews.db")
        db.execute("""
            CREATE TABLE IF NOT EXISTS Users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        db.execute("""
            CREATE TABLE IF NOT EXISTS Reviews (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                game_title TEXT NOT NULL,
                review_text TEXT NOT NULL,
                rating INTEGER NOT NULL CHECK(rating >= 1 AND rating <= 5),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES Users(id) ON DELETE CASCADE
            )
        """)
        
        db.commit()
        db.close()


def get_db():
    db = sqlite3.connect("database/reviews.db")
    db.row_factory = sqlite3.Row
    return db


def get_all_reviews():
    db = get_db()
    reviews = db.execute("""
        SELECT Reviews.*, Users.username 
        FROM Reviews 
        JOIN Users ON Reviews.user_id = Users.id 
        ORDER BY Reviews.created_at DESC
    """).fetchall()
    db.close()
    return reviews


def get_review_by_id(review_id):
    db = get_db()
    review = db.execute("""
        SELECT Reviews.*, Users.username 
        FROM Reviews 
        JOIN Users ON Reviews.user_id = Users.id 
        WHERE Reviews.id = ?
    """, (review_id,)).fetchone()
    db.close()
    return review


def search_reviews(query):
    db = get_db()
    reviews = db.execute("""
        SELECT Reviews.*, Users.username 
        FROM Reviews 
        JOIN Users ON Reviews.user_id = Users.id 
        WHERE game_title LIKE ? OR review_text LIKE ?
        ORDER BY Reviews.created_at DESC
    """, (f'%{query}%', f'%{query}%')).fetchall()
    db.close()
    return reviews


def add_review(user_id, game_title, review_text, rating):
    if not all([user_id, game_title, review_text, rating]):
        return False
    
    db = get_db()
    db.execute("""
        INSERT INTO Reviews (user_id, game_title, review_text, rating)
        VALUES (?, ?, ?, ?)
    """, (user_id, game_title, review_text, rating))
    db.commit()
    db.close()
    return True


def update_review(review_id, game_title, review_text, rating):
    db = get_db()
    db.execute("""
        UPDATE Reviews 
        SET game_title = ?, review_text = ?, rating = ?, updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
    """, (game_title, review_text, rating, review_id))
    db.commit()
    db.close()
    return True


def delete_review(review_id):
    db = get_db()
    db.execute("DELETE FROM Reviews WHERE id = ?", (review_id,))
    db.commit()
    db.close()
    return True


def check_login(username, password):
    db = get_db()
    user = db.execute("SELECT * FROM Users WHERE username = ?", (username,)).fetchone()
    db.close()
    
    if user and check_password_hash(user['password'], password):
        return user
    return None


def register_user(username, password):
    if not username or not password:
        return False
    
    try:
        db = get_db()
        hash_pwd = generate_password_hash(password)
        db.execute("INSERT INTO Users (username, password) VALUES (?, ?)", 
                  (username, hash_pwd))
        db.commit()
        db.close()
        return True
    except sqlite3.IntegrityError:
        return False
    