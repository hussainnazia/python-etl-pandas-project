import requests
import psycopg2
import os
import logging
from dotenv import load_dotenv
from datetime import datetime,timezone

load_dotenv()

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s-%(levelname)s-%(message)s")


def get_last_successful_run():
    conn = None
    cursor = None

    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            database=os.getenv("DB_DATABASE"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            port=os.getenv("DB_PORT")
        )

        cursor = conn.cursor()

        cursor.execute("""
            SELECT last_successful_run
            FROM etl_control
            WHERE pipeline_name = %s
        """, ("api_users_pipeline",))

        result = cursor.fetchone()

        return result[0] if result else None

    except psycopg2.Error as e:
        logging.error(f"Failed to read ETL watermark: {e}")
        return None

    finally:
        if cursor:
            cursor.close()

        if conn:
            conn.close()

# --------------------
# 1. EXTRACT
# --------------------





def extract_data():
    url = "https://jsonplaceholder.typicode.com/users"

    try:
        response = requests.get(url,timeout=10)
        response.raise_for_status()

        
        users = response.json()
        
        logging.info(f"Extracted {len(users)} users from API")
        return users
        
        
    
    except requests.exceptions.RequestException as e:
        logging.error(f"API request failed: {e}")
        return None


# --------------------
# 2. TRANSFORM
# --------------------

def transform_data(users):
    clean_users = []
    rejected_users = []

    for user in users:
        try:
            clean_users.append({
                "id": user["id"],
                "name": user["name"],
                "email": user["email"],
                "city": user["address"]["city"],
                "company": user["company"]["name"]
            })

        except(KeyError,TypeError) as e:
            logging.error(f"skipping invalid user: {e}")
            rejected_users.append({
        "user": user,
        "reason": str(e)
    })

    logging.info(f"Transformed {len(clean_users)} users")
    logging.info(f"Rejected {len(rejected_users)} users")

    return clean_users ,rejected_users 

# --------------------
# 3. LOAD
# --------------------


def load_data(clean_users):
    conn = None
    cursor = None
    run_time= datetime.now(timezone.utc)

    inserted = 0
    updated = 0
    skipped = 0

    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            database=os.getenv("DB_DATABASE"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            port=os.getenv("DB_PORT")
        )

        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, name, email, city, company
            FROM api_users
        """)

        existing_users = cursor.fetchall()

        existing_users_dict = {
            row[0]: {
                "name": row[1],
                "email": row[2],
                "city": row[3],
                "company": row[4]
            }
            for row in existing_users
        }

        for user in clean_users:

            existing_user = existing_users_dict.get(user["id"])

            if existing_user is None:

                cursor.execute("""
                    INSERT INTO api_users
                        (id, name, email, city, company, last_updated)
                    VALUES
                        (%s, %s, %s, %s, %s, clock_timestamp())
                """, (
                    user["id"],
                    user["name"],
                    user["email"],
                    user["city"],
                    user["company"]
                ))

                inserted += 1

            else:

                
                if(
                existing_user["name"] != user["name"]
                or existing_user["email"] != user["email"]
                or existing_user["city"] != user["city"]
                or existing_user["company"] != user["company"]
                ):

                    cursor.execute("""
                        UPDATE api_users
                        SET
                            name = %s,
                            email = %s,
                            city = %s,
                            company = %s,
                            last_updated = clock_timestamp()
                        WHERE id = %s
                    """, (
                        user["name"],
                        user["email"],
                        user["city"],
                        user["company"],
                        user["id"]
                    ))

                    updated += 1

                else:
                    skipped += 1

        cursor.execute("""
                        INSERT INTO etl_control (pipeline_name, last_successful_run)
                        VALUES (%s, %s)
                        ON CONFLICT (pipeline_name)
                        DO UPDATE SET
                            last_successful_run = EXCLUDED.last_successful_run
                    """, (
                        "api_users_pipeline",
                        run_time
                    ))

        conn.commit()

        logging.info(
            f"Inserted: {inserted}, Updated: {updated}, Skipped: {skipped}"
        )

        return True

    except psycopg2.Error as e:

        if conn:
            conn.rollback()

        logging.error(f"Database error: {e}")
        return False

    finally:

        if cursor:
            cursor.close()

        if conn:
            conn.close()



def load_rejected_users(rejected_users):
    if not rejected_users:
        logging.info("No rejected users to load.")
        return True

    conn = None
    cursor = None

    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            database=os.getenv("DB_DATABASE"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            port=os.getenv("DB_PORT")
        )

        cursor = conn.cursor()

        for rejected in rejected_users:
            user = rejected["user"]
            reason = rejected["reason"]

            cursor.execute("""
                INSERT INTO rejected_users
                    (id, name, email, rejection_reason, rejected_at)
                VALUES
                    (%s, %s, %s, %s, clock_timestamp())
            """, (
                user.get("id"),
                user.get("name"),
                user.get("email"),
                reason
            ))

        conn.commit()

        logging.info(
            f"Loaded {len(rejected_users)} rejected users"
        )

        return True

    except psycopg2.Error as e:
        if conn:
            conn.rollback()

        logging.error(f"Failed to load rejected users: {e}")
        return False

    finally:
        if cursor:
            cursor.close()

        if conn:
            conn.close()

    
# --------------------
# MAIN ETL PIPELINE
# --------------------

users = extract_data()
 
last_run = get_last_successful_run()

logging.info("Last successful run: %s", last_run)


if users is None:
    logging.error("ETL pipeline failed during extraction.")
else:
    clean_users, rejected_users = transform_data(users)

load_success = load_data(clean_users)

if load_success:
    rejected_success = load_rejected_users(rejected_users)

    if rejected_success:
        logging.info("ETL pipeline completed successfully!")
    else:
        logging.info("ETL pipeline failed while loading rejected records.")
else:
    logging.error("ETL pipeline failed during loading.")
    
