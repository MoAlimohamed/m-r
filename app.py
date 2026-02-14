import streamlit as st
import base64
import time
from datetime import datetime

# --- 1. Page Configuration ---
st.set_page_config(
    page_title="Rahma ❤️",
    page_icon="❤️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. State Management ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'memories' not in st.session_state:
    st.session_state.memories = []  # List to store memory dicts
if 'login_error' not in st.session_state:
    st.session_state.login_error = False

# --- 3. Helper Functions ---
def get_image_base64(uploaded_file):
    """Convert uploaded file to base64 for HTML embedding"""
    try:
        bytes_data = uploaded_file.getvalue()
        b64 = base64.b64encode(bytes_data).decode()
        return f"data:{uploaded_file.type};base64,{b64}"
    except Exception:
        return None

def set_page(page_name):
    st.session_state.page = page_name
    st.rerun()

# --- 4. Custom CSS (The Design Engine) ---
def inject_custom_css():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Amiri:ital,wght@0,400;0,700;1,400;1,700&display=swap');
        
        /* Global App Styling */
        .stApp {
            background: linear-gradient(135deg, #fff0f5 0%, #ffffff 50%, #fff0f5 100%);
            font-family: 'Amiri', serif;
        }
        
        /* Remove Default Streamlit Elements but KEEP Header for Sidebar Toggle */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        /* header {visibility: hidden;}  <-- Removed to allow sidebar toggle */
        
        /* Force RTL and Font */
        * {
            font-family: 'Amiri', serif !important;
        }
        
        /* Custom Button Styling (Pink Gradient) */
        div.stButton > button {
            background: linear-gradient(to right, #f43f5e, #db2777);
            color: white !important;
            border: none;
            border-radius: 20px;
            padding: 15px 30px;
            font-size: 20px;
            font-weight: bold;
            box-shadow: 0 10px 15px -3px rgba(244, 63, 94, 0.3);
            transition: all 0.3s ease;
            width: 100%;
        }
        div.stButton > button:hover {
            transform: translateY(-3px) scale(1.02);
            box-shadow: 0 20px 25px -5px rgba(244, 63, 94, 0.4);
            color: white !important;
        }
        
        /* Input Fields */
        div[data-baseweb="input"] > div {
            background-color: rgba(255, 255, 255, 0.8);
            border: 2px solid #ffe4e6;
            border-radius: 16px;
            color: #881337;
        }
        
        /* Text Area */
        div[data-baseweb="textarea"] > div {
            background-color: rgba(255, 255, 255, 0.8);
            border: 2px solid #ffe4e6;
            border-radius: 16px;
        }

        /* Sidebar Styling */
        section[data-testid="stSidebar"] {
            background-color: rgba(255, 255, 255, 0.7);
            backdrop-filter: blur(20px);
            border-right: 1px solid #ffe4e6;
        }
        
        /* Card Styling for Memories */
        .memory-card {
            background: white;
            border-radius: 24px;
            overflow: hidden;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            border: 1px solid #ffe4e6;
            margin-bottom: 20px;
            transition: transform 0.3s ease;
            direction: rtl;
        }
        .memory-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 20px 25px -5px rgba(244, 63, 94, 0.2);
        }
        .memory-img {
            width: 100%;
            height: 250px;
            object-fit: cover;
        }
        .memory-content {
            padding: 20px;
            text-align: right;
        }
        .memory-caption {
            color: #881337;
            font-size: 18px;
            line-height: 1.6;
            font-weight: 500;
        }
        .memory-date {
            color: #fb7185;
            font-size: 14px;
            margin-top: 10px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        /* Animations */
        @keyframes float {
            0% { transform: translateY(0px) rotate(0deg); opacity: 0; }
            50% { opacity: 0.6; }
            100% { transform: translateY(-100vh) rotate(360deg); opacity: 0; }
        }
        @keyframes pulse-soft {
            0% { transform: scale(1); }
            50% { transform: scale(1.05); }
            100% { transform: scale(1); }
        }
        .heart-bg {
            position: fixed;
            top: 0; left: 0; width: 100%; height: 100%;
            pointer-events: none;
            z-index: 0;
        }
        .heart-particle {
            position: absolute;
            bottom: -50px;
            font-size: 24px;
            color: rgba(244, 63, 94, 0.3);
            animation: float 15s infinite ease-in;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Inject Flying Hearts
    hearts_html = ""
    for i in range(20):
        left = i * 5
        delay = i % 7
        duration = 10 + (i % 8)
        hearts_html += f'<div class="heart-particle" style="left: {left}%; animation-duration: {duration}s; animation-delay: {delay}s;">❤️</div>'
    st.markdown(f'<div class="heart-bg">{hearts_html}</div>', unsafe_allow_html=True)

# --- 5. Application Pages ---

def login_screen():
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Card Container
        st.markdown("""
<div style="background: rgba(255, 255, 255, 0.9); backdrop-filter: blur(10px); padding: 40px; border-radius: 40px; border: 1px solid #ffe4e6; box-shadow: 0 25px 50px -12px rgba(244, 63, 94, 0.25); text-align: center;">
    <div style="width: 100px; height: 100px; background: linear-gradient(135deg, #f43f5e, #db2777); border-radius: 50%; margin: 0 auto 20px; display: flex; align-items: center; justify-content: center; box-shadow: 0 10px 20px rgba(244, 63, 94, 0.4); animation: pulse-soft 2s infinite;">
        <span style="font-size: 50px; color: white;">❤️</span>
    </div>
    <h1 style="font-size: 60px; background: linear-gradient(to right, #be123c, #db2777); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin: 0;">رحمه</h1>
    <p style="color: #fb7185; font-size: 20px; margin-top: 5px;">أهلاً بك في عالمي</p>
</div>
""", unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        with st.form("login_form"):
            st.markdown('<p style="text-align: right; color: #9f1239; font-size: 20px; font-weight: bold; margin-bottom: 5px;">👀 عامله ايه ياروو بحبك</p>', unsafe_allow_html=True)
            password = st.text_input("Password", type="password", label_visibility="collapsed")
            
            submitted = st.form_submit_button("👀 اتكي براحه هنا")
            
            if submitted:
                if password == "15/8":
                    st.session_state.logged_in = True
                    st.session_state.login_error = False
                    st.rerun()
                else:
                    st.session_state.login_error = True

        if st.session_state.login_error:
            st.error("الرمز خطأ يا قلبي 🥺")

def sidebar():
    with st.sidebar:
        st.markdown("""
<div style="text-align: center; padding: 20px;">
    <div style="font-size: 40px; color: #e11d48; margin-bottom: 10px;">❤️</div>
    <h2 style="color: #881337; margin: 0;">رحمه</h2>
    <p style="color: #fda4af; font-size: 14px;">صُنع بحب</p>
</div>
""", unsafe_allow_html=True)
        
        if st.button("🏠 الرئيسية"):
            set_page("home")
            
        st.markdown("<div style='height: 10px'></div>", unsafe_allow_html=True)
        
        if st.button("📸 الذكريات"):
            set_page("memories")

        st.markdown("---")
        st.markdown('<h3 style="text-align: right; color: #be123c;">🎵 موسيقى</h3>', unsafe_allow_html=True)
        
        # Audio Player
        uploaded_audio = st.file_uploader("Upload Song", type=['mp3'], label_visibility="collapsed")
        
        # Default song if none uploaded
        audio_url = "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3"
        
        if uploaded_audio:
            st.audio(uploaded_audio, format='audio/mp3')
        else:
            st.audio(audio_url, format='audio/mp3')

def home_page():
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Define columns before using them
    c1, c2, c3 = st.columns([1, 8, 1])
    
    with c2:
        # Note: Removing indentation inside string to ensure HTML renders correctly in Streamlit
        st.markdown("""
<div style="text-align: center; position: relative; z-index: 10; padding-bottom: 50px;">
    <div style="position: relative; display: inline-block;">
        <div style="position: absolute; inset: -20px; background: linear-gradient(to right, #fbcfe8, #fecdd3); border-radius: 50%; filter: blur(30px); opacity: 0.7; animation: pulse 3s infinite;"></div>
        <div style="position: relative; width: 220px; height: 220px; background: white; border-radius: 50%; display: flex; align-items: center; justify-content: center; border: 8px solid #fff1f2; box-shadow: 0 20px 50px rgba(244, 63, 94, 0.2); margin: 0 auto;">
            <span style="font-size: 100px; color: #e11d48;">❤️</span>
        </div>
    </div>
    <h1 style="font-size: 90px; margin-top: 40px; margin-bottom: 0; background: linear-gradient(to right, #be123c, #fb7185); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: bold; text-shadow: 0 4px 10px rgba(255, 255, 255, 0.5);">
        رحمه
    </h1>
    <p style="font-size: 32px; color: #9f1239; margin-top: 10px; font-weight: 500;">
        كل عام وأنت الحب ❤️
    </p>
</div>
""", unsafe_allow_html=True)
        
        # Button centering using nested columns
        col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
        with col_btn2:
            if st.button("📸 الذهاب إلى ألبوم الذكريات"):
                set_page("memories")

def memories_page():
    st.markdown("""
<div style="text-align: right; margin-bottom: 30px;">
    <h1 style="color: #881337; font-size: 45px; display: inline-block;">ألبوم الذكريات 📸</h1>
    <p style="color: #fb7185; font-size: 20px;">لنصنع ذكريات لا تُنسى ❤️</p>
</div>
""", unsafe_allow_html=True)

    col_input, col_gallery = st.columns([1, 1.5], gap="large")

    # --- Left Column: Upload ---
    with col_input:
        st.markdown("""
<div style="background: white; padding: 30px; border-radius: 30px; border: 1px solid #ffe4e6; box-shadow: 0 10px 30px rgba(0,0,0,0.05); text-align: right;">
    <h3 style="color: #be123c; margin-bottom: 20px;">إضافة صورة جديدة ✨</h3>
""", unsafe_allow_html=True)
        
        uploaded_file = st.file_uploader("", type=['jpg', 'jpeg', 'png'], label_visibility="collapsed")
        
        if uploaded_file:
            st.image(uploaded_file, use_container_width=True)
        else:
            st.markdown("""
<div style="border: 2px dashed #fda4af; border-radius: 20px; padding: 40px; text-align: center; color: #fda4af; background: #fff1f2;">
    اختاري صورة من جهازك
</div>
""", unsafe_allow_html=True)
            
        st.markdown("<div style='height: 15px'></div>", unsafe_allow_html=True)
        caption = st.text_area("", placeholder="اكتبي ذكرى جميلة هنا...", height=100)
        st.markdown("<div style='height: 15px'></div>", unsafe_allow_html=True)
        
        if st.button("حفظ الذكرى"):
            if uploaded_file and caption:
                img_b64 = get_image_base64(uploaded_file)
                if img_b64:
                    new_memory = {
                        "id": str(int(time.time())),
                        "image": img_b64,
                        "caption": caption,
                        "date": datetime.now().strftime("%Y/%m/%d")
                    }
                    st.session_state.memories.insert(0, new_memory)
                    st.success("تم الحفظ!")
                    time.sleep(0.5)
                    st.rerun()
            else:
                st.warning("الصورة والكلام مهمين يا روحي!")
        
        st.markdown("</div>", unsafe_allow_html=True)

    # --- Right Column: Gallery ---
    with col_gallery:
        st.markdown(f"<h3 style='color: #9f1239; text-align: right; margin-bottom: 20px;'>معرض صورنا ({len(st.session_state.memories)})</h3>", unsafe_allow_html=True)
        
        if not st.session_state.memories:
            st.markdown("""
<div style="text-align: center; padding: 60px; color: #fca5a5; opacity: 0.7;">
    <div style="font-size: 60px; margin-bottom: 10px;">🖼️</div>
    <h3>لسه مفيش صور..</h3>
    <p>ضيفي أول صورة لينا سوا</p>
</div>
""", unsafe_allow_html=True)
        
        for i, memory in enumerate(st.session_state.memories):
            st.markdown(f"""
<div class="memory-card">
    <img src="{memory['image']}" class="memory-img" />
    <div class="memory-content">
        <div class="memory-caption">{memory['caption']}</div>
        <div class="memory-date">
            <span>{memory['date']}</span>
            <span>❤️</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)
            
            # Delete Button (Streamlit Logic)
            c_del1, c_del2 = st.columns([1, 4])
            with c_del1:
                if st.button("حذف", key=f"del_{memory['id']}"):
                    st.session_state.memories.pop(i)
                    st.rerun()

# --- 6. Main Execution ---

inject_custom_css()

if not st.session_state.logged_in:
    login_screen()
else:
    sidebar()
    if st.session_state.page == "home":
        home_page()
    elif st.session_state.page == "memories":
        memories_page()
