import streamlit as st
from groq import Groq
import json

# --- 1. إعدادات الهوية والأمان ---
st.set_page_config(page_title="Amarous Orders", page_icon="🛍️", layout="wide")

if 'login' not in st.session_state:
    st.session_state.login = False
if 'user_role' not in st.session_state:
    st.session_state.user_role = None

# --- 2. واجهة تسجيل الدخول (مع اختيار نوع المستخدم) ---
if not st.session_state.login:
    st.markdown("<h1 style='text-align: center;'>🔐 Amarous Login</h1>", unsafe_allow_index=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        user_type = st.selectbox("نوع المستخدم", ["Admin (bego)", "Manager", "Stock Keeper (kota)"])
        user = st.text_input("اسم المستخدم")
        pw = st.text_input("كلمة السر", type="password")
        if st.button("دخول النظام"):
            # التحقق من الحسابات التي صممتها
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
    # --- 3. محرك الذكاء الاصطناعي (تطبيقك المخصص) ---
    # ضع مفتاح Groq الخاص بك هنا
    client = Groq(api_key="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")

    # تعليمات تطبيقك (التي استخرجتها من المحادثة)
    SYSTEM_INSTRUCTIONS = """
    أنت نظام "أماروس" (Amarous Orders) المتطور لإدارة الفواتير.
    قواعد العمل الخاصة بك:
    1. تقسيم الفواتير:
       - فواتير الويبسايت: تبدأ بتسلسل #W- (مثال #W-101).
       - فواتير السوشيال ميديا: تبدأ بتسلسل #S- (مثال #S-50).
    2. الحسابات المالية:
       - الإجمالي = (سعر المنتجات * الكمية) + مصاريف الشحن - الخصم.
       - المتبقي (Balance) باللون الأحمر = الإجمالي - المدفوع.
    3. الصلاحيات:
       - bego (Admin): له كامل الصلاحيات (حذف، تعديل، برمجة، إدارة مستخدمين).
       - kota (Stock Keeper): يرى فقط "موافقة المخزن" ويحدد (متوفر/غير متوفر).
    4. استخراج البيانات: استخلص (رقم الفاتورة، العميل، العنوان، المنتجات، الأسعار، طريقة الدفع: نقداً/فيزا/انستاباي).
    """

    # --- 4. واجهة التطبيق الرئيسية (Theme بوهيمي) ---
    st.markdown("""
        <style>
        .stApp {
            background-color: #FAF9F6;
            background-image: radial-gradient(#9CAF88 0.5px, transparent 0.5px);
            background-size: 20px 20px;
        }
        .main-card { background: white; padding: 20px; border-radius: 15px; border-left: 5px solid #D4A373; }
        </style>
    """, unsafe_allow_index=True)

    # الهيدر واللوجو
    st.image("https://i.ibb.co/6c2Y6y2/logo.jpg", width=150) # الرابط الذي ظهر في محادثتك
    st.title(f"👋 أهلاً بك، {st.session_state.user_role}")

    # أزرار الإضافة (مرتبة تحت بعضها كما طلبت)
    with st.sidebar:
        st.header("إضافة فواتير")
        if st.session_state.user_role == "admin":
            st.button("➕ إضافة فاتورة ويبسايت", use_container_width=True)
            st.button("📱 إضافة فاتورة سوشيال", use_container_width=True)
            st.button("📦 رفع فواتير متعددة (Batch)", use_container_width=True)
            if st.button("⚙️ قسم البرمجة"):
                st.info("واجهة Gemini 3.1 Pro Code Assistant مفعلة")
        
        if st.button("🚪 تسجيل خروج"):
            st.session_state.login = False
            st.rerun()

    # شاشة العمل الرئيسية
    tab1, tab2 = st.tabs(["📋 جدول الفواتير", "☁️ مكتبة الوسائط"])
    
    with tab1:
        st.markdown("<div class='main-card'>", unsafe_allow_index=True)
        col_f1, col_f2 = st.columns(2)
        with col_f1: st.selectbox("فلتر المحافظة", ["الكل", "Cairo", "Giza", "Alexandria"])
        with col_f2: st.selectbox("حالة الجاهزية", ["الكل", "جاهز ✅", "غير جاهز ❌"])
        
        # مثال لجدول الفواتير (نفس التقسيمة المطلوبة)
        st.table({
            "رقم الفاتورة": ["#W-101", "#S-50"],
            "العميل": ["محمد علي", "سارة أحمد"],
            "المكان": ["القاهرة", "الجيزة"],
            "المبلغ المتبقي": ["0 EGP", "150 EGP"],
            "الحالة": ["جاهز", "في الانتظار"]
        })
        st.markdown("</div>", unsafe_allow_index=True)

    with tab2:
        if st.session_state.user_role == "admin":
            st.write("📂 جميع الملفات واللوجو محفوظة هنا (Database)")
        else:
            st.warning("عذراً، هذه المكتبة للمدير فقط.")
