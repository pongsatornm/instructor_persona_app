import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from io import BytesIO

# ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="Instructor Persona Self-Check", layout="wide")

st.title("Instructor Persona Self-Check")

st.markdown("""
**คำชี้แจง:**

กรุณาประเมินตัวเองในแต่ละหัวข้อโดยเลือกคะแนน 0–5  
(0 = ไม่เคยคิดในแง่นี้หรือไม่มีเลย, 5 = ตรงมากที่สุด)

เมื่อทำเสร็จ กดปุ่ม **Submit** เพื่อดูผลลัพธ์ของคุณทันที
""")

# กำหนดคำถามสำหรับแต่ละ Persona
questions = {
    "Cognitive Architect": [
        "ฉันสามารถจัดลำดับเนื้อหาในบทเรียนให้เข้าใจง่ายได้",
        "ฉันสามารถเชื่อมโยงแนวคิดต่าง ๆ ในบทเรียนได้อย่างมีระบบ",
        "ฉันสามารถออกแบบกิจกรรมเพื่อกระตุ้นการคิดวิเคราะห์ของนักศึกษา",
        "ฉันสามารถชี้นำให้นักศึกษาพัฒนาทักษะการคิดเชิงระบบได้ด้วยตนเอง",
        "ฉันสามารถประเมินและปรับปรุงโครงสร้างบทเรียนตามผลการเรียนรู้ของนักศึกษา"
    ],
    "Empathic Communicator": [
        "ฉันใส่ใจความรู้สึกของนักศึกษาในชั้นเรียน",
        "ฉันสามารถปรับการสื่อสารตามอารมณ์และความต้องการของนักศึกษา",
        "ฉันสามารถฟังและเข้าใจเบื้องหลังปัญหาของนักศึกษา",
        "ฉันสามารถใช้การสื่อสารเพื่อสร้างแรงบันดาลใจและการเติบโตทางอารมณ์ให้นักศึกษา",
        "ฉันสามารถประเมินผลกระทบของการสื่อสารของตนเองต่อความรู้สึกและพฤติกรรมของนักศึกษา"
    ],
    "Relevance Integrator": [
        "ฉันสามารถยกตัวอย่างที่สอดคล้องกับชีวิตประจำวันของนักศึกษา",
        "ฉันสามารถเชื่อมโยงความรู้กับประเด็นทางวิชาชีพได้",
        "ฉันสามารถออกแบบเนื้อหาที่ส่งเสริมความหมายในการเรียนรู้",
        "ฉันสามารถผลักดันให้นักศึกษาเห็นคุณค่าของการเรียนรู้เชิงลึกต่อชีวิตและอาชีพ",
        "ฉันสามารถประเมินและปรับปรุงเนื้อหาให้สอดคล้องกับบริบทและความต้องการของนักศึกษา"
    ],
    "Reflective Enabler": [
        "ฉันส่งเสริมให้นักศึกษาคิดทบทวนการเรียนรู้ของตนเอง",
        "ฉันสามารถตั้งคำถามกระตุ้นให้นักศึกษาค้นพบจุดแข็งและจุดอ่อนของตนเอง",
        "ฉันสามารถนำกระบวนการสะท้อนคิดไปเชื่อมโยงกับการพัฒนาวิชาชีพ",
        "ฉันสามารถปลูกฝังนิสัยการประเมินและพัฒนาตนเองอย่างต่อเนื่องให้นักศึกษา",
        "ฉันสามารถประเมินประสิทธิภาพของกระบวนการสะท้อนคิดที่ใช้ในการสอน"
    ],
    "Intrinsic Motivator": [
        "ฉันสามารถสร้างแรงจูงใจในการเรียนรู้โดยไม่ต้องใช้รางวัลภายนอก",
        "ฉันสามารถกระตุ้นความอยากรู้และความภาคภูมิใจในตนเองของนักศึกษา",
        "ฉันสามารถกระตุ้นให้นักศึกษาเรียนรู้เพราะเห็นคุณค่าในตัวความรู้เอง",
        "ฉันสามารถเสริมแรงให้นักศึกษาพัฒนาความมุ่งมั่นและความเพียรในระยะยาว",
        "ฉันสามารถประเมินและปรับกลยุทธ์การสร้างแรงจูงใจภายในให้เหมาะสมกับนักศึกษาแต่ละคน"
    ],
    "Educational Strategist": [
        "ฉันสามารถวางแผนการสอนอย่างมีระบบและยืดหยุ่น",
        "ฉันสามารถเลือกกลยุทธ์การสอนที่เหมาะสมกับเป้าหมายการเรียนรู้",
        "ฉันสามารถประเมินและปรับแผนการสอนตามสภาพจริงในชั้นเรียน",
        "ฉันสามารถพัฒนากลยุทธ์การสอนใหม่ ๆ เพื่อรองรับบริบทที่เปลี่ยนแปลง",
        "ฉันสามารถประเมินผลกระทบของกลยุทธ์การสอนที่ใช้ต่อผลการเรียนรู้ของนักศึกษา"
    ],
    "Systemic Challenger": [
        "ฉันสามารถตั้งคำถามให้นักศึกษาท้าทายกรอบความคิดเดิม ๆ",
        "ฉันสามารถผลักดันให้นักศึกษาตั้งข้อสงสัยต่อสิ่งที่เรียนรู้อย่างสร้างสรรค์",
        "ฉันสามารถกระตุ้นให้นักศึกษาเห็นความสัมพันธ์ของระบบที่ซับซ้อน",
        "ฉันสามารถส่งเสริมให้นักศึกษาเป็นผู้สร้างการเปลี่ยนแปลงในสังคมผ่านความรู้",
        "ฉันสามารถประเมินและปรับปรุงแนวทางการสอนเพื่อส่งเสริมการคิดเชิงระบบในนักศึกษา"
    ]
}

# กำหนดสี pastel สำหรับแต่ละ Persona
persona_colors = {
    "Cognitive Architect": "#AEC6CF",
    "Empathic Communicator": "#FFB347",
    "Relevance Integrator": "#77DD77",
    "Reflective Enabler": "#CBAACB",
    "Intrinsic Motivator": "#FDFD96",
    "Educational Strategist": "#FF6961",
    "Systemic Challenger": "#B39EB5"
}

# กำหนดสัญลักษณ์เฉพาะของแต่ละ Persona
persona_symbols = {
    "Cognitive Architect": "circle",
    "Empathic Communicator": "square",
    "Relevance Integrator": "diamond",
    "Reflective Enabler": "cross",
    "Intrinsic Motivator": "x",
    "Educational Strategist": "triangle-up",
    "Systemic Challenger": "star"
}

responses = {}

with st.form("persona_form"):
    for idx, (persona, qs) in enumerate(questions.items(), 1):
        st.subheader(f"Axis {idx}")
        for q_idx, q in enumerate(qs, 1):
            key = f"{persona}_Q{q_idx}"
            responses[key] = st.select_slider(
                q,
                options=[0, 1, 2, 3, 4, 5],
                value=0,
                key=key
            )
    submitted = st.form_submit_button("Submit")

if submitted:
    # คำนวณคะแนนรวม
    result = {}
    for persona in questions.keys():
        total = sum([responses[f"{persona}_Q{i}"] for i in range(1, 6)])
        result[persona] = total

    st.success("แบบสอบถามเสร็จสมบูรณ์!")

    # แสดงผลลัพธ์เป็นตาราง
    st.subheader("คะแนนรวมแต่ละ Persona")
    df_result = pd.DataFrame.from_dict(result, orient='index', columns=['คะแนนรวม']).reset_index()
    df_result.rename(columns={'index': 'Persona'}, inplace=True)
    st.dataframe(df_result, use_container_width=True)

    # วาด Radar Plot
    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=list(result.values()),
        theta=list(result.keys()),
        fill='toself',
        name='คะแนนของคุณ',
        line=dict(color='rgba(106,81,163,1)', width=2),
        marker=dict(
            size=8,
            color='rgba(106,81,163,1)',
            symbol=[persona_symbols[persona] for persona in result.keys()]
        )
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 25],
                tickfont=dict(size=10)
            ),
            angularaxis=dict(
                tickfont=dict(size=10)
            )
        ),
        showlegend=False,
        template='plotly_white'
    )

    st.plotly_chart(fig, use_container_width=True)

    # เพิ่มปุ่มดาวน์โหลดผลลัพธ์เป็นไฟล์ .xlsx
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df_result.to_excel(writer, index=False, sheet_name='ผลลัพธ์')
        writer.save()
        processed_data = output.getvalue()

    st.download_button(
        label="📄 ดาวน์โหลดผลลัพธ์เป็นไฟล์ Excel",
        data=processed_data,
        file_name="instructor_persona_results.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

st.markdown("---")
st.caption("Created by ChatGPT")
