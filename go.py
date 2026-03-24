import streamlit as st
import google.generativeai as genai

# إعداد الدخول
if 'login' not in st.session_state: st.session_state.login = False

if not st.session_state.login:
    st.title("🔐 دخول لتطبيقي الخاص")
    user = st.text_input("اسم المستخدم")
    pw = st.text_input("كلمة السر", type="password")
    if st.button("دخول"):
        if user == "admin" and pw == "123":
            st.session_state.login = True
            st.rerun()
else:
    st.title("🚀 تطبيق AI Studio المخصص")
    
    # ضع مفتاحك الجديد هنا (تأكد إنه API Key جديد)
    API_KEY = "AIzaSyD2LJKLk16l0otJVTIwLvs1d1ib6__HiDQ"
    genai.configure(api_key=API_KEY)

    # استخدام الموديل المستقر (اللي شغال في كل مكان)
    model = genai.GenerativeModel('gemini-pro')

    user_input = st.text_area("تحدث مع تطبيقك المخصص:")
    if st.button("إرسال"):
        if user_input:
            with st.spinner('جاري الرد من تطبيقك...'):
                try:
                    response = model.generate_content(user_input)
                    st.markdown(f"**الرد:** {response.text}")
                except Exception as e:
                    st.error(f"جوجل ترفض الطلب حالياً: {e}")
                    st.info("تأكد من إنشاء API Key جديد في 'New Project' من AI Studio")
