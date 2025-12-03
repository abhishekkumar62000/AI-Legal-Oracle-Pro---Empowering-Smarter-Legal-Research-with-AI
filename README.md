
---

# ⚖️ **AI Legal Oracle Pro**

### **Empowering Smarter Legal Research with AI Agents**

<p align="center">
  <img src="https://github.com/user-attachments/assets/6283838c-8640-4f22-87d4-6d4bfcbbb093" width="120">
</p>

### **🔗 Live App:**

[https://ai-legal-oracle-pro---empowering-smarter-legal-research.streamlit.app/](https://ai-legal-oracle-pro---empowering-smarter-legal-research.streamlit.app/)

---

# 🚀 **AI Legal Oracle Pro – Complete Overview**

AI Legal Oracle Pro is an advanced **AI-powered legal research assistant** designed to help lawyers, students, professionals, and businesses analyze documents, extract citations, compare contracts, generate insights, and answer legal questions using RAG (Retrieval Augmented Generation).

It combines **Streamlit**, **LangChain**, **OpenAI**, and **FAISS** to deliver a fast, interactive, and insightful legal intelligence platform.

---

# ⚡ Quick Overview

### **🎯 Purpose**

A full-stack **AI legal research assistant** that can:

* Analyze legal documents (PDF, DOCX, TXT)
* Extract citations, clauses, entities, and case references
* Perform RAG-based legal Q&A
* Compare contracts topic-wise
* Provide risk scoring + analytics
* Generate legal drafts
* Create legal timelines
* Support collaborative annotations

---

# 🖥️ **Frontend (Streamlit UI)**

* Sidebar **Control Panel** for switching modes
* Modern gradient UI
* Clean layout with metric cards
* Quick action buttons
* Demo mode for instant testing
* Multi-tab structured workflow

---

# 🧠 **AI Core Engine**

* **LangChain** for RAG pipelines
* **OpenAI embeddings** (text-embedding-3-small)
* **FAISS Vector Store** for fast semantic search
* Intelligent fallback retriever when FAISS isn’t available
* Chat powered by **ChatOpenAI**

---

# 🗂️ **Modes & Capabilities**

### **1. Document Analysis**

* Upload PDFs, DOCX, or TXT
* PyPDF2 + DOCX extraction
* Document cleaning & chunking
* Embedding + vector indexing
* Citation detection
* Entity extraction
* Risk scoring
* Annotated analysis

---

### **2. Legal Chat (RAG Q&A)**

* Retrieval-based question answering
* Chat with context + citations
* Fallback simple retriever when FAISS unavailable
* Suggested prompts
* Recent chat history

---

### **3. Citation Finder**

Detects and visualizes:

* IPC sections
* Constitution articles
* Case references
* Sections & clauses
* Multi-category classification

Plotly-based visual hooks included.

---

### **4. Compare Documents**

Topic-wise comparison across multiple files:

* Termination
* Payment
* Confidentiality
* Liability
* Duration
* Jurisdiction

Includes:

* Context snippets
* Stats
* Common themes
* Bar chart visualization

---

### **5. Advanced Analytics**

* Risk gauge visualization
* Pie chart distribution
* Entities (dates, amounts, emails, phones)
* Insights cards
* Query timeline
* Knowledge graph demo

---

### **6. Draft & Review**

Generate drafts for:

* NDA
* Employment Contract
* Service Agreement
* Lease Agreement
* Custom templates

Includes AI review suggestions.

---

### **7. Semantic Search**

Search across all uploaded documents:

* Natural language queries
* Semantic scoring
* Answers with citations
* Source snippets

---

### **8. Legal Timeline**

* Case/event timeline builder
* Add custom events
* Plotly timeline renderer

---

### **9. Regulatory Monitoring**

Track legal domains:

* Data Protection
* Labour Law
* Tax Compliance
* Custom regulatory alerts

(Mock integration for demo.)

---

### **10. Collaboration**

* Multi-user style annotation system
* Attach comments to specific document sections
* Clean UI for shared notes

---

# 🎨 **UI/UX Enhancements**

* Gradient themes
* Modern card components
* Developer photo in sidebar
* Status indicators (Docs processed, API key, FAISS status)
* Reset & cleanup buttons
* Smooth layout transitions

---

# 🛠️ **Tech Stack & Architecture**

### **Core Libraries**

* Streamlit
* PyPDF2
* python-docx (optional)
* LangChain + LangChain Community
* OpenAI
* FAISS
* Plotly
* NetworkX
* Pandas
* Python-Dotenv

### **Config**

* Uses `.env` for OpenAI key
* Streamlit `secrets` preferred for deployment

---

# 🏗️ **Stability**

README recommends using:

```
app_stable.py
```

for best reliability.
Enhanced versions include more features but add complexity.

---

# 🔄 **User Flow**

### **1. Upload → Process → Analyze**

Upload documents → Extract text → Chunk → Embed → Index.

### **2. Chat & Search**

RAG Q&A → Source snippets → Citation-backed answers.

### **3. Explore Analytics**

Risk → Entities → Insights → Knowledge Graph.

### **4. Compare Documents**

Topic-based analysis & visualization.

### **5. Draft Documents**

Auto-generate & review legal drafts.

### **6. Timeline / Monitoring / Collaboration**

Manage legal events & notes.

---

# ⚠️ Limitations

* Regex-based citation extraction may need tuning
* Knowledge graph is demo-based
* DOCX requires python-docx installed
* FAISS availability varies; simple retriever used as fallback

---

# 📦 Requirements

```
streamlit
PyPDF2
langchain
langchain-community
pandas
plotly
networkx
openai
python-dotenv
faiss-cpu
python-docx
```

---

# 🙌 Contribute / Suggest Features

Pull requests and feature suggestions are welcome!

---

---

# 🌳 **AI Legal Oracle Pro – LangGraph Workflow Tree**

```
AI Legal Oracle Pro (Main App)
│
├── 1. Initialization Layer
│     ├── Load Environment (.env / Streamlit Secrets)
│     ├── Initialize OpenAI Client
│     ├── Check python-docx availability
│     ├── Setup Session State
│     ├── Create Empty Store:
│     │       ├── uploaded_docs[]
│     │       ├── extracted_text{}
│     │       ├── chunks{}
│     │       ├── embeddings{}
│     │       ├── vector_store (FAISS or fallback retriever)
│     │       ├── citations[]
│     │       ├── entities{}
│     │       ├── risk_scores{}
│     │       ├── chat_history[]
│     │       └── analytics{}
│
├── 2. UI Controller (Mode Router)
│     ├── Document Analysis
│     ├── Legal Chat (RAG)
│     ├── Citation Finder
│     ├── Compare Documents
│     ├── Draft & Review
│     ├── Semantic Search
│     ├── Advanced Analytics
│     ├── Legal Timeline
│     ├── Regulatory Monitoring
│     └── Collaboration / Annotations
│
├── 3. Document Intake Pipeline
│     ├── Upload Handler
│     │     ├── PDF
│     │     ├── DOCX (if supported)
│     │     └── TXT
│     ├── Extract Text
│     │     ├── PyPDF2 → pages + metadata
│     │     ├── python-docx → paragraphs
│     │     └── raw text read (TXT)
│     ├── Clean Text
│     │     └── whitespace + formatting normalization
│     ├── Chunking
│     │     ├── RecursiveCharacterTextSplitter
│     │     ├── chunk_size: 1000–1200
│     │     └── overlap: 100–150
│     └── Embeddings + Vector Index
│           ├── OpenAI embeddings (text-embedding-3-small)
│           ├── try: FAISS vector_store
│           └── except: SimpleRetriever fallback
│
├── 4. Legal Chat Pipeline (RAG)
│     ├── Input Question
│     ├── Retrieve Context
│     │     ├── vector_store.as_retriever(k=4)
│     │     └── or SimpleRetriever
│     ├── Compose Prompt
│     │     ├── context summary
│     │     ├── safety instructions
│     │     └── “Answer only from provided text”
│     ├── LLM Response
│     │     └── ChatOpenAI model (gpt-4o-mini, gpt-4o, etc.)
│     ├── Attach Citations
│     └── Save to chat_history[]
│
├── 5. Citation Extraction Pipeline
│     ├── Regex Engine
│     │     ├── IPC sections (Section \d+)
│     │     ├── Constitution articles (Article \d+)
│     │     ├── Case references (X vs Y)
│     │     └── Clauses / subsections
│     ├── Classification Layer
│     │     ├── Criminal Law
│     │     ├── Civil Law
│     │     ├── Constitution
│     │     └── Others
│     └── Visualization Layer
│           └── Plotly chart hooks
│
├── 6. Risk & Entity Analytics Engine
│     ├── Risk Detection
│     │     ├── keyword heuristic scoring
│     │     ├── risk levels: High / Medium / Low
│     │     └── percentage score output
│     ├── Entity Extraction
│     │     ├── Dates
│     │     ├── Monetary amounts
│     │     ├── Emails
│     │     └── Phone numbers
│     └── Insights Engine
│           ├── strengths
│           ├── concerns
│           └── query timeline analytics
│
├── 7. Compare Documents Workflow
│     ├── Document Selector
│     ├── Topic Selector
│     │     ├── Termination
│     │     ├── Payment
│     │     ├── Confidentiality
│     │     ├── Liability
│     │     ├── Jurisdiction
│     │     └── Duration
│     ├── Context Extraction per Topic
│     ├── Document Statistics
│     └── Common Theme Extraction
│           └── frequency-based bar chart
│
├── 8. Drafting & Review Workflow
│     ├── Template Selector
│     │     ├── NDA
│     │     ├── Service Agreement
│     │     ├── Employment Contract
│     │     ├── Lease
│     │     └── Custom
│     ├── Input fields (Parties, Dates, Terms)
│     ├── Draft Generation (LLM)
│     └── Review Suggestions
│
├── 9. Semantic Search Engine
│     ├── Query Input
│     ├── Search over vector index
│     ├── Retrieve top-K chunks
│     ├── Compose Answer
│     └── Attach citations
│
├── 10. Legal Timeline System
│     ├── Timeline Data Store
│     ├── Add Event
│     ├── Plotly Timeline Rendering
│     └── Reverse Y-axis for readability
│
├── 11. Regulatory Monitoring System
│     ├── Tracked Topics
│     │     ├── Data Protection
│     │     ├── Labour Law
│     │     ├── Tax Compliance
│     │     └── Custom
│     ├── Generate Alerts (mock)
│     └── Display Alerts
│
└── 12. Collaboration / Annotations System
      ├── Select Document Section
      ├── Add Annotation (comment + user)
      ├── Store to annotation list
      └── Display annotations in UI
```
                                 [AI Legal Oracle Pro]
                                        /       \
                                       /         \
                         [Initialize System]     [UI Mode Router]
                           /           \            /          \
                          /             \          /            \
        [Load API Keys & Env]   [Setup Session]  [Analysis]   [Chat & Others]
                   /    \            /    \        /   \           /     \
                  /      \          /      \      /     \         /       \
     [OpenAI Client] [Check DOCX] [Store Init] [Flags] [Doc Intake] [Other Modes]
          /   \              / \        / \       / \         / \        /    \
         /     \            /   \      /   \     /   \       /   \      /      \
 [Embeddings] [LLM Ready] [docs] [text] [chunks] [index] [Upload] [Chunk] [Citation] [Compare]
        / \                    / \       /  \      /  \     /  \     / \       / \        /  \
       /   \                  /   \     /    \    /    \   /    \   /   \     /   \      /    \
 [VectorDB] [Fallback] [risk] [entity] [FAISS] [fallback] [extract] [clean] [regex] [viz] [themes] [stats]
       / \                     / \        / \       / \      / \     / \      / \        / \      / \
      /   \                   /   \      /   \     /   \    /   \   /   \    /   \      /   \    /   \
 [Retriever] [Search]  [dates] [money] [load] [save] [pdf] [docx] [IPC] [Articles] [keys] [topics] [compare]
       / \                                                                          
      /   \    
[Answer] [Citations]
     / \
    /   \
[Timeline] [Drafting]
    / \        / \
   /   \      /   \
[events] [plot] [templates] [review]

---
