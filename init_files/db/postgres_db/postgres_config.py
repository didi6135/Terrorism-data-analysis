import os
from contextlib import contextmanager

from dotenv import load_dotenv

load_dotenv(verbose=True)

def get_db_connection():
    return psycopg2.connect(os.environ['SQL_URI'], cursor_factory=RealDictCursor)


@contextmanager
def db_connection():
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        yield cursor
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise e
    finally:
        cursor.close()
        connection.close()