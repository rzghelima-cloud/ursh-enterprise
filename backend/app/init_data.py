from sqlalchemy import inspect
from sqlalchemy.orm import Session
from app.core.database import Base, engine
from app.core.security import hash_password
from app.models.department import Department
from app.models.team import Team
from app.models.user import User

def auto_init_system():
    inspector = inspect(engine)
    if not inspector.has_table("users"):
        Base.metadata.create_all(bind=engine)

    db = Session(bind=engine)

    departments_data = [
        {"id": 1, "ar": "الدراسات الفلسفية النظرية", "la": "Theoretical Philosophical Studies", "sh": "TPS", "head": "أ.د. عبد اللاوي عبد الله", "user": "head_tps"},
        {"id": 2, "ar": "الدراسات الفلسفية التطبيقية", "la": "Applied Philosophical Studies", "sh": "APS", "head": "أ.د. دراس شهر زاد", "user": "head_aps"},
        {"id": 3, "ar": "الدراسات الدينية والاتجاهات الروحية", "la": "Religious Studies and Spiritual Trends", "sh": "RSST", "head": "أ.د. رزقي بن عومر", "user": "head_rsst"},
        {"id": 4, "ar": "الدراسات السوسيولوجية", "la": "Sociological Studies", "sh": "SS", "head": "أ.د. شنافي فوزية", "user": "head_ss"},
        {"id": 5, "ar": "الدراسات الأنثروبولوجية", "la": "Anthropological studies", "sh": "AS", "head": "أ.د. مباركة بلحسن", "user": "head_as"},
        {"id": 6, "ar": "الدراسات الإنسانية، اللغات، والترجمة", "la": "Humanities, Languages, and Translation", "sh": "HLT", "head": "د. جميل نسيمة", "user": "head_hlt"},
    ]

    pw_hash = hash_password("12345")

    try:
        for d in departments_data:
            dept = db.query(Department).filter(Department.id == d["id"]).first()
            if not dept:
                dept = Department(id=d["id"], name_ar=d["ar"], name_la=d["la"], short_name=d["sh"], head_name=d["head"])
                db.add(dept)
                db.flush()

                t1 = Team(
                    name=f"فرقة بحث {d['sh']} - النموذجية",
                    name_en=f"Research Team {d['sh']} - Standard",
                    short_name=f"{d['sh']}-A",
                    head_name="د. باحث رئيسي",
                    description="فرقة تعنى بالدراسات المعمقة في التخصص وتطوير المناهج العلمية الحديثة.",
                    classification="بحث أساسي وتطبيقي",
                    domains="العلوم الإنسانية، الفلسفة، المجتمع",
                    keywords="مجتمع، هوية، تراث، حداثة",
                    program_desc="مشروع بحثي يهدف إلى دراسة التحولات الاجتماعية والثقافية في المجتمع الجزائري.",
                    department_id=dept.id,
                )
                db.add(t1)
                db.commit()

            if not db.query(User).filter(User.username == d["user"]).first():
                db.add(User(
                    username=d["user"],
                    full_name=d["head"],
                    password_hash=pw_hash,
                    role="dept_head",
                    member_type="permanent",
                    department_id=d["id"],
                ))
                db.commit()

        if not db.query(User).filter(User.username == "admin").first():
            db.add(User(username="admin", full_name="المدير العام", password_hash=pw_hash, role="admin", member_type="admin"))
            db.commit()
    finally:
        db.close()
