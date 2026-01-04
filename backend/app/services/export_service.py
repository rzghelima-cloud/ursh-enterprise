import io, json
import pandas as pd

def works_to_excel(df: pd.DataFrame) -> bytes:
    output = io.BytesIO()
    export_df = df.copy()

    if "details" in export_df.columns:
        def fmt_details(x):
            try:
                d = json.loads(x) if x else {}
                parts = [f"{k}:{v}" for k, v in d.items() if v not in (None, "", [], {})]
                return " | ".join(parts)
            except Exception:
                return ""
        export_df["تفاصيل"] = export_df["details"].apply(fmt_details)

    cols_map = {
        "title": "العنوان",
        "activity_type": "النوع",
        "publication_date": "التاريخ",
        "points": "النقاط",
        "researcher": "الباحث",
        "team": "الفرقة",
        "department": "القسم",
    }
    export_df = export_df.rename(columns=cols_map)
    final_cols = [c for c in cols_map.values() if c in export_df.columns]
    if "تفاصيل" in export_df.columns:
        final_cols.append("تفاصيل")
    export_df = export_df[final_cols] if not export_df.empty else export_df

    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        export_df.to_excel(writer, index=False, sheet_name="التقرير")
    return output.getvalue()
