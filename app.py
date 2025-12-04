# app.py
import streamlit as st
import google.generativeai as genai
import os

# Page configuration
st.set_page_config(
    page_title="Medical AI Assistant",
    page_icon="🏥",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E3A8A;
        text-align: center;
        margin-bottom: 1rem;
    }
    .info-box {
        background-color: #E0F2FE;
        border-left: 5px solid #0EA5E9;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 0.5rem;
    }
    .success-box {
        background-color: #D1FAE5;
        border-left: 5px solid #10B981;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 0.5rem;
    }
    .warning-box {
        background-color: #FEF3C7;
        border-left: 5px solid #F59E0B;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.markdown('<h1 class="main-header">🏥 Medical AI Assistant</h1>', unsafe_allow_html=True)

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'model' not in st.session_state:
    st.session_state.model = None

# Sidebar
with st.sidebar:
    st.title("⚙️ Configuration")
    
    # API Key input
    if 'GEMINI_API_KEY' in st.secrets:
        api_key = st.secrets['GEMINI_API_KEY']
        st.success("✅ Using API key from secrets")
    else:
        api_key = st.text_input(
            "Enter Gemini API Key:",
            type="password",
            help="Get it from https://makersuite.google.com/app/apikey"
        )
    
    # Model selection
    st.subheader("Model Selection")
    model_option = st.selectbox(
        "Choose model:",
        [
            "gemini-1.5-pro-latest",
            "gemini-1.5-flash-latest",
            "gemini-pro",
            "models/gemini-1.5-pro-latest",
            "models/gemini-1.5-flash-latest"
        ],
        index=0
    )
    
    st.markdown("---")
    
    # Test connection button
    if api_key and model_option:
        if st.button("Test Connection", use_container_width=True):
            try:
                genai.configure(api_key=api_key)
                
                # Try different model names
                models_to_try = [
                    model_option,
                    "gemini-1.5-pro-latest",
                    "gemini-1.5-flash-latest",
                    "gemini-pro",
                    "models/gemini-1.5-pro-latest"
                ]
                
                success = False
                for model_name in models_to_try:
                    try:
                        model = genai.GenerativeModel(model_name)
                        response = model.generate_content("Hello")
                        st.success(f"✅ Connected! Using model: {model_name}")
                        st.session_state.available_model = model_name
                        success = True
                        break
                    except:
                        continue
                
                if not success:
                    st.error("❌ Could not connect with any model. Check your API key.")
                    
            except Exception as e:
                st.error(f"❌ Connection error: {str(e)}")

# Main content
if not api_key:
    st.markdown("""
    <div class="info-box">
    <h3>🔑 Get Started</h3>
    <p>To use this Medical AI Assistant, you need a Gemini API key:</p>
    <ol>
    <li>Go to <a href="https://makersuite.google.com/app/apikey" target="_blank">Google AI Studio</a></li>
    <li>Sign in with Google</li>
    <li>Click "Get API Key" → "Create API Key"</li>
    <li>Copy the key and paste it in the sidebar</li>
    </ol>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.subheader("💡 Sample Questions")
    samples = [
        "What are the symptoms of migraine?",
        "How to manage high blood pressure?",
        "What are heart attack warning signs?",
        "Tell me about diabetes prevention"
    ]
    
    cols = st.columns(2)
    for i, sample in enumerate(samples):
        with cols[i % 2]:
            st.info(sample)
else:
    # Initialize Gemini
    try:
        genai.configure(api_key=api_key)
        
        # Try to get available models
        try:
            models = genai.list_models()
            available_models = [model.name for model in models]
            
            # Find the best model
            preferred_models = [
                "models/gemini-1.5-pro-latest",
                "gemini-1.5-pro-latest",
                "models/gemini-1.5-flash-latest",
                "gemini-1.5-flash-latest",
                "models/gemini-pro",
                "gemini-pro"
            ]
            
            selected_model = None
            for model in preferred_models:
                if model in str(available_models):
                    selected_model = model
                    break
            
            if selected_model:
                st.session_state.model = genai.GenerativeModel(selected_model)
                st.markdown(f"""
                <div class="success-box">
                ✅ Connected to: <strong>{selected_model}</strong>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.error("No supported models found. Available models:")
                for model in available_models:
                    st.write(f"- {model}")
                
        except Exception as e:
            st.error(f"Error listing models: {str(e)}")
            # Fallback to a common model
            try:
                st.session_state.model = genai.GenerativeModel("gemini-1.5-flash-latest")
                st.success("✅ Connected using fallback model")
            except:
                st.error("Could not connect to any model")
        
    except Exception as e:
        st.error(f"Configuration error: {str(e)}")

# Chat interface
if api_key and st.session_state.model:
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask a medical question..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    # Medical context prompt
                    medical_prompt = f"""You are a medical AI assistant. Provide accurate, helpful medical information.
                    
                    Question: {prompt}
                    
                    Guidelines:
                    1. Provide evidence-based information
                    2. Mention when to seek medical help
                    3. Include important precautions
                    4. End with: "⚠️ Disclaimer: This is for educational purposes. Consult a healthcare professional for medical advice."
                    
                    Response:"""
                    
                    response = st.session_state.model.generate_content(medical_prompt)
                    st.markdown(response.text)
                    st.session_state.messages.append({"role": "assistant", "content": response.text})
                    
                except Exception as e:
                    error_msg = f"Error: {str(e)}"
                    st.error(error_msg)
    
    # Clear chat button
    if st.session_state.messages:
        if st.button("Clear Chat"):
            st.session_state.messages = []
            st.rerun()

# Alternative simplified version (if above doesn't work)
st.markdown("---")
with st.expander("🔄 Alternative: Use this simple test"):
    if st.button("Test Simple Connection"):
        try:
            genai.configure(api_key=api_key)
            
            # List available models
            st.write("📋 Available Models:")
            models = genai.list_models()
            for model in models:
                st.write(f"- {model.name}")
            
            # Try to use the first available model
            if models:
                model_name = models[0].name
                model = genai.GenerativeModel(model_name)
                response = model.generate_content("Hello, test")
                st.success(f"✅ Success with model: {model_name}")
                st.write(f"Response: {response.text}")
                
        except Exception as e:
            st.error(f"Error: {str(e)}")

# Footer
st.markdown("---")
st.caption("⚠️ For educational purposes only. Not for medical diagnosis.")
