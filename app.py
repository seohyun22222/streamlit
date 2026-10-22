import pandas as pd
import streamlit as st

# 페이지 기본 설정
st.set_page_config(
    page_title="맞춤형 여행지 추천 앱", page_icon="✈️", layout="wide"
)

# 1. 샘플 여행지 데이터 구축
data = {
    "이름": [
        "제주도 서귀포",
        "강원도 강릉",
        "부산 해운대",
        "교토 (일본)",
        "파리 (프랑스)",
        "치앙마이 (태국)",
    ],
    "카테고리": [
        "힐링/휴식",
        "미식 탐방",
        "액티비티",
        "역사/문화",
        "역사/문화",
        "힐링/휴식",
    ],
    "예산": ["중간", "저예산", "중간", "중간", "고예산", "저예산"],
    "동행자": ["연인", "친구", "친구", "혼자", "연인", "혼자"],
    "설명": [
        "푸른 바다와 올레길, 따뜻한 남쪽의 여유를 즐길 수 있는 힐링 여행지",
        "초당순두부와 안목해변 커피거리, 탁 트인 동해 바다가 있는 미식의 도시",
        "시원한 해수욕장과 화려한 야경, 다양한 해양 레포츠를 즐길 수 있는 곳",
        "고즈넉한 사찰과 전통 가옥, 차분하게 사색하기 좋은 역사·문화 도시",
        "낭만이 가득한 예술과 미식의 도시, 에펠탑과 박물관이 기다리는 곳",
        "여유로운 카페 문화와 저렴한 물가, 디지털 노마드의 천국",
    ],
    "아이콘": ["🌴", "☕", "🌊", "⛩️", "🗼", "🥥"],
}

df = pd.DataFrame(data)

# 앱 타이틀 및 설명
st.title("✈️ 나의 성향에 딱 맞는 여행지 추천 앱")
st.markdown(
    "사이드바에서 원하는 **여행 스타일, 예산, 동행자**를 선택하시면 알맞은 여행지를 추천해 드립니다!"
)

# 2. 사이드바 필터 구성
st.sidebar.header("🔍 여행 취향 설정")

selected_category = st.sidebar.selectbox(
    "1. 여행 스타일", ["전체", "힐링/휴식", "액티비티", "역사/문화", "미식 탐방"]
)
selected_budget = st.sidebar.selectbox(
    "2. 예산 수준", ["전체", "저예산", "중간", "고예산"]
)
selected_companion = st.sidebar.selectbox(
    "3. 동행자", ["전체", "혼자", "친구", "연인", "가족"]
)

# 3. 필터링 로직 적용
filtered_df = df.copy()

if selected_category != "전체":
    filtered_df = filtered_df[filtered_df["카테고리"] == selected_category]

if selected_budget != "전체":
    filtered_df = filtered_df[filtered_df["예산"] == selected_budget]

if selected_companion != "전체":
    # 동행자가 '전체'가 아닐 경우 정확히 일치하거나 유연하게 매칭
    filtered_df = filtered_df[
        (filtered_df["동행자"] == selected_companion)
        | (filtered_df["동행자"] == "친구")
    ]

# 4. 결과 출력 섹션
st.markdown("---")
st.subheader(f"🎯 추천 결과 (총 {len(filtered_df)}개의 여행지)")

if filtered_df.empty:
    st.warning(
        "💡 조건에 정확히 일치하는 여행지가 없습니다. 필터를 조금 더 넓혀보세요!"
    )
else:
    for index, row in filtered_df.iterrows():
        with st.container():
            col1, col2 = st.columns([1, 6])
            with col1:
                st.markdown(
                    f"<h1 style='text-align: center; font-size: 60px;'>{row['아이콘']}</h1>",
                    unsafe_allow_html=True,
                )
            with col2:
                st.markdown(f"### {row['이름']}")
                st.markdown(
                    f"🏷️ **스타일:** {row['카테고리']} &nbsp;|&nbsp; 💰 **예산:** {row['예산']} &nbsp;|&nbsp; 👥 **추천 동행:** {row['동행자']}"
                )
                st.write(row["설명"])
            st.markdown("---")

# 5. 하단 부가 기능 (즐겨찾기 저장 예시)
st.sidebar.markdown("---")
st.sidebar.info("💡 **팁:** 마음에 드는 여행지를 찜해 나만의 여행 계획을 세워보세요!")
