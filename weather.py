import streamlit as st
import requests
import pandas as pd

st.title("날씨 대시보드")

cities = {
    "서울": {"lat": 37.5665, "lon": 126.9780},
    "구미": {"lat": 36.1195, "lon": 128.3446},
    "김천": {"lat": 36.1398, "lon": 128.1136},
    "칠곡": {"lat": 35.9953, "lon": 128.4017},
    "부산": {"lat": 35.1796, "lon": 129.0756},
    "제주": {"lat": 33.4996, "lon": 126.5312},
}

city = st.selectbox(
    "도시를 선택하세요",
    list(cities.keys())
)

lat = cities[city]["lat"]
lon = cities[city]["lon"]

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

st.subheader(f"{city} 현재 날씨")

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "현재 기온",
        f"{current['temperature_2m']}°C"
    )

with col2:
    st.metric(
        "풍속",
        f"{current['wind_speed_10m']} km/h"
    )

st.subheader("시간별 날씨 변화")

df = pd.DataFrame({
    "시간": data["hourly"]["time"][:24],
    "기온": data["hourly"]["temperature_2m"][:24],
    "풍속": data["hourly"]["wind_speed_10m"][:24],
    "강수확률": data["hourly"]["precipitation_probability"][:24],
})

df["시간"] = pd.to_datetime(df["시간"])
df["시간"] = df["시간"].dt.strftime("%H시")

# 시간별 기온 변화 그래프
st.subheader("시간별 기온 변화")

st.line_chart(
    df,
    x="시간",
    y="기온"
)

# 데이터 표
st.dataframe(df)