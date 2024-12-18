import os

from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv(verbose=True, dotenv_path='../../../.env')

driver = GraphDatabase.driver(
    os.environ.get("NEO4J_URI"),
    auth=(os.environ.get("NEO4J_USER"), os.environ.get("NEO4J_PASS")),

)


def test_neo4j_connection():
    try:
        with driver.session() as session:
            result = session.run("RETURN 1 AS test")
            print("Connection successful:", result.single()["test"] == 1)
    except Exception as e:
        print("Connection failed:", e)

test_neo4j_connection()
