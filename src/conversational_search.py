import sys

from transformers import GPT2Tokenizer, GPT2LMHeadModel

from src.elastic_wrapper import ElasticWrapper
from src.embedding_manager import EmbeddingManager
from src.qdrant_wrapper import QdrantWrapper
from src.search_engine import SearchEngine
import os


class ConversationalSearch:
    def __init__(self, search_engine):
        self.search_engine = search_engine

    def start_conversation(self):
        print("Welcome to the Dataset Search Engine. Ask me anything about the datasets.")
        print("Type 'exit' to end the conversation.")

        while True:
            user_query = input("You: ")
            if user_query.lower() == 'exit':
                print("Goodbye!")
                break

            results = self.search_engine.search(user_query)
            response = self.search_engine.generate_response(user_query, results)
            print(f"Search Engine: {response}")


if __name__ == "__main__":

    cloud_id = os.getenv('CLOUD_ID')
    es_username = os.getenv('ES_USERNAME')
    es_password = os.getenv('ES_PASSWORD')
    elastic_wrapper = ElasticWrapper(cloud_id, es_username, es_password, "datasets_with_embeddings")
    # qdrant_wrapper = QdrantWrapper()
    embedding_manager = EmbeddingManager('sentence-transformers/all-MiniLM-L6-v2')

    search_engine = SearchEngine(elastic_wrapper=elastic_wrapper)

    # Start the conversation
    conversational_search = ConversationalSearch(search_engine)
    conversational_search.start_conversation()
