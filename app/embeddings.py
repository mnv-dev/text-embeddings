import os
from typing import List

import vertexai
from dotenv import load_dotenv
from vertexai.language_models import TextEmbeddingModel
import math

load_dotenv()

class EmbeddingGenerator:
    def __init__(self, project_id: str = None, location: str = None):
        self.project_id = os.getenv("GOOGLE_PROJECT_ID")
        self.location = os.getenv("GOOGLE_CLOUD_LOCATION")
        if not self.project_id:
            raise ValueError("No Google Project ID provided!!")

        vertexai.init(project=self.project_id, location=self.location)
        self.model_name = "text-embedding-005"

    def generate_embedding(self, text: str) -> List[float]:
        model = TextEmbeddingModel.from_pretrained(self.model_name)
        embeddings = model.get_embeddings([text])
        return embeddings[0].values

    def generate_embeddings(self, texts: list[str]) -> list[list[float]]:
        # The API supports only up to 250 items per request.
        model = TextEmbeddingModel.from_pretrained(self.model_name)
        batch_size = 250

        all_embeddings = []
        total = len(texts)
        num_batches = math.ceil(total / batch_size)
        print(f"Generating embeddings in {num_batches} batches")

        for i in range(0, total, batch_size):
            batch = texts[i: i + batch_size]
            embeddings = model.get_embeddings(batch)
            all_embeddings.extend([embedding.values for embedding in embeddings])

        print(f"Finished generating embeddings in {num_batches} batches!!")
        return all_embeddings

