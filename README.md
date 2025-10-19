# Text Embeddings & Semantic Search API

A Python-based text embeddings generator and semantic search engine powered by **Google Vertex AI** and **Qdrant** vector database. This project provides a **FastAPI REST API** for generating text embeddings and performing semantic similarity searches using multiple distance metrics.

---

## Features

- **Text Embeddings Generation**: Generate high-quality embeddings using Google's `text-embedding-005` model via Vertex AI
- **Semantic Search**: Find semantically similar texts using vector similarity
- **Multiple Similarity Metrics**: 
  - Cosine Similarity
  - Euclidean Distance
  - Dot Product Similarity
- **Vector Storage**: Persistent storage using Qdrant vector database
- **REST API**: FastAPI-based endpoints for easy integration
- **Batch Processing**: Support for generating embeddings in batches (up to 250 items)
- **Interactive Demos**: Command-line scripts for testing similarity and vector search

---

## 📋 Prerequisites

- **Python 3.13+**
- **Google Cloud Project** with Vertex AI API enabled
- **Qdrant** instance (local or cloud)
- **virtualenv** for environment management

---