import streamlit as st

# 페이지 설정
st.set_page_config(page_title="🧭 MBTI 여행 추천기", page_icon="🌍", layout="wide")

# 제목
st.title("🌟 나에게 딱 맞는 여행지 찾기!")
st.markdown("당신의 **MBTI**를 선택하면, ✨성격에 맞는 여행 코스를 추천해드릴게요!")

# MBTI 선택
mbti_list = [
    "INTJ", "INTP", "ENTJ", "ENTP",
    "INFJ", "INFP", "ENFJ", "ENFP",
    "ISTJ", "ISFJ", "ESTJ", "ESFJ",
    "ISTP", "ISFP", "ESTP", "ESFP"
]
mbti = st.selectbox("🧠 나의 MBTI는?", mbti_list)

# 추천 여행지 함수
def recommend_trip(mbti_type):
    group = mbti_type[:2]
    if group in ["IN", "IS"]:
        return {
            "장소": "📚 교토, 일본",
            "추천": "조용한 사찰과 정원 속에서 사색과 힐링을 즐겨보세요 🍵🌸",
            "테마": "혼자만의 여유로운 시간"
        }
    elif group in ["EN", "ES"]:
        return {
            "장소": "🎉 바르셀로나, 스페인",
            "추천": "유쾌한 거리 예술과 열정적인 플라멩코! 사람들과 어울리기 딱이죠 💃🕺",
            "테마": "사람들과 어우러지는 열정 여행"
        }
    elif group.startswith("IT"):
        return {
            "장소": "🏕️ 캐나다 로키산맥",
            "추천": "대자연 속 캠핑과 액티비티! 스릴과 모험이 넘치는 코스 ⛺🛶",
            "테마": "모험과 도전의 여행"
        }
    elif group.startswith("EF"):
        return {
            "장소": "🏖️ 세부, 필리핀",
            "추천": "바닷가에서 휴식하며 다양한 액티비티도 함께! 🌊🐠",
            "테마": "재충전과 즐거움 가득한 리조트 여행"
        }
    else:
        return {
            "장소": "🏞️ 프라하, 체코",
            "추천": "고즈넉한 골목길과 감성적인 야경, 잔잔한 음악이 흐르는 도시 🌆🎻",
            "테마": "감성 충전 힐링 여행"
        }

# 결과 출력
if mbti:
    result = recommend_trip(mbti)
    st.balloons()
    st.subheader(f"🌈 {mbti} 유형에게 추천하는 여행지는...")
    st.success(f"🚩 여행지: **{result['장소']}**")
    st.info(f"✨ 추천 포인트: {result['추천']}")
    st.warning(f"🧳 여행 테마: {result['테마']}")

# 푸터
st.markdown("---")
st.caption("💡 여행지는 MBTI 특성을 바탕으로 센스 있게 제안되었어요. 실제 취향과 다를 수도 있어요 :)")
