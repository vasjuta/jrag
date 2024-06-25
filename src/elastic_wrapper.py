from elasticsearch import Elasticsearch, helpers


class ElasticWrapper:
    def __init__(self, cloud_id, username, password, index_name):
        self.es = Elasticsearch(
            cloud_id=cloud_id,
            basic_auth=(username, password)
        )
        self.index_name = index_name

    def create_index_with_embeddings(self, index_name, vector_dim):
        settings = {
            "settings": {
                "number_of_shards": 1,
                "number_of_replicas": 0
            },
            "mappings": {
                "properties": {
                    "combined_text": {"type": "text"},
                    "repository": {"type": "text"},
                    "link": {"type": "text"},
                    "description": {"type": "text"},
                    "remarks (internal)": {"type": "text"},
                    "organization": {"type": "text"},
                    "organization type": {"type": "text"},
                    "contact form": {"type": "text"},
                    "additional contacts": {"type": "text"},
                    "contact name": {"type": "text"},
                    "contact e-mail": {"type": "text"},
                    "categories 1": {"type": "text"},
                    "categories 2": {"type": "text"},
                    "categories 3": {"type": "text"},
                    "categories 4": {"type": "text"},
                    "technology": {"type": "text"},
                    "embeddings": {
                        "type": "dense_vector",
                        "dims": vector_dim
                    }
                }
            }
        }
        self.es.indices.create(index=index_name, body=settings)

    def create_index(self, index_name):
        # Define index settings and mappings
        settings = {
            "settings": {
                "number_of_shards": 1,
                "number_of_replicas": 0
            },
            "mappings": {
                "properties": {
                    "combined_text_vector": {
                        "type": "dense_vector",
                        "dims": 1536,
                        "index": "true",
                        "similarity": "cosine"
                    },
                    "combined_text": {
                        "type": "text"
                    },
                    "repository": {"type": "text"},
                    "link": {"type": "text"},
                    "description": {"type": "text"},
                    "remarks (internal)": {"type": "text"},
                    "organization": {"type": "text"},
                    "organization type": {"type": "text"},
                    "contact form": {"type": "text"},
                    "additional contacts": {"type": "text"},
                    "contact name": {"type": "text"},
                    "contact e-mail": {"type": "text"},
                    "categories 1": {"type": "text"},
                    "categories 2": {"type": "text"},
                    "categories 3": {"type": "text"},
                    "categories 4": {"type": "text"},
                    "technology": {"type": "text"}
                }
            }
        }

        self.es.indices.create(index=index_name, body=settings)

    def index_data(self, index_name, data):
        records = data.to_dict(orient='records')
        actions = [
            {
                "_index": index_name,
                "_source": record
            }
            for record in records
        ]
        helpers.bulk(self.es, actions)

    def index_data_with_embeddings(self, index_name, data, embeddings):
        records = data.to_dict(orient='records')
        for i, record in enumerate(records):
            record['embeddings'] = embeddings[i].tolist()
        actions = [
            {
                "_index": index_name,
                "_source": record
            }
            for record in records
        ]
        helpers.bulk(self.es, actions)

    def search(self, query):
        search_query = {
            "query": {
                "multi_match": {
                    "query": query,
                    "fields": ["combined_text"]
                }
            },
            "_source": True
        }
        results = self.es.search(index=self.index_name, body=search_query)
        return [hit["_source"] for hit in results["hits"]["hits"]]

    def search_with_embeddings(self, index_name, query_embedding, k=3):
        search_query = {
            "size": k,
            "query": {
                "script_score": {
                    "query": {"match_all": {}},
                    "script": {
                        "source": "cosineSimilarity(params.query_vector, 'embeddings') + 1.0",
                        "params": {"query_vector": query_embedding}
                    }
                }
            }
        }
        results = self.es.search(index=index_name, body=search_query)
        return [hit["_source"] for hit in results["hits"]["hits"]]