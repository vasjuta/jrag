# src/embedding_manager.py
from transformers import AutoTokenizer, AutoModel
import torch
from sentence_transformers import SentenceTransformer


class EmbeddingManager:
    def __init__(self, model_name='sentence-transformers/all-MiniLM-L6-v2'):
        if 'sentence-transformers' in model_name:
            self.model = SentenceTransformer(model_name)
        else:
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = AutoModel.from_pretrained(model_name)

    def get_embeddings(self, texts):
        if isinstance(self.model, SentenceTransformer):
            embeddings = self.model.encode(texts, convert_to_tensor=True)
        else:
            inputs = self.tokenizer(texts, return_tensors='pt', padding=True, truncation=True)
            with torch.no_grad():
                outputs = self.model(**inputs)
            embeddings = outputs.last_hidden_state.mean(dim=1)
        return embeddings.numpy()
