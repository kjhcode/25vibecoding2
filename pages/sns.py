import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="SNS 이용률 분석", layout="wide")

st.title("📱 10대 학년별 SNS 이용률 분석")
st.markdown("한국언론진흥재단 데이터를 기반으로 학년별 SNS 이용 트렌드를 시각화합니다.")

# 파일 업로드
uploaded_file = st.file_uploader("CSV 파일을 업로드하세요", type=["csv"])
if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file, encoding='cp949')
    except:
        df = pd.read_csv(uploaded_file, encoding='utf-8')

    st.subheader("🔍 원본 데이터 미리보기")
    st.dataframe(df)

    # 시각화
    st.subheader("📊 학년별 SNS 이용률 시각화")

    # 학년 컬럼과 색상 정의
    grades = ['초등학생 이용현황', '중학생 이용현황', '고등학생 이용현황']
    colors = ['#636EFA', '#EF553B', '#00CC96']

    # 그래프 객체 생성
    fig = go.Figure()

    for grade, color in zip(grades, colors):
        fig.add_trace(go.Bar(
            x=df['SNS 종류'],
            y=df[grade],
            name=grade.replace(' 이용현황', ''),
            marker_color=color,
            text=df[grade],
            textposition='auto',
            hovertemplate=f'%{{x}}<br>{grade}: %{{y}}%',
        ))

    fig.update_layout(
        title='10대 학년별 SNS 이용률 비교',
        xaxis_title='SNS 종류',
        yaxis_title='이용률 (%)',
        barmode='group',
        template='plotly_white',
        font=dict(family='Arial', size=14),
        title_font=dict(size=20),
        legend_title='학년',
        height=600
    )

    st.plotly_chart(fig, use_container_width=True)

else:
    st.info("먼저 CSV 파일을 업로드해주세요.")
