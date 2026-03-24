import streamlit as st
import requests
import json

# --- 1. إعدادات الأمان ومنع الأخطاء ---
if 'login' not in st.session_state:
    st.session_state.login = False
if 'user_name' not in st.session_state:
    st.session_state.user_name = ""

# --- 2. شاشة الدخول ---
if not st.session_state.login:
    st.title("🔐 تسجيل الدخول")
    user = st.text_input("اسم المستخدم")
    pw = st.text_input("كلمة السر", type="password")
    if st.button("دخول"):
        if user == "admin" and pw == "123":
            st.session_state.login = True
            st.session_state.user_name = user
            st.rerun()
        else:
            st.error("بيانات خطأ")
else:
    # --- 3. واجهة التطبيق بعد الدخول ---
    st.sidebar.title(f"مرحباً {st.session_state.user_name}")
    if st.sidebar.button("تسجيل خروج"):
        st.session_state.login = False
        st.rerun()

    st.title("🚀 مساعدي الذكي (نسخة Groq السريعة)")
    
    # ضع مفتاح Groq هنا (الذي يبدأ بـ gsk_...)
    GROQ_API_KEY = "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"

    user_question = st.text_input("اسألني أي شيء:")

    if st.button("إرسال"):
        if user_question:
            # استخدام محرك Groq الموثوق
            url = "https://api.groq.com/openai/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            }
            data = {
                "model": "llama-3.1-8b-instant",
                "messages": [{"role": "user", "content": user_question}]
            }
            
            try:
                response = requests.post(url, headers=headers, json=data)
                result = response.json()
                
                if response.status_code == 200:
                    answer = result['choices'][0]['message']['content']
                    st.success("الرد:")
                    st.write(answer)
                    
                    # حفظ المحادثة
                    with open("chat_logs.txt", "a", encoding="utf-8") as f:
                        f.write(f"سؤال: {user_question} | رد: {answer}\n")
                        f.write("-" * 20 + "\n")
                else:
                    st.error(f"خطأ في الاتصال: {result['error']['message']}")
            except Exception as e:
                st.error(f"فشل الاتصال: {e}")