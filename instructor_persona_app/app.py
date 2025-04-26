import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Instructor Persona Self-Check", layout="wide")

st.title("Instructor Persona Self-Check")

st.markdown("""
โปรดประเมินตนเองในแต่ละข้อ โดยใช้คะแนนดังนี้:
- 0: ไม่เคยคิดในแง่นี้ หรือไม่มี
- 1: น้อย
- 2: ปานกลาง
- 3: มาก
""")

questions = {
    "Axis 1": [
        "ฉันสามารถอธิบายเนื้อหาได้อย่างชัดเจน",
        "ฉันสามารถใช้ตัวอย่างเพื่อเสริมความเข้าใจ",
        "ฉันสามารถตอบคำถามของผู้เรียนได้อย่างมั่นใจ",
        "ฉันสามารถจัดการเวลาในการสอนได้อย่างมีประสิทธิภาพ",
        "ฉันสามารถประเมินผลการเรียนรู้ของผู้เรียนได้"
    ],
    "Axis 2": [
        "ฉันสามารถเชื่อมโยงความรู้กับประเด็นทางวิชาชีพได้",
        "ฉันสามารถนำเทคโนโลยีมาใช้ในการสอน",
        "ฉันสามารถปรับเนื้อหาให้เหมาะสมกับผู้เรียน",
        "ฉันสามารถใช้วิธีการสอนที่หลากหลาย",
        "ฉันสามารถสร้างกิจกรรมที่ส่งเสริมการเรียนรู้"
    ],
    "Axis 3": [
        "ฉันสามารถสะท้อนผลการสอนของตนเอง",
        "ฉันสามารถปรับปรุงการสอนจากผลสะท้อน",
        "ฉันสามารถรับฟังความคิดเห็นจากผู้เรียน",
        "ฉันสามารถวางแผนพัฒนาตนเองในอนาคต",
        "ฉันสามารถแบ่งปันประสบการณ์กับเพื่อนร่วมงาน"
    ]
}

scores = {}
total_scores = {}

for axis, qs in questions.items():
    st.subheader(axis)
    scores[axis] = []
    for q in qs:
        score = st.slider(q, 0, 3, 0, key=q)
        scores[axis].append(score)
    total_scores[axis] = sum(scores[axis])

if st.button("แสดงผลการประเมิน"):
    df = pd.DataFrame({
        "Persona": list(total_scores.keys()),
        "คะแนนรวม": list(total_scores.values())
    })

    fig = px.line_polar(df, r="คะแนนรวม", theta="Persona", line_close=True)
    st.plotly_chart(fig)
