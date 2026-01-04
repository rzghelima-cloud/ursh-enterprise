CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800&family=Tajawal:wght@400;500;700&display=swap');
html, body, .stApp { font-family: 'Tajawal', sans-serif; direction: rtl; text-align: right; }
h1, h2, h3, h4, h5 { font-family: 'Cairo'; font-weight: 800; text-align: right !important; }
[data-testid="stSidebar"] { background: #fff; border-left: 1px solid #e2e8f0; }
.stTextInput input, .stSelectbox div, .stTextArea textarea, .stDateInput input { text-align: right; direction: rtl; border-radius: 8px; font-family: 'Tajawal'; }
.stButton>button { width: 100%; border-radius: 8px; font-family: 'Cairo'; font-weight: bold; }
.kpi-container { background-color: white; padding: 14px 18px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.04); border: 1px solid #f1f5f9; border-right: 4px solid #3b82f6; display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; }
.kpi-value { font-family: 'Cairo'; font-size: 26px; font-weight: 800; color: #0f172a; }
.kpi-label { font-size: 13px; color: #64748b; font-weight: 600; }
.kpi-icon { width: 42px; height: 42px; background-color: #eff6ff; border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 20px; color: #3b82f6; }
.chart-container { background-color: white; padding: 16px; border-radius: 15px; border: 1px solid #e2e8f0; box-shadow: 0 2px 4px rgba(0,0,0,0.02); margin-bottom: 20px; }
.rtl-header { text-align: right; direction: rtl; width: 100%; display: block; font-family: 'Cairo'; font-weight: 700; color: #1f2937; margin-bottom: 10px; font-size: 18px; }
</style>
"""
