# test_models.py
import google.generativeai as genai

api_key = "AIzaSyApdw7DT1rJC4Nk79c1-fsJ-jR0QeqBmvo"  # Replace with your key
genai.configure(api_key=api_key)

try:
    print("📋 Available Models:")
    models = genai.list_models()
    
    for i, model in enumerate(models):
        print(f"{i+1}. {model.name}")
        print(f"   Description: {model.description}")
        print(f"   Supported methods: {model.supported_generation_methods}")
        print()
    
    # Try to use the most likely model
    preferred_models = [
        "gemini-1.5-pro-latest",
        "gemini-1.5-flash-latest",
        "gemini-pro"
    ]
    
    for model_name in preferred_models:
        try:
            print(f"\n🔧 Testing model: {model_name}")
            model = genai.GenerativeModel(model_name)
            response = model.generate_content("Hello, are you working?")
            print(f"✅ Success! Response: {response.text}")
            break
        except Exception as e:
            print(f"❌ Failed: {e}")
            
except Exception as e:
    print(f"❌ Error: {e}")
