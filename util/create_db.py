import sqlite3

conn = sqlite3.connect("voting.db")
cursor = conn.cursor()

# USERS
cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    google_id TEXT UNIQUE,
    email TEXT UNIQUE,
    name TEXT,
    is_admin INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

# ELECTIONS
cursor.execute("""
CREATE TABLE IF NOT EXISTS elections(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    description TEXT,
    start_date TEXT,
    end_date TEXT,
    is_active INTEGER DEFAULT 0
)
""")

# POSITIONS
cursor.execute("""
CREATE TABLE IF NOT EXISTS positions(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    election_id INTEGER,
    name TEXT,
    max_votes INTEGER DEFAULT 1,
    FOREIGN KEY(election_id) REFERENCES elections(id)
)
""")

# CANDIDATES
cursor.execute("""
CREATE TABLE IF NOT EXISTS candidates(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    position_id INTEGER,
    user_id INTEGER,
    bio TEXT,
    photo_url TEXT,
    FOREIGN KEY(position_id) REFERENCES positions(id),
    FOREIGN KEY(user_id) REFERENCES users(id)
)
""")

# VOTES
cursor.execute("""
CREATE TABLE IF NOT EXISTS votes(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    voter_id INTEGER,
    candidate_id INTEGER,
    position_id INTEGER,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(voter_id, position_id),
    FOREIGN KEY(voter_id) REFERENCES users(id),
    FOREIGN KEY(candidate_id) REFERENCES candidates(id)
)
""")

# LOGIN LOGS
cursor.execute("""
CREATE TABLE IF NOT EXISTS login_logs(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    login_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ip_address TEXT,
    FOREIGN KEY(user_id) REFERENCES users(id)
)
""")

conn.commit()
conn.close()

print("Database created.")