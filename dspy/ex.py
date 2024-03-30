# pip install transformers torch faiss-cpu
import os
import faiss
from transformers import AutoTokenizer, AutoModelForTokenClassification, AutoModel, pipeline

# Load models
tokenizer_encoder = AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
model_encoder = AutoModel.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
