from flask import Flask, request, jsonify

from src.data_manager import DataManager
from src.elastic_wrapper import ElasticWrapper
from src.search_engine import SearchEngine

app = Flask(__name__)

# Elasticsearch connection details
CLOUD_ID = "My_deployment:bWUtd2VzdDEuZ2NwLmVsYXN0aWMtY2xvdWQuY29tOjQ0MyRlNjMwNWFmYjMzMjU0NDMzODBiOTRiZjg5ZmUzYjc3ZiRmMTZhYjZlMzUyOTU0YzMzYWQ4MWJmODA3Nzc4NzU5Nw=="
ES_USERNAME = "elastic"
ES_PASSWORD = "Y6rqS2X7rt56XdqKrEoQNbVD"
INDEX_NAME = 'datasets'

# Initialize the Elasticsearch wrapper
elastic_wrapper = ElasticWrapper(CLOUD_ID, ES_USERNAME, ES_PASSWORD)

# Initialize the search engine
search_engine = SearchEngine(elastic_wrapper)


@app.route('/search', methods=['POST'])
def search():
    query = request.json['query']
    search_results = search_engine.search_datasets(query, INDEX_NAME)
    response = search_engine.generate_response(query, search_results)
    return jsonify({'response': response})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
