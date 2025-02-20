-- Create Tables
-- CREATE TABLE IF NOT EXISTS Reviews(
--     id INTEGER PRIMARY KEY AUTOINCREMENT,
--     user_id INTEGER,
--     date TEXT NOT NULL, 
--     rating INTEGER CHECK(rating BETWEEN 1 AND 5),
--     game TEXT NOT NULL,
--     review_text TEXT,
--     FOREIGN KEY(user_id) REFERENCES Users(id)
-- );

-- CREATE TABLE IF NOT EXISTS Users(
--     id INTEGER PRIMARY KEY AUTOINCREMENT,
--     username TEXT UNIQUE NOT NULL,
--     password NOT NULL
-- );

-- Sample data updates
-- INSERT INTO Users('username', 'password') 
--     VALUES("johnno","scrypt:...");  -- keep existing hashes

-- INSERT INTO Reviews('user_id', 'date', 'rating', 'game', 'review_text')
--     VALUES(1, "2024-10-27", 4, "Brute Force", "Challenging but rewarding gameplay..."),
--     (2, "2024-10-29", 5, "Zenless Zone Zero", "Absolutely stunning visuals...");