import os
os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'

import openai
import faiss
from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline

import dotenv
import os
import numpy as np

dotenv.load_dotenv() 

from openai import OpenAI
client = OpenAI()

# Load NER pipeline
#ner_pipeline = pipeline("ner", model="dbmdz/bert-large-cased-finetuned-conll03-english", aggregation_strategy="simple")

# Function to encode text to a vector using OpenAI's API
def encode_text(text):
    text = text.replace("\n", " ")
    vector= client.embeddings.create(input = [text], model="text-embedding-3-small").data[0].embedding
    # Ensure the vector is a numpy array with type float32
    np_vector = np.array(vector, dtype='float32')
    # Check and reshape the vector to match the (1, dimension) shape expected by FAISS
    if np_vector.ndim == 1:
        np_vector = np_vector.reshape(1, -1)
    # Check if the vector dimension matches the index dimension
    if np_vector.shape[1] != dimension:
        raise ValueError(f"Vector dimension {np_vector.shape[1]} does not match index dimension {dimension}.")
    
    print(f"Vector shape: {np_vector.shape}")
    return np_vector

# Initialize FAISS index
dimension = 1536  # Adjust based on the chosen embedding model's output dimension
index = faiss.IndexFlatL2(dimension)
metadata_list = []

import spacy
# Function to extract metadata using NER
def extract_metadata(text):
     # Load the pre-trained SpaCy model
    nlp = spacy.load("en_core_web_sm")
    
    # Process the text through the model
    doc = nlp(text)
    
    # Extract entities
    entities = []
    for ent in doc.ents:
        entities.append((ent.text, ent.label_))

    metadata = {"project": [], "people": [], "date": []}
    for entity in entities:
        if entity[1] == "PERSON":
            metadata["people"].append(entity[0])
        elif entity[1] == "ORG":  # Adjust based on your requirements
            metadata["project"].append(entity[0])
        elif entity[1] == "DATE":
            metadata["date"].append(entity[0])
    return metadata

# Traverse folder and process files
def process_folder(folder_path):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".md"):
                file_path = os.path.join(root, file)
                with open(file_path, "r", encoding="utf-8") as md_file:
                    content = md_file.read()
                    vector = encode_text(content)
                    # FAISS requires vectors to be in a 2D numpy array
                    faiss_vector = np.array(vector).astype('float32').reshape(1, -1)
                    index.add(faiss_vector)  # Add vector to FAISS index
                    metadata = extract_metadata(content)
                    metadata["folder"] = root  # Add folder to metadata
                    metadata_list.append(metadata)

# Example folder - change as needed
process_folder('/users/luis/Documents/obsvault/1on1')

# Example search and metadata retrieval
def search(query, k=5):
    query_vector = encode_text(query)
    # FAISS requires query vectors to be in a 2D numpy array
    faiss_query_vector = np.array(query_vector).reshape(1, -1).astype('float32')
    D, I = index.search(faiss_query_vector, k)
    results = []
    for i in I[0]:
        results.append(metadata_list[i])
    return results

# Replace 'your_query_here' with your actual query
search_results = search("meeting with david donnellan")
for result in search_results:
    print(result)
