import streamlit as st
import json
from core.constants import ACTIVITY_TYPES
from services import api_client

def render():
    st.title("📝 تسجيل نتاج علمي جديد")
    token = st.session_state["token"]
    me = st.session_state["me"]

    if me["role"] in ("admin", "dept_head"):
        st.error("⚠️ عذراً، لا يمكنك تسجيل نتاج علمي بهذه الصفة.")
        return

    st.markdown('<div class="rtl-header">📌 اختر نوع النشاط لتخصيص الحقول:</div>', unsafe_allow_html=True)
    w_type = st.selectbox("", ACTIVITY_TYPES, label_visibility="collapsed")

    st.markdown("---")
    st.markdown(f'<div class="rtl-header">📄 تفاصيل: {w_type}</div>', unsafe_allow_html=True)

    with st.form("new_work"):
        c1, c2 = st.columns([3, 1])
        title = c1.text_input("العنوان الكامل للعمل *")
        date_pub = c2.date_input("التاريخ *")
        lang = st.selectbox("اللغة", ["العربية", "الإنجليزية", "الفرنسية"])
        details = {"lang": lang}
        pts, cls = 10, "غير مصنف"

        if w_type == "مقال في مجلة علمية":
            c1, c2 = st.columns(2)
            j = c1.text_input("اسم المجلة *")
            issn = c2.text_input("ISSN")
            cls = st.selectbox("التصنيف", ["A", "B", "C", "Q1", "Q2", "Q3", "Q4"])
            idx = st.multiselect("الفهرسة", ["ASJP", "Scopus", "WoS"])
            details.update({"journal": j, "issn": issn, "indexing": idx})
            pts = 100 if cls in ["A", "Q1"] else (75 if cls in ["B", "Q2"] else 50)

        elif w_type == "مداخلة في مؤتمر":
            c1, c2 = st.columns(2)
            conf = c1.text_input("اسم الملتقى *")
            org = c2.text_input("الجهة المنظمة")
            scope = st.selectbox("النطاق", ["وطني", "دولي"])
            details.update({"conf": conf, "organizer": org, "scope": scope})
            pts = 50 if scope == "دولي" else 25

        elif w_type in ["تأليف كتاب", "فصل في كتاب"]:
            c1, c2 = st.columns(2)
            pub = c1.text_input("دار النشر *")
            isbn = c2.text_input("ISBN")
            details.update({"publisher": pub, "isbn": isbn})
            pts = 80 if w_type == "تأليف كتاب" else 40

        elif w_type == "تأطير مذكرة":
            c1, c2 = st.columns(2)
            stud = c1.text_input("اسم الطالب")
            lvl = c2.selectbox("المستوى", ["ماستر", "دكتوراه"])
            details.update({"student": stud, "level": lvl})
            pts = 20

        elif w_type == "مشروع بحث":
            c1, c2 = st.columns(2)
            code = c1.text_input("رمز المشروع")
            role = c2.selectbox("الصفة", ["رئيس", "عضو"])
            details.update({"code": code, "role": role})
            pts = 60

        elif w_type == "براءة اختراع":
            c1, c2 = st.columns(2)
            num = c1.text_input("رقم البراءة")
            body = c2.text_input("الهيئة المانحة")
            details.update({"number": num, "body": body})
            pts = 150

        submitted = st.form_submit_button("💾 حفظ البيانات", type="primary", use_container_width=True)

    if submitted:
        if not title.strip():
            st.warning("يرجى إدخال عنوان العمل")
            return
        payload = {
            "title": title.strip(),
            "details": details,
            "activity_type": w_type,
            "classification": cls,
            "publication_date": date_pub.isoformat(),
            "points": int(pts),
        }
        api_client.create_work(token, payload)
        st.success("✅ تم الحفظ بنجاح!")
