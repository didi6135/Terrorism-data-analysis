from init_files.db.database_neo4j import driver
from dataclasses import fields


class Neo4jCRUD:

    @staticmethod
    def create_relationship(
            start_entity: str,
            start_identifier_key: str,
            start_identifier_value: str,
            end_entity: str,
            end_identifier_key: str,
            end_identifier_value: str,
            relationship: str,
            start_properties: dict = None,
            end_properties: dict = None,
            rel_properties: dict = None
    ):
        with driver.session() as session:
            query = f"""
                MERGE (a:{start_entity} {{{start_identifier_key}: $start_identifier_value}})
                ON CREATE SET a += $start_properties
                MERGE (b:{end_entity} {{{end_identifier_key}: $end_identifier_value}})
                ON CREATE SET b += $end_properties
                MERGE (a)-[r:{relationship}]->(b)
                SET r += $rel_properties
                RETURN type(r) AS relationship, properties(r) AS rel_properties
            """
            params = {
                'start_identifier_value': start_identifier_value,
                'end_identifier_value': end_identifier_value,
                'start_properties': start_properties or {},
                'end_properties': end_properties or {},
                'rel_properties': rel_properties or {}
            }
            try:
                res = session.run(query, params).single()
                return {
                    'relationship': res['relationship'],
                    'rel_properties': res['rel_properties']
                } if res else None
            except Exception as e:
                print(f"Error creating relationship: {str(e)}")
                return {"error": "Database Error", "details": str(e)}

    @staticmethod
    def get_all(entity: str):
        with driver.session() as session:
            query = f"MATCH (e:{entity}) RETURN e"
            try:
                res = session.run(query).data()
                return [dict(record['e']) for record in res] if res else []
            except Exception as e:
                return {"error": "Database Error", "details": str(e)}

    @staticmethod
    def get_one(entity: str, identifier_key: str, identifier_value: str):
        with driver.session() as session:
            query = f"MATCH (e:{entity} {{{identifier_key}: $identifier_value}}) RETURN e"
            params = {'identifier_value': identifier_value}
            try:
                res = session.run(query, params).single()
                return dict(res['e']) if res else None
            except Exception as e:
                return {"error": "Database Error", "details": str(e)}

    @staticmethod
    def create(entity: str, data: dict, model: type):
        with driver.session() as session:
            try:
                validated_data = model(**data)
            except TypeError as e:
                return {"error": "Validation Error", "details": str(e)}

            node_data = validated_data.__dict__
            query = f"CREATE (e:{entity} $data) RETURN e"
            params = {'data': node_data}
            try:
                res = session.run(query, params).single()
                return dict(res['e']) if res else None
            except Exception as e:
                return {"error": "Database Error", "details": str(e)}

    @staticmethod
    def update(entity: str, identifier_key: str, identifier_value: str, update_details: dict, model: type):
        with driver.session() as session:
            model_fields = {f.name for f in fields(model)}

            # Validate fields
            invalid_fields = set(update_details) - model_fields
            if invalid_fields:
                return {"error": "Validation Error", "details": f"Invalid fields: {', '.join(invalid_fields)}"}

            query = f"""
                MATCH (e:{entity} {{{identifier_key}: $identifier_value}})
                SET e += $update_details
                RETURN e
            """
            params = {
                'identifier_value': identifier_value,
                'update_details': update_details
            }
            try:
                res = session.run(query, params).single()
                return dict(res['e']) if res else None
            except Exception as e:
                return {"error": "Database Error", "details": str(e)}

    @staticmethod
    def delete(entity: str, identifier_key: str, identifier_value: str):
        with driver.session() as session:
            query = f"""
                MATCH (e:{entity} {{{identifier_key}: $identifier_value}})
                DETACH DELETE e
                RETURN COUNT(e) AS deleted_count
            """
            params = {"identifier_value": identifier_value}
            try:
                res = session.run(query, params).single()
                return res["deleted_count"] > 0 if res else False
            except Exception as e:
                print(f"Error deleting node: {str(e)}")
                return False

    @staticmethod
    def get_relationship(entity: str, identifier_key: str, identifier_value: str, relationship: str, direction: str):
        with driver.session() as session:
            if direction == "outgoing":
                rel_query = f"->(b)"
            elif direction == "incoming":
                rel_query = f"<-(b)"
            else:  # both directions
                rel_query = f"-(b)"
            query = f"""
                MATCH (a:{entity} {{{identifier_key}: $identifier_value}})-[r:{relationship}]{rel_query}
                RETURN type(r) AS relationship, properties(r) AS rel_properties, properties(b) AS end_node
            """
            params = {'identifier_value': identifier_value}
            try:
                res = session.run(query, params).data()
                return [
                    {
                        'relationship': record['relationship'],
                        'rel_properties': record['rel_properties'],
                        'end_node': record['end_node']
                    } for record in res
                ]
            except Exception as e:
                return {"error": "Database Error", "details": str(e)}

    @staticmethod
    def delete_relationship(
            start_entity: str,
            start_identifier_key: str,
            start_identifier_value: str,
            end_entity: str,
            end_identifier_key: str,
            end_identifier_value: str,
            relationship: str
    ):
        with driver.session() as session:
            query = f"""
                MATCH (a:{start_entity} {{{start_identifier_key}: $start_identifier_value}})
                      -[r:{relationship}]->
                      (b:{end_entity} {{{end_identifier_key}: $end_identifier_value}})
                DELETE r
                RETURN COUNT(r) AS deleted_count
            """
            params = {
                "start_identifier_value": start_identifier_value,
                "end_identifier_value": end_identifier_value
            }
            try:
                res = session.run(query, params).single()
                return res["deleted_count"] > 0 if res else False
            except Exception as e:
                print(f"Error deleting relationship: {str(e)}")
                return False
