import re

def fixed_chunks(text, size=450, overlap=80):
    text = re.sub(r"\s+", " ", text).strip()
    out=[]
    start=0
    while start < len(text):
        end=min(len(text), start+size)
        out.append(text[start:end])
        if end == len(text): break
        start=end-overlap
    return out

def sentence_chunks(text, max_sentences=2):
    sentences=[x.strip() for x in re.split(r"(?<=[.!?])\s+", text.strip()) if x.strip()]
    return [" ".join(sentences[i:i+max_sentences]) for i in range(0,len(sentences),max_sentences)]
