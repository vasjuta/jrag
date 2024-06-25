
from src.data_manager import DataManager
from src.elastic_wrapper import ElasticWrapper
from src.embedding_manager import EmbeddingManager
from src.qdrant_wrapper import QdrantWrapper
from src.search_engine import SearchEngine

# Elasticsearch connection details
CLOUD_ID = "My_deployment:bWUtd2VzdDEuZ2NwLmVsYXN0aWMtY2xvdWQuY29tOjQ0MyRlNjMwNWFmYjMzMjU0NDMzODBiOTRiZjg5ZmUzYjc3ZiRmMTZhYjZlMzUyOTU0YzMzYWQ4MWJmODA3Nzc4NzU5Nw=="
ES_USERNAME = "elastic"
ES_PASSWORD = "Y6rqS2X7rt56XdqKrEoQNbVD"
INDEX_NAME = 'datasets'

# Initialize the Elasticsearch wrapper
elastic_wrapper = ElasticWrapper(CLOUD_ID, ES_USERNAME, ES_PASSWORD, "datasets_with_embeddings")

# Initialize the data manager
data_manager = DataManager('../data/datasets.xlsx')
data_manager.print_eda()
data = data_manager.get_all_data()
embedding_manager = EmbeddingManager()
# Get data and generate embeddings

combined_texts = data_manager.get_combined_texts()
embeddings = embedding_manager.get_embeddings(combined_texts)

# Create index with embedding dimension
# vector_dim = embeddings.shape[1]
# elastic_wrapper.create_index_with_embeddings('datasets_with_embeddings', vector_dim)
# # Index data with embeddings
# elastic_wrapper.index_data_with_embeddings('datasets_with_embeddings', data, embeddings)

# qdrant_wrapper = QdrantWrapper()
# qdrant_wrapper.initialize_collection()
# qdrant_wrapper.insert_data(data, embeddings)


# Initialize the SearchEngine
search_engine = SearchEngine(elastic_wrapper=elastic_wrapper, qdrant_wrapper=qdrant_wrapper)

# Sample query
query = "Can you find datasets related to Holocaust survivor testimonies?"
query_embedding = embedding_manager.get_embeddings([query])[0]

# Search in Elasticsearch
results_es = elastic_wrapper.search_with_embeddings('datasets_with_embeddings', query_embedding)
results_qd = qdrant_wrapper.search(query_vector=query_embedding)
print(results_es)
print(results_qd)
#print(search_engine.search_query(query))

