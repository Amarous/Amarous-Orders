import streamlit as st
from groq import Groq

# --- إعدادات الهوية ---
st.set_page_config(page_title="Amarous Orders", page_icon="🛍️", layout="wide")

if 'login' not in st.session_state: st.session_state.login = False
if 'user_role' not in st.session_state: st.session_state.user_role = None

# --- واجهة تسجيل الدخول ---
if not st.session_state.login:
    st.markdown("<h1 style='text-align: center;'>🔐 Amarous Login</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        user_type = st.selectbox("نوع المستخدم", ["Admin (bego)", "Stock Keeper (kota)"])
        user = st.text_input("اسم المستخدم")
        pw = st.text_input("كلمة السر", type="password")
        if st.button("دخول النظام"):
            if user == "bego" and pw == "992023":
                st.session_state.login = True
                st.session_state.user_role = "admin"
                st.rerun()
            elif user == "kota" and pw == "kota123":
                st.session_state.login = True
                st.session_state.user_role = "stock_keeper"
                st.rerun()
            else:
                st.error("بيانات الدخول غير صحيحة")
else:
    # --- واجهة التطبيق الذكي ---
    st.sidebar.image("https://i.ibb.co/6c2Y6y2/logo.jpg", width=100)
    st.sidebar.title(f"مرحباً {st.session_state.user_role}")
    
    # محرك Groq (استبدل gsk_... بمفتاحك الحقيقي)
    client = Groq(api_key="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")
    
    st.title("🤖 مساعد أماروس الذكي")
    user_input = st.text_area("اسأل تطبيقك (يفكر ويبحث الآن):")

    if st.button("إرسال"):
        if user_input:
            with st.spinner('جاري التحليل...'):
                try:
                    chat_completion = client.chat.completions.create(
                        messages=[
                            {"role": "system", "content": "أنت نظام أماروس الخبير في إدارة الفواتير والطلبات."},
                            {"role": "user", "content": user_input}
                        ],
                        model="llama-3.3-70b-versatile",
                    )
                    st.success("الرد:")
                    st.write(chat_completion.choices[0].message.content)
                except Exception as e:
                    st.error(f"عذراً، هناك مشكلة في المفتاح: {e}")
        else:
            st.warning("اكتب شيئاً أولاً.")

    if st.sidebar.button("🚪 تسجيل خروج"):
        st.session_state.login = False
        st.rerun()
