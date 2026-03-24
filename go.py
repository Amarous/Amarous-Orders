import streamlit as st
from google import genai
from google.genai import types

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
    st.title("🤖 تطبيق Gemini الذكي")
    
    # ضع مفتاحك هنا
    GEMINI_API_KEY = "AIzaSyC8njO_svdjYqKO9eMH8DkklfqHfjyiYIQ"
    client = genai.Client(api_key=GEMINI_API_KEY)
    
    user_input = st.text_area("اسأل تطبيقك المخصص:")

    if st.button("إرسال"):
        if user_input:
            # قائمة بالموديلات المتاحة لنجربها بالترتيب
            models_to_try = [
                "gemini-2.0-flash-exp", 
                "gemini-1.5-flash", 
                "gemini-1.5-pro"
            ]
            
            success = False
            for model_name in models_to_try:
                try:
                    # محاولة الاتصال بالموديل
                    response = client.models.generate_content(
                        model=model_name,
                        contents=user_input,
                        config=types.GenerateContentConfig(
                            tools=[types.Tool(googleSearch=types.GoogleSearch())]
                        )
                    )
                    st.success(f"تم الرد بنجاح باستخدام موديل: {model_name}")
                    st.write(response.text)
                    success = True
                    break 
                except Exception:
                    continue 

            if not success:
                st.error("جوجل ترفض الوصول للموديلات حالياً. تأكد من تفعيل 'Pay-as-you-go' في Google Cloud أو استخدام API Key جديد تماماً.")
        else:
            st.warning("برجاء كتابة سؤال.")
