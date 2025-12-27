from transformers import pipeline
from pprint import pprint

nli = pipeline("text-classification", model="roberta-large-mnli")

TARGET_DIR = "./TOC_generation(analyze)/"
OPTIMIZED = "optimized_compressed.md"
UNOPTIMIZED = "unoptimized-1_compressed.md"

with open(TARGET_DIR + OPTIMIZED) as f:
   o_resp = f.read()
with open(TARGET_DIR + UNOPTIMIZED) as f:
    uo_resp = f.read()

def entailment_score(premise, hypothesis):
    out = nli({"text": premise, "text_pair": hypothesis}, top_k=None)
    return out
    # d = {x["label"].lower(): x["score"] for x in out}
    # return d.get("entailment", 0.0), d.get("contradiction", 0.0), d.get("neutral", 0.0)

o_ent_uo = entailment_score(o_resp, uo_resp)
uo_ent_o = entailment_score(uo_resp, o_resp)

pprint(o_ent_uo)
pprint(uo_ent_o)

# print("optimized -> unoptimized (entail, contra, neutral):", o_ent_uo)
# print("unoptimized -> optimized (entail, contra, neutral):", uo_ent_o)
