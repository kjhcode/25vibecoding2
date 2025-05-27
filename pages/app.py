import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="10대 SNS 이용률 분석", layout="wide")

st.title("📱 10대 학년별 SNS 이용률 분석")
st.markdown("한국언론진흥재단 데이터를 기반으로 학년별 SNS 이용 트렌드를 분석하고 시각화합니다.")

# 파일 업로드
uploaded_file = st.file_uploader("CSV 파일을 업로드하세요", type=["csv"])
if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file, encoding='cp949')
    except:
        df = pd.read_csv(uploaded_file, encoding='utf-8')

    st.subheader("🔍 원본 데이터 미리보기")
    st.dataframe(df)

    # ==== 사이드바 옵션 ====
    st.sidebar.header("📌 시각화 옵션")

    # 학년 필터
    grade_options = {
        '초등학생': '초등학생 이용현황',
        '중학생': '중학생 이용현황',
        '고등학생': '고등학생 이용현황'
    }
    selected_grades = st.sidebar.multiselect(
        "학년 선택",
        options=list(grade_options.keys()),
        default=list(grade_options.keys())
    )
    selected_columns = [grade_options[g] for g in selected_grades]

    # 차트 유형 선택
    chart_type = st.sidebar.radio("차트 유형", ["막대그래프", "라인차트"])

    # 정렬 옵션
    sort_order = st.sidebar.radio("SNS 정렬 기준", ["원래 순서", "이용률 순 정렬 (평균 기준)"])
    if sort_order == "이용률 순 정렬 (평균 기준)":
        df['이용률 평균'] = df[selected_columns].mean(axis=1)
        df = df.sort_values(by='이용률 평균', ascending=False)

    # ==== 그래프 시각화 ====
    st.subheader("📊 선택한 조건에 따른 SNS 이용률 시각화")

    colors = {
        '초등학생 이용현황': '#636EFA',
        '중학생 이용현황': '#EF553B',
        '고등학생 이용현황': '#00CC96'
    }

    fig = go.Figure()

    for col in selected_columns:
        if chart_type == "막대그래프":
            fig.add_trace(go.Bar(
                x=df['SNS 종류'],
                y=df[col],
                name=col.replace(" 이용현황", ""),
                marker_color=colors[col],
                text=df[col],
                textposition='auto',
                hovertemplate=f'%{{x}}<br>{col}: %{{y}}%',
            ))
        elif chart_type == "라인차트":
            fig.add_trace(go.Scatter(
                x=df['SNS 종류'],
                y=df[col],
                name=col.replace(" 이용현황", ""),
                marker_color=colors[col],
                mode='lines+markers',
                line=dict(width=3),
                hovertemplate=f'%{{x}}<br>{col}: %{{y}}%',
            ))

    fig.update_layout(
        title='10대 학년별 SNS 이용률 비교',
        xaxis_title='SNS 종류',
        yaxis_title='이용률 (%)',
        barmode='group' if chart_type == "막대그래프" else None,
        template='plotly_white',
        font=dict(family='Arial', size=14),
        title_font=dict(size=20),
        legend_title='학년',
        height=600
    )

    st.plotly_chart(fig, use_container_width=True)

    # ==== PDF 저장 ====
    st.markdown("📥 차트를 저장하고 싶다면 아래 버튼을 클릭하세요:")
    st.download_button(
        label="📄 차트 PNG로 저장",
        data=fig.to_image(format="png"),
        file_name="sns_usage_chart.png",
        mime="image/png"
    )

else:
    st.info("먼저 CSV 파일을 업로드해주세요.")
