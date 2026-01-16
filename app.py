import streamlit as st
import pandas as pd
from pandasai import SmartDataframe
from pandasai_litellm.litellm import LiteLLM
import os


st.set_page_config(page_title="DataTalker AI", layout="wide", page_icon="🤖")

# UI CSS 

st.markdown("""
<style>
    /* Main Background*/
    .stApp {
        background: linear-gradient(to bottom right, #0E1117, #161b22);
    }

    h1 {
        background: -webkit-linear-gradient(45deg, #00FF99, #00CCFF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-family: 'Courier New', monospace;
        text-shadow: 0 0 10px rgba(0, 255, 153, 0.3);
    }
    
    [data-testid="stSidebar"] {
        background-color: rgba(20, 20, 30, 0.8);
        border-right: 1px solid rgba(0, 255, 153, 0.2);
        backdrop-filter: blur(10px);
    }
    
    .stButton>button {
        background: linear-gradient(45deg, #00FF99, #00CCFF);
        color: black;
        border: none;
        border-radius: 20px;
        font-weight: bold;
        transition: all 0.3s ease;
        box-shadow: 0 0 15px rgba(0, 255, 153, 0.4);
    }
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 0 25px rgba(0, 255, 153, 0.7);
    }
    
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        background-color: #1E1E1E;
        color: #00FF99;
        border: 1px solid #333;
        border-radius: 10px;
    }
    .stTextInput>div>div>input:focus, .stTextArea>div>div>textarea:focus {
        border-color: #00FF99;
        box-shadow: 0 0 10px rgba(0, 255, 153, 0.3);
    }
    

    [data-testid="stDataFrame"] {
        border: 1px solid #333;
        border-radius: 10px;
        overflow: hidden;
    }
</style>
""", unsafe_allow_html=True)


st.title("🤖 DataChat AI")
st.caption("🚀 Powered by Groq & Llama 3.3")

# sidebar 

with st.sidebar:
    st.header("⚙️ Control Panel")
    
    api_key = ""
    try:
        if "GROQ_API_KEY" in st.secrets:
            api_key = st.secrets["GROQ_API_KEY"]
            st.success("✅ System Online: API Connected")
    except FileNotFoundError:
        pass

    if not api_key:
        api_key = st.text_input("🔑 Enter API Key", type="password")
    
    st.markdown("---")
    uploaded_file = st.file_uploader("📂 Upload Dataset (CSV)", type=['csv'])

# main logic 

if uploaded_file is not None and api_key:
    
    try:
        df = pd.read_csv(uploaded_file)
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.info("Data Preview")
            st.dataframe(df.head(5), use_container_width=True)
        
        with col2:
            st.info("AI Analysis Hub")
            
            llm = LiteLLM(api_key=api_key, model="groq/llama-3.3-70b-versatile")
            sdf = SmartDataframe(df, config={"llm": llm})
            
            # Chat Interface
            query = st.text_area("💬 Query Database:", placeholder="e.g., 'Visualize the relationship between Reach and Engagement'", height=100)
            
            if st.button("Initialize Analysis"):
                if query:
                    with st.spinner("🔄 Processing Neural Request..."):
                        # Cleanup old charts
                        chart_dir = "exports/charts"
                        if os.path.exists(chart_dir):
                            for f in os.listdir(chart_dir):
                                try: os.remove(os.path.join(chart_dir, f))
                                except: pass

                        try:
                            response = sdf.chat(query)
                            
                            st.markdown("### ⚡ Insight Generated:")
                            st.write(response)
                            
                            # Display Chart
                            if os.path.exists(chart_dir) and os.listdir(chart_dir):
                                files = [os.path.join(chart_dir, f) for f in os.listdir(chart_dir)]
                                latest_file = max(files, key=os.path.getctime)
                                st.image(latest_file, caption="Generated Visualization", use_column_width=True)
                                
                        except Exception as e:
                            st.error(f"❌ System Error: {e}")
                else:
                    st.warning("⚠️ Input Required: Please enter a query.")
                
    except Exception as e:
        st.error(f"❌ Read Error: {e}")

elif not api_key:
    st.warning("👈 Awaiting Security Key in Sidebar...")
elif not uploaded_file:
    st.info("👈 Awaiting Dataset in Sidebar...")