import dotenv
import os

dotenv.load_dotenv() 

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

from glob import glob

files = glob("*")

from langchain_community.document_loaders import DirectoryLoader
loader = DirectoryLoader('/users/luis/Documents/obsvault/1on1', glob="**/*.md")
docs = loader.load()


import logging

# Create logger 
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Create console handler
c_handler = logging.StreamHandler()
c_handler.setLevel(logging.DEBUG)

# Create formatter and add to console handler
c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
c_handler.setFormatter(c_format)

# Add console handler to logger
logger.addHandler(c_handler)

# Log message
logger.info("Number of documents: %s", len(docs)) 


from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
texts = text_splitter.split_documents(docs)
embeddings = OpenAIEmbeddings()
db = FAISS.from_documents(texts, embeddings)

# let's try to search some documents
question = " what is the latest 1on1 with david donnellan, only include documents that have in the text the name of David?"
searchDocs = db.similarity_search(question)
#logger.info("Title of first document: : %s", searchDocs[0].page_content) 
#print( "Title of first document: " + searchDocs[0].page_content)

retriever = db.as_retriever(search_kwargs={"k": 3})

from langchain.prompts import PromptTemplate

template = """Use the following pieces of context to answer the question at the end. 
Keep the answer as concise as possible. 
{context}
Question: {question}
Helpful Answer:"""

QA_CHAIN_PROMPT = PromptTemplate.from_template(template)
#logger.info(QA_CHAIN_PROMPT)


from langchain_openai import OpenAI
from langchain.chains import RetrievalQA
from langchain.agents import Tool

openai_llm = OpenAI(
    openai_api_key=OPENAI_API_KEY,
    temperature=0
)



# Run the RetrievalQA chain with prompt
qa_chain = RetrievalQA.from_chain_type(
    openai_llm,
    retriever=db.as_retriever(search_kwargs={"k": 3}),
    return_source_documents=True,
    chain_type_kwargs={"prompt": QA_CHAIN_PROMPT}
)

question = "when was the latest meeting with david donnellan?"

result = qa_chain.invoke({"query": question})
print(result["result"])
print(result["source_documents"][0])