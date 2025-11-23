# Exercise 3: Retrieval-Augmented Generation (RAG)

---

## What is RAG?

**RAG = Retrieval-Augmented Generation**

### The Problem

Standard LLMs have limitations:
- ❌ Can only use knowledge from training data
- ❌ Can't access your company documents
- ❌ Can't answer questions about proprietary information
- ❌ Outdated when information changes

### The Solution: RAG

RAG augments the LLM with external knowledge by:

```
User Question
    ↓
Search your documents for relevant info
    ↓
Include found documents in the prompt
    ↓
LLM generates response using both:
  • Its training knowledge
  • Retrieved document content
    ↓
Accurate, grounded answer
```

### How RAG Works Step-by-Step

**Example: User asks "What is Python?"**

```
Step 1: USER QUESTION
   "What is Python?"

Step 2: RETRIEVE FROM DOCUMENTS
   Search finds: python_basics.txt (90% match)
                 python_packages.txt (50% match)
   
Step 3: BUILD AUGMENTED PROMPT
   System: "You are helpful assistant"
   Context: "[python_basics.txt] Python is..."
            "[python_packages.txt] Popular packages..."
   Question: "What is Python?"

Step 4: LLM GENERATES RESPONSE
   Response: "Python is a programming language..."
   (Based on documents + training knowledge)
```

### Benefits of RAG

✅ **Accurate**: Grounds answers in your actual documents  
✅ **Current**: Update documents, get updated answers  
✅ **Flexible**: No model fine-tuning needed  
✅ **Transparent**: Can show which document was used  
✅ **Scalable**: Add documents without retraining  

---

## The Two Approaches: Keyword vs Semantic

This exercise teaches you two ways to retrieve documents:

### Approach 1: Keyword Search

**How it works:**
Split query and documents into words, count matching keywords

```
Query: "What is Python?"
Words: {what, is, python}

Document 1: "Python basics"
Words: {python, basics, variables, ...}
Overlap: {python} → Score = 1

Document 2: "Java programming"
Words: {java, programming, ...}
Overlap: {} → Score = 0

Result: Document 1 wins!
```

**Pros:**
- ⚡ Very fast
- 💻 No extra model needed
- 🎯 Works for exact terms

**Cons:**
- ❌ Misses synonyms ("ML" vs "machine learning")
- ❌ Fails on typos ("Pyton" won't match "Python")
- ❌ Doesn't understand meaning

**Best for:** Fast retrieval, exact keywords, limited resources

### Approach 2: Semantic Search

**How it works:**
Convert text to embeddings (numbers), measure similarity

```
Query: "What is machine learning?"
   ↓
Embedding Model converts to vector:
[0.1, 0.5, -0.2, 0.8, 0.3, ...]

Document 1: "ML is a subset of AI"
   ↓
Embedding: [0.12, 0.48, -0.15, 0.82, 0.35, ...]
   ↓
Cosine Similarity: 0.95 ✅ (very similar!)

Document 2: "Python is a language"
   ↓
Embedding: [0.05, 0.1, 0.3, 0.2, 0.1, ...]
   ↓
Cosine Similarity: 0.42 ⚠️ (not similar)

Result: Document 1 wins (0.95 > 0.42)!
```

**Pros:**
- 🧠 Understands meaning, not just keywords
- 🔄 Works with synonyms ("ML" = "machine learning")
- 📝 Handles paraphrasing

**Cons:**
- 🐢 Slower (needs embedding generation)
- 📦 Requires separate embedding model
- 💾 Uses more memory

**Best for:** Better accuracy, general questions, understanding intent

---

## Key Differences Table

| Aspect | Keyword Search | Semantic Search |
|--------|---|---|
| **Speed** | ⚡ Very fast | 🐢 Slower |
| **Accuracy** | 🎯 Exact match | 🧠 Understands intent |
| **Synonyms** | ❌ "ML" ≠ "machine learning" | ✅ "ML" ≈ "machine learning" |
| **Setup Complexity** | ✅ Simple | ⚠️ Need embedding model |
| **Best for** | Known exact keywords | General questions |
| **Example Match** | "Python" → "Python" | "ML" → ML papers, ML courses, etc. |

---

## Exercise 3a: Keyword Search for RAG

**Start here!** Learn the fundamentals with simple keyword matching.

### What You'll Do

1. Load documents into memory
2. Match queries using keyword overlap
3. Experiment with `top_k` (how many documents to retrieve)
4. Observe which documents are relevant

### Quick Start

```powershell
python exercises/03_retrieval_augmented_generation/3a_keyword_search.py
```

### Test It

Ask these questions and observe what documents are retrieved:

```
You: What is Python?
You: Tell me about OOP
You: What are transformers?
```

### Commands

```
history   → Show conversation history
docs      → List all loaded documents
mode      → Show current retrieval mode
exit      → Quit chat
```

### TODO: Experiment with top_k

Inside the code, try changing `top_k`:

```python
# Try these values
top_k = 1  # Only use 1 document
top_k = 3  # Use 3 documents (default)
top_k = 5  # Use 5 documents
```

For each value, ask the same questions and observe:
- Do answers improve with more documents?
- Is there a point where more documents don't help?
- Which value seems best for your questions?

### Key Insights

✅ Keyword search is **fast and simple**  
✅ Works well for **exact term matching**  
⚠️ Misses **semantic relationships**  
⚠️ Fails on **synonyms** (e.g., "ML" vs "machine learning")  

---

## Exercise 3b: Semantic Search with Embeddings

**After 3a!** Compare with semantic search using embeddings.

### What You'll Do

1. Load an embedding model (converts text to vectors)
2. Generate embeddings for all documents
3. Find similar documents using cosine similarity
4. Compare results with Exercise 3a

### Embedding Models

Choose one of these models (they're fast and work well):

**1. all-MiniLM-L6-v2-f16.gguf** ⭐ **RECOMMENDED**
- Size: 22 MB
- Speed: Fast ⚡
- Quality: Good for most use cases

**2. bge-small-en-v1.5-f16.gguf**
- Size: 27 MB  
- Speed: Slightly slower 🐢
- Quality: Better for complex queries

### Quick Start

```powershell
python exercises/03_retrieval_augmented_generation/3b_semantic_search.py
```

### TODO: Load the Embedding Model

In the code, find this section and uncomment it:

```python
# TODO: Uncomment this to load the embedding model
# Choose one of the two models above
embedding_model = Llama(
    model_path="./models/all-MiniLM-L6-v2-f16.gguf",
    embed=True,
    n_threads=4
)
```

### Test It

Ask the same questions as Exercise 3a:

```
You: What is Python?
You: Tell me about OOP
You: What are transformers?
```

Compare the results!

### Compare 3a vs 3b

Ask these edge-case questions in both:

```
3a: "ML basics"
    Result: Might find nothing (no exact "ML")

3b: "ML basics"
    Result: Should find machine learning docs ✅

3a: "neural networks"
    Result: Finds docs with exact phrase

3b: "neural networks"
    Result: Finds semantically related docs ✅
```

### Commands

```
history   → Show conversation history
docs      → List all loaded documents
mode      → Show current retrieval mode (keyword/semantic)
exit      → Quit chat
```

### Key Insights

✅ Semantic search understands **meaning, not just words**  
✅ Works with **synonyms** (ML = machine learning)  
✅ Handles **paraphrasing** (different ways to ask same thing)  
⚠️ Slower than keyword search (requires embedding generation)  
⚠️ Requires separate embedding model  

---

## Exercise 3c: Hybrid Search (Optional Advanced)

**After 3a and 3b!** Combine both approaches for best results.

**Hybrid Pattern**: Combine keyword and semantic search with weights.

### What You'll Do

1. Load both embedding and text models
2. Calculate keyword scores (term overlap)
3. Calculate semantic scores (cosine similarity)
4. Combine with weights: **70% semantic + 30% keyword**
5. Compare results with 3a and 3b

### Why Hybrid Search?

Hybrid search balances the strengths of both approaches:

```
Semantic (Understanding): Finds "machine learning" when you ask "ML"
Keyword (Precision):      Finds exact "Python" when important

Hybrid (Best of both):    Finds both! Gets intent + catches exact terms
```

### Quick Start

```powershell
python exercises/03_retrieval_augmented_generation/3c_hybrid_search.py
```

### The Hybrid Formula

**Current weighting:**
```python
# 70% semantic similarity + 30% keyword overlap
hybrid_score = (0.7 * semantic) + (0.3 * keyword)
```

**Try different weights:**
```python
# More semantic (better for general questions)
hybrid_score = (0.8 * semantic) + (0.2 * keyword)

# More keyword (better for exact matches)
hybrid_score = (0.6 * semantic) + (0.4 * keyword)

# Equal balance (try both equally)
hybrid_score = (0.5 * semantic) + (0.5 * keyword)
```

### TODO: Experiment with Weights

In the code, find the hybrid formula and try changing the weights:

```python
# TODO: Try different weight combinations
# Current: (0.7 * semantic) + (0.3 * keyword)
# Change to: (0.8 * semantic) + (0.2 * keyword)
# or: (0.6 * semantic) + (0.4 * keyword)
# Which works best for your questions?
```

### Test It

Ask the same questions from 3a and 3b:

```
You: What is Python?
You: Tell me about OOP
You: machine learning basics
You: neural network training
```

Observe the hybrid scores - you should see both components working together!

### Compare All Three

Run the same question through all three:

```
Question: "ML basics"

3a (Keyword):  
  Finds: Nothing (no exact "ML" keyword)
  Score: 0.0

3b (Semantic):
  Finds: embeddings_and_vectors.txt, llms_and_transformers.txt
  Score: 0.85, 0.72

3c (Hybrid):
  Finds: Same as 3b but weighted with keywords
  Score: Balanced combination
```

### Commands

```
history   → Show conversation history
docs      → List all loaded documents
mode      → Show current retrieval mode (hybrid)
exit      → Quit chat
```

### Use Cases for Hybrid Search

Hybrid search is ideal when you need both:

**Financial Systems:**
- Must find exact terms ("derivative", "hedge")
- Also understand intent ("how to reduce risk")

**Customer Support:**
- Exact FAQ matches important
- But also understand paraphrased questions

**Legal Documents:**
- Specific clauses matter ("force majeure")
- Context and relationships important

**E-Commerce Search:**
- Product names must match ("iPhone 15")
- But users search with synonyms ("Apple phone")

---

## All Three Methods Compared

| Aspect | 3a (Keyword) | 3b (Semantic) | 3c (Hybrid) |
|--------|---|---|---|
| **Speed** | ⚡⚡⚡ Very fast | 🐢 Slow | ⚡⚡ Moderate |
| **Accuracy** | 🎯 Exact match only | 🧠 Understands intent | 🎯+🧠 Balanced |
| **Synonyms** | ❌ "ML" ≠ "machine learning" | ✅ "ML" ≈ "machine learning" | ✅ Both work |
| **Setup** | ✅ Simple, no models | ⚠️ Embedding model | ⚠️ Embedding model |
| **Best for** | Known exact keywords | General questions | Both types |
| **Formula** | Term overlap count | Cosine similarity | 70%+30% weights |
| **When to use** | FAQ/known queries | Understanding intent | Balance both |  

---

## What Makes Embeddings Work?

### The Idea

Text can be represented as vectors (lists of numbers):

```
Text: "Python is great"
   ↓
Embedding Model
   ↓
Vector: [0.12, 0.45, -0.33, 0.89, ...]
```

Similar text has similar numbers! For example:
- "Python" embedding ≈ "Python programming" embedding
- "ML" embedding ≈ "machine learning" embedding
- "Python" embedding ≠ "Java" embedding

### Cosine Similarity Formula

How similar are two vectors? Use cosine similarity:

```python
def cosine_similarity(vec1, vec2):
    dot = sum(a * b for a, b in zip(vec1, vec2))
    norm1 = sqrt(sum(a*a for a in vec1))
    norm2 = sqrt(sum(b*b for b in vec2))
    return dot / (norm1 * norm2)
```

Result ranges from **0 to 1**:
- **1.0** = identical (or very similar meaning)
- **0.5** = moderately similar
- **0.0** = completely different meaning

### In Practice

```
Query embedding: [0.1, 0.5, -0.2, 0.8]
Doc 1 embedding: [0.12, 0.48, -0.15, 0.82]
Similarity: 0.97 ✅ Very relevant!

Query embedding: [0.1, 0.5, -0.2, 0.8]
Doc 2 embedding: [0.8, 0.1, 0.3, 0.05]
Similarity: 0.31 ⚠️ Not relevant
```

---

## Available Documents

Both exercises use these documents in `./data/`:

| File | Topic | Examples |
|------|-------|----------|
| **python_basics.txt** | Python fundamentals | Variables, types, functions, control flow |
| **python_oop.txt** | Object-oriented programming | Classes, inheritance, polymorphism, methods |
| **python_packages.txt** | Popular libraries | pip, numpy, pandas, requests, etc. |
| **llms_and_transformers.txt** | Large language models | LLMs, transformers, attention, BERT, GPT |
| **embeddings_and_vectors.txt** | Embeddings and vectors | Embeddings, cosine similarity, vector databases |

Try questions related to these topics!

---

## Common Questions

**Q: Should I always use semantic search?**  
A: Not necessarily! Use keyword search for speed, semantic search when you need better understanding, hybrid for balance.

**Q: Why is semantic search slower?**  
A: It must generate an embedding for the query and compare with all documents' embeddings.

**Q: Can I combine all approaches (hybrid)?**  
A: Yes! Hybrid search (Exercise 3c) does exactly this with weighted scoring.

**Q: What if I have thousands of documents?**  
A: All three work. For massive scale (millions), use vector databases like Pinecone, Weaviate, or Milvus.

**Q: How do I choose an embedding model?**  
A: Start with `all-MiniLM-L6-v2-f16.gguf` (fast, good quality). Use `bge-small-en-v1.5-f16.gguf` if you need better accuracy.

**Q: Can I change weights in hybrid search?**  
A: Yes! Try different combinations (80/20, 60/40, 50/50) to optimize for your use case.

---

## Summary

### What You've Learned

✅ RAG augments LLMs with external documents  
✅ **Keyword search**: fast, simple, exact matching (3a)  
✅ **Semantic search**: intelligent, understands meaning (3b)  
✅ **Hybrid search**: balanced, combines both (3c - optional)  
✅ When to use each approach  
✅ How embeddings and cosine similarity work  
✅ Real trade-offs in search strategies  

### The Three Patterns

1. **Patrón A - Palabras Clave (Keyword)**: Simple, fast, exact matches
2. **Patrón A - Semántico (Semantic)**: Intelligent, slow, understands intent
3. **Patrón B - Híbrido (Hybrid)**: Balanced approach combining both

### Workshop Progression

1. **Exercise 1**: Basic chatbot (API + memory)
2. **Exercise 2**: Memory strategies (conversation context)
3. **Exercise 3**: RAG systems (document retrieval) ← You are here
   - 3a: Keyword search
   - 3b: Semantic search
   - 3c: Hybrid search (optional advanced)
4. **Exercise 4**: Agents & tools (reasoning + tool use)

### Next Steps

→ **Exercise 4: Agents & Tools**

In Exercise 4, you'll create an AI that:
- 🧠 Remembers context (Exercise 2)
- 📚 Accesses documents (Exercise 3)
- 🛠️ Uses tools and reasons (Exercise 4)

This combination powers ChatGPT and modern AI assistants!
