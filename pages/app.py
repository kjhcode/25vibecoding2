import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="10대 SNS 대시보드", layout="wide")

st.title("📱 10대 학년별 SNS 이용률 분석 대시보드")

# CSV 파일 업로드
uploaded_file = st.file_uploader("CSV 파일 업로드 (예: 한국언론진흥재단 SNS 통계)", type=["csv"])
if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file, encoding='cp949')
    except:
        df = pd.read_csv(uploaded_file, encoding='utf-8')

    # 데이터 전처리
    df_long = df.melt(id_vars='SNS 종류',
                      value_vars=['초등학생 이용현황', '중학생 이용현황', '고등학생 이용현황'],
                      var_name='학년',
                      value_name='이용률')

    df_long['학년'] = df_long['학년'].str.replace(' 이용현황', '')
    df_long['사용자'] = df_long['학년'].map({
        '초등학생': '사용자 A',
        '중학생': '사용자 B',
        '고등학생': '사용자 C'
    })

    # ===== 사이드바 필터 =====
    st.sidebar.header("📌 필터")
    
    selected_sns = st.sidebar.multiselect(
        "보고 싶은 SNS 종류 선택", 
        options=df_long['SNS 종류'].unique(),
        default=list(df_long['SNS 종류'].unique())
    )

    selected_users = st.sidebar.multiselect(
        "사용자(학년) 선택",
        options=df_long['사용자'].unique(),
        default=list(df_long['사용자'].unique())
    )

    # 필터 적용
    filtered_df = df_long[
        df_long['SNS 종류'].isin(selected_sns) &
        df_long['사용자'].isin(selected_users)
    ]

    # ===== 애니메이션 시각화 =====
    st.subheader("📊 학년(사용자)별 SNS 이용률 애니메이션")
    fig = px.bar(
        filtered_df,
        x="SNS 종류",
        y="이용률",
        color="SNS 종류",
        animation_frame="사용자",
        range_y=[0, 100],
        title="학년별 SNS 이용률 (애니메이션)",
        text="이용률"
    )

    fig.update_layout(
        xaxis_title="SNS 종류",
        yaxis_title="이용률 (%)",
        title_font_size=20,
        legend_title="SNS",
        font=dict(size=14),
        template="plotly_white",
        height=600
    )
    st.plotly_chart(fig, use_container_width=True)

    # ===== 사용자별 대시보드 =====
    st.subheader("📈 사용자(학년)별 이용률 상세 대시보드")
    for user in selected_users:
        st.markdown(f"### 👤 {user}")
        user_df = filtered_df[filtered_df['사용자'] == user]
        chart = px.pie(user_df, names='SNS 종류', values='이용률', title=f"{user}의 SNS 선호도")
        chart.update_traces(textinfo='percent+label')
        st.plotly_chart(chart, use_container_width=True)

else:
    st.info("먼저 CSV 파일을 업로드해주세요.")
