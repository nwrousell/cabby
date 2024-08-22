from concurrent.futures import ThreadPoolExecutor
import json
import os
import numpy as np
from openai import OpenAI

from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

# a vector database that uses numpy and json files
class VectorDatabase:
    embedding_dimension = 1536 # dimension for openai's text-embedding-3-small model
    
    def __init__(self, embeddings_path: str = './db/embeddings.npy', documents_path: str = './db/documents.json'):
        self.embeddings_path = embeddings_path
        self.documents_path = documents_path
        
        if os.path.exists(embeddings_path) and os.path.exists(documents_path):
            print(f'loading database from {embeddings_path} and {documents_path}')
            self.embeddings = np.load(embeddings_path)
            self.documents = json.load(open(documents_path, 'rt'))
            print(f'Finished loading database. Contains {len(self.documents)} documents.')
        else:
            print("Database doesn't exist, creating...")
            self.embeddings = np.empty((0, self.embedding_dimension))
            self.documents = []
            self.save_db()
    
    '''
    Uses str_func to turn each document to a string, embeds that string,
    and adds the documents and their embeddings to the database
    '''
    def add_documents(self, documents: list, str_func = None):
        print(f'adding {len(documents)} documents to database...')
        doc_strs = list(map(str_func, documents)) if str_func is not None else documents
        vectors = np.array(self.embed_documents(doc_strs))
            
        assert vectors.shape == (len(doc_strs), self.embedding_dimension)
        
        self.embeddings = np.vstack((self.embeddings, vectors))
        self.documents += documents
        
        self.save_db()
        print(f'added {len(documents)} documents to database')
    
    def gen_embedding(self, s: str):
        return client.embeddings.create(model='text-embedding-3-small', input=s).data[0].embedding
    
    def save_db(self):
        os.makedirs('/'.join(self.embeddings_path.split("/")[:-1]), exist_ok=True)
        os.makedirs('/'.join(self.documents_path.split("/")[:-1]), exist_ok=True)
        np.save(self.embeddings_path, self.embeddings)
        json.dump(self.documents, open(self.documents_path, 'wt'))
    
    def embed_documents(self, documents: list[str]):
        with ThreadPoolExecutor(max_workers=10) as pool:
            vectors = list(pool.map(self.gen_embedding, documents))
        return vectors
    
    '''
    Performs cosine similarity of embedding to vectors in db and returns top k most-similar documents
    '''
    def retrieve_top_k(self, embedding: list[float], k: int = 5):
        embedding = np.array(embedding)
        embedding_magnitude = np.sum(embedding ** 2)
        embeddings_magnitudes = np.sum(self.embeddings ** 2, axis=-1)
        cosine_similarities = np.dot(self.embeddings, embedding) / (embedding_magnitude * embeddings_magnitudes)
        
        top_k_indices = np.argsort(cosine_similarities)[-k:]
        # top_k_scores = cosine_similarities[top_k_indices]
        top_k_documents = list(map(lambda i: self.documents[i], top_k_indices))

        return top_k_documents        
    

def make_course_str(c: dict):
    s = ''
    for k, v in c.items():
        s += f'{k}: {v}\n\n'
    return s

if __name__ == '__main__':
    courses = json.load(open('./data/all_courses.json'))
    course_strs = list(map(make_course_str, courses))
    
    db = VectorDatabase()
    db.add_documents(course_strs)
    
    