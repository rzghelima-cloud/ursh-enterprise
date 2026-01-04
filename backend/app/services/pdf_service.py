import os
import requests
import arabic_reshaper
from bidi.algorithm import get_display
from fpdf import FPDF

from app.core.constants import MEMBER_TYPES

FONT_NAME = "Amiri"
FONT_FILE = "Amiri-Regular.ttf"
FONT_URL = "https://github.com/google/fonts/raw/main/ofl/amiri/Amiri-Regular.ttf"

def ensure_font_exists(font_path: str) -> str | None:
    if os.path.exists(font_path):
        return font_path
    try:
        r = requests.get(FONT_URL, timeout=10)
        if r.status_code == 200:
            with open(font_path, "wb") as f:
                f.write(r.content)
            return font_path
    except Exception:
        pass
    return None

def process_ar(text: str) -> str:
    if not text:
        return ""
    try:
        reshaped = arabic_reshaper.reshape(str(text))
        return get_display(reshaped)
    except Exception:
        return str(text)

class PDF(FPDF):
    def header(self):
        return
    def footer(self):
        self.set_y(-15)
        try:
            self.set_font(FONT_NAME, "", 8)
        except Exception:
            self.set_font("helvetica", "", 8)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")

def generate_cv_pdf(full_name: str, member_type: str, role: str, org_label: str, works_df) -> bytes:
    # Place font in current working directory (container /app)
    font_path = ensure_font_exists(FONT_FILE)
    pdf = PDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    if font_path:
        pdf.add_font(FONT_NAME, "", font_path)
        pdf.add_page()
        pdf.set_font(FONT_NAME, "", 18)
        pdf.cell(0, 10, process_ar(f"السيرة الذاتية الأكاديمية: {full_name}"),
                 new_x="LMARGIN", new_y="NEXT", align="C")
        pdf.ln(5)

        pdf.set_font(FONT_NAME, "", 11)
        role_str = MEMBER_TYPES.get(member_type, role) or "غير محدد"
        pdf.cell(0, 6, process_ar(f"الصفة: {role_str}"), new_x="LMARGIN", new_y="NEXT", align="R")
        pdf.cell(0, 6, process_ar(f"الهيكل: {org_label}"), new_x="LMARGIN", new_y="NEXT", align="R")
        pdf.ln(8)

        pdf.set_font(FONT_NAME, "", 14)
        pdf.cell(0, 10, process_ar("قائمة الأنشطة والنتاجات العلمية"),
                 new_x="LMARGIN", new_y="NEXT", align="R")
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(5)

        if works_df is not None and not works_df.empty:
            df_sorted = works_df.sort_values(by=["activity_type", "year"], ascending=[True, False])
            current_type = None

            for _, row in df_sorted.iterrows():
                if row["activity_type"] != current_type:
                    current_type = row["activity_type"]
                    if pdf.get_y() > 250:
                        pdf.add_page()
                    else:
                        pdf.ln(3)
                    pdf.set_font(FONT_NAME, "", 13)
                    pdf.set_text_color(30, 60, 140)
                    pdf.set_x(10)
                    pdf.cell(190, 8, process_ar(f"• {current_type}"), ln=True, align="R")

                pdf.set_text_color(0, 0, 0)
                pdf.set_font(FONT_NAME, "", 11)
                title = str(row.get("title", ""))
                d = str(row.get("publication_date", ""))
                txt = process_ar(f"- {title} ({d})")
                pdf.set_x(10)
                pdf.multi_cell(190, 6, txt, align="R")
        else:
            pdf.set_font(FONT_NAME, "", 12)
            pdf.set_x(10)
            pdf.cell(190, 10, process_ar("لا توجد أعمال مسجلة حتى الآن."), ln=True, align="R")

        return bytes(pdf.output())
    else:
        # Fallback English-only if font unavailable
        pdf.add_page()
        pdf.set_font("helvetica", "", 12)
        pdf.cell(0, 10, "Arabic font not loaded.", ln=True)
        return bytes(pdf.output())
