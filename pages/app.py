import streamlit as st
import pandas as pd
import plotly.express as px
import io

# Streamlit 설정
st.set_page_config(page_title="10대 SNS 대시보드", layout="wide")
st.title("📱 10대 학년별 SNS 이용률 분석 대시보드")

# 파일 업로드
uploaded_file = st.file_uploader("CSV 파일 업로드 (예: 한국언론진흥재단 SNS 통계)", type=["csv"])

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file, encoding='cp949')
    except:
        df = pd.read_csv(uploaded_file, encoding='utf-8')

    # 데이터 가공
    df_long = df.melt(id_vars='SNS 종류',
                      value_vars=['초등학생 이용현황', '중학생 이용현황', '고등학생 이용현황'],
                      var_name='학년', value_name='이용률')
    df_long['학년'] = df_long['학년'].str.replace(' 이용현황', '')
    df_long['사용자'] = df_long['학년'].map({
        '초등학생': '사용자 A',
        '중학생': '사용자 B',
        '고등학생': '사용자 C'
    })
    df_long['연도'] = [2020, 2021, 2022] * (len(df_long) // 3)

    df_long['카테고리'] = df_long['SNS 종류'].map({
        '인스타그램': '사진/영상 공유',
        '페이스북': '소셜 네트워크',
        '트위터': '마이크로블로그',
        '핀터레스트': '사진/영상 공유',
        '밴드': '커뮤니티',
        '틱톡': '짧은 영상',
        '카카오스토리': '소셜 네트워크'
    }).fillna('기타')

    # 필터
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

    filtered_df = df_long[
        df_long['SNS 종류'].isin(selected_sns) &
        df_long['사용자'].isin(selected_users)
    ]

    # 시계열 애니메이션
    st.subheader("📽 연도별 SNS 이용률 변화 (시계열 애니메이션)")
    fig_time = px.bar(
        filtered_df,
        x='SNS 종류',
        y='이용률',
        color='학년',
        animation_frame='연도',
        barmode='group',
        title='연도별 SNS 이용률 변화',
        range_y=[0, 100],
        text='이용률'
    )
    st.plotly_chart(fig_time, use_container_width=True)

    # 카테고리 분석
    st.subheader("🗂 SNS 유형(카테고리)별 이용률 분석")
    cat_summary = df_long.groupby('카테고리')['이용률'].mean().reset_index()
    fig_cat = px.pie(cat_summary, names='카테고리', values='이용률', title='SNS 카테고리별 평균 이용률')
    st.plotly_chart(fig_cat, use_container_width=True)

    # 사용자별 대시보드
    st.subheader("📈 사용자(학년)별 이용률 상세 대시보드")
    for user in selected_users:
        st.markdown(f"### 👤 {user}")
        user_df = filtered_df[filtered_df['사용자'] == user]
        chart = px.pie(user_df, names='SNS 종류', values='이용률', title=f"{user}의 SNS 선호도")
        chart.update_traces(textinfo='percent+label')
        st.plotly_chart(chart, use_container_width=True)

    # Excel 리포트 다운로드
    st.subheader("📁 리포트 다운로드")
    excel_buffer = io.BytesIO()
    with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='원본 데이터')
        df_long.to_excel(writer, index=False, sheet_name='가공 데이터')
        cat_summary.to_excel(writer, index=False, sheet_name='카테고리 분석')

    st.download_button(
        label="📊 Excel 리포트 다운로드",
        data=excel_buffer.getvalue(),
        file_name="SNS_분석_리포트.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    st.markdown("📄 PDF 보고서는 Plotly 차트를 PNG로 저장 후 [PDF 변환 도구](https://pdfcrowd.com/) 등을 활용하세요.")

else:
    st.info("먼저 CSV 파일을 업로드해주세요.")
