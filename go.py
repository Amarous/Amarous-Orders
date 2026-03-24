import streamlit as st
import requests

# --- 1. الإعدادات ---
if 'login' not in st.session_state:
    st.session_state.login = False

# --- 2. شاشة الدخول ---
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
    # --- 3. واجهة Gemini (تطبيقك الأصلي) ---
    st.sidebar.title("إعدادات التطبيق")
    if st.sidebar.button("تسجيل خروج"):
        st.session_state.login = False
        st.rerun()

    st.title("🤖 تطبيق Gemini الأصلي")
    
    # ضع مفتاح Google AI Studio هنا (الذي يبدأ بـ AIza)
    GEMINI_API_KEY = "AIzaSyC8njO_svdjYqKO9eMH8DkklfqHfjyiYIQ"

    user_question = st.text_area("تحدث مع تطبيقك الذي صممته:", placeholder="اكتب سؤالك هنا...")

    if st.button("إرسال إلى Gemini"):
        if user_question:
            # الرابط العالمي المستقر لـ Gemini 1.5 Flash
url = f"https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key={GEMINI_API_KEY}"            
            headers = {'Content-Type': 'application/json'}
            data = {
                "contents": [{
                    "parts": [{"text": user_question}]
                }]
            }
            
            try:
                response = requests.post(url, headers=headers, json=data)
                result = response.json()
                
                if response.status_code == 200:
                    # استخراج الرد من هيكل بيانات جوجل
                    answer = result['candidates'][0]['content']['parts'][0]['text']
                    st.success("رد Gemini:")
                    st.write(answer)
                else:
                    st.error(f"خطأ من جوجل: {result.get('error', {}).get('message', 'خطأ غير معروف')}")
            except Exception as e:
                st.error(f"فشل الاتصال بجوجل: {e}")
        else:
            st.warning("رجاءً اكتب سؤالك أولاً.")
