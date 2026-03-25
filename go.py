import streamlit as st
from google import genai
from google.genai import types

# --- 1. إعدادات الهوية (أماروس) ---
st.set_page_config(page_title="Amarous Orders - AI Studio", page_icon="🛍️", layout="wide")

if 'login' not in st.session_state: st.session_state.login = False

# --- 2. واجهة الدخول (bego / 992023) ---
if not st.session_state.login:
    st.markdown("<h1 style='text-align: center;'>🔐 دخول نظام أماروس المخصص</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        user = st.text_input("اسم المستخدم")
        pw = st.text_input("كلمة السر", type="password")
        if st.button("دخول"):
            if user == "bego" and pw == "992023":
                st.session_state.login = True
                st.rerun()
            else: st.error("بيانات خطأ")
else:
    # --- 3. تصميم تطبيقك من AI Studio ---
    st.image("https://i.ibb.co/6c2Y6y2/logo.jpg", width=120)
    st.title("🚀 Amarous Orders - AI System")
    
    # حط المفتاح الجديد هنا (اللي عملته في New Project)
    API_KEY = "AIzaSyBEB4CIiKhaa-bntCINzcfvhF51ovLmIGo"
    
    try:
        client = genai.Client(api_key=API_KEY)
        
        # --- واجهة الإدخال المخصصة (زي اللي في صورتك) ---
        user_input = st.text_area("أدخل تفاصيل الأوردر أو الملف (سيتم تطبيق التفكير والبحث):")

        if st.button("تنفيذ التصميم (Generate)"):
            if user_input:
                with st.spinner('جاري تشغيل محرك Gemini المخصص...'):
                    # إعدادات الـ Thinking والبحث اللي أنت عاملها
                    config = types.GenerateContentConfig(
                        thinking_config=types.ThinkingConfig(thinking_level="HIGH"),
                        tools=[types.Tool(googleSearch=types.GoogleSearch())],
                    )

                    # الموديل اللي بيشغل التصميم ده حالياً أونلاين
                    response = client.models.generate_content(
                        model="gemini-2.0-flash-thinking-exp-01-21",
                        contents=user_input,
                        config=config,
                    )
                    
                    st.success("النتيجة طبقاً لتصميمك:")
                    st.write(response.text)
            else: st.warning("اكتب شيئاً...")
                
    except Exception as e:
        st.error(f"خطأ في الربط: {e}")

    if st.sidebar.button("🚪 خروج"):
        st.session_state.login = False
        st.rerun()
