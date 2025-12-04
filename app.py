# app.py
import streamlit as st
import os
import json
import sys
import tempfile
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="Medical RAG Assistant",
    page_icon="🏥",
    layout="wide"
)

# Add custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E3A8A;
        text-align: center;
        margin-bottom: 2rem;
    }
    .stButton button {
        background-color: #3B82F6;
        color: white;
        font-weight: bold;
    }
    .warning-box {
        background-color: #FEF3C7;
        border-left: 5px solid #F59E0B;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 0.25rem;
    }
</style>
""", unsafe_allow_html=True)

# Display title
st.markdown('<h1 class="main-header">🏥 Medical RAG Assistant</h1>', unsafe_allow_html=True)

# Disclaimer
st.markdown("""
<div class="warning-box">
⚠️ <strong>Disclaimer:</strong> This is an educational tool. Not for medical diagnosis or treatment.
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.title("⚙️ Setup")
    
    api_key = st.text_input("Enter Gemini API Key:", type="password")
    
    st.markdown("---")
    st.subheader("Instructions")
    st.info("""
    1. Enter your Gemini API key
    2. Click 'Initialize System'
    3. Ask medical questions
    """)
    
    st.markdown("---")
    st.subheader("Support")
    st.write("For issues, check the terminal logs.")

# Main content area
st.subheader("🔍 Ask Medical Questions")

# Initialize session state
if 'initialized' not in st.session_state:
    st.session_state.initialized = False
if 'error' not in st.session_state:
    st.session_state.error = None

# Initialize button
if not st.session_state.initialized:
    if st.button("🚀 Initialize System", use_container_width=True):
        with st.spinner("Setting up system..."):
            try:
                # Try to import dependencies
                import chromadb
                from chromadb.utils import embedding_functions
                import google.generativeai as genai
                
                st.success("✅ Libraries imported successfully!")
                
                # Create a mock RAG system for demo
                class DemoRAGSystem:
                    def __init__(self):
                        self.demo_data = {
                            "migraine": "Migraine symptoms include headache, nausea, sensitivity to light/sound. Risk factors: family history, hormonal changes.",
                            "chest pain": "Chest pain evaluation includes ECG, troponin tests, chest X-ray. Common causes: angina, GERD, anxiety.",
                            "hypertension": "Hypertension management: lifestyle changes, ACE inhibitors, beta-blockers. Monitor BP regularly.",
                            "diabetes": "Diabetes symptoms: increased thirst, frequent urination, fatigue. Management: diet, exercise, medication.",
                            "asthma": "Asthma: wheezing, shortness of breath, chest tightness. Triggers: allergens, exercise, cold air."
                        }
                    
                    def query(self, question, top_k=3):
                        results = []
                        for key, value in self.demo_data.items():
                            if any(word in question.lower() for word in key.split()):
                                results.append(value)
                        return results if results else ["No specific information found. Please consult a healthcare professional."]
                
                # Initialize AI
                if api_key:
                    genai.configure(api_key=api_key)
                    model = genai.GenerativeModel('gemini-pro')
                    st.session_state.model = model
                    st.session_state.rag = DemoRAGSystem()
                    st.session_state.initialized = True
                    st.success("✅ System initialized successfully!")
                    st.rerun()
                else:
                    st.error("Please enter your Gemini API key")
                    
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                st.session_state.error = str(e)
    
    if st.session_state.error:
        with st.expander("Error Details"):
            st.code(st.session_state.error)

# If initialized, show chat interface
if st.session_state.initialized:
    # Chat input
    question = st.text_area("Enter your medical question:", height=100)
    
    col1, col2 = st.columns([1, 5])
    with col1:
        ask_btn = st.button("Ask", type="primary")
    
    if ask_btn and question:
        with st.spinner("Thinking..."):
            try:
                # Get context from RAG
                context_chunks = st.session_state.rag.query(question)
                context = "\n".join(context_chunks)
                
                # Generate response
                prompt = f"""You are a medical assistant. Use this context to answer the question:
                
Context: {context}

Question: {question}

Provide a helpful, accurate answer. Include:
1. Key information
2. When to seek medical help
3. Important precautions

Always remind users to consult healthcare professionals."""

                response = st.session_state.model.generate_content(prompt)
                
                # Display response
                st.markdown("### 🤖 AI Response")
                st.markdown(response.text)
                
                # Show context used
                with st.expander("📚 Context Used"):
                    for i, chunk in enumerate(context_chunks):
                        st.markdown(f"**Source {i+1}:**")
                        st.info(chunk)
                        
            except Exception as e:
                st.error(f"Error: {str(e)}")
    
    # Sample questions
    st.markdown("---")
    st.subheader("💡 Sample Questions")
    
    samples = [
        "What are migraine symptoms?",
        "How is chest pain evaluated?",
        "What is hypertension management?",
        "Tell me about diabetes symptoms",
        "What are asthma triggers?"
    ]
    
    cols = st.columns(3)
    for i, sample in enumerate(samples):
        with cols[i % 3]:
            if st.button(sample, use_container_width=True):
                st.session_state.sample_question = sample
                st.rerun()
    
    if 'sample_question' in st.session_state:
        st.text_input("Selected question:", value=st.session_state.sample_question, disabled=True)

# Instructions for Streamlit Cloud
with st.expander("ℹ️ Deployment Instructions"):
    st.markdown("""
    ### For Streamlit Cloud:
    
    1. **Create requirements.txt:**
    ```txt
    streamlit
    chromadb
    sentence-transformers
    google-generativeai
    ```
    
    2. **Add your files to GitHub:**
    - app.py
    - requirements.txt
    
    3. **Deploy on Streamlit Cloud:**
    - Go to [share.streamlit.io](https://share.streamlit.io)
    - Connect your GitHub repository
    - Main file path: `app.py`
    
    4. **Add secrets:**
    - Go to app settings → Secrets
    - Add your Gemini API key:
    ```toml
    GEMINI_API_KEY = "your-api-key-here"
    ```
    """)

# Footer
st.markdown("---")
st.markdown("Built with ❤️ using Streamlit, Gemini AI, and ChromaDB")
