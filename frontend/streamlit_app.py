import streamlit as st
from services import api_client
from core.constants import ACTIVATION_CODES, MEMBER_TYPES
from core.ui_style import CSS

from pages import dashboard, org, add_work, manage_works, my_works, admin_users, settings

st.set_page_config(page_title="URSH - بوابة البحث العلمي", layout="wide", initial_sidebar_state="expanded", page_icon="🎓")
st.markdown(CSS, unsafe_allow_html=True)

def logout():
    for k in ["token", "me"]:
        st.session_state.pop(k, None)
    st.rerun()

def login_view():
    c1, c2, c3 = st.columns([1, 1.5, 1])
    with c2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown('<div style="font-size: 80px; margin-bottom: 10px; text-align:center;">🏛️</div>', unsafe_allow_html=True)
        st.markdown("""<div style="display:flex; flex-direction:column; align-items:center; justify-content:center; text-align:center; width:100%; margin-bottom:30px;">
            <h1 style="color:#2563eb; font-family:'Cairo'; margin:0; font-size:2.5rem;">بوابة البحث العلمي</h1>
            <p style="opacity:0.7; font-size:1.1rem; margin-top:5px;">نظام إدارة المخابر الجامعية الموحد</p>
        </div>""", unsafe_allow_html=True)

        tab_login, tab_signup = st.tabs(["🔐 تسجيل الدخول", "📝 حساب جديد (بالكود)"])

        with tab_login:
            with st.form("login"):
                u = st.text_input("اسم المستخدم")
                p = st.text_input("كلمة المرور", type="password")
                ok = st.form_submit_button("دخول", type="primary", use_container_width=True)
            if ok:
                data = api_client.login(u, p)
                if data:
                    st.session_state["token"] = data["access_token"]
                    st.session_state["me"] = api_client.me(st.session_state["token"])
                    st.rerun()
                else:
                    st.error("بيانات خاطئة")

        with tab_signup:
            st.markdown("##### 🆕 إنشاء حساب باستخدام كود التفعيل")
            c_a, c_b = st.columns(2)
            new_name = c_a.text_input("الاسم الكامل")
            new_user = c_b.text_input("اسم المستخدم (للدخول)")

            c_pass, c_role = st.columns(2)
            new_pass = c_pass.text_input("كلمة المرور", type="password")
            role_key = c_role.selectbox("الصفة", list(ACTIVATION_CODES.keys()))

            m_type_key = "permanent"
            if role_key in ["leader", "researcher"]:
                m_type_key = st.selectbox("نوع العضوية", list(MEMBER_TYPES.keys()), format_func=lambda x: MEMBER_TYPES[x])

            sel_dept_id = None
            sel_team_id = None

            try:
                depts = api_client.departments(token=None)
                d_map = {d["name_ar"]: d["id"] for d in depts if d.get("name_ar")}
                if role_key != "admin" and d_map:
                    d_name = st.selectbox("القسم", list(d_map.keys()))
                    sel_dept_id = d_map[d_name]
                    if role_key in ["leader", "researcher"]:
                        teams = api_client.teams(token=None, department_id=sel_dept_id)
                        if teams:
                            t_map = {t["name"]: t["id"] for t in teams if t.get("name")}
                            t_name = st.selectbox("الفرقة", list(t_map.keys()))
                            sel_team_id = t_map[t_name]
                        else:
                            st.warning("⚠️ لا توجد فرق في هذا القسم.")
            except Exception:
                st.warning("تعذر جلب الأقسام/الفرق (تأكد من تشغيل الـ API).")

            act_code = st.text_input("🔑 كود التفعيل", type="password")

            if st.button("إنشاء الحساب", type="primary", use_container_width=True):
                if new_user and new_pass and act_code:
                    payload = {
                        "full_name": new_name,
                        "username": new_user,
                        "password": new_pass,
                        "role": role_key,
                        "activation_code": act_code,
                        "department_id": sel_dept_id,
                        "team_id": sel_team_id,
                        "member_type": m_type_key,
                    }
                    try:
                        api_client.register(payload)
                        st.success("✅ تم إنشاء الحساب. يمكنك الآن تسجيل الدخول.")
                    except Exception as e:
                        st.error(str(e))
                else:
                    st.warning("جميع الحقول مطلوبة")

def app_view():
    token = st.session_state["token"]
    me_ = st.session_state["me"]

    with st.sidebar:
        st.markdown(f"<div style='text-align:center; margin-bottom:12px; font-weight:bold; opacity:0.7;'>مرحباً بك: {me_['full_name']} 👋</div>", unsafe_allow_html=True)

        menu_options = {
            "📊 لوحة القيادة": "dashboard",
            "🏢 الهيكل التنظيمي": "org",
            "🗂️ إدارة الأنشطة": "manage",
            "⚙️ الإعدادات": "settings",
        }

        if me_["role"] in ["leader", "researcher"]:
            menu_options["📝 تسجيل نتاج جديد"] = "add_work"
            menu_options["📂 سجل أعمالي"] = "my_works"

        if me_["role"] == "admin":
            menu_options["👥 إدارة المستخدمين (يدوي)"] = "admin_users"

        choice_label = st.radio("القائمة", list(menu_options.keys()), label_visibility="collapsed")
        choice = menu_options[choice_label]

        st.markdown("---")
        if st.button("تسجيل الخروج", type="secondary"):
            logout()

    if choice == "dashboard":
        dashboard.render()
    elif choice == "org":
        org.render()
    elif choice == "add_work":
        add_work.render()
    elif choice == "manage":
        manage_works.render()
    elif choice == "my_works":
        my_works.render()
    elif choice == "admin_users":
        admin_users.render()
    elif choice == "settings":
        settings.render()

if "token" not in st.session_state:
    login_view()
else:
    if "me" not in st.session_state:
        st.session_state["me"] = api_client.me(st.session_state["token"])
    app_view()
