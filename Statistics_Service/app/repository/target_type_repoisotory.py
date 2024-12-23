from Data_Cleaning_Service.app.db.postgres_db.database import session_maker
from Data_Cleaning_Service.app.db.postgres_db.models import TargetType


def get_all_target_types():
    with session_maker() as session:
        target_types = session.query(TargetType.id, TargetType.name).order_by(TargetType.name.asc()).all()
        return [{"id": tg.id, "name": tg.name} for tg in target_types]
