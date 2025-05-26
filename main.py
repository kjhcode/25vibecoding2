import streamlit as st
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="나만의 위치 지도", layout="centered")

st.title("🗺️ 나만의 위치 북마크 지도")
st.write("아래에 장소 정보를 입력하고 버튼을 눌러 지도에 마커를 추가해보세요!")

# 📍 장소 입력
place = st.text_input("장소 이름", value="광주동신여자고등학교")
lat = st.number_input("위도 (Latitude)", value=35.161361, format="%.6f")
lon = st.number_input("경도 (Longitude)", value=126.881795, format="%.6f")

# 💾 세션 상태에 마커 저장
if "places" not in st.session_state:
    st.session_state.places = []

# ➕ 마커 추가
if st.button("지도에 추가하기"):
    st.session_state.places.append((place, lat, lon))
    st.success(f"{place} 위치가 지도에 추가되었습니다.")

# ❌ 마커 전체 삭제
if st.button("모든 마커 지우기"):
    st.session_state.places = []
    st.warning("모든 마커가 삭제되었습니다.")

# 🗺️ 지도 그리기 (최근 입력 위치를 중심으로)
if st.session_state.places:
    last_location = st.session_state.places[-1]
    m = folium.Map(location=[last_location[1], last_location[2]], zoom_start=13)
else:
    m = folium.Map(location=[35.161361, 126.881795], zoom_start=6)

# 모든 마커 추가
for name, lat, lon in st.session_state.places:
    folium.Marker(
        [lat, lon],
        tooltip=name,
        popup=f"<b>{name}</b><br>위도: {lat}<br>경도: {lon}"
    ).add_to(m)

# 📌 Folium 지도 출력
st.subheader("📍 지도 보기")
st_folium(m, width=700, height=500)
