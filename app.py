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

    # 사이드바에서 학년 선택
    st.sidebar.header("📌 학년 필터")
    grade_options = {
        '초등학생': '초등학생 이용현황',
        '중학생': '중학생 이용현황',
        '고등학생': '고등학생 이용현황'
    }
    selected_grades = st.sidebar.multiselect(
        "보고 싶은 학년을 선택하세요",
        options=list(grade_options.keys()),
        default=list(grade_options.keys())
    )

    # 선택된 학년에 따라 필터링
    selected_columns = [grade_options[grade] for grade in selected_grades]

    # 색상 지정
    color_map = {
        '초등학생 이용현황': '#636EFA',
        '중학생 이용현황': '#EF553B',
        '고등학생 이용현황': '#00CC96'
    }

    # 그래프 생성
    fig = go.Figure()

    for column in selected_columns:
        fig.add_trace(go.Bar(
            x=df['SNS 종류'],
            y=df[column],
            name=column.replace(" 이용현황", ""),
            marker_color=color_map[column],
            text=df[column],
            textposition='auto',
            hovertemplate=f'%{{x}}<br>{column}: %{{y}}%',
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

    st.subheader("📊 선택한 학년의 SNS 이용률")
    st.plotly_chart(fig, use_container_width=True)

else:
    st.info("먼저 CSV 파일을 업로드해주세요.")
