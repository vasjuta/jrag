from qdrant_client import QdrantClient
from qdrant_client.grpc import Distance
from qdrant_client.http.models import PointStruct, Filter
import numpy as np


class QdrantWrapper:
    def __init__(self, host='localhost', port=6333, collection_name='datasets_collection'):
        self.client = QdrantClient(host=host, port=port)
        self.collection_name = collection_name
        self.initialize_collection()

    def initialize_collection(self):
        try:
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config={
                    "size": 512,  # Update this size based on your embeddings
                    "distance": Distance.Cosine
                }
            )
        except Exception as e:
            print(f"Collection {self.collection_name} already exists or could not be created. Error: {e}")

    def insert_data(self, data, embeddings):
        points = [
            PointStruct(
                id=i,
                vector=embeddings[i].tolist(),
                payload = row.to_dict()
            ) for i, row in data.iterrows()
        ]
        self.client.upsert(collection_name=self.collection_name, points=points)

    def search(self, query_vector, top_k=5):
        search_result = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_vector,
            limit=top_k
        )
        return [hit.payload for hit in search_result]
