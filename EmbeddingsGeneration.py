import numpy as np
from openai import OpenAI
from config import openai_api_key
import sqlite3
import chromadb
from tqdm import trange

from sklearn.metrics.pairwise import cosine_similarity
vclient = chromadb.PersistentClient('paper_embeddings.db')

try:
   vclient.delete_collection("PaperEmbeddings")
except:
   pass

conn = sqlite3.connect('papers.db')
c = conn.cursor()

vcol = vclient.create_collection("PaperEmbeddings")
client = OpenAI(api_key=openai_api_key)

"""
Just so you know - the embedding function returns a list
"""
def get_embedding(text, model="text-embedding-3-small"):
   text = text.replace("\n", " ")
   return client.embeddings.create(input = [text], model=model).data[0].embedding

c.execute("SELECT PaperID, Title, Abstract FROM Papers;")
paper_ids = c.fetchall()

for x in trange(len(paper_ids)):
   paper = paper_ids[x]
   paper_id = paper[0]
   paper_title = paper[1]
   paper_abstract = paper[2]
   paper_contents = "Title: " + paper_title + ". " + "Abstract: " + paper_abstract
   paper_embedding = get_embedding(paper_contents)

   vcol.add(paper_id, embeddings=paper_embedding)



print(paper_ids)

