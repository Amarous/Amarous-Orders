import streamlit as st
import google.generativeai as genai

# إعداد حالة تسجيل الدخول
if 'login' not in st.session_state:
    st.session_state.login = False

# واجهة تسجيل الدخول
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
    # واجهة التطبيق بعد الدخول
    st.sidebar.button("تسجيل خروج", on_click=lambda: st.session_state.update({"login": False}))
    st.title("🤖 تطبيق Gemini الذكي")

    # --- ضع مفتاحك هنا ---
    GEMINI_API_KEY = "AIzaSyC8njO_svdjYqKO9eMH8DkklfqHfjyiYIQ" 
    # تأكد من استبدال الكلمة أعلاه بمفتاحك الحقيقي الذي يبدأ بـ AIza
    
    genai.configure(api_key=GEMINI_API_KEY)

    user_question = st.text_area("اسأل تطبيقك الآن:", placeholder="اكتب سؤالك هنا...")

    if st.button("إرسال إلى Gemini"):
        if user_question:
            # قائمة بالموديلات المتاحة لنجربها تلقائياً
            models_to_try = [
                'gemini-1.5-flash', 
                'gemini-1.5-pro', 
                'gemini-pro'
            ]
            
            success = False
            with st.spinner('جاري البحث عن أفضل موديل متاح في حسابك...'):
                for model_name in models_to_try:
                    try:
                        model = genai.GenerativeModel(model_name)
                        response = model.generate_content(user_question)
                        
                        # إذا وصلنا هنا فهذا يعني أن الموديل اشتغل!
                        st.success(f"تم الرد بنجاح باستخدام موديل: {model_name}")
                        st.write(response.text)
                        success = True
                        break 
                    except Exception:
                        continue # فشل؟ جرب الموديل التالي في القائمة
            
            if not success:
                st.error("للأسف، جوجل ترفض جميع الموديلات حالياً.")
                st.info("نصيحة: اذهب لـ Google AI Studio وتأكد من إنشاء API Key جديد في 'New Project'.")
        else:
            st.warning("رجاءً اكتب سؤالك أولاً.")
