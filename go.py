import streamlit as st
from groq import Groq

# --- 1. إعدادات الهوية والأمان ---
st.set_page_config(page_title="Amarous Orders", page_icon="🛍️", layout="wide")

if 'login' not in st.session_state:
    st.session_state.login = False
if 'user_role' not in st.session_state:
    st.session_state.user_role = None

# --- 2. واجهة تسجيل الدخول ---
if not st.session_state.login:
    st.markdown("<h1 style='text-align: center;'>🔐 Amarous Login</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        user_type = st.selectbox("نوع المستخدم", ["Admin (bego)", "Manager", "Stock Keeper (kota)"])
        user = st.text_input("اسم المستخدم")
        pw = st.text_input("كلمة السر", type="password")
        if st.button("دخول النظام"):
            if user == "bego" and pw == "992023" and user_type == "Admin (bego)":
                st.session_state.login = True
                st.session_state.user_role = "admin"
                st.rerun()
            elif user == "kota" and pw == "kota123" and user_type == "Stock Keeper (kota)":
                st.session_state.login = True
                st.session_state.user_role = "stock_keeper"
                st.rerun()
            else:
                st.error("بيانات الدخول غير صحيحة")
else:
    # --- واجهة التطبيق بعد الدخول ---
    st.title(f"👋 أهلاً بك، {st.session_state.user_role}")
    st.write("تم ربط تطبيقك بنجاح! يمكنك الآن البدء في إدارة الأوردرات.")
    
    if st.sidebar.button("🚪 تسجيل خروج"):
        st.session_state.login = False
        st.rerun()
