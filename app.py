import streamlit as st
import requests
import json

st.set_page_config(page_title="Paisa-Mind", page_icon="💰", layout="centered")
st.title("Paisa-Mind: AI Personal Finance & Tax Assistant 💰")

# Direct Gemini Key
GEMINI_API_KEY = "AIzaSyDkRDEIYVY9YywmypqFEkzUkFgs7jzvpHQ"

# Session state for document knowledge
if "tax_knowledge" not in st.session_state:
    st.session_state["tax_knowledge"] = ""

# --- SIDEBAR: DIRECT DATA INGESTION ---
with st.sidebar:
    st.header("📁 Knowledge Base Setup")
    uploaded_file = st.file_uploader("Upload Tax Data (.txt)", type=["txt"])
    
    if uploaded_file is not None:
        st.session_state["tax_knowledge"] = uploaded_file.getvalue().decode("utf-8")
        st.success("Data successfully loaded into memory!")

# --- MAIN SCREEN: CHAT INTERFACE ---
st.write("Ask any question regarding your taxes, zakat, or savings plans based on your data.")

user_query = st.text_input("💬 Apna Sawal Likhein (e.g., How much tax on 100k income?):")

if user_query:
    with st.spinner("AI is thinking and analyzing regulations..."):
        context = st.session_state["tax_knowledge"] if st.session_state["tax_knowledge"] else "No official document uploaded yet."
        
        prompt = f"""
        You are Paisa-Mind, an expert AI Personal Finance & Tax Assistant for Pakistan.
        Your task is to answer the user's question accurately based ONLY on the provided context.
        
        Rules:
        1. If the answer is found in the context, provide a detailed and clear response.
        2. If the user asks a relevant tax question but it's not in the context, guide them generally using current Pakistani tax rules.
        3. Keep the tone helpful, professional, and technical.
        
        Context:
        {context}
        
        User Question: {user_query}
        
        Expert Answer:
        """
        
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"
        
        headers = {'Content-Type': 'application/json'}
        payload = {
            "contents": [{
                "parts": [{"text": prompt}]
            }]
        }
        
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        
        if response.status_code == 200:
            response_json = response.json()
            answer = response_json['candidates'][0]['content']['parts'][0]['text']
            st.write("### 🤖 Paisa-Mind Response:")
            st.info(answer)
        else:
            st.error(f"API Error ({response.status_code})")