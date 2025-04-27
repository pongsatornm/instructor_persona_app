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
    "Cognitive Architect": [...],  # เติมเหมือนโค้ดต้นฉบับได้เลย
    "Empathic Communicator": [...],
    "Relevance Integrator": [...],
    "Reflective Enabler": [...],
    "Intrinsic Motivator": [...],
    "Educational Strategist": [...],
    "Systemic Challenger": [...]
}

# สี pastel แต่ละ Persona
persona_colors = {
    "Cognitive Architect": "#AEC6CF",
    "Empathic Communicator": "#FFB347",
    "Relevance Integrator": "#77DD77",
    "Reflective Enabler": "#CBAACB",
    "Intrinsic Motivator": "#FDFD96",
    "Educational Strategist": "#FF6961",
    "Systemic Challenger": "#B39EB5"
}

# สัญลักษณ์แต่ละ Persona
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

# รับข้อมูลผู้ใช้
with st.form("persona_form"):
    for idx, (persona, qs) in enumerate(questions.items(), 1):
        st.subheader(f"Axis {idx}: {persona}")
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

    for persona in result.keys():
        fig.add_trace(go.Scatterpolar(
            r=[result[persona]] * len(result),
            theta=list(result.keys()),
            name=persona,
            marker=dict(
                color=persona_colors[persona],
                symbol=persona_symbols[persona],
                size=10,
                line=dict(width=1)
            ),
            line=dict(color=persona_colors[persona], width=2),
            mode='markers+lines'
        ))

    fig.update_layout(
        polar=dict(
            bgcolor="rgba(255,255,255,0)",
            radialaxis=dict(
                visible=True,
                range=[0, 25],
                showline=True,
                linewidth=1,
                gridcolor="lightgrey",
                gridwidth=0.5,
                tickfont=dict(size=10)
            ),
            angularaxis=dict(
                tickfont=dict(size=10),
                gridcolor="lightgrey",
                gridwidth=0.5
            )
        ),
        showlegend=True,
        legend=dict(
            title="Persona",
            orientation="h",
            yanchor="bottom",
            y=-0.3,
            xanchor="center",
            x=0.5
        ),
        template='plotly_white'
    )

    st.plotly_chart(fig, use_container_width=True)

    # ดาวน์โหลดผลลัพธ์เป็น Excel
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df_result.to_excel(writer, index=False, sheet_name='ผลลัพธ์')
    processed_data = output.getvalue()

    st.download_button(
        label="📄 ดาวน์โหลดผลลัพธ์เป็นไฟล์ Excel",
        data=processed_data,
        file_name="instructor_persona_results.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

st.markdown("---")
st.caption("Created by ChatGPT")
