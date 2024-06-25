# Initialize the search engine
from src.elastic_wrapper import ElasticWrapper
from src.search_engine import SearchEngine
import os


class QueryingTests:
    def __init__(self, search_engine):
        self.search_engine = search_engine

    def test_queries(self):
        queries = [
            "What dataset can you suggest for family photos from the ghetto period?",
            "Are there any datasets about Jewish cultural artifacts?",
            "Can you find datasets related to Holocaust survivor testimonies?",
            "What datasets are available for Jewish community records in the 19th century?",
            "Do you have datasets about Jewish genealogical records?"
        ]

        for query in queries:
            print(f"Query: {query}")
            results = self.search_engine.search(query)
            print(f"Response: {self.search_engine.format_results(results)}\n")


if __name__ == '__main__':
    cloud_id = os.getenv('CLOUD_ID')
    es_username = os.getenv('ES_USERNAME')
    es_password = os.getenv('ES_PASSWORD')
    elastic_wrapper = ElasticWrapper(cloud_id, es_username, es_password, "datasets_with_embeddings")
    search_engine = SearchEngine(elastic_wrapper)
    qt = QueryingTests(search_engine)
    qt.test_queries()
