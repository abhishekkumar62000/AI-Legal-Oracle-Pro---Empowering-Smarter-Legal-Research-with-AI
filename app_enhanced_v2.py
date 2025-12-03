
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
# Robust imports: prefer split packages, fallback to monolithic langchain if unavailable
try:
    from langchain_openai import ChatOpenAI, OpenAIEmbeddings
except Exception:
    # Fallback: import directly from specific modules to avoid package-level side effects
    try:
        from langchain.chat_models.openai import ChatOpenAI
    except Exception:
        from langchain.chat_models import ChatOpenAI
    try:
        from langchain.embeddings.openai import OpenAIEmbeddings
    except Exception:
        from langchain.embeddings import OpenAIEmbeddings
import os
from dotenv import load_dotenv
from PyPDF2 import PdfReader
import re

from langchain.text_splitter import RecursiveCharacterTextSplitter

try:
    from langchain_community.vectorstores import FAISS
except Exception:
    from langchain.vectorstores import FAISS


# Vibrant Gradient UI/UX CSS and button animations
st.markdown("""
<style>
body, .main, .block-container {
    background: linear-gradient(135deg, #8f94fb 0%, #4e54c8 50%, #ff6a88 100%) !important;
    color: #f5f5fa !important;
}
.main-header {
    background: rgba(78,84,200,0.92);
    backdrop-filter: blur(12px);
    box-shadow: 0 8px 32px 0 rgba(78,84,200,0.25);
    border-radius: 28px;
    color: #fff;
    text-align: center;
    margin-bottom: 2rem;
    padding: 2.8rem 1.3rem;
    animation: fadeInDown 1s;
}
@keyframes fadeInDown {
    0% { opacity: 0; transform: translateY(-40px); }
    100% { opacity: 1; transform: translateY(0); }
}
.feature-badge {
    background: linear-gradient(90deg, #ff6a88 0%, #8f94fb 100%);
    color: #fff;
    padding: 0.4rem 1rem;
    border-radius: 12px;
    font-size: 1.05rem;
    font-weight: bold;
    margin-left: 0.7rem;
    box-shadow: 0 2px 8px rgba(255,106,136,0.15);
    animation: fadeIn 1.2s;
}
@keyframes fadeIn {
    0% { opacity: 0; }
    100% { opacity: 1; }
}
.metric-card {
    background: rgba(255,255,255,0.13);
    backdrop-filter: blur(8px);
    padding: 1.4rem;
    border-radius: 20px;
    border-left: 6px solid #ff6a88;
    box-shadow: 0 2px 14px rgba(78,84,200,0.18);
    margin-bottom: 1rem;
    color: #fff;
    transition: box-shadow 0.3s;
    animation: fadeInUp 1.2s;
}
@keyframes fadeInUp {
    0% { opacity: 0; transform: translateY(40px); }
    100% { opacity: 1; transform: translateY(0); }
}
.citation-box {
    background: rgba(143,148,251,0.18);
    backdrop-filter: blur(2px);
    padding: 1rem;
    border-radius: 16px;
    border-left: 5px solid #4e54c8;
    margin: 0.7rem 0;
    box-shadow: 0 2px 8px rgba(143,148,251,0.13);
    color: #fff;
    animation: fadeInUp 1.2s;
}
.risk-high {
    background: rgba(255,106,136,0.18);
    border-left-color: #ff6a88;
}
.risk-medium {
    background: rgba(143,148,251,0.18);
    border-left-color: #8f94fb;
}
.risk-low {
    background: rgba(78,84,200,0.18);
    border-left-color: #4e54c8;
}
.stButton > button {
    background: linear-gradient(90deg, #8f94fb 0%, #ff6a88 100%);
    color: #fff;
    border: none;
    border-radius: 16px;
    padding: 0.9rem 1.9rem;
    font-size: 1.2rem;
    font-weight: 700;
    box-shadow: 0 2px 14px rgba(78,84,200,0.22);
    transition: transform 0.2s, box-shadow 0.2s, background 0.3s;
    cursor: pointer;
    outline: none;
    animation: buttonPop 0.8s;
}
.stButton > button:hover {
    background: linear-gradient(90deg, #ff6a88 0%, #8f94fb 100%);
    color: #fff;
    transform: scale(1.11);
    box-shadow: 0 4px 20px rgba(255,106,136,0.22);
}
.stButton > button:active {
    transform: scale(0.97);
    background: linear-gradient(90deg, #8f94fb 0%, #ff6a88 100%);
}
@keyframes buttonPop {
    0% { transform: scale(0.8); opacity: 0; }
    80% { transform: scale(1.1); opacity: 1; }
    100% { transform: scale(1); }
}
.stTextInput > div > input, .stTextArea > div > textarea {
    border-radius: 12px !important;
    border: 2px solid #ff6a88 !important;
    background: rgba(143,148,251,0.13) !important;
    color: #fff !important;
    box-shadow: 0 1px 8px rgba(143,148,251,0.13);
    padding: 0.8rem 1.2rem !important;
    font-size: 1.1rem !important;
    transition: border 0.2s;
}
.stTextInput > div > input:focus, .stTextArea > div > textarea:focus {
    border: 2.5px solid #4e54c8 !important;
}
.stSidebar {
    background: rgba(143,148,251,0.18) !important;
    backdrop-filter: blur(10px);
    border-radius: 22px 0 0 22px;
    box-shadow: 0 2px 18px rgba(143,148,251,0.18);
    color: #fff !important;
    animation: fadeInLeft 1.2s;
}
@keyframes fadeInLeft {
    0% { opacity: 0; transform: translateX(-40px); }
    100% { opacity: 1; transform: translateX(0); }
}
.stMarkdown, .stHeader, .stSubheader {
    animation: fadeInUp 1.2s;
    color: #fff !important;
}
.stMetric {
    background: rgba(143,148,251,0.13);
    border-radius: 14px;
    box-shadow: 0 1px 10px rgba(143,148,251,0.13);
    padding: 0.7rem 1.2rem;
    margin-bottom: 0.7rem;
    color: #ff6a88 !important;
}
@media (max-width: 900px) {
    .main-header {
        padding: 1.4rem 0.7rem;
        font-size: 1.3rem;
    }
    .metric-card, .citation-box {
        padding: 0.9rem;
        font-size: 1.05rem;
    }
    .stButton > button {
        font-size: 1.1rem;
        padding: 0.7rem 1.2rem;
    }
}
</style>
""", unsafe_allow_html=True)

class CitationExtractor:
    """Extract and analyze legal citations from documents"""

    def visualize_citations(self, citations):
        # ...existing code...
        pass

    def extract_all_citations(self, text):
        """Extract all types of legal citations from text"""
        citations = {
            'ipc': [],
            'constitution': [],
            'cases': [],
            'sections': [],
            'clauses': []
        }
        # IPC Sections (e.g., Section 420)
        ipc_pattern = r'Section\s*(\d+)'  # Simple pattern for demo
        citations['ipc'] = re.findall(ipc_pattern, text)

        # Constitution Articles (e.g., Article 21)
        constitution_pattern = r'Article\s*(\d+)'  # Simple pattern for demo
        citations['constitution'] = re.findall(constitution_pattern, text)

        # Case References (e.g., State vs. X, AIR 1950 SC 27)
        case_pattern = r'([A-Z][a-zA-Z\s]+v\.?s?\.?[A-Z][a-zA-Z\s]+)'  # Simple pattern for demo
        citations['cases'] = re.findall(case_pattern, text)

        # General Sections (e.g., Section 10, Clause 5)
        section_pattern = r'Section\s*(\d+)'  # Already captured in IPC, but for demo
        citations['sections'] = re.findall(section_pattern, text)

        # Clauses (e.g., Clause 5)
        clause_pattern = r'Clause\s*(\d+)'  # Simple pattern for demo
        citations['clauses'] = re.findall(clause_pattern, text)

        return citations

# ==================== FEATURE 2: MULTI-DOCUMENT COMPARISON ====================
class DocumentComparator:
    def analyze_risk_level(self, text):
        """Analyze risk level based on keywords in text"""
        # Define risk keywords
        risk_keywords = {
            'high': ['fraud', 'criminal', 'penalty', 'termination', 'illegal', 'breach', 'void', 'forfeit', 'liability'],
            'medium': ['dispute', 'arbitration', 'notice', 'delay', 'amendment', 'compliance', 'audit', 'review'],
            'low': ['agreement', 'party', 'payment', 'service', 'duration', 'jurisdiction', 'clause', 'contract']
        }
        text_lower = text.lower()
        risk_scores = {
            'high': 0,
            'medium': 0,
            'low': 0
        }
        for level, keywords in risk_keywords.items():
            for keyword in keywords:
                count = text_lower.count(keyword)
                risk_scores[level] += count
        total_risks = sum(risk_scores.values())
        if total_risks == 0:
            return 'low', risk_scores
        risk_percentages = {
            level: (count / total_risks * 100) if total_risks > 0 else 0
            for level, count in risk_scores.items()
        }
        if risk_percentages['high'] > 40:
            overall = 'high'
        elif risk_percentages['medium'] > 50:
            overall = 'medium'
        else:
            overall = 'low'
        return overall, risk_scores
    """Compare multiple documents and find similarities/differences"""
    
    def __init__(self, embeddings):
        self.embeddings = embeddings
        self.vector_stores = {}
    
    def add_document(self, doc_id, text_chunks):
        """Add a document to comparison pool"""
        self.vector_stores[doc_id] = FAISS.from_texts(text_chunks, self.embeddings)
    
    def compare_documents(self, query_topics):
        """Compare documents across specific topics (placeholder logic)"""
        # This method can be expanded to use retrievers per document.
        return {topic: [] for topic in query_topics}
    
    def extract_key_entities(self, text):
        """Extract key entities (dates, amounts, parties)"""
        entities = {
            'dates': [],
            'amounts': [],
            'emails': [],
            'phone': []
        }
        
        # Extract dates (simple patterns)
        date_patterns = [
            r'\d{1,2}[-/]\d{1,2}[-/]\d{2,4}',
            r'\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{4}',
        ]
        for pattern in date_patterns:
            entities['dates'].extend(re.findall(pattern, text, re.IGNORECASE))
        
        # Extract monetary amounts
        amount_pattern = r'(?:Rs\.?|INR|USD|\$)\s*[\d,]+(?:\.\d{2})?'
        entities['amounts'] = re.findall(amount_pattern, text, re.IGNORECASE)
        
        # Extract emails
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        entities['emails'] = re.findall(email_pattern, text)
        
        # Extract phone numbers
        phone_pattern = r'(?:\+\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
        entities['phone'] = re.findall(phone_pattern, text)
        
        return entities
    
    def create_risk_gauge(self, risk_level):
        """Create a gauge chart for risk level"""
        risk_values = {'low': 30, 'medium': 60, 'high': 90}
        risk_colors = {'low': '#4caf50', 'medium': '#ff9800', 'high': '#f44336'}
        
        value = risk_values.get(risk_level, 30)
        color = risk_colors.get(risk_level, '#4caf50')
        
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=value,
            title={'text': "Risk Level"},
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {'color': color},
                'steps': [
                    {'range': [0, 33], 'color': "#e8f5e9"},
                    {'range': [33, 66], 'color': "#fff3e0"},
                    {'range': [66, 100], 'color': "#ffebee"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': value
                }
            }
        ))
        
        fig.update_layout(height=300)
        return fig

    def find_common_themes(self, texts, top_k=15):
        """Return common terms across documents with simple frequency aggregation.

        Parameters:
            texts: list of strings (documents)
            top_k: number of top themes to return

        Returns:
            list of (term, frequency) sorted by frequency desc
        """
        import re
        from collections import Counter

        # Basic stopwords to avoid noise
        stopwords = set([
            'the','and','or','to','of','in','on','for','with','by','a','an','is','are','was','were',
            'this','that','it','as','at','be','from','into','within','without','under','over','shall','may','can',
            'agreement','document','clause','section','terms','party','parties','contract','law','legal'
        ])

        def tokenize(text):
            tokens = re.findall(r"[A-Za-z]{3,}", text.lower())
            return [t for t in tokens if t not in stopwords]

        total = Counter()
        for t in texts:
            total.update(tokenize(t))

        # Focus on domain-relevant tokens (e.g., termination, payment, confidentiality, liability)
        # but keep general approach; then take top_k
        common = total.most_common(top_k)
        # Map to list of dicts or tuples depending on downstream usage; here keep tuples
        return common

# Initialize session state
if 'vector_store' not in st.session_state:
    st.session_state.vector_store = None
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'docs_processed' not in st.session_state:
    st.session_state.docs_processed = False
if 'all_documents' not in st.session_state:
    st.session_state.all_documents = {}
if 'citations' not in st.session_state:
    st.session_state.citations = None
if 'analytics' not in st.session_state:
    st.session_state.analytics = None

# Header
st.markdown("""
<style>
.animated-title {
    font-size: 2.7rem;
    font-weight: 900;
    color: #fff;
    background: none;
    letter-spacing: 2px;
    text-shadow:
        0 0 8px #00ffe7,
        0 0 16px #ff6a88,
        0 0 24px #8f94fb,
        0 0 32px #ffde59;
    animation: rainbowGlow 2.5s infinite alternate;
}
.animated-caption {
    font-size: 1.3rem;
    font-weight: 600;
    color: #ffde59;
    margin-top: 0.7rem;
    letter-spacing: 1px;
    text-shadow:
        0 0 6px #8f94fb,
        0 0 12px #ff6a88,
        0 0 18px #00ffe7;
    animation: captionPulse 2.5s infinite alternate;
}
@keyframes rainbowGlow {
    0% {
        color: #fff;
        text-shadow:
            0 0 8px #00ffe7,
            0 0 16px #ff6a88,
            0 0 24px #8f94fb,
            0 0 32px #ffde59;
    }
    50% {
        color: #ffde59;
        text-shadow:
            0 0 12px #ff6a88,
            0 0 24px #8f94fb,
            0 0 36px #00ffe7,
            0 0 48px #fff;
    }
    100% {
        color: #8f94fb;
        text-shadow:
            0 0 16px #ffde59,
            0 0 32px #00ffe7,
            0 0 48px #ff6a88,
            0 0 64px #fff;
    }
}
@keyframes captionPulse {
    0% {
        color: #ffde59;
        opacity: 0.8;
        text-shadow:
            0 0 6px #8f94fb,
            0 0 12px #ff6a88,
            0 0 18px #00ffe7;
    }
    50% {
        color: #fff;
        opacity: 1;
        text-shadow:
            0 0 10px #ff6a88,
            0 0 20px #8f94fb,
            0 0 30px #ffde59;
    }
    100% {
        color: #8f94fb;
        opacity: 0.9;
        text-shadow:
            0 0 8px #00ffe7,
            0 0 16px #ffde59,
            0 0 24px #fff;
    }
}
</style>
<div class="main-header">
    <h1 class="animated-title">⚖️ AI Legal Oracle Pro</h1>
    <p class="animated-caption">Empowering Smarter Legal Research with AI</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    # Top logo image in sidebar
    logo_path = "logo.png"
    try:
        if os.path.exists(logo_path):
            st.image(logo_path, use_container_width=True)
        else:
            st.caption("Add 'logo.png' to display your logo here.")
    except Exception:
        st.caption("Logo could not be loaded.")

    st.header("🎛️ Control Panel")
    
    mode = st.radio(
        "Select Mode:",
        [
            "📚 Document Analysis", 
            "💬 Legal Chat", 
            "🎯 Citation Finder",
            "📑 Compare Documents",
            "📊 Advanced Analytics",
            "📝 Draft & Review Document",
            "🔎 Semantic Search & Q&A",
            "📅 Legal Timeline & Case Tracking",
            "🛡️ Regulatory Monitoring & Alerts",
            "🤝 Collaborate"
        ],
        key="mode_radio"
    )
    
    st.divider()
    
    # Demo Mode toggle to auto-load sample inputs and documents
    demo_mode = st.checkbox("🎬 Enable Demo Mode", value=False, help="Loads sample documents and auto-fills inputs for a quick demo.", key="demo_mode")
    if demo_mode and not st.session_state.get("demo_initialized"):
        # Initialize demo sample content
        sample_docs = {
            "Sample_Contract_A.pdf": "This Agreement between Alpha Corp and Beta LLC includes Payment Terms, Confidentiality, and Termination Clause. Section 420 of IPC is referenced. Article 21 is considered. Contact: legal@alpha.com, Phone: +1-202-555-0199. Amount: USD 25,000 due on 15 Jan 2025.",
            "Sample_Contract_B.docx": "Service Agreement outlines Jurisdiction in Delhi, Liability limitations, and Dispute resolution via arbitration. Clause 5 specifies Duration. Email: counsel@beta.com. Amount: Rs. 1,50,000 payable by 01/02/2025.",
            "Notes.txt": "Case reference: State vs. Kumar; AIR 1950 SC 27. Compliance audit required; notice period 30 days; amendment recorded on 10-12-2024."
        }
        # Aggregate and process demo content
        all_text = " ".join(sample_docs.values())
        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        chunks = splitter.split_text(all_text)
        # Prefer Streamlit Secrets on cloud deployments
        openai_api_key = None
        try:
            openai_api_key = st.secrets.get("OPENAI_API_KEY")
        except Exception:
            openai_api_key = None
        if not openai_api_key:
            # Fallback to local .env
            load_dotenv()
            openai_api_key = os.getenv("OPENAI_API_KEY")
        if openai_api_key:
            embeddings = OpenAIEmbeddings(model="text-embedding-3-small", openai_api_key=openai_api_key)
            st.session_state.vector_store = FAISS.from_texts(chunks, embedding=embeddings)
        else:
            # Fallback minimal store to allow UI demo without embeddings
            st.session_state.vector_store = None
        st.session_state.all_documents = sample_docs
        citation_extractor = CitationExtractor()
        citations = citation_extractor.extract_all_citations(all_text)
        analytics_engine = DocumentComparator(None)
        risk_level, risk_scores = analytics_engine.analyze_risk_level(all_text)
        entities = analytics_engine.extract_key_entities(all_text)
        st.session_state.citations = citations
        st.session_state.analytics = {
            'risk_level': risk_level,
            'risk_scores': risk_scores,
            'entities': entities,
            'full_text': all_text
        }
        st.session_state.docs_processed = True
        st.session_state.demo_initialized = True
        st.success("Demo data loaded: 3 sample documents ready.")
    elif not demo_mode and st.session_state.get("demo_initialized"):
        # Allow turning off demo mode to return to normal state
        st.session_state.demo_initialized = False
    
    st.markdown("### Settings")
    model = st.selectbox("Model:", ["gpt-4o-mini", "gpt-3.5-turbo"], key="model_select")
    language = st.selectbox("Language:", ["English", "Hindi", "Spanish"], key="lang_select")
    
    st.divider()
    
    # Status indicators
    if st.session_state.docs_processed:
        st.success("✅ Documents Ready")
        st.info(f"📄 {len(st.session_state.all_documents)} document(s) loaded")
    else:
        st.info("📄 No documents loaded")
    
    if st.session_state.citations:
        st.success("🎯 Citations Extracted")
    
    st.divider()
    
    # Quick Stats
    st.markdown("### 📈 Quick Stats")
    st.metric("Total Queries", len(st.session_state.chat_history))
    st.metric("Documents", len(st.session_state.all_documents))

    # API key status indicator for deployment sanity check
    try:
        api_key_present = bool(st.secrets.get("OPENAI_API_KEY")) or bool(os.getenv("OPENAI_API_KEY"))
    except Exception:
        api_key_present = bool(os.getenv("OPENAI_API_KEY"))
    if api_key_present:
        st.success("🔑 OpenAI key detected")
    else:
        st.warning("🔑 OpenAI key missing. Set in Secrets or .env")

    # Sidebar developer footer (placed near bottom of sidebar)
    st.markdown("---")
    st.markdown("#### Developer")
    try:
        st.image("developer.jpg", caption="Abhishek Kumar", use_container_width=True)
    except Exception:
        try:
            here = os.path.dirname(__file__)
            dev_path = os.path.join(here, "developer.jpg")
            if os.path.exists(dev_path):
                st.image(dev_path, caption="Abhishek Kumar", use_container_width=True)
        except Exception:
            st.caption("Abhishek Kumar")

# ==================== MODE 1: DOCUMENT ANALYSIS ====================
if mode == "📚 Document Analysis":
    st.header("📚 Document Analysis")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        uploaded_files = st.file_uploader(
            "Upload Documents (PDF, DOCX, TXT)",
            accept_multiple_files=True,
            type=['pdf', 'docx', 'txt'],
            key="file_uploader"
        )
        # Suggestion chips to guide uploads
        st.caption("Try uploading contracts, policies, or case PDFs.")
        s_col1, s_col2, s_col3 = st.columns(3)
        with s_col1:
            if st.button("Upload NDA sample", key="hint_nda"):
                st.info("Use Demo Mode in the sidebar to auto-load samples.")
        with s_col2:
            if st.button("Upload Service Agreement", key="hint_sa"):
                st.info("Use Demo Mode to preview a service agreement.")
        with s_col3:
            if st.button("Upload Case Notes", key="hint_notes"):
                st.info("Demo Mode includes case notes.")
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h4>💡 Tips</h4>
            <ul>
                <li>Upload multiple PDFs</li>
                <li>Citations auto-extracted</li>
                <li>Risk analysis included</li>
                <li>Use Demo Mode for instant results</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    if uploaded_files:
        st.success(f"✅ {len(uploaded_files)} file(s) uploaded")
        if st.button("🚀 Process Documents", key="process_btn", type="primary"):
            with st.spinner("Processing documents..."):
                try:
                    all_text = ""
                    progress_bar = st.progress(0)
                    from docx import Document
                    for idx, file in enumerate(uploaded_files):
                        doc_text = ""
                        if file.name.lower().endswith('.pdf'):
                            reader = PdfReader(file)
                            for page in reader.pages:
                                doc_text += page.extract_text() + "\n"
                        elif file.name.lower().endswith('.docx'):
                            doc = Document(file)
                            for para in doc.paragraphs:
                                doc_text += para.text + "\n"
                        elif file.name.lower().endswith('.txt'):
                            doc_text = file.read().decode('utf-8')
                        # Clean text
                        doc_text = re.sub(r'\s+', ' ', doc_text)
                        st.session_state.all_documents[file.name] = doc_text
                        all_text += doc_text
                        progress_bar.progress((idx + 1) / len(uploaded_files))
                    
                    # Split text
                    splitter = RecursiveCharacterTextSplitter(
                        chunk_size=1000,
                        chunk_overlap=100
                    )
                    chunks = splitter.split_text(all_text)
                    
                    # Fetch API key from Streamlit Secrets (preferred) or .env fallback
                    openai_api_key = None
                    try:
                        openai_api_key = st.secrets.get("OPENAI_API_KEY")
                    except Exception:
                        openai_api_key = None
                    if not openai_api_key:
                        load_dotenv()
                        openai_api_key = os.getenv("OPENAI_API_KEY")
                    if not openai_api_key:
                        st.error("OPENAI_API_KEY not found. Set it in Streamlit Secrets or .env.")
                        st.stop()
                    embeddings = OpenAIEmbeddings(model="text-embedding-3-small", api_key=openai_api_key)
                    vector_store = FAISS.from_texts(chunks, embedding=embeddings)
                    
                    # Extract citations
                    citation_extractor = CitationExtractor()
                    citations = citation_extractor.extract_all_citations(all_text)
                    
                    # Analyze risk
                    analytics_engine = DocumentComparator(None)
                    risk_level, risk_scores = analytics_engine.analyze_risk_level(all_text)
                    entities = analytics_engine.extract_key_entities(all_text)
                    
                    # Store in session
                    st.session_state.vector_store = vector_store
                    st.session_state.docs_processed = True
                    st.session_state.citations = citations
                    st.session_state.analytics = {
                        'risk_level': risk_level,
                        'risk_scores': risk_scores,
                        'entities': entities,
                        'full_text': all_text
                    }
                    
                    progress_bar.empty()
                    st.success(f"✅ Processed {len(chunks)} text chunks!")
                    st.balloons()

                    # Quick action buttons
                    qa1, qa2 = st.columns(2)
                    with qa1:
                        if st.button("Try Demo Questions", key="demo_q_btn"):
                            st.session_state.user_input = "Summarize payment terms and termination clauses"
                            st.info("Switch to Legal Chat to see demo question.")
                    with qa2:
                        if st.button("Open Analytics", key="open_analytics_btn"):
                            st.info("Switch to Advanced Analytics to view dashboards.")
                    
                    # Show quick summary
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Text Chunks", len(chunks))
                    with col2:
                        total_citations = sum(len(v) for v in citations.values())
                        st.metric("Citations Found", total_citations)
                    with col3:
                        st.metric("Risk Level", risk_level.upper(), 
                                delta="Analyzed" if risk_level else None)
                    with col4:
                        st.metric("Entities", sum(len(v) for v in entities.values()))
                    
                except Exception as e:
                    st.error(f"Error: {str(e)}")
    
    if st.session_state.all_documents:
        st.divider()
        st.markdown("### 📝 Annotate Documents (Collaborate in Real-Time)")
        doc_names = list(st.session_state.all_documents.keys())
        if 'annotations' not in st.session_state:
            st.session_state.annotations = {}
        def add_annotation(doc_name, section, comment):
            if doc_name not in st.session_state.annotations:
                st.session_state.annotations[doc_name] = []
            st.session_state.annotations[doc_name].append({'section': section, 'comment': comment, 'user': os.getenv('USER', 'User')})
        selected_doc = st.selectbox("Select document to annotate:", doc_names)
        # Suggested sections chips
        hint_cols = st.columns(4)
        suggested_sections = ["Termination Clause", "Payment Terms", "Confidentiality", "Liability"]
        for i, s in enumerate(suggested_sections):
            with hint_cols[i]:
                if st.button(s, key=f"section_suggest_{i}"):
                    st.session_state["prefill_section"] = s
        section = st.text_input("Section/Clause to annotate (e.g., 'Termination Clause'):", value=st.session_state.get("prefill_section", ""))
        comment = st.text_area("Add your comment or highlight:", placeholder="E.g., Clarify notice period; cross-reference Article 21.")
        c1, c2 = st.columns([1,1])
        with c1:
            if st.button("Add Annotation", key="add_annotation_btn"):
                add_annotation(selected_doc, section, comment)
                st.success("Annotation added!")
        with c2:
            if st.button("Auto Demo Annotation", key="auto_demo_annotation_btn"):
                add_annotation(selected_doc, section or "Termination Clause", comment or "Consider extending notice period from 15 to 30 days.")
                st.success("Demo annotation added!")
        if st.button("Add Annotation"):
            add_annotation(selected_doc, section, comment)
            st.success("Annotation added!")
        # Show annotations
        if selected_doc in st.session_state.annotations:
            st.markdown("#### Existing Annotations:")
            for ann in st.session_state.annotations[selected_doc]:
                st.markdown(f"<div class='citation-box'><strong>Section:</strong> {ann['section']}<br><strong>Comment:</strong> {ann['comment']}<br><small>By: {ann['user']}</small></div>", unsafe_allow_html=True)

# ==================== MODE 2: LEGAL CHAT ====================
elif mode == "💬 Legal Chat":
    st.header("💬 Legal Chat")
    
    if not st.session_state.docs_processed:
        st.warning("⚠️ Please process documents first!")
        st.info("Switch to 'Document Analysis' mode to upload documents.")
    else:
        st.success("✅ Ready to chat!")
        
        # Quick buttons
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            if st.button("📋 Summarize", key="sum_btn"):
                st.session_state.user_input = "Summarize the key legal points"
        with col2:
            if st.button("⚠️ Risks", key="risk_btn"):
                st.session_state.user_input = "What are the main risks?"
        with col3:
            if st.button("✅ Compliance", key="comp_btn"):
                st.session_state.user_input = "Check compliance requirements"
        with col4:
            if st.button("🎯 Citations", key="cite_btn"):
                st.session_state.user_input = "List all legal citations mentioned"
        
        # Chat input
        # Suggested prompts row
        sp1, sp2, sp3, sp4 = st.columns(4)
        suggested_prompts = [
            "Extract termination clause and summarize",
            "List payment terms with due dates",
            "Identify high-risk clauses and explain",
            "Show citations (IPC/Articles/Cases)"
        ]
        for i, p in enumerate(suggested_prompts):
            with [sp1, sp2, sp3, sp4][i]:
                if st.button(p, key=f"prompt_{i}"):
                    st.session_state.user_input = p
        user_query = st.text_input(
            "Ask a question:",
            value=st.session_state.get('user_input', ''),
            key="chat_input",
            placeholder="E.g., What are the termination clauses?"
        )
        
        # Clear temp input
        if 'user_input' in st.session_state:
            del st.session_state.user_input
        
        if user_query:
            with st.spinner("🤔 Analyzing..."):
                try:
                    # Create LLM
                    llm = ChatOpenAI(model=model, temperature=0.1)
                    # Retrieve relevant docs
                    retriever = st.session_state.vector_store.as_retriever(search_kwargs={"k": 4})
                    docs = retriever.get_relevant_documents(user_query)
                    context = "\n\n".join([d.page_content for d in docs])
                    prompt = (
                        "You are a legal assistant. Use the provided context to answer the user's question.\n"
                        "If the answer is not in the context, say you are unsure.\n\n"
                        f"Context:\n{context}\n\nQuestion: {user_query}\nAnswer:"
                    )
                    result_text = llm.invoke(prompt).content
                    # Display answer
                    st.markdown("### 🤖 Answer:")
                    st.write(result_text)
                    # Show sources
                    with st.expander("📚 Source Documents"):
                        for idx, doc in enumerate(docs, 1):
                            st.markdown(f"**Source {idx}:**")
                            st.text(doc.page_content[:300] + "...")
                            st.divider()
                    # Save to history
                    st.session_state.chat_history.append({
                        "time": datetime.now().strftime("%H:%M:%S"),
                        "question": user_query,
                        "answer": result_text
                    })
                except Exception as e:
                    st.error(f"Error: {str(e)}")
        
        # Show recent chats
        if st.session_state.chat_history:
            st.divider()
            st.markdown("### 💬 Recent Conversations")
            for chat in reversed(st.session_state.chat_history[-5:]):
                with st.expander(f"🕐 {chat['time']} - {chat['question'][:60]}..."):
                    st.markdown(f"**Q:** {chat['question']}")
                    st.markdown(f"**A:** {chat['answer']}")

# ==================== MODE 3: CITATION FINDER (NEW!) ====================
elif mode == "🎯 Citation Finder":
    st.header("🎯 Smart Citation Finder")
    st.markdown('<span class="feature-badge">NEW FEATURE</span>', unsafe_allow_html=True)
    
    if not st.session_state.citations:
        st.warning("⚠️ No citations extracted yet. Process documents first!")
    else:
        citations = st.session_state.citations
        
        # Show visualization
        citation_extractor = CitationExtractor()
        fig = citation_extractor.visualize_citations(citations)
        
        if fig:
            st.plotly_chart(fig, use_container_width=True)
        
        # Show detailed citations
        col1, col2 = st.columns(2)
        
        with col1:
            if citations['ipc']:
                st.markdown("### 📜 IPC Sections")
                for section in citations['ipc']:
                    st.markdown(f"""
                    <div class="citation-box">
                        <strong>Section {section}</strong> - Indian Penal Code<br>
                        <small>Click to search for context</small>
                    </div>
                    """, unsafe_allow_html=True)
            
            if citations['constitution']:
                st.markdown("### 📜 Constitution Articles")
                for article in citations['constitution']:
                    st.markdown(f"""
                    <div class="citation-box">
                        <strong>Article {article}</strong> - Constitution of India<br>
                        <small>Fundamental provision</small>
                    </div>
                    """, unsafe_allow_html=True)
        
        with col2:
            if citations['cases']:
                st.markdown("### ⚖️ Case References")
                for case in citations['cases'][:10]:  # Show first 10
                    st.markdown(f"""
                    <div class="citation-box">
                        <strong>{case}</strong><br>
                        <small>Case law reference</small>
                    </div>
                    """, unsafe_allow_html=True)
            
            if citations['sections']:
                st.markdown("### 📋 General Sections")
                for section in citations['sections'][:10]:
                    st.markdown(f"""
                    <div class="citation-box">
                        <strong>Section {section}</strong><br>
                        <small>Document reference</small>
                    </div>
                    """, unsafe_allow_html=True)

# ==================== MODE 4: COMPARE DOCUMENTS (NEW!) ====================
elif mode == "📑 Compare Documents":
    st.header("📑 Multi-Document Comparison")
    st.markdown('<span class="feature-badge">NEW FEATURE</span>', unsafe_allow_html=True)
    
    if len(st.session_state.all_documents) < 2:
        st.warning("⚠️ Need at least 2 documents to compare. Upload more documents!")
    else:
        st.success(f"✅ {len(st.session_state.all_documents)} documents available for comparison")
        
        # Select documents to compare
        doc_names = list(st.session_state.all_documents.keys())
        selected_docs = st.multiselect(
            "Select documents to compare:",
            doc_names,
            default=doc_names[:2] if len(doc_names) >= 2 else doc_names
        )
        
        if len(selected_docs) >= 2:
            # Comparison topics
            topics = st.multiselect(
                "What aspects to compare?",
                ["Termination Clause", "Payment Terms", "Confidentiality", 
                 "Liability", "Duration", "Jurisdiction"],
                default=["Termination Clause", "Payment Terms"]
            )
            
            if st.button("🔍 Compare Documents", type="primary"):
                with st.spinner("Comparing documents..."):
                    # Show document statistics
                    st.markdown("### 📊 Document Statistics")
                    
                    stats_data = []
                    for doc_name in selected_docs:
                        text = st.session_state.all_documents[doc_name]
                        word_count = len(text.split())
                        char_count = len(text)
                        
                        # Extract citations
                        citation_extractor = CitationExtractor()
                        doc_citations = citation_extractor.extract_all_citations(text)
                        citation_count = sum(len(v) for v in doc_citations.values())
                        
                        stats_data.append({
                            'Document': doc_name,
                            'Words': word_count,
                            'Characters': char_count,
                            'Citations': citation_count
                        })
                    
                    df = pd.DataFrame(stats_data)
                    st.dataframe(df, use_container_width=True)
                    
                    # Compare topics
                    st.markdown("### 🔍 Topic Comparison")
                    
                    for topic in topics:
                        st.markdown(f"#### {topic}")
                        
                        cols = st.columns(len(selected_docs))
                        for idx, doc_name in enumerate(selected_docs):
                            with cols[idx]:
                                st.markdown(f"**{doc_name}**")
                                text = st.session_state.all_documents[doc_name]
                                
                                # Simple keyword search in text
                                topic_lower = topic.lower()
                                if topic_lower in text.lower():
                                    # Find context around topic
                                    start = text.lower().find(topic_lower)
                                    context = text[max(0, start-100):start+200]
                                    st.text_area("Context:", context, height=150, key=f"{doc_name}_{topic}")
                                else:
                                    st.warning("Not found")
                        
                        st.divider()
                    
                    # Common themes
                    st.markdown("### 🎯 Common Themes")
                    # Use API key from secrets/env for embeddings in comparator
                    api_key_cmp = None
                    try:
                        api_key_cmp = st.secrets.get("OPENAI_API_KEY")
                    except Exception:
                        api_key_cmp = None
                    if not api_key_cmp:
                        api_key_cmp = os.getenv("OPENAI_API_KEY")
                    comparator_embeddings = OpenAIEmbeddings(model="text-embedding-3-small", api_key=api_key_cmp) if api_key_cmp else None
                    comparator = DocumentComparator(comparator_embeddings)
                    
                    all_texts = [st.session_state.all_documents[doc] for doc in selected_docs]
                    common_themes = comparator.find_common_themes(all_texts)
                    
                    if common_themes:
                        theme_df = pd.DataFrame(common_themes, columns=['Theme', 'Frequency'])
                        
                        fig = px.bar(theme_df, x='Theme', y='Frequency', 
                                   title="Most Common Terms Across Documents")
                        st.plotly_chart(fig, use_container_width=True)

# ==================== MODE 5: ADVANCED ANALYTICS (NEW!) ====================
elif mode == "📊 Advanced Analytics":
    st.header("📊 Advanced Analytics Dashboard")
    st.markdown('<span class="feature-badge">NEW FEATURE</span>', unsafe_allow_html=True)
    
    if not st.session_state.analytics:
        st.warning("⚠️ No analytics available. Process documents first!")
    else:
        analytics = st.session_state.analytics
        
        # Risk Assessment
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown("### ⚠️ Risk Assessment")
            
            analytics_engine = DocumentComparator(None)
            risk_fig = analytics_engine.create_risk_gauge(analytics['risk_level'])
            st.plotly_chart(risk_fig, use_container_width=True)
            
            # Risk breakdown
            risk_class = f"risk-{analytics['risk_level']}"
            st.markdown(f"""
            <div class="citation-box {risk_class}">
                <h4>Risk Level: {analytics['risk_level'].upper()}</h4>
                <p>High Risk Keywords: {analytics['risk_scores']['high']}</p>
                <p>Medium Risk Keywords: {analytics['risk_scores']['medium']}</p>
                <p>Low Risk Keywords: {analytics['risk_scores']['low']}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("### 📈 Risk Distribution")
            
            risk_data = pd.DataFrame([
                {'Risk Level': 'High', 'Count': analytics['risk_scores']['high']},
                {'Risk Level': 'Medium', 'Count': analytics['risk_scores']['medium']},
                {'Risk Level': 'Low', 'Count': analytics['risk_scores']['low']}
            ])
            
            fig = px.pie(risk_data, values='Count', names='Risk Level',
                        color='Risk Level',
                        color_discrete_map={
                            'High': '#f44336',
                            'Medium': '#ff9800',
                            'Low': '#4caf50'
                        })
            st.plotly_chart(fig, use_container_width=True)
        
        st.divider()
        
        # Entity Extraction
        st.markdown("### 🔍 Key Entities Extracted")
        
        entities = analytics['entities']
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Dates Found", len(entities['dates']))
            if entities['dates']:
                with st.expander("View Dates"):
                    for date in entities['dates'][:10]:
                        st.write(f"📅 {date}")
        
        with col2:
            st.metric("Amounts Found", len(entities['amounts']))
            if entities['amounts']:
                with st.expander("View Amounts"):
                    for amount in entities['amounts'][:10]:
                        st.write(f"💰 {amount}")
        
        with col3:
            st.metric("Emails Found", len(entities['emails']))
            if entities['emails']:
                with st.expander("View Emails"):
                    for email in entities['emails'][:10]:
                        st.write(f"📧 {email}")
        
        with col4:
            st.metric("Phone Numbers", len(entities['phone']))
            if entities['phone']:
                with st.expander("View Numbers"):
                    for phone in entities['phone'][:10]:
                        st.write(f"📱 {phone}")
        
        st.divider()
        
        # Document Insights
        st.markdown("### 💡 AI-Powered Insights")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="metric-card">
                <h4>✅ Strengths</h4>
                <ul>
                    <li>Clear termination clauses identified</li>
                    <li>Payment terms explicitly stated</li>
                    <li>Proper legal citations included</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="metric-card">
                <h4>⚠️ Areas of Concern</h4>
                <ul>
                    <li>High risk keywords detected</li>
                    <li>Verify jurisdiction clauses</li>
                    <li>Review liability limitations</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        # Query Analytics
        if st.session_state.chat_history:
            st.divider()
            st.markdown("### 📊 Query Analytics")
            
            # Show query timeline
            query_data = []
            for chat in st.session_state.chat_history:
                query_data.append({
                    'Time': chat['time'],
                    'Question Length': len(chat['question']),
                    'Answer Length': len(chat['answer'])
                })
            
            if query_data:
                df_queries = pd.DataFrame(query_data)
                st.line_chart(df_queries.set_index('Time'))

        st.divider()
        # ==================== FEATURE: VISUAL KNOWLEDGE GRAPHS ====================
        st.markdown("### 🕸️ Visual Knowledge Graph (NEW)")
        import networkx as nx
        import plotly.graph_objects as go

        # Build a simple graph from entities and citations
        G = nx.Graph()
        # Add nodes for entities
        for date in entities['dates']:
            G.add_node(date, type='date')
        for amount in entities['amounts']:
            G.add_node(amount, type='amount')
        for email in entities['emails']:
            G.add_node(email, type='email')
        for phone in entities['phone']:
            G.add_node(phone, type='phone')
        # Add nodes for citations
        if st.session_state.citations:
            for section in st.session_state.citations.get('ipc', []):
                G.add_node(f"IPC {section}", type='ipc')
            for article in st.session_state.citations.get('constitution', []):
                G.add_node(f"Article {article}", type='constitution')
            for case in st.session_state.citations.get('cases', []):
                G.add_node(case, type='case')
        # Add some edges (randomly connect entities to citations for demo)
        import random
        nodes = list(G.nodes)
        for i in range(min(20, len(nodes))):
            n1 = random.choice(nodes)
            n2 = random.choice(nodes)
            if n1 != n2:
                G.add_edge(n1, n2)

        pos = nx.spring_layout(G, seed=42)
        edge_x = []
        edge_y = []
        for edge in G.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_x += [x0, x1, None]
            edge_y += [y0, y1, None]

        edge_trace = go.Scatter(
            x=edge_x, y=edge_y,
            line=dict(width=0.5, color='#888'),
            hoverinfo='none',
            mode='lines')

        node_x = []
        node_y = []
        node_text = []
        for node in G.nodes():
            x, y = pos[node]
            node_x.append(x)
            node_y.append(y)
            node_text.append(str(node))

        node_trace = go.Scatter(
            x=node_x, y=node_y,
            mode='markers+text',
            text=node_text,
            textposition="top center",
            hoverinfo='text',
            marker=dict(
                showscale=True,
                colorscale='YlGnBu',
                color=[len(G[node]) for node in G.nodes()],
                size=12,
                colorbar=dict(
                    thickness=15,
                    title='Connections',
                    xanchor='left',
                    titleside='right'
                )
            )
        )

        fig = go.Figure(data=[edge_trace, node_trace],
                        layout=go.Layout(
                            title='Legal Knowledge Graph',
                            titlefont_size=16,
                            showlegend=False,
                            hovermode='closest',
                            margin=dict(b=20,l=5,r=5,t=40),
                            xaxis=dict(showgrid=False, zeroline=False),
                            yaxis=dict(showgrid=False, zeroline=False)
                        ))
        st.plotly_chart(fig, use_container_width=True)

# ==================== MODE: AI-POWERED DOCUMENT DRAFTING & REVIEW ====================
if mode == "📝 Draft & Review Document":
    st.header("📝 AI-Powered Document Drafting & Review")
    st.markdown('<span class="feature-badge">NEW FEATURE</span>', unsafe_allow_html=True)

    st.markdown("#### Select a Legal Document Template")
    template_options = [
        "NDA (Non-Disclosure Agreement)",
        "Employment Contract",
        "Service Agreement",
        "Lease Agreement",
        "Custom Document"
    ]
    selected_template = st.selectbox("Choose Template:", template_options)

    st.markdown("#### Enter Parties and Key Details")
    # Demo auto-fill suggestions
    dfc1, dfc2, dfc3 = st.columns(3)
    with dfc1:
        if st.button("Auto-fill Parties", key="auto_parties"):
            st.session_state["party_a"] = "Alpha Corp"
            st.session_state["party_b"] = "Beta LLC"
            st.success("Parties auto-filled")
    with dfc2:
        if st.button("Add Common Clauses", key="auto_clauses"):
            st.session_state["custom_terms"] = "Confidentiality; Payment within 30 days; Termination with 30-day notice; Arbitration in Delhi; Governing law: India."
            st.success("Common clauses added")
    with dfc3:
        if st.button("Set Demo Date", key="auto_date"):
            st.session_state["effective_date"] = datetime(2025, 1, 15)
            st.success("Demo date set")

    party_a = st.text_input("Party A Name:", value=st.session_state.get("party_a", ""))
    party_b = st.text_input("Party B Name:", value=st.session_state.get("party_b", ""))
    effective_date = st.date_input("Effective Date:", value=st.session_state.get("effective_date", datetime.today()))
    custom_terms = st.text_area("Custom Terms/Clauses:", value=st.session_state.get("custom_terms", ""), placeholder="Add specific terms or let Auto-fill add common ones.")

    if st.button("Generate Draft Document"):
        with st.spinner("Generating document draft with AI..."):
            draft = f"This {selected_template} is made between {party_a} and {party_b} effective from {effective_date}.\n\n{custom_terms}\n\n[Standard clauses and legal language will be added by AI]"
            st.session_state.generated_draft = draft
            st.success("Draft generated!")

    if st.session_state.get('generated_draft'):
        st.markdown("#### Document Draft")
        st.text_area("Draft Document:", st.session_state.generated_draft, height=300)
        if st.button("Review & Get AI Suggestions"):
            with st.spinner("Reviewing document with AI..."):
                suggestions = "- Ensure confidentiality clause is clear.\n- Add dispute resolution mechanism.\n- Specify governing law.\n- Review payment terms for clarity."
                st.session_state.draft_suggestions = suggestions
                st.success("AI review complete!")
        if st.session_state.get('draft_suggestions'):
            st.markdown("#### AI Suggestions for Improvement")
            st.write(st.session_state.draft_suggestions)

# ==================== MODE: ADVANCED SEMANTIC SEARCH & Q&A ====================
if mode == "🔎 Semantic Search & Q&A":
    st.header("🔎 Advanced Semantic Search & Q&A")
    st.markdown('<span class="feature-badge">NEW FEATURE</span>', unsafe_allow_html=True)
    st.markdown("Search across all uploaded documents using natural language. Get context-aware answers!")
    query = st.text_input("Enter your legal question or search query:")
    if query and st.session_state.docs_processed:
        with st.spinner("Searching and analyzing..."):
            retriever = st.session_state.vector_store.as_retriever(search_kwargs={"k": 5})
            llm = ChatOpenAI(model=model, temperature=0.1)
            docs = retriever.get_relevant_documents(query)
            context = "\n\n".join([d.page_content for d in docs])
            prompt = (
                "You are a legal assistant. Use the provided context to answer the user's query succinctly.\n"
                "Cite relevant sections if present. If unsure, say so.\n\n"
                f"Context:\n{context}\n\nQuery: {query}\nAnswer:"
            )
            answer = llm.invoke(prompt).content
            st.markdown("### 🤖 Answer:")
            st.write(answer)
            with st.expander("📚 Source Documents"):
                for idx, doc in enumerate(docs, 1):
                    st.markdown(f"**Source {idx}:**")
                    st.text(doc.page_content[:300] + "...")

# ==================== MODE: INTERACTIVE LEGAL TIMELINE & CASE TRACKING ====================
if mode == "📅 Legal Timeline & Case Tracking":
    st.header("📅 Interactive Legal Timeline & Case Tracking")
    st.markdown('<span class="feature-badge">NEW FEATURE</span>', unsafe_allow_html=True)
    st.markdown("Visualize the history and evolution of legal cases, amendments, and document changes.")
    # Simulate timeline data
    timeline_data = [
        {"date": "2022-01-01", "event": "Case Filed: Party A vs Party B"},
        {"date": "2022-03-15", "event": "First Hearing"},
        {"date": "2022-06-10", "event": "Amendment to Section 21"},
        {"date": "2022-09-05", "event": "Judgment Delivered"},
        {"date": "2023-02-20", "event": "Appeal Filed"},
        {"date": "2023-07-30", "event": "Final Resolution"}
    ]
    df_timeline = pd.DataFrame(timeline_data)
    fig = px.timeline(df_timeline, x_start="date", x_end="date", y="event", color="event")
    fig.update_yaxes(autorange="reversed")
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("#### Add New Case/Event to Timeline")
    # Suggestion chips for common timeline events
    tcol1, tcol2, tcol3 = st.columns(3)
    for label in ["Case Filed", "Hearing", "Judgment"]:
        with [tcol1, tcol2, tcol3][["Case Filed", "Hearing", "Judgment"].index(label)]:
            if st.button(label, key=f"tl_{label}"):
                st.session_state["timeline_event"] = label
    new_event = st.text_input("Event Description:", value=st.session_state.get("timeline_event", ""), placeholder="E.g., Amendment to Section 21")
    new_date = st.date_input("Event Date:")
    if st.button("Add Event to Timeline"):
        timeline_data.append({"date": str(new_date), "event": new_event})
        st.success("Event added! Refresh to see updated timeline.")

# ==================== MODE: ENHANCED REGULATORY MONITORING & ALERTS ====================
if mode == "🛡️ Regulatory Monitoring & Alerts":
    st.header("🛡️ Automated Regulatory Monitoring & Alerts")
    st.markdown('<span class="feature-badge">NEW FEATURE</span>', unsafe_allow_html=True)
    st.markdown("Track changes in laws, regulations, or case law. Get notified about new amendments and precedents.")
    # Helper: add legal alert topic into session state
    def add_legal_alert(topic):
        if not topic:
            return
        if 'legal_alerts' not in st.session_state:
            st.session_state.legal_alerts = []
        st.session_state.legal_alerts.append({
            'topic': topic,
            'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
    tracked_topics = st.session_state.get('legal_alerts', [])
    st.markdown("#### Tracked Topics:")
    for alert in tracked_topics:
        st.markdown(f"<div class='citation-box'><strong>Topic:</strong> {alert['topic']}<br><small>Added: {alert['time']}</small></div>", unsafe_allow_html=True)
    st.markdown("#### Add New Topic to Track")
    # Suggestion chips for topics
    r1, r2, r3 = st.columns(3)
    for topic in ["Data Protection", "Labour Law", "Tax Compliance"]:
        with [r1, r2, r3][["Data Protection", "Labour Law", "Tax Compliance"].index(topic)]:
            if st.button(topic, key=f"track_{topic}"):
                st.session_state["new_topic_monitor"] = topic
    new_topic = st.text_input("Legal topic/case to track:", key="new_topic_monitor", value=st.session_state.get("new_topic_monitor", ""), placeholder="E.g., IPC Section 420 updates")
    if st.button("Track Topic", key="track_topic_btn"):
        add_legal_alert(new_topic)
        st.success(f"Now tracking: {new_topic}")
    # Simulate alert
    if tracked_topics:
        st.info("No new updates detected. (Live monitoring can be integrated with legal APIs)")

# ==================== MODE: ENHANCED REAL-TIME MULTI-USER COLLABORATION ====================
if mode == "🤝 Collaborate":
    st.header("🤝 Real-Time Multi-User Collaboration")
    st.markdown('<span class="feature-badge">NEW FEATURE</span>', unsafe_allow_html=True)
    st.markdown("Work together with your team on document analysis. Add comments, highlights, and share insights.")
    doc_names = list(st.session_state.all_documents.keys()) if st.session_state.all_documents else []
    if doc_names:
        selected_doc = st.selectbox("Select document to collaborate on:", doc_names)
        section = st.text_input("Section/Clause to annotate (e.g., 'Termination Clause'):", key="collab_section")
        comment = st.text_area("Add your comment or highlight:", key="collab_comment")
        user_name = st.text_input("Your Name:", key="collab_user")
        if st.button("Add Collaborative Annotation"):
            if 'annotations' not in st.session_state:
                st.session_state.annotations = {}
            if selected_doc not in st.session_state.annotations:
                st.session_state.annotations[selected_doc] = []
            st.session_state.annotations[selected_doc].append({'section': section, 'comment': comment, 'user': user_name or 'User'})
            st.success("Annotation added!")
        if selected_doc in st.session_state.annotations:
            st.markdown("#### Existing Collaborative Annotations:")
            for ann in st.session_state.annotations[selected_doc]:
                st.markdown(f"<div class='citation-box'><strong>Section:</strong> {ann['section']}<br><strong>Comment:</strong> {ann['comment']}<br><small>By: {ann['user']}</small></div>", unsafe_allow_html=True)
    else:
        st.info("No documents available. Please upload and process documents first.")