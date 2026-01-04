import streamlit as st
from services import api_client

def render():
    st.title("⚙️ الإعدادات")
    token = st.session_state["token"]

    with st.form("pwd"):
        st.subheader("تغيير كلمة المرور")
        p1 = st.text_input("كلمة المرور الجديدة", type="password")
        p2 = st.text_input("تأكيد كلمة المرور", type="password")
        ok = st.form_submit_button("تغيير كلمة المرور")
    if ok:
        if p1 == p2 and len(p1) > 0:
            api_client.change_password(token, p1)
            st.success("تم التغيير بنجاح")
        else:
            st.warning("كلمات المرور غير متطابقة")
