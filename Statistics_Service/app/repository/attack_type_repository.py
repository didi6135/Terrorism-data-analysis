import json

import pandas as pd
from sqlalchemy import func, desc
from sqlalchemy.orm import sessionmaker

from Data_Cleaning_Service.app.db.postgres_db.database import session_maker
from Data_Cleaning_Service.app.db.postgres_db.models import AttackType, TargetType, event_attacks_type, Event, \
    event_targets_type, Casualty


from sqlalchemy import func, desc

def get_most_deadly_attack_types(limit=None):

    with session_maker() as session:
        query = (
            session.query(
                AttackType.name.label("attack_type"),  # Name of the attack type
                func.sum(Casualty.total_killed).label("total_killed"),  # Total killed
                func.sum(Casualty.total_injured).label("total_injured"),  # Total injured
                func.sum(Casualty.total_killed * 2 + Casualty.total_injured).label("score")  # Calculated score
            )
            .join(Event.attack_types)  # Join between Event and AttackType
            .join(Event.casualty)  # Join between Event and Casualty
            .group_by(AttackType.name)  # Group by attack type
            .order_by(desc("score"))  # Order by score descending
        )

        if limit:
            query = query.limit(limit)

        results = query.all()

        return [
            {
                "attack_type": row.attack_type,
                "total_killed": row.total_killed,
                "total_injured": row.total_injured,
                "score": row.score
            }
            for row in results
        ]




def analyze_attack_target_correlation():

    with session_maker() as session:
        results = (
            session.query(
                AttackType.name.label("attack_type"),
                TargetType.name.label("target_type")
            )
            .join(event_attacks_type, event_attacks_type.c.attack_type_id == AttackType.id)
            .join(Event, Event.id == event_attacks_type.c.event_id)
            .join(event_targets_type, event_targets_type.c.event_id == Event.id)
            .join(TargetType, TargetType.id == event_targets_type.c.target_type_id)
            .all()
        )

        data = pd.DataFrame(results, columns=["attack_type", "target_type"])

        correlation_table = pd.crosstab(data["attack_type"], data["target_type"])

        return correlation_table.to_dict()

