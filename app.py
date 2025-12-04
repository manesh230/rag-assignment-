# app.py
import streamlit as st
import google.generativeai as genai
import os
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Medical AI Assistant",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.8rem;
        color: #1E3A8A;
        text-align: center;
        margin-bottom: 0.5rem;
        font-weight: 700;
    }
    .sub-header {
        text-align: center;
        color: #4B5563;
        margin-bottom: 2rem;
        font-size: 1.1rem;
    }
    .card {
        background: white;
        border-radius: 10px;
        padding: 1.5rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        margin: 1rem 0;
        border-left: 5px solid #3B82F6;
    }
    .warning-card {
        background: #FEF3C7;
        border-left: 5px solid #F59E0B;
    }
    .success-card {
        background: #D1FAE5;
        border-left: 5px solid #10B981;
    }
    .info-card {
        background: #E0F2FE;
        border-left: 5px solid #0EA5E9;
    }
    .step-number {
        display: inline-block;
        background: #3B82F6;
        color: white;
        width: 30px;
        height: 30px;
        border-radius: 50%;
        text-align: center;
        line-height: 30px;
        margin-right: 10px;
        font-weight: bold;
    }
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: 600;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 8px;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
    }
    .chat-user {
        background: #E3F2FD;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
    }
    .chat-assistant {
        background: #F3E5F5;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.markdown('<h1 class="main-header">🏥 Medical AI Assistant</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Get accurate medical information powered by Google Gemini AI</p>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.header("🔑 API Configuration")
    
    # Option 1: Use secrets (for deployed app)
    if 'GEMINI_API_KEY' in st.secrets:
        api_key = st.secrets['GEMINI_API_KEY']
        st.success("✅ Using API key from secrets")
    else:
        # Option 2: User input
        api_key = st.text_input(
            "Enter your Gemini API Key:",
            type="password",
            placeholder="AIzaSyBcDeFgHiJkLmNoPqRsTuVwXyZ...",
            help="Click 'Get Free API Key' button below to create one"
        )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Get API Key Button
    st.markdown('<div class="info-card">', unsafe_allow_html=True)
    st.header("🎯 Get Free API Key")
    if st.button("📝 Create Free API Key", use_container_width=True):
        st.session_state.show_key_guide = True
    
    if st.session_state.get('show_key_guide', False):
        st.markdown("""
        **Follow these steps:**
        
        1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
        2. Sign in with Google account
        3. Click "Get API Key" → "Create API Key"
        4. Copy the 39-character key
        5. Paste it above
        """)
        
        # Direct link
        st.markdown('[🚀 Click here to create API key](https://makersuite.google.com/app/apikey)')
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Test Connection
    if api_key:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        if st.button("🔗 Test API Connection", use_container_width=True):
            try:
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel('gemini-pro')
                response = model.generate_content("Test connection - Hello!")
                st.success("✅ Connection successful!")
                st.session_state.api_valid = True
            except Exception as e:
                st.error(f"❌ Connection failed: {str(e)}")
                st.session_state.api_valid = False
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Sample Questions
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.header("💡 Sample Questions")
    
    samples = [
        "What are common migraine symptoms?",
        "How to manage high blood pressure?",
        "Heart attack warning signs",
        "Diabetes prevention tips",
        "Stroke symptoms and first aid"
    ]
    
    for sample in samples:
        if st.button(f"🗨️ {sample}", key=f"btn_{sample[:10]}"):
            st.session_state.user_question = sample
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# Main Content Area
tab1, tab2, tab3 = st.tabs(["💬 Chat", "📚 Learn", "⚙️ Setup Guide"])

with tab1:
    if not api_key:
        st.markdown('<div class="warning-card">', unsafe_allow_html=True)
        st.header("⚠️ API Key Required")
        st.markdown("""
        To start using the Medical AI Assistant, you need a Gemini API key.
        
        **Don't worry - it's FREE and easy to get:**
        
        <div class="step-number">1</div> Click the **"Get Free API Key"** button in the sidebar  
        <div class="step-number">2</div> Follow the simple steps to create your key  
        <div class="step-number">3</div> Paste the key in the sidebar input  
        <div class="step-number">4</div> Click **"Test API Connection"**  
        <div class="step-number">5</div> Start asking medical questions!
        """, unsafe_allow_html=True)
        
        # Quick access button
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            if st.button("🚀 Take me to API Key creation", use_container_width=True):
                js = """
                <script>
                window.open('https://makersuite.google.com/app/apikey', '_blank');
                </script>
                """
                st.components.v1.html(js, height=0)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
    else:
        # Initialize chat
        if 'chat_history' not in st.session_state:
            st.session_state.chat_history = []
        
        if 'model' not in st.session_state:
            try:
                genai.configure(api_key=api_key)
                st.session_state.model = genai.GenerativeModel('gemini-pro')
                st.session_state.api_configured = True
            except Exception as e:
                st.error(f"Error configuring API: {str(e)}")
                st.session_state.api_configured = False
        
        # Display chat history
        for message in st.session_state.chat_history:
            if message['role'] == 'user':
                st.markdown(f"""
                <div class="chat-user">
                <strong>👤 You:</strong><br>
                {message['content']}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="chat-assistant">
                <strong>🤖 Assistant:</strong><br>
                {message['content']}
                </div>
                """, unsafe_allow_html=True)
        
        # Chat input
        default_question = st.session_state.get('user_question', '')
        question = st.chat_input(
            "Type your medical question here...",
            value=default_question
        )
        
        if question:
            # Add to history
            st.session_state.chat_history.append({'role': 'user', 'content': question})
            
            # Generate response
            with st.spinner("🤔 Analyzing your question..."):
                try:
                    # Medical context
                    medical_context = """You are Dr. Gemini, a knowledgeable medical AI assistant. 
                    Provide accurate, helpful medical information following these guidelines:
                    
                    1. Be evidence-based and factual
                    2. Explain in simple, clear language
                    3. Include symptoms, causes, prevention when relevant
                    4. Always mention when to seek professional help
                    5. Add important precautions
                    6. End with: "⚠️ Remember: This is general information. Always consult a healthcare professional for personal medical advice."
                    
                    Structure your response clearly with headings and bullet points when helpful."""
                    
                    response = st.session_state.model.generate_content(
                        f"{medical_context}\n\nQuestion: {question}"
                    )
                    
                    # Add to history
                    st.session_state.chat_history.append({
                        'role': 'assistant', 
                        'content': response.text
                    })
                    
                    # Rerun to display
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"Error: {str(e)}")
            
            # Clear sample question
            if 'user_question' in st.session_state:
                del st.session_state.user_question
        
        # Clear chat button
        if st.session_state.chat_history:
            if st.button("🗑️ Clear Chat", type="secondary"):
                st.session_state.chat_history = []
                st.rerun()

with tab2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.header("📚 Medical Topics")
    
    topics = {
        "Cardiology": ["Heart attack", "Hypertension", "Heart failure", "Arrhythmia"],
        "Neurology": ["Migraine", "Stroke", "Epilepsy", "Alzheimer's"],
        "Endocrinology": ["Diabetes", "Thyroid disorders", "Obesity"],
        "Gastroenterology": ["GERD", "IBD", "Liver disease"],
        "Respiratory": ["Asthma", "COPD", "Pneumonia"]
    }
    
    for category, conditions in topics.items():
        st.subheader(f"❤️ {category}")
        cols = st.columns(3)
        for i, condition in enumerate(conditions):
            with cols[i % 3]:
                if st.button(f"📖 {condition}", key=f"topic_{condition}"):
                    st.session_state.user_question = f"Tell me about {condition}"
                    st.switch_page("💬 Chat")
    st.markdown('</div>', unsafe_allow_html=True)

with tab3:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.header("📋 Complete Setup Guide")
    
    st.markdown("""
    ### Step-by-Step Setup
    
    <div class="step-number">1</div> **Create Google Cloud Account** (if you don't have one)
    - Go to [console.cloud.google.com](https://console.cloud.google.com)
    - Sign up with Google - it's free with $300 credits
    
    <div class="step-number">2</div> **Get Gemini API Key**
    - Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
    - Click "Get API Key" → "Create API Key"
    - Copy the key (39 characters starting with AIzaSy)
    
    <div class="step-number">3</div> **Enable Billing** (Free Tier Available)
    - Free quota: 60 requests per minute
    - First 60 requests per month are free
    - Requires credit card but won't charge unless you upgrade
    
    <div class="step-number">4</div> **Paste Key & Test**
    - Paste key in sidebar
    - Click "Test API Connection"
    - Start chatting!
    
    ### 💰 Pricing
    - **Free tier**: 60 requests/minute
    - **Gemini Pro**: ~$0.00025 per 1K characters
    - **Estimated cost**: Less than $1/month for personal use
    """, unsafe_allow_html=True)
    
    # FAQ
    with st.expander("❓ Frequently Asked Questions"):
        st.markdown("""
        **Q: Is it really free?**  
        A: Yes! First 60 requests per minute are free. Personal use costs pennies per month.
        
        **Q: Do I need a credit card?**  
        A: Yes for verification, but you won't be charged on free tier.
        
        **Q: Is my data safe?**  
        A: Google doesn't use your API data for training models.
        
        **Q: Can I use this commercially?**  
        A: Check Google's terms. For production, consider paid plans.
        """)
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
col1, col2, col3 = st.columns([1,2,1])
with col2:
    st.markdown("""
    <div style="text-align: center; color: #666;">
    <p>⚕️ For educational purposes only | ⚠️ Not for medical diagnosis</p>
    <p>Need help? The API key guide is in the "Setup Guide" tab</p>
    </div>
    """, unsafe_allow_html=True)
