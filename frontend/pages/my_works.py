import streamlit as st
import pandas as pd
from services import api_client

def render():
    st.title("📂 سجل أعمالي")
    token = st.session_state["token"]
    me = st.session_state["me"]

    if me["role"] in ("admin", "dept_head"):
        st.error("⚠️ عذراً، لا يتوفر سجل أعمال خاص لهذه الصلاحية.")
        return

    rows = api_client.reports_works(token, params={})
    df = pd.DataFrame(rows)
    if df.empty:
        st.info("لا توجد بيانات.")
        return

    df_my = df[df["user_id"] == me["id"]] if "id" in me else df
    if df_my.empty:
        st.info("لا توجد أعمال مسجلة لك.")
        return

    st.markdown("### 📄 تصدير السيرة الذاتية")
    if st.button("🚀 إنشاء وتصدير CV (PDF)", type="primary"):
        pdf, dispo = api_client.export_cv(token, me["id"])
        fname = "CV.pdf"
        if "filename=" in dispo:
            fname = dispo.split("filename=")[-1].strip('"')
        st.download_button("📥 اضغط لتحميل ملف الـ PDF", pdf, fname, "application/pdf", type="primary")

    st.markdown("---")
    unique_types = sorted(df_my["activity_type"].dropna().unique().tolist())
    tabs = st.tabs(["الكل"] + unique_types)

    with tabs[0]:
        st.dataframe(df_my[["title", "activity_type", "publication_date", "points"]], use_container_width=True)

    for i, t in enumerate(unique_types, start=1):
        with tabs[i]:
            sub = df_my[df_my["activity_type"] == t]
            st.dataframe(sub[["title", "publication_date", "points"]], use_container_width=True)
