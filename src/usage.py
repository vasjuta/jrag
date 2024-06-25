import requests
import json


class Usage:
    def __init__(self, api_url):
        self.api_url = api_url

    def send_query(self, query):
        response = requests.post(
            f"{self.api_url}/search",
            json={'query': query}
        )
        if response.status_code == 200:
            return response.json().get('response')
        else:
            return f"Error: {response.status_code}"

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
            response = self.send_query(query)
            print(f"Response: {response}\n")


if __name__ == "__main__":
    usage = Usage(api_url="http://127.0.0.1:5000")
    usage.test_queries()
