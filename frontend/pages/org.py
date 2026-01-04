import streamlit as st
from services import api_client


def _rank_key(name: str):
    n = (name or "").strip()
    if n.startswith("أ.د"):
        return (1, n)
    if n.startswith("د."):
        return (2, n)
    if n.startswith("ط"):
        return (3, n)
    return (4, n)


def _render_team(team: dict, members: list[dict]):
    st.markdown(
        f"""**🧬 {team.get('name','')}**  
**المختصر:** {team.get('short_name','-')} | **رئيس الفرقة:** {team.get('head_name','-')}  
**التصنيف:** {team.get('classification','-')}  
**الميادين:** {team.get('domains','-')}  
**الكلمات المفتاحية:** {team.get('keywords','-')}"""
    )
    st.markdown("**التعريف:**")
    st.write(team.get("description") or "لا يوجد وصف")
    st.markdown("**البرنامج العلمي:**")
    st.write(team.get("program_desc") or "لم يتم إدخال وصف البرنامج العلمي بعد.")
    st.markdown("---")
    st.markdown("### 👥 القوائم الاسمية")

    buckets = {
        "permanent": [],
        "phd_student": [],
        "affiliate": [],
        "associate": [],
    }
    for m in members or []:
        k = m.get("member_type") or "permanent"
        if k not in buckets:
            k = "permanent"
        buckets[k].append(m)

    cols = st.columns(4)
    groups = [
        ("الدائمون", "permanent", "🏛️"),
        ("طلبة الدكتوراه", "phd_student", "🎓"),
        ("ملحق بحث", "affiliate", "🤝"),
        ("عضو مشارك", "associate", "🌍"),
    ]
    for col, (title, key, icon) in zip(cols, groups):
        with col:
            st.markdown(f"#### {icon} {title}")
            arr = sorted(buckets.get(key, []), key=lambda x: _rank_key(x.get("full_name", "")))
            if not arr:
                st.caption("فارغ")
            else:
                for m in arr:
                    st.write(f"- {m.get('full_name','')}")


def _render_department(full: dict, only_team_id: int | None = None):
    dept = full.get("department") or {}
    if dept:
        st.markdown(
            f"""**📂 {dept.get('name_ar','')}**  
**اللاتينية:** {dept.get('name_la','-')} | **المختصر:** {dept.get('short_name','-')} | **الرقم:** {dept.get('id','-')}  
**رئيس القسم:** {dept.get('head_name','-')}"""
        )

    st.markdown("---")
    st.markdown("#### 🔽 الفرق التابعة:")

    for item in full.get("teams", []) or []:
        team = item.get("team", {}) or {}
        members = item.get("members", []) or []

        if only_team_id is not None and team.get("id") != only_team_id:
            continue

        # ✅ Expander واحد فقط للفرق (مسموح)
        with st.expander(f"الفرقة: {team.get('name','')}", expanded=False):
            _render_team(team, members)


def render():
    st.title("🏢 الهيكل التنظيمي (التفصيلي)")

    token = st.session_state.get("token")
    me = st.session_state.get("me") or {}
    role = me.get("role")

    if not token or not role:
        st.warning("يرجى تسجيل الدخول.")
        return

    if role == "admin":
        depts = api_client.departments(token=None)  # public endpoint
        if not depts:
            st.info("لا توجد أقسام.")
            return

        # ✅ قابل للطي بدون nested expanders: استخدم Tabs للأقسام
        labels = []
        dept_ids = []
        for d in depts:
            labels.append(d.get("name_ar") or f"Department {d.get('id')}")
            dept_ids.append(int(d["id"]))

        tabs = st.tabs([f"📂 {x}" for x in labels])

        for tab, dept_id in zip(tabs, dept_ids):
            with tab:
                full = api_client.department_full(token, dept_id)
                _render_department(full)

    elif role == "dept_head":
        dept_id = me.get("department_id")
        if not dept_id:
            st.warning("غير مرتبط بقسم.")
            return
        full = api_client.department_full(token, int(dept_id))
        _render_department(full)

    elif role in ("leader", "researcher"):
        dept_id = me.get("department_id")
        team_id = me.get("team_id")
        if not dept_id:
            st.warning("غير مرتبط بقسم.")
            return

        full = api_client.department_full(token, int(dept_id))
        if team_id:
            st.success(f"أنت عضو في قسم: {(full.get('department') or {}).get('name_ar','')}")
            _render_department(full, only_team_id=int(team_id))
        else:
            _render_department(full)

    else:
        st.info("لا توجد صلاحية عرض لهذه الصفحة.")