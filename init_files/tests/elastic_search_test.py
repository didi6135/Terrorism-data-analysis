import pytest




@pytest.fixture(scope="module")
def es_index(es_client):
   index_name = "products"
   if not es_client.indices.exists(index=index_name):
       es_client.indices.create(index=index_name, body={
           "settings": {
               "number_of_shards": 2,
               "number_of_replicas": 2
           }
       })
   yield index_name
   es_client.indices.delete(index=index_name)


def test_create_product_document(es_index, es_client):
   # Define the document
   document = {
       "name": "Coffee maker",
       "price": 64,
       "in_stock": 10
   }
   response = es_client.index(index=es_index, body=document)
   print(response)
   assert response['result'] == 'created'
   assert response['_index'] == es_index