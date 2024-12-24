from Data_Cleaning_Service.app.db.postgres_db.database import session_maker

def link_entity_to_event(event_id: int, entity_id: int, table, event_column: str, entity_column: str):
    with session_maker() as session:
        try:
            exists = session.query(table).filter_by(**{event_column: event_id, entity_column: entity_id}).first()

            if not exists:
                session.execute(
                    table.insert().values(**{event_column: event_id, entity_column: entity_id})
                )
                session.commit()
                print(f"Linked {entity_column} {entity_id} to {event_column} {event_id}")
        except Exception as e:
            session.rollback()
            print(f"Error linking {entity_column} {entity_id} to {event_column} {event_id}: {e}")
