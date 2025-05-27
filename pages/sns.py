import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="SNS 이용률 분석", layout="wide")

st.title("📊 10대 SNS 서비스 이용률 분석")
st.write("한국언론진흥재단 제공 데이터를 기반으로 학년별 SNS 이용률을 시각화합니다.")

# 파일 업로드
uploaded_file = st.file_uploader("CSV 파일을 업로드하세요", type=["csv"])
if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file, encoding='cp949')
    except UnicodeDecodeError:
        df = pd.read_csv(uploaded_file, encoding='utf-8')

    st.subheader("원본 데이터 미리보기")
    st.dataframe(df)

    # 데이터 전처리
    df_melted = df.melt(
        id_vars='SNS 종류',
        value_vars=['초등학생 이용현황', '중학생 이용현황', '고등학생 이용현황'],
        var_name='학년',
        value_name='이용률'
    )

    # Plotly 그래프
    fig = px.bar(
        df_melted,
        x='SNS 종류',
        y='이용률',
        color='학년',
        barmode='group',
        title='SNS 서비스별 학년별 이용률 비교'
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("왼쪽 사이드바 또는 위에서 CSV 파일을 업로드하면 분석이 시작됩니다.")
