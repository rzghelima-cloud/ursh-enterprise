import streamlit as st
from services import api_client
from core.constants import MEMBER_TYPES

def render():
    st.title("👥 إدارة المستخدمين (إضافة يدوية)")
    token = st.session_state["token"]

    c1, c2 = st.columns(2)
    name = c1.text_input("الاسم الكامل")
    uname = c2.text_input("اسم الدخول")

    c3, c4 = st.columns(2)
    pas = c3.text_input("كلمة المرور", type="password")
    role_label = c4.selectbox("الصفة", ["رئيس قسم", "رئيس فرقة", "باحث"])

    m_type = "permanent"
    if role_label in ["رئيس فرقة", "باحث"]:
        m_type = st.selectbox("نوع العضوية", list(MEMBER_TYPES.keys()), format_func=lambda x: MEMBER_TYPES[x])

    depts = api_client.departments(token)
    d_map = {d["name_ar"]: d["id"] for d in depts if d.get("name_ar")}
    sel_d_id = None
    sel_t_id = None

    if role_label != "رئيس قسم":
        d_name = st.selectbox("القسم", list(d_map.keys()))
        sel_d_id = d_map[d_name]
        if role_label in ["رئيس فرقة", "باحث"]:
            teams = api_client.teams(token, department_id=sel_d_id)
            if teams:
                t_map = {t["name"]: t["id"] for t in teams if t.get("name")}
                t_name = st.selectbox("الفرقة", list(t_map.keys()))
                sel_t_id = t_map[t_name]
            else:
                st.warning("⚠️ هذا القسم فارغ من الفرق")

    if st.button("إضافة المستخدم", type="primary", use_container_width=True):
        r_code = "dept_head" if role_label == "رئيس قسم" else ("leader" if role_label == "رئيس فرقة" else "researcher")
        payload = {
            "username": uname,
            "full_name": name,
            "password": pas,
            "role": r_code,
            "department_id": sel_d_id,
            "team_id": sel_t_id,
            "member_type": m_type,
        }
        api_client.add_user_manual(token, payload)
        st.success("تمت الإضافة بنجاح")
