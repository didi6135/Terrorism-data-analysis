from typing import TypeVar, List, Optional, Type
from sqlalchemy.exc import SQLAlchemyError

from data_cleaning.app.db.postgres_db import session_maker
from data_cleaning.app.utils.logger import log

T = TypeVar('T')  # Generic type for models


class PostgresCRUD:
    """
    A generic CRUD class for interacting with SQLAlchemy models.
    """

    @staticmethod
    def find_by_id(model: Type[T], entity_id: int) -> Optional[T]:
        """
        Find an entity by its ID.
        """
        with session_maker() as session:
            return session.query(model).filter(model.id == entity_id).first()

    @staticmethod
    def find_all(model: Type[T], limit: int = 100) -> List[T]:
        """
        Retrieve all entities of a given model with an optional limit.
        """
        with session_maker() as session:
            return session.query(model).limit(limit).all()

    @staticmethod
    def insert(entity, model):
        """Insert a new entity into the database."""
        if not isinstance(entity, model):
            raise TypeError(f"Expected {model.__name__}, got {type(entity).__name__}")
        with session_maker() as session:
            try:
                session.add(entity)
                session.commit()
                session.refresh(entity)
                return entity  # Return the inserted entity
            except SQLAlchemyError as e:
                session.rollback()
                raise Exception(f"Error inserting {model.__name__}: {e}")

    @staticmethod
    def get_or_insert(model: Type[T], filters: dict, entity: T):
        """
        Get an existing record or insert a new one.
        """
        with session_maker() as session:
            try:
                # Check if the record already exists
                instance = session.query(model).filter_by(**filters).first()
                if instance:
                    return instance  # Return the existing record

                # Insert the new entity
                session.add(entity)
                session.commit()
                session.refresh(entity)
                return entity  # Return the newly inserted record
            except SQLAlchemyError as e:
                session.rollback()
                raise Exception(f"Error in get_or_insert for {model.__name__}: {e}")

    @staticmethod
    def insert_range(entities: List[T], model: Type[T]) -> Optional[str]:
        """
        Insert multiple entities into the database with type validation.
        """
        if not all(isinstance(entity, model) for entity in entities):
            return f"Type Error: All entities must be instances of {model.__name__}"

        with session_maker() as session:
            try:
                session.add_all(entities)
                session.commit()
                return None  # Success
            except SQLAlchemyError as e:
                session.rollback()
                return str(e)  # Return error message

    @staticmethod
    def update(model: Type[T], entity_id: int, updated_data: dict) -> Optional[str]:
        """
        Update an existing entity in the database.
        """
        with session_maker() as session:
            try:
                entity_to_update = session.query(model).filter(model.id == entity_id).first()
                if not entity_to_update:
                    return f"No {model.__name__} with id {entity_id} found."

                # Check updated_data keys against the model's attributes
                for key, value in updated_data.items():
                    if hasattr(entity_to_update, key):
                        setattr(entity_to_update, key, value)
                    else:
                        return f"Type Error: '{key}' is not a valid attribute of {model.__name__}"

                session.commit()
                session.refresh(entity_to_update)
                return None  # Success
            except SQLAlchemyError as e:
                session.rollback()
                return str(e)  # Return error message

    @staticmethod
    def delete(model: Type[T], entity_id: int) -> Optional[str]:
        """
        Delete an entity from the database.
        """
        with session_maker() as session:
            try:
                entity_to_delete = session.query(model).filter(model.id == entity_id).first()
                if not entity_to_delete:
                    return f"No {model.__name__} with id {entity_id} found."

                session.delete(entity_to_delete)
                session.commit()
                return None  # Success
            except SQLAlchemyError as e:
                session.rollback()
                return str(e)  # Return error message