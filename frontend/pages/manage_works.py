import streamlit as st
import pandas as pd
from services import api_client

def render():
    st.title("🗂️ إدارة الأنشطة البحثية")
    token = st.session_state["token"]
    me = st.session_state["me"]

    search = st.text_input("🔎 بحث سريع (العنوان، الباحث)...")

    rows = api_client.reports_works(token, params={"search": search} if search else {})
    df = pd.DataFrame(rows)
    if df.empty:
        st.info("لا توجد بيانات.")
        return

    st.info(f"عدد السجلات: {len(df)}")
    for _, row in df.iterrows():
        label = f"{row.get('activity_type')} | {row.get('title')} (👤 {row.get('researcher')})"
        with st.expander(label):
            c1, c2 = st.columns([3, 1])
            nt = c1.text_input("تعديل العنوان", row.get("title") or "", key=f"t_{row['id']}")
            nd = c2.date_input("تعديل التاريخ", pd.to_datetime(row.get("publication_date")).date(), key=f"d_{row['id']}")
            b1, b2 = st.columns(2)
            if b1.button("حفظ التعديلات", key=f"sv_{row['id']}"):
                api_client.update_work(token, int(row["id"]), {"title": nt, "publication_date": nd.isoformat()})
                st.success("تم التعديل")
                st.rerun()
            if b2.button("حذف نهائي", key=f"dl_{row['id']}"):
                api_client.delete_work(token, int(row["id"]))
                st.success("تم الحذف")
                st.rerun()
