#!/usr/bin/env python3
"""rag_system.py -- Minimal RAG: chunk docs, embed, numpy cosine search, format context."""

import numpy as np, sys, time

SEP = "=" * 72

# ---------------------------------------------------------------------------
# Sample knowledge base
# ---------------------------------------------------------------------------
DOCS = [
    ("RAG Overview",
     "Retrieval Augmented Generation (RAG) combines retrieval-based and "
     "generation-based approaches. It retrieves relevant documents from a "
     "knowledge base, then uses a language model to generate answers based "
     "on the retrieved context. Embedding models convert text to vectors "
     "for semantic search. Retrieved documents are concatenated with the "
     "query to form an LLM prompt, reducing hallucination."),
    ("Embeddings",
     "Embedding models convert text into dense vector representations that "
     "capture semantic meaning. Popular models include OpenAI's "
     "text-embedding-ada-002 and sentence-transformers like all-MiniLM-L6-v2. "
     "Semantically similar texts map to nearby points in vector space. "
     "Cosine similarity measures distance between embeddings. Dimensionality "
     "ranges from 384 (MiniLM) to 1536 (Ada-002)."),
    ("Vector Databases",
     "Vector databases enable efficient similarity search over high-dimensional "
     "vectors. Options include ChromaDB, Pinecone, Weaviate, Milvus, and FAISS. "
     "They use ANN algorithms like HNSW and IVF for fast search with millions "
     "of vectors. Most support metadata filtering, hybrid search, and scaling."),
    ("Chunking Strategies",
     "Chunking strategies are crucial for RAG performance. Approaches include "
     "fixed-size, sentence-based, recursive, and semantic chunking. Optimal "
     "chunk size depends on the embedding model's context window. Overlapping "
     "chunks maintain context across boundaries. Typical sizes: 128-512 tokens."),
    ("Cosine Similarity",
     "Cosine similarity measures similarity between non-zero vectors as the "
     "cosine of the angle between them. Range: -1 (opposite) to 1 (identical). "
     "For unit-normalized vectors it equals the dot product. It is invariant "
     "to vector magnitude, making it suitable for comparing documents."),
    ("Prompt Engineering",
     "Prompt engineering designs inputs to communicate effectively with LLMs. "
     "Key techniques: few-shot prompting, chain-of-thought, instruction tuning. "
     "In RAG, the prompt combines the user's question with retrieved context "
     "and system instructions. Well-structured prompts improve answer quality "
     "and reduce hallucination."),
]

# ---------------------------------------------------------------------------
# Embedder with fallback
# ---------------------------------------------------------------------------
class Embedder:
    def __init__(self, dim=384):
        self.dim = dim
        self.real = False
        try:
            from sentence_transformers import SentenceTransformer
            self.model = SentenceTransformer("all-MiniLM-L6-v2", device="cpu")
            self.real = True
            self.dim = self.model.get_sentence_embedding_dimension()
        except Exception:
            pass

    def encode(self, texts):
        if self.real:
            return np.array(self.model.encode(texts, show_progress_bar=False), dtype=np.float32)
        embs = np.zeros((len(texts), self.dim), dtype=np.float32)
        for i, t in enumerate(texts):
            rng = np.random.RandomState(hash(t) % 2**31)
            v = rng.randn(self.dim).astype(np.float32)
            embs[i] = v / (np.linalg.norm(v) + 1e-10)
        return embs

# ---------------------------------------------------------------------------
# Vector store (numpy)
# ---------------------------------------------------------------------------
class VectorStore:
    def __init__(self, embedder):
        self.embedder = embedder
        self.vectors, self.chunks, self.meta = None, [], []

    def build(self, chunks, meta):
        self.chunks, self.meta = chunks, meta
        self.vectors = self.embedder.encode(chunks)

    def search(self, query, k=3):
        qv = self.embedder.encode([query])[0]
        qv /= np.linalg.norm(qv)
        sims = np.dot(self.vectors, qv)
        top = np.argsort(sims)[-k:][::-1]
        return [(self.chunks[i], self.meta[i], float(sims[i])) for i in top]

# ---------------------------------------------------------------------------
# RAG Pipeline
# ---------------------------------------------------------------------------
def rag_query(vs, question, k=2):
    t0 = time.perf_counter()
    results = vs.search(question, k=k)
    rt = (time.perf_counter() - t0) * 1000
    ctx_parts = []
    for i, (chunk, src, score) in enumerate(results, 1):
        ctx_parts.append(f"[{i}] (source: {src}, relevance: {score:.4f})\n    {chunk[:200]}")
    context = "\n\n".join(ctx_parts)
    prompt = (f"Answer the following question based on the provided context.\n\n"
              f"Question: {question}\n\nContext:\n{context}\n\nAnswer:")
    return {"chunks": [{"text": c[:120], "score": s} for c, _, s in results],
            "context": context, "prompt": prompt, "time_ms": rt}

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    print(f"  Minimal RAG System  |  NumPy {np.__version__}")
    print(SEP)

    embed = Embedder()
    print(f"  Embedder: {'sentence-transformers' if embed.real else 'simulated (numpy)'} (dim={embed.dim})")

    chunks, meta = [], []
    for src, text in DOCS:
        words = text.split()
        for i in range(0, len(words), 100):
            chunk = " ".join(words[i:i+100])
            chunks.append(chunk); meta.append(src)

    print(f"  Chunks: {len(chunks)} from {len(DOCS)} documents\n")

    vs = VectorStore(embed)
    vs.build(chunks, meta)
    print(f"  Index: {vs.vectors.shape[0]} vectors x {vs.vectors.shape[1]} dims\n{SEP}")

    queries = [
        "What is RAG and how does it work?",
        "How do embedding models represent text?",
        "What chunking strategies work best for RAG?",
    ]

    for qi, q in enumerate(queries, 1):
        print(f"\n  [Query {qi}] {q}")
        res = rag_query(vs, q)
        print(f"  Retrieved {len(res['chunks'])} chunks ({res['time_ms']:.1f}ms):")
        for c in res["chunks"]:
            print(f"    score={c['score']:.4f}: {c['text']}...")
        print(f"\n  Context (LLM prompt excerpt):")
        for line in res["prompt"].split("\n")[:7]:
            print(f"  {line}")

    print(f"\n{SEP}")
    size = vs.vectors.nbytes
    print(f"  Store: {size/1024:.1f} KB ({vs.vectors.shape[0]}x{vs.vectors.shape[1]})")
    print(f"  Dependencies: numpy only (sentence-transformers optional)")
    print("  RAG Demo Complete\n")


if __name__ == "__main__":
    main()
