import streamlit as st
import requests

if 'login' not in st.session_state:
    st.session_state.login = False

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
    st.sidebar.title("إعدادات التطبيق")
    if st.sidebar.button("تسجيل خروج"):
        st.session_state.login = False
        st.rerun()

    st.title("🤖 تطبيق Gemini الأصلي")
    
    # ضع مفتاح Google AI Studio هنا
    GEMINI_API_KEY = "AIzaSyC8njO_svdjYqKO9eMH8DkklfqHfjyiYIQ"

    user_question = st.text_area("تحدث مع تطبيقك:", placeholder="اكتب سؤالك هنا...")

    if st.button("إرسال إلى Gemini"):
        if user_question:
            # الرابط المستقر والمجرب
            url = f"https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key={GEMINI_API_KEY}"
            
            headers = {'Content-Type': 'application/json'}
            data = {"contents": [{"parts": [{"text": user_question}]}]}
            
            try:
                response = requests.post(url, headers=headers, json=data)
                result = response.json()
                
                if response.status_code == 200:
                    answer = result['candidates'][0]['content']['parts'][0]['text']
                    st.success("رد Gemini:")
                    st.write(answer)
                else:
                    st.error(f"خطأ: {result.get('error', {}).get('message', 'حدث خطأ ما')}")
            except Exception as e:
                st.error(f"فشل الاتصال: {e}")
        else:
            st.warning("رجاءً اكتب سؤالك أولاً.")
