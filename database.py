import sqlite3

def connect_db():
    """Establish a connection to the SQLite database."""
    return sqlite3.connect("candidates.db", check_same_thread=False)

def create_tables():
    """Create the necessary tables if they do not exist."""
    conn = connect_db()
    cursor = conn.cursor()
    
    # Candidate details
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS candidates (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        phone TEXT NOT NULL UNIQUE,
        experience INTEGER CHECK (experience >= 0),
        position TEXT,
        location TEXT,
        tech_stack TEXT
    )
    """)

    # Store generated questions separately
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS questions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question TEXT NOT NULL UNIQUE
    )
    """)

    # Store responses linked to questions & candidates
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS responses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        candidate_id INTEGER NOT NULL,
        question_id INTEGER NOT NULL,
        answer TEXT NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (candidate_id) REFERENCES candidates(id) ON DELETE CASCADE,
        FOREIGN KEY (question_id) REFERENCES questions(id) ON DELETE CASCADE
    )
    """)
    
    conn.commit()
    conn.close()

def insert_candidate(name, email, phone, experience, position, location, tech_stack):
    """Insert a new candidate's details into the database."""
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute("""
        INSERT INTO candidates (name, email, phone, experience, position, location, tech_stack)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (name, email, phone, experience, position, location, tech_stack))
        
        candidate_id = cursor.lastrowid
        conn.commit()
        return candidate_id
    except sqlite3.IntegrityError:
        print("Error: Duplicate email or phone number detected.")
        return None
    finally:
        conn.close()

def insert_question(question):
    """Insert a new unique question into the database."""
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO questions (question) VALUES (?)", (question,))
        question_id = cursor.lastrowid
        conn.commit()
        return question_id
    except sqlite3.IntegrityError:
        print("Error: Question already exists.")
        return None
    finally:
        conn.close()

def insert_response(candidate_id, question_id, answer):
    """Insert a candidate's response to a specific question."""
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute("""
    INSERT INTO responses (candidate_id, question_id, answer)
    VALUES (?, ?, ?)
    """, (candidate_id, question_id, answer))
    
    conn.commit()
    conn.close()

def fetch_all_candidates():
    """Retrieve all candidates from the database."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM candidates")
    candidates = cursor.fetchall()
    conn.close()
    return candidates

def fetch_candidate_by_id(candidate_id):
    """Retrieve a candidate by their ID."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM candidates WHERE id = ?", (candidate_id,))
    candidate = cursor.fetchone()
    conn.close()
    return candidate

def fetch_responses(candidate_id):
    """Retrieve all responses for a specific candidate, including the questions."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT q.question, r.answer, r.timestamp
        FROM responses r
        JOIN questions q ON r.question_id = q.id
        WHERE r.candidate_id = ?
        ORDER BY r.timestamp DESC
    """, (candidate_id,))
    
    responses = cursor.fetchall()
    conn.close()
    return responses

# Initialize the database
create_tables()