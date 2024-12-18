from typing import TypeVar, List, Optional
from sqlalchemy.exc import SQLAlchemyError
from init_files.settings.postgres_settings import session_maker

T = TypeVar('T')


class MongodbCRUD:
    @staticmethod
    def find_by_id(model: type[T], entity_id: int) -> Optional[T]:
        """
        Find an entity by its ID.
        """
        with session_maker() as session:
            return session.query(model).filter(model.id == entity_id).first()

    @staticmethod
    def find_all(model: type[T], limit: int = 100) -> List[T]:
        """
        Find all entities of a given model with an optional limit.
        """
        with session_maker() as session:
            return session.query(model).limit(limit).all()

    @staticmethod
    def insert(entity: T) -> Optional[str]:
        """
        Insert a new entity into the database.
        """
        with session_maker() as session:
            try:
                session.add(entity)
                session.commit()
                session.refresh(entity)
                return None  # Success, no error message
            except SQLAlchemyError as e:
                session.rollback()
                return str(e)  # Return the error message on failure

    @staticmethod
    def insert_range(entities: List[T]) -> Optional[str]:
        """
        Insert multiple entities into the database.
        """
        with session_maker() as session:
            try:
                session.add_all(entities)
                session.commit()
                return None  # Success, no error message
            except SQLAlchemyError as e:
                session.rollback()
                return str(e)  # Return the error message on failure

    @staticmethod
    def update(model: type[T], entity_id: int, updated_entity: T) -> Optional[str]:
        """
        Update an entity in the database.
        """
        with session_maker() as session:
            try:
                entity_to_update = session.get(model, entity_id)
                if not entity_to_update:
                    return f"No {model.__name__} with id: {entity_id} found"

                for key, value in updated_entity.__dict__.items():
                    if key != "id" and key in model.__dict__:
                        setattr(entity_to_update, key, value)

                session.commit()
                session.refresh(entity_to_update)
                return None  # Success, no error message
            except SQLAlchemyError as e:
                session.rollback()
                return str(e)  # Return the error message on failure

    @staticmethod
    def delete(model: type[T], entity_id: int) -> Optional[str]:
        """
        Delete an entity from the database.
        """
        with session_maker() as session:
            try:
                entity_to_delete = DatabaseManager.find_by_id(model, entity_id)
                if not entity_to_delete:
                    return f"No {model.__name__} with id: {entity_id} found"

                session.delete(entity_to_delete)
                session.commit()
                return None  # Success, no error message
            except SQLAlchemyError as e:
                session.rollback()
                return str(e)  # Return the error message on failure
