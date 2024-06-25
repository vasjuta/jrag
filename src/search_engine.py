from transformers import GPT2Tokenizer, GPT2LMHeadModel

from src.embedding_manager import EmbeddingManager
import os
from transformers import GPT2Tokenizer, GPT2LMHeadModel
from dotenv import load_dotenv
from openai import OpenAI
load_dotenv()

os.environ["TOKENIZERS_PARALLELISM"] = "false"


class SearchEngine:
    def __init__(self, elastic_wrapper=None, qdrant_wrapper=None,
                 embedding_model_name='sentence-transformers/all-MiniLM-L6-v2',
                 gpt_model_name='gpt2', max_length=512):
        self.elastic_wrapper = elastic_wrapper
        self.qdrant_wrapper = qdrant_wrapper
        self.index_name = 'datasets_with_embeddings'
        self.max_length = max_length

        # Initialize tokenizer and model for GPT-2
        self.tokenizer = GPT2Tokenizer.from_pretrained(gpt_model_name)
        self.model = GPT2LMHeadModel.from_pretrained(gpt_model_name)
        self.embedding_manager = EmbeddingManager(embedding_model_name)

        # OpenAI API setup
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        self.openai_model_name = 'gpt-3.5-turbo'
        self.openai_client = OpenAI()

    def search(self, user_query):
        query_embedding = self.embedding_manager.get_embeddings([user_query])[0]
        if self.elastic_wrapper:
            results = self.elastic_wrapper.search_with_embeddings(self.index_name, query_embedding)
        if self.qdrant_wrapper:
            results = self.qdrant_wrapper.search(query_embedding)

        return results

    def format_results(self, results):
        seen_links = set()
        formatted_results = []
        for result in results:
            link = result.get('link', 'N/A')
            description = result.get('description', 'N/A')
            if link in seen_links:
                continue
            seen_links.add(link)
            formatted_results.append(f"Title: {result.get('title', 'N/A')}\n"
                                     f"Link: {link}\n"
                                     f"Description: {description}\n")
        return "\n\n".join(formatted_results)

    def generate_response(self, user_query, search_results):
        context = self.format_results(search_results)

        if context:
            messages = [
                {"role": "system",
                 "content": "You are a knowledge base assistant for datasets. "
                            "Answer the user's queries and provide relevant dataset information."},
                {"role": "user", "content": user_query},
                {"role": "system", "content": context}
            ]
        else:
            messages = [
                {"role": "system",
                 "content": "You are a knowledge base assistant for datasets. "
                            "Answer the user's queries and provide relevant dataset information."},
                {"role": "user", "content": user_query}
            ]

        response = self.openai_client.chat.completions.create(
            model=self.openai_model_name,
            messages=messages,
            max_tokens=self.max_length
        )

        response_text = response['choices'][0]['text']

        # Clean the response to remove redundant repetitions
        response_text = self.clean_response(response_text)
        return response_text.strip()

    def clean_response(self, response):
        # Remove repeated blocks of text
        unique_responses = []
        seen = set()
        for line in response.split('\n'):
            if line not in seen:
                unique_responses.append(line)
                seen.add(line)
        return '\n'.join(unique_responses)
