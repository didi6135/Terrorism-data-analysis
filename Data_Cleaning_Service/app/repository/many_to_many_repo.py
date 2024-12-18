from Data_Cleaning_Service.app.db.postgres_db import session_maker
from Data_Cleaning_Service.app.models.many_to_many_tables import event_targets_type, event_attacks_type, event_groups, \
    event_weapons_type, event_events_type
from sqlalchemy.orm import sessionmaker



def link_target_type_to_event(event_id: int, target_type_id: int):

    with session_maker() as session:
        try:
            exists = session.query(event_targets_type).filter_by(
                event_id=event_id, target_type_id=target_type_id
            ).first()

            if not exists:
                session.execute(
                    event_targets_type.insert().values(event_id=event_id, target_type_id=target_type_id)
                )
                session.commit()
                print(f"Linked target_type_id {target_type_id} to event_id {event_id}")
        except Exception as e:
            session.rollback()
            print(f"Error linking target_type_id {target_type_id} to event_id {event_id}: {e}")



def link_attack_type_to_event(event_id: int, attack_type_id: int):
    with session_maker() as session:
        try:
            exists = session.query(event_attacks_type).filter_by(
                event_id=event_id, attack_type_id=attack_type_id
            ).first()

            if not exists:
                session.execute(
                    event_attacks_type.insert().values(event_id=event_id, attack_type_id=attack_type_id)
                )
                session.commit()
                print(f"Linked attack_type_id {attack_type_id} to event_id {event_id}")
        except Exception as e:
            session.rollback()
            print(f"Error linking attack_type_id {attack_type_id} to event_id {event_id}: {e}")



def link_group_to_event(event_id: int, group_id: int):
    with session_maker() as session:
        try:
            exists = session.query(event_groups).filter_by(event_id=event_id, group_id=group_id).first()

            if not exists:
                session.execute(event_groups.insert().values(event_id=event_id, group_id=group_id))
                session.commit()
                print(f"Linked group_id {group_id} to event_id {event_id}")
        except Exception as e:
            session.rollback()
            print(f"Error linking group_id {group_id} to event_id {event_id}: {e}")



def link_weapon_type_to_event(event_id: int, weapon_type_id: int):
    with session_maker() as session:
        try:
            exists = session.query(event_weapons_type).filter_by(
                event_id=event_id, weapon_type_id=weapon_type_id
            ).first()

            if not exists:
                session.execute(
                    event_weapons_type.insert().values(event_id=event_id, weapon_type_id=weapon_type_id)
                )
                session.commit()
                print(f"Linked weapon_type_id {weapon_type_id} to event_id {event_id}")
        except Exception as e:
            session.rollback()
            print(f"Error linking weapon_type_id {weapon_type_id} to event_id {event_id}: {e}")



def link_event_type_to_event(event_id: int, event_type_id: int):
    with session_maker() as session:
        try:
            exists = session.query(event_events_type).filter_by(
                event_id=event_id, event_type_id=event_type_id
            ).first()

            if not exists:
                session.execute(
                    event_events_type.insert().values(event_id=event_id, event_type_id=event_type_id)
                )
                session.commit()
                print(f"Linked event_type_id {event_type_id} to event_id {event_id}")
        except Exception as e:
            session.rollback()
            print(f"Error linking event_type_id {event_type_id} to event_id {event_id}: {e}")
