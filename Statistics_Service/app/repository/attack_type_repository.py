import pandas as pd
from sqlalchemy.orm import sessionmaker

from Data_Cleaning_Service.app.db.postgres_db.database import session_maker
from Data_Cleaning_Service.app.db.postgres_db.models import AttackType, TargetType, event_attacks_type, Event, \
    event_targets_type


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
