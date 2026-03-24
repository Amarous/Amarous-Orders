import streamlit as st
import google.generativeai as genai

# --- الإعدادات ---
if 'login' not in st.session_state:
    st.session_state.login = False

# --- شاشة الدخول ---
if not st.session_state.login:
    st.title("🔐 تسجيل الدخول")
    user = st.text_input("اسم المستخدم")
    pw = st.text_input("كلمة السر", type="password")
    if st.button("دخول"):
        if user == "admin" and pw == "123":
            st.session_state.login = True
            st.rerun()
        else:
            st.error("بيانات خطأ")
else:
    # --- واجهة التطبيق ---
    st.sidebar.button("تسجيل خروج", on_click=lambda: st.session_state.update({"login": False}))
    st.title("🤖 تطبيق Gemini الأصلي")

    # ضع مفتاحك هنا
    GEMINI_API_KEY = "AIzaSyC8njO_svdjYqKO9eMH8DkklfqHfjyiYIQ"
    genai.configure(api_key=GEMINI_API_KEY)

    user_question = st.text_area("تحدث مع تطبيقك:", placeholder="اكتب سؤالك هنا...")

    if st.button("إرسال إلى Gemini"):
        if user_question:
            try:
                # محاولة استخدام الموديل المتاح في حسابك تلقائياً
                model = genai.GenerativeModel('gemini-1.5-flash')
                response = model.generate_content(user_question)
                st.success("رد Gemini:")
                st.write(response.text)
            except Exception as e:
                st.error(f"حدث خطأ في الاتصال بجوجل: {e}")
                st.info("نصيحة: تأكد أن الـ API Key مفعل في Google AI Studio")
        else:
            st.warning("رجاءً اكتب سؤالك أولاً.")
