import streamlit as st
from google import genai
from google.genai import types

# 1. إعدادات الدخول (عشان موقعك يبقى مؤمن)
if 'login' not in st.session_state:
    st.session_state.login = False

if not st.session_state.login:
    st.title("🔐 تسجيل الدخول لتطبيقي")
    user = st.text_input("اسم المستخدم")
    pw = st.text_input("كلمة السر", type="password")
    if st.button("دخول"):
        if user == "admin" and pw == "123":
            st.session_state.login = True
            st.rerun()
        else:
            st.error("بيانات خطأ")
else:
    # 2. واجهة تطبيقك اللي صممته في AI Studio
    st.title("🧠 تطبيق Gemini المخصص (Thinking & Search)")
    
    # ضع مفتاحك هنا (الذي يبدأ بـ AIza)
    GEMINI_API_KEY = "AIzaSyC8njO_svdjYqKO9eMH8DkklfqHfjyiYIQ"
    
    client = genai.Client(api_key=GEMINI_API_KEY)
    
    user_input = st.text_area("اسأل تطبيقك المخصص (سيفكر بعمق ويبحث في جوجل):")

    if st.button("إرسال"):
        if user_input:
            with st.spinner('جاري التفكير والبحث...'):
                try:
                    # نفس إعدادات تطبيقك من AI Studio بالظبط
                    config = types.GenerateContentConfig(
                        thinking_config=types.ThinkingConfig(thinking_level="HIGH"),
                        tools=[types.Tool(googleSearch=types.GoogleSearch())],
                    )

                    # الموديل اللي أنت اخترته (أو النسخة المستقرة منه)
                    response = client.models.generate_content(
                        model="gemini-2.0-flash-thinking-exp-01-21", 
                        contents=user_input,
                        config=config,
                    )
                    
                    st.success("الرد النهائي:")
                    st.write(response.text)
                    
                except Exception as e:
                    st.error(f"حدث خطأ: {e}")
        else:
            st.warning("برجاء كتابة سؤال.")
