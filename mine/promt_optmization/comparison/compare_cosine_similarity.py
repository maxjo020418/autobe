from sentence_transformers import SentenceTransformer
import numpy as np

def cosine_sim(a, b):
    a = a / np.linalg.norm(a)
    b = b / np.linalg.norm(b)
    return float(np.dot(a, b))

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

TARGET_DIR = "./TOC_generation(analyze)/"
OPTIMIZED = "optimized.md"
UNOPTIMIZED = "unoptimized-1.md"

with open(TARGET_DIR + OPTIMIZED) as f:
   o_resp = f.read()
with open(TARGET_DIR + UNOPTIMIZED) as f:
    uo_resp = f.read()

emb = model.encode([o_resp, uo_resp], normalize_embeddings=True)
sim = float(np.dot(emb[0], emb[1]))  # cosine normalized

print("cosine similarity:", sim)