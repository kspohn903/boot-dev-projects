import os
# Use simple relative imports since they are in the same folder
from .keyword_search import InvertedIndex
from .semantic_search import ChunkedSemanticSearch

class HybridSearch():
    def __init__(self, documents):
        self.documents = documents
        
        # 1. Load stopwords to maintain consistent tokenization
        stopwords = set()
        stopwords_path = os.path.join("data", "stopwords.txt")
        if os.path.exists(stopwords_path):
            with open(stopwords_path, "r") as f:
                stopwords = set(f.read().splitlines())

        # 2. Initialize Keyword Engine with stopwords
        self.idx = InvertedIndex(stopwords) 
        
        # Use existing cache or build a new traditional index
        try:
            self.idx.load() 
        except (IOError, EOFError) as file_err:
            self.idx.build(documents)
            self.idx.save()
        
        # 3. Initialize Semantic Engine
        self.semantic_search = ChunkedSemanticSearch()
        self.semantic_search.load_or_create_chunk_embeddings(documents)

        # 4. Initialize Keyword Engine
        self.idx = InvertedIndex()
        if not os.path.exists(self.idx.index_path):
            self.idx.build(documents) # Ensure your build takes docs if needed
            self.idx.save()
        else:
            self.idx.load()

    def _normalize_scores(self, results):
        if not results:
            return []

        scores = [r["score"] for r in results]
        min_s, max_s = min(scores), max(scores)
        
        if min_s == max_s:
            for r in results:
                r["score"] = 1.0
            return results
            
        for r in results:
            r["score"] = (r["score"] - min_s) / (max_s - min_s)
        return results

    def _bm25_search(self, query, limit):
        """Helper to wrap the inverted index search."""
        self.idx.load() # Ensure index is loaded before searching
        return self.idx.bm25_search(query, limit)

    def rrf_search(self, query, k, limit=10):
        """Reciprocal Rank Fusion hybrid search (Placeholder)."""
        raise NotImplementedError("RRF hybrid search is not implemented yet.")
    
    def weighted_search(self, query, alpha=0.5, limit=5):
        # 1. Fetch oversized result sets
        internal_limit = limit * 500
        bm25_res = self._bm25_search(query, internal_limit)
        semantic_res = self.semantic_search.search_chunks(query, internal_limit)

        # 2. Normalize both sets independently
        bm25_norm = self._normalize_scores(bm25_res)
        sem_norm = self._normalize_scores(semantic_res)

        # 3. Combine scores using a map
        combined = {}
        
        for r in bm25_norm:
            doc_id = r["id"]
            combined[doc_id] = {
                "title": r["title"],
                "document": r["document"],
                "bm25": r["score"],
                "semantic": 0.0
            }
            
        for r in sem_norm:
            doc_id = r["id"]
            if doc_id in combined:
                combined[doc_id]["semantic"] = r["score"]
            else:
                combined[doc_id] = {
                    "title": r["title"],
                    "document": r["document"],
                    "bm25": 0.0,
                    "semantic": r["score"]
                }

        # 4. Calculate final hybrid scores
        final_results = []
        for doc_id, data in combined.items():
            h_score = (alpha * data["bm25"]) + ((1 - alpha) * data["semantic"])
            final_results.append({
                "title": data["title"],
                "document": data["document"],
                "hybrid_score": h_score,
                "bm25": data["bm25"],
                "semantic": data["semantic"]
            })

        # 5. Sort by hybrid score descending
        final_results.sort(key=lambda x: x["hybrid_score"], reverse=True)
        return final_results
