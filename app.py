import streamlit as st
import google.generativeai as genai

API_KEY = st.secrets["GEMINI_KEY"]

st.set_page_config(page_title="Jadu The Study Buddy", page_icon="🔮", layout="wide")

genai.configure(api_key=API_KEY)

@st.cache_resource
def get_model():
    return genai.GenerativeModel('gemini-2.5-flash')

model = get_model()

if "study_kit" not in st.session_state:
    st.session_state.study_kit = ""

st.markdown("""
    <style>
    .stApp {
        background-image: url("https://images.unsplash.com/photo-1475274047050-1d0c0975c63e?ixlib=rb-4.0.3&auto=format&fit=crop&w=2944&q=80");
        background-attachment: fixed;
        background-size: cover;
    }

    [data-testid="stSidebar"] {
        background-color: rgba(20, 20, 40, 0.4) !important;
        backdrop-filter: blur(15px);
        -webkit-backdrop-filter: blur(15px);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .result-card {
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(108, 99, 255, 0.5);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        padding: 30px;
        border-radius: 20px;
        margin-top: 20px;
        color: #e0e0e0;
    }

    h1, h2, h3 { 
        color: #a29bfe !important; 
        text-shadow: 0px 0px 10px rgba(0,0,0,1); 
    }
    p, label, .stMarkdown, li, span {
        color: #ffffff !important;
        text-shadow: 0px 0px 5px rgba(0,0,0,0.8);
    }

    .stButton>button {
        width: 100%; 
        border-radius: 12px; 
        background: linear-gradient(135deg, #6c63ff 0%, #2a2a72 100%);
        color: white; 
        font-weight: bold; 
        border: 1px solid rgba(255,255,255,0.2); 
        box-shadow: 0 5px 15px rgba(0,0,0,0.3);
        transition: all 0.3s ease;
    }
    .stButton>button:hover { 
        transform: translateY(-3px);
        box-shadow: 0 0 20px rgba(108, 99, 255, 0.8);
    }

    .stTextArea textarea {
        background-color: rgba(0, 0, 0, 0.5) !important; 
        backdrop-filter: blur(5px);
        color: #fff !important;
        border: 1px solid #6c63ff;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center;'>🚀 JADU <span style='color:white;'>THE STUDY BUDDY</span></h1>", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### ⚙️ Study Settings")
    subject = st.selectbox("Subject", ["Physics", "Chemistry", "Mathematics", "Computer Science"])
    level = st.selectbox("Exam Target", ["School Boards", "JEE Mains", "JEE Advanced"])
    
    st.divider()
    
    if st.button("🗑️ Clear / Reset"):
        st.session_state.study_kit = "" 
        st.rerun()

user_input = st.text_area("📥 Paste NCERT/Chapter Text:", height=200, placeholder="Paste your chapter notes or question here...")

if st.button("✨ GENERATE STUDY KIT"):
    if user_input:
        with st.spinner('🧬 Jadu is analyzing your text...'):
            try:
                prompt = f"""
                Act as an expert Class 11 tutor for {subject}. 
                Create a high-quality revision kit for {level} level based on this text:
                
                "{user_input}"
                
                Please generate the response in TWO PARTS separated by the text "---SOLUTIONS---":
                
                PART 1 (Visible Study Material):
                1. **Formula Sheet**: Extract all mathematical formulas using LaTeX format (e.g., $$E=mc^2$$).
                2. **Concept Summary**: 3-4 bullet points explaining the core idea.
                3. **Exam Practice**: Create 3 High-Level MCQ questions relevant to {level}. 
                   (IMPORTANT: Show the Questions and Options ONLY. Do NOT show the correct answer here.)

                ---SOLUTIONS---

                PART 2 (Hidden Solutions):
                Provide the Correct Option (A/B/C/D) and a short explanation for each question above.
                """
                
                response = model.generate_content(prompt)
                st.session_state.study_kit = response.text
                
            except Exception as e:
                st.error(f"❌ Error: {e}")
    else:
        st.warning("⚠️ Please provide some text to analyze!")

if st.session_state.study_kit:
    st.markdown("---")
    st.markdown("### 📚 Your AI Study Kit")
    
    if "---SOLUTIONS---" in st.session_state.study_kit:
        parts = st.session_state.study_kit.split("---SOLUTIONS---")
        study_material = parts[0]
        solutions = parts[1]
    else:
        study_material = st.session_state.study_kit
        solutions = "No solutions were generated. Please try again."

    with st.container():
        st.markdown('<div class="result-card">', unsafe_allow_html=True)
        st.markdown(study_material)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    with st.expander("🕵️‍♂️ Click to Reveal Answers & Solutions"):
        st.markdown('<div class="result-card" style="border-color: #00ff00;">', unsafe_allow_html=True)
        st.markdown("### ✅ Correct Answers")
        st.markdown(solutions)
        st.markdown('</div>', unsafe_allow_html=True)