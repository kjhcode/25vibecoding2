import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.title("🧭 연령별 인구 시각화 대시보드")

# 1. 사용자 파일 업로드
mf_file = st.file_uploader("📄 남녀구분 인구 CSV 파일 업로드", type="csv", key="mf")
total_file = st.file_uploader("📄 남녀합계 인구 CSV 파일 업로드", type="csv", key="total")

if mf_file is not None and total_file is not None:
    # 2. CSV 읽기
    mf_df = pd.read_csv(mf_file, encoding='cp949')
    total_df = pd.read_csv(total_file, encoding='cp949')

    # 3. 컬럼 공백 제거
    mf_df.columns = mf_df.columns.str.strip()
    total_df.columns = total_df.columns.str.strip()

    # 4. 연령 관련 컬럼 추출
    age_cols_mf = [col for col in mf_df.columns if "세" in col]
    age_cols_total = [col for col in total_df.columns if "세" in col]

    # 5. 숫자형으로 변환
    def clean_numeric(df, cols):
        for col in cols:
            if df[col].dtype == object:
                df[col] = df[col].str.replace(",", "").astype(int)
        return df

    mf_df = clean_numeric(mf_df, age_cols_mf)
    total_df = clean_numeric(total_df, age_cols_total)

    # 6. 지역명 추출
    mf_df['지역'] = mf_df['행정구역'].str.extract(r"([\uAC00-\uD7AF\s]+구|\w+시|\w+군|\w+읍|\w+면)")
    region_options = mf_df['지역'].dropna().unique().tolist()
    region_options.sort()

    # 7. UI 탭 구성
    tab1, tab2 = st.tabs(["👫 남녀 인구 피라미드", "👥 전체 인구 구조"])

    # 탭 1 - 남녀 인구 피라미드
    with tab1:
        region = st.selectbox("지역 선택 (남녀 피라미드)", region_options, key="tab1")
        filtered = mf_df[mf_df['지역'] == region]

        if not filtered.empty:
            male_cols = [col for col in age_cols_mf if "_남_" in col]
            female_cols = [col for col in age_cols_mf if "_여_" in col]
            age_labels = [col.split("_")[-1] for col in male_cols]

            male = filtered.iloc[0][male_cols].values * -1  # 좌측 대칭
            female = filtered.iloc[0][female_cols].values

            fig = go.Figure()
            fig.add_trace(go.Bar(x=male, y=age_labels, orientation='h', name='남성', marker_color='blue'))
            fig.add_trace(go.Bar(x=female, y=age_labels, orientation='h', name='여성', marker_color='red'))

            fig.update_layout(
                title=f"{region} 인구 피라미드",
                barmode='relative',
                xaxis=dict(title='인구 수', tickvals=[-2000, 0, 2000]),
                yaxis=dict(title='연령'),
                height=700
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("해당 지역 데이터가 없습니다.")

    # 탭 2 - 전체 인구 구조
    with tab2:
        region2 = st.selectbox("지역 선택 (전체 인구)", region_options, key="tab2")
        filtered2 = total_df[total_df['행정구역'].str.contains(region2)]

        if not filtered2.empty:
            age_labels = [col.split("_")[-1] for col in age_cols_total]
            total_pop = filtered2.iloc[0][age_cols_total].values

            fig2 = go.Figure()
            fig2.add_trace(go.Scatter(x=age_labels, y=total_pop, mode='lines+markers', name='총인구'))
            fig2.update_layout(
                title=f"{region2} 연령별 인구 구조",
                xaxis_title='연령',
                yaxis_title='인구 수',
                height=600
            )
            st.plotly_chart(fig2, use_container_width=True)
        else:
            st.warning("해당 지역 데이터가 없습니다.")
else:
    st.info("좌측 상단에서 두 개의 CSV 파일을 모두 업로드해 주세요.")
