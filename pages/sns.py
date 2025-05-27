import pandas as pd
import plotly.express as px
import streamlit as st

# CSV 파일 경로
file_path = "한국언론진흥재단_10대미디어이용통계_SNS 서비스별 이용률_20221231.csv",'cp=949'

# 데이터 불러오기 (한글 인코딩 처리)
df = pd.read_csv(file_path, encoding='cp949')

# 컬럼 이름 정리
df = df.rename(columns={"내 용": "SNS"})

# Streamlit 앱 제목
st.title("📱 10대 학생의 SNS 이용률 분석")

# 원본 데이터 표시
st.subheader("📋 원본 데이터")
st.dataframe(df)

# 데이터 변환: 학령별로 melt하여 long-form으로 변환
df_melted = df.melt(id_vars="SNS", var_name="학령", value_name="이용률")

# 전체 SNS 이용률 막대 그래프
st.subheader("📊 SNS별 학령 구분 이용률 비교")
fig = px.bar(
    df_melted,
    x="SNS",
    y="이용률",
    color="학령",
    barmode="group",
    title="SNS 서비스별 학령 구분 이용률 (%)",
    text_auto=True,
    height=500
)
st.plotly_chart(fig)

# 선택된 SNS의 학령별 이용률 파이차트
selected_sns = st.selectbox("🔍 특정 SNS를 선택해 학령별 이용률 보기", df["SNS"].unique())
filtered = df_melted[df_melted["SNS"] == selected_sns]
fig2 = px.pie(
    filtered,
    names="학령",
    values="이용률",
    title=f"{selected_sns} 이용률 구성비 (%)",
    hole=0.4
)
st.plotly_chart(fig2)
