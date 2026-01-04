import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date
from services import api_client

def render():
    st.markdown("## 📊 لوحة القيادة والتحليل البياني")
    token = st.session_state["token"]
    user = st.session_state["me"]

    # Load base report (scoped by backend)
    rows = api_client.reports_works(token, params={})
    df = pd.DataFrame(rows)

    if df.empty:
        st.info("لا توجد بيانات متاحة لعرضها.")
        return

    df["publication_date"] = pd.to_datetime(df["publication_date"]).dt.date

    with st.expander("🔍 تصفية البيانات", expanded=True):
        col_d1, col_d2 = st.columns(2)
        min_date = df["publication_date"].min()
        max_date = df["publication_date"].max()
        d_from = col_d1.date_input("من تاريخ", min_date)
        d_to = col_d2.date_input("إلى تاريخ", max_date)

        years = sorted(df["year"].dropna().unique().tolist(), reverse=True)
        selected_year = st.selectbox("أو اختر سنة محددة (تتجاوز التاريخ)", ["الكل"] + years)

        c1, c2, c3 = st.columns(3)
        depts = sorted(df["department"].fillna("غير محدد").unique().tolist())
        sel_dept = c1.selectbox("القسم", ["الكل"] + depts)
        if sel_dept != "الكل":
            teams = sorted(df[df["department"] == sel_dept]["team"].fillna("غير محدد").unique().tolist())
        else:
            teams = sorted(df["team"].fillna("غير محدد").unique().tolist())
        sel_team = c2.selectbox("الفرقة", ["الكل"] + teams)
        types = sorted(df["activity_type"].fillna("غير محدد").unique().tolist())
        sel_type = c3.selectbox("نوع النشاط", ["الكل"] + types)

        search = st.text_input("🔎 بحث سريع (العنوان، الباحث)...", "")

    params = {}
    if selected_year != "الكل":
        params["year"] = int(selected_year)
    else:
        params["date_from"] = d_from.isoformat()
        params["date_to"] = d_to.isoformat()
    if sel_dept != "الكل": params["department"] = sel_dept
    if sel_team != "الكل": params["team"] = sel_team
    if sel_type != "الكل": params["activity_type"] = sel_type
    if search.strip(): params["search"] = search.strip()

    rows2 = api_client.reports_works(token, params=params)
    filtered = pd.DataFrame(rows2)
    if filtered.empty:
        st.info("لا توجد نتائج حسب الفلاتر.")
        return
    filtered["publication_date"] = pd.to_datetime(filtered["publication_date"]).dt.date

    # Export Excel
    excel_bytes, dispo = api_client.export_excel(token, params=params)
    fname = "report.xlsx"
    if "filename=" in dispo:
        fname = dispo.split("filename=")[-1].strip('"')
    st.download_button("📥 تحميل التقرير (Excel)", excel_bytes, fname, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

    st.markdown("<br>", unsafe_allow_html=True)
    k1, k2, k3, k4 = st.columns(4)
    with k4:
        st.markdown(f'<div class="kpi-container"><div><div class="kpi-value">{len(filtered)}</div><div class="kpi-label">إجمالي النتاج</div></div><div class="kpi-icon">📚</div></div>', unsafe_allow_html=True)
    with k3:
        st.markdown(f'<div class="kpi-container"><div><div class="kpi-value">{filtered["researcher"].nunique()}</div><div class="kpi-label">الباحثون</div></div><div class="kpi-icon">👥</div></div>', unsafe_allow_html=True)
    with k2:
        st.markdown(f'<div class="kpi-container"><div><div class="kpi-value">{int(filtered["points"].fillna(0).sum())}</div><div class="kpi-label">النقاط</div></div><div class="kpi-icon">⭐</div></div>', unsafe_allow_html=True)
    with k1:
        yr = int(filtered["year"].mode().iloc[0]) if not filtered.empty and not filtered["year"].isna().all() else "-"
        st.markdown(f'<div class="kpi-container"><div><div class="kpi-value">{yr}</div><div class="kpi-label">السنة النشطة</div></div><div class="kpi-icon">📅</div></div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 🏆 مؤشرات الأداء والتميز")

    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        top_res = filtered.groupby("researcher")["points"].sum().reset_index().sort_values("points", ascending=False).head(5)
        fig = px.bar(top_res, x="points", y="researcher", orientation="h", title="🥇 أكثر الباحثين تميزاً (حسب النقاط)", text_auto=True)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        tree_data = filtered.groupby(["department", "team"])["points"].sum().reset_index()
        fig2 = px.treemap(tree_data, path=["department", "team"], values="points", title="🧬 مساهمة الهياكل (خريطة شجرية)", color="department")
        fig2.update_traces(textinfo="label+value+percent entry")
        st.plotly_chart(fig2, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        fig3 = px.pie(filtered, names="activity_type", hole=0.5, title="📊 توزيع الأنشطة")
        st.plotly_chart(fig3, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        yearly = filtered.groupby("year").size().reset_index(name="count")
        fig4 = px.bar(yearly, x="year", y="count", title="📈 التطور السنوي", text_auto=True)
        st.plotly_chart(fig4, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
