import streamlit as st
import folium
from streamlit_folium import st_folium

# 페이지 설정
st.set_page_config(page_title="🇰🇷 한국인이 사랑한 Top 10 여행지", layout="wide")
st.title("💖 한국인이 가장 사랑하는 Top 10 여행지")
st.markdown("한국인의 마음을 사로잡은 여행지들을 소개합니다! 하트를 눌러 사랑을 표현해보세요 💌")

# 여행지 정보 (좌표 + 설명)
locations = [
    {"name": "서울", "lat": 37.5665, "lon": 126.9780, "desc": "과거와 현재가 공존하는 도시, 쇼핑과 먹거리가 가득!"},
    {"name": "부산", "lat": 35.1796, "lon": 129.0756, "desc": "해운대와 광안리, 그리고 맛있는 회까지! 바다의 매력 도시 💙"},
    {"name": "제주도", "lat": 33.4996, "lon": 126.5312, "desc": "한국의 하와이 🌴 감귤향 가득한 힐링 섬"},
    {"name": "경주", "lat": 35.8562, "lon": 129.2247, "desc": "천년의 고도, 유네스코 문화유산이 가득한 역사 도시"},
    {"name": "강릉", "lat": 37.7519, "lon": 128.8761, "desc": "바다와 커피, 그리고 감성 가득한 카페 거리 🌊☕"},
    {"name": "속초", "lat": 38.2049, "lon": 128.5912, "desc": "설악산과 바다, 자연을 모두 느낄 수 있는 도시 🌲"},
    {"name": "전주", "lat": 35.8242, "lon": 127.1479, "desc": "한옥마을과 전주비빔밥의 도시, 전통과 맛의 향연 🍱"},
    {"name": "인천", "lat": 37.4563, "lon": 126.7052, "desc": "차이나타운과 월미도의 도시, 공항도 있는 관문 도시 ✈️"},
    {"name": "여수", "lat": 34.7604, "lon": 127.6622, "desc": "밤바다의 도시 🎶 낭만 가득한 남해 여행지"},
    {"name": "남이섬", "lat": 37.7902, "lon": 127.5252, "desc": "사계절 내내 아름다운 섬, 드라마 명소 🌸❄️"}
]

# Folium 지도 생성
m = folium.Map(location=[36.5, 127.8], zoom_start=7, tiles="CartoDB positron")

# 마커 추가
for loc in locations:
    folium.Marker(
        location=[loc["lat"], loc["lon"]],
        popup=f"<b>{loc['name']}</b><br>{loc['desc']}",
        icon=folium.Icon(color="pink", icon="heart", prefix="fa"),
    ).add_to(m)

# Streamlit에 지도 표시
st_folium(m, width=900, height=600)
