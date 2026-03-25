import streamlit as st
import google.generativeai as genai

# --- إعدادات الصفحة ---
st.set_page_config(page_title="Amarous Orders", layout="wide")

if 'login' not in st.session_state: st.session_state.login = False

# --- واجهة الدخول ---
if not st.session_state.login:
    st.markdown("<h1 style='text-align: center;'>🔐 دخول نظام أماروس</h1>", unsafe_allow_html=True)
    user = st.text_input("اسم المستخدم")
    pw = st.text_input("كلمة السر", type="password")
    if st.button("دخول"):
        if user == "bego" and pw == "992023":
            st.session_state.login = True
            st.rerun()
        else: st.error("بيانات خطأ")
else:
    # --- تشغيل تصميمك من AI Studio ---
    st.title("🛍️ تطبيق Amarous المخصص")
    
    # ضع مفتاحك هنا (تأكد أنه مفتاح جديد من New Project)
    API_KEY = "ضع_مفتاحك_هنا"
    genai.configure(api_key=API_KEY)

    user_input = st.text_area("أدخل مدخلات الأوردر (تطبيقك سيفكر ويبحث الآن):")

    if st.button("تشغيل التصميم"):
        if user_input:
            with st.spinner('جاري المعالجة...'):
                try:
                    # اختيار الموديل الذي يدعم ميزاتك حالياً
                    model = genai.GenerativeModel(
                        model_name='gemini-1.5-pro', # الموديل الأكثر استقراراً لبرمجتك
                        tools=[{'google_search': {}}] # تفعيل أداة البحث التي صممتها
                    )
                    
                    response = model.generate_content(user_input)
                    st.success("النتيجة:")
                    st.write(response.text)
                except Exception as e:
                    st.error(f"حدث خطأ: {e}")
