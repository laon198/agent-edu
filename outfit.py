import streamlit as st
import requests
import pandas as pd
import urllib.parse
import base64
from config import client

st.title("AI 날씨 코디 추천")


# -------------------------
# 세션 상태
# -------------------------
if "result" not in st.session_state:
    st.session_state.result = ""

if "search_keyword" not in st.session_state:
    st.session_state.search_keyword = ""


# -------------------------
# 도시 정보
# -------------------------
cities = {
    "서울": {"lat": 37.5665, "lon": 126.9780},
    "구미": {"lat": 36.1195, "lon": 128.3446},
    "부산": {"lat": 35.1796, "lon": 129.0756},
    "제주": {"lat": 33.4996, "lon": 126.5312},
}

city = st.selectbox(
    "도시를 선택하세요",
    list(cities.keys())
)

lat = cities[city]["lat"]
lon = cities[city]["lon"]


# -------------------------
# 날씨 API
# -------------------------
url = "https://api.open-meteo.com/v1/forecast"

params = {
    "latitude": lat,
    "longitude": lon,
    "current": "temperature_2m,wind_speed_10m",
    "hourly": "temperature_2m,wind_speed_10m,precipitation_probability",
    "timezone": "Asia/Seoul"
}

response = requests.get(url, params=params)
data = response.json()

current = data["current"]


# -------------------------
# 현재 날씨 표시
# -------------------------
st.subheader(f"{city} 현재 날씨")

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "현재 기온",
        f"{current['temperature_2m']}℃"
    )

with col2:
    st.metric(
        "풍속",
        f"{current['wind_speed_10m']} km/h"
    )


# -------------------------
# 시간별 날씨
# -------------------------
df = pd.DataFrame({
    "시간": data["hourly"]["time"][:24],
    "기온": data["hourly"]["temperature_2m"][:24],
    "풍속": data["hourly"]["wind_speed_10m"][:24],
    "강수확률": data["hourly"]["precipitation_probability"][:24],
})

df["시간"] = pd.to_datetime(df["시간"])
df["시간"] = df["시간"].dt.strftime("%H시")
df = df.set_index("시간")


# -------------------------
# 이미지 Base64 변환
# -------------------------
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(
            image_file.read()
        ).decode("utf-8")


# -------------------------
# 프롬프트 생성
# -------------------------
def make_prompt(weather_text):
    return f"""
당신은 패션 코디 전문가입니다.

사진 속 사용자의 옷차림을 분석하고,
현재 날씨에 적절한 코디인지 평가해주세요.

다음 내용을 포함해주세요.

1. 현재 코디 설명
2. 날씨에 적합한 점
3. 개선하면 좋은 점
4. 추천 아이템
5. 최종 코디 추천

날씨 정보:

{weather_text}

마지막 줄에는 반드시 다음 형식으로
추천 쇼핑 검색어 하나를 출력하세요.

SHOPPING_KEYWORD=검색어

예:
SHOPPING_KEYWORD=남성 겨울 패딩
"""


# -------------------------
# 날씨 문자열 생성
# -------------------------
def make_weather_text(city, current, df):
    return f"""
지역: {city}

현재 날씨:
- 현재 기온: {current['temperature_2m']}℃
- 현재 풍속: {current['wind_speed_10m']} km/h

오늘 시간별 날씨:
{df.to_string()}
"""


# -------------------------
# 검색어 추출
# -------------------------
def extract_search_keyword(result):
    for line in result.split("\n"):
        line = line.strip()

        if line.startswith("SHOPPING_KEYWORD="):
            return line.replace(
                "SHOPPING_KEYWORD=",
                ""
            ).strip()

    return "옷"


# -------------------------
# 쇼핑 링크
# -------------------------
def show_shopping_links(search_keyword):
    encoded = urllib.parse.quote(search_keyword)

    musinsa_url = (
        "https://www.musinsa.com/search/goods"
        f"?keyword={encoded}"
    )

    naver_url = (
        "https://search.shopping.naver.com/search/all"
        f"?query={encoded}"
    )

    st.subheader("🛍️ 쇼핑몰 검색")
    st.write("검색어:", search_keyword)

    col1, col2 = st.columns(2)

    with col1:
        st.link_button(
            "무신사 검색",
            musinsa_url,
            width="stretch"
        )

    with col2:
        st.link_button(
            "네이버 쇼핑 검색",
            naver_url,
            width="stretch"
        )


# -------------------------
# 고정 이미지
# -------------------------
image_path = "./assets/summer_look.png"

col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.image(
        image_path,
        caption="오늘의 코디",
        width="stretch"
    )

    evaluate_button = st.button(
        "AI 코디 평가 받기",
        width="stretch"
    )


# -------------------------
# AI 코디 평가
# -------------------------
if evaluate_button:

    weather_text = make_weather_text(
        city,
        current,
        df
    )

    prompt = make_prompt(weather_text)

    base64_image = encode_image(image_path)

    with st.spinner("AI가 코디를 평가하는 중입니다..."):

        ai_response = client.chat.completions.create(
            model="Qwen/Qwen2.5-VL-7B-Instruct",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url":
                                f"data:image/png;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ]
        )

        result = ai_response.choices[0].message.content

        st.session_state.result = result
        st.session_state.search_keyword = (
            extract_search_keyword(result)
        )


# -------------------------
# AI 결과 출력
# -------------------------
if st.session_state.result:

    st.subheader("🤖 AI 코디 평가 결과")

    st.write(
        st.session_state.result
    )


# -------------------------
# 쇼핑 링크 출력
# -------------------------
if st.session_state.search_keyword:

    show_shopping_links(
        st.session_state.search_keyword
    )