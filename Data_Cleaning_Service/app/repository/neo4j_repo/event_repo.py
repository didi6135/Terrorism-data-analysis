from Data_Cleaning_Service.app.db.neo4j_db.models.node_models import EvenTNeo4j
from Data_Cleaning_Service.app.utils.generic_for_neo4j import Neo4jCRUD


def insert_or_get_event(event_data):

    existing_event = Neo4jCRUD.get_one("Event", "event_id", event_data["event_id"])
    if existing_event:
        print(f"Event with ID {event_data['event_id']} already exists.")
        return existing_event

    print(f"Inserting new Event with ID {event_data['event_id']}.")
    return Neo4jCRUD.create("Event", event_data, EvenTNeo4j)
