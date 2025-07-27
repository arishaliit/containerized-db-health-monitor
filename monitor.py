# This Python script connects to the PostgreSQL database and performs various health checks.
import psycopg2
import os
import time
from datetime import datetime

# Database connection details from docker-compose.yml
DB_NAME = os.getenv('POSTGRES_DB', 'health_db')
DB_USER = os.getenv('POSTGRES_USER', 'health_user')
DB_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'health_password')
DB_HOST = os.getenv('DB_HOST', 'localhost') # 'localhost' for local, 'db' for docker-compose internal
DB_PORT = os.getenv('DB_PORT', '5432')

def log_message(level, message):
    """Helper function for consistent logging."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {level.upper()}: {message}")

def run_health_checks():
    """Connects to the DB and runs various health checks."""
    conn = None
    try:
        log_message("INFO", f"Attempting to connect to database at {DB_HOST}:{DB_PORT}...")
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        conn.autocommit = True # For simple queries, good for health checks
        cursor = conn.cursor()
        log_message("INFO", "Database connection successful.")

        # --- Health Check 1: Basic Connection Test ---
        cursor.execute("SELECT 1")
        log_message("SUCCESS", "Basic connection test passed.")

        # --- Health Check 2: Users Table Row Count ---
        start_time = time.time()
        cursor.execute("SELECT COUNT(*) FROM users")
        user_count = cursor.fetchone()[0]
        end_time = time.time()
        log_message("INFO", f"Users table row count: {user_count} (Query took {end_time - start_time:.4f}s)")

        # --- Health Check 3: Logs Table Last Entry Time ---
        start_time = time.time()
        cursor.execute("SELECT MAX(created_at) FROM logs")
        last_log_time = cursor.fetchone()[0]
        end_time = time.time()
        log_message("INFO", f"Last log entry timestamp: {last_log_time} (Query took {end_time - start_time:.4f}s)")
        if last_log_time is None:
            log_message("WARNING", "No entries found in the logs table.")

        # --- Health Check 4: Check for NULL emails in users table (Data Integrity) ---
        start_time = time.time()
        cursor.execute("SELECT COUNT(*) FROM users WHERE email IS NULL")
        null_email_count = cursor.fetchone()[0]
        end_time = time.time()
        if null_email_count > 0:
            log_message("ERROR", f"Found {null_email_count} users with NULL email addresses. (Query took {end_time - start_time:.4f}s)")
            return False # Indicate failure
        else:
            log_message("SUCCESS", f"No users found with NULL email addresses. (Query took {end_time - start_time:.4f}s)")

        log_message("INFO", "All health checks completed successfully.")
        return True # Indicate success

    except psycopg2.Error as e:
        log_message("ERROR", f"Database error: {e}")
        return False
    except Exception as e:
        log_message("ERROR", f"An unexpected error occurred: {e}")
        return False
    finally:
        if conn:
            conn.close()
            log_message("INFO", "Database connection closed.")

if __name__ == "__main__":
    # Wait for DB to be ready in some environments (e.g., CI/CD or initial docker-compose up)
    # For local 'run_monitor.sh', the shell script handles waiting
    if os.getenv('WAIT_FOR_DB', 'false') == 'true':
        log_message("INFO", "Waiting for database to be ready...")
        max_retries = 10
        for i in range(max_retries):
            try:
                conn = psycopg2.connect(
                    dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT, connect_timeout=5
                )
                conn.close()
                log_message("INFO", "Database is ready!")
                break
            except psycopg2.OperationalError:
                log_message("WARNING", f"Database not ready yet, retrying in 5 seconds... ({i+1}/{max_retries})")
                time.sleep(5)
        else:
            log_message("ERROR", "Database did not become ready in time. Exiting.")
            exit(1)

    if not run_health_checks():
        log_message("CRITICAL", "One or more health checks failed.")
        exit(1) # Exit with a non-zero code to indicate failure
