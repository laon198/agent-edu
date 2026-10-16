import streamlit as st
import base64
from urllib.parse import quote
from config import client

# -------------------------
# 이미지 Base64 변환
# -------------------------
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(
            image_file.read()
        ).decode("utf-8")

# -------------------------
# 세션 상태 초기화
# -------------------------
if "ai_result" not in st.session_state:
    st.session_state.ai_result = None

# -------------------------
# 화면 구성
# -------------------------
st.title("🍳 AI 레시피 추천")

image_path = "./assets/ingredents.png"

col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.image(image_path, caption="오늘의 식재료")
    recipe_button = st.button("레시피 요청", width="stretch")

# -------------------------
# 레시피 요청 버튼 클릭
# -------------------------
if recipe_button:
    base64_image = encode_image(image_path)

    with st.spinner("AI가 식재료를 분석하고 있습니다..."):
        response = client.chat.completions.create(
            model="Qwen/Qwen2.5-VL-7B-Instruct",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text":
                            "1. 이 사진 속 음식재료를 인식 "
                            "2. 그 재료로 만들 수 있는 메뉴를 세 개 추천"
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ]
        )
    st.session_state.ai_result = response.choices[0].message.content
# -------------------------
# AI 결과가 있으면 계속 보여주기
# -------------------------
if st.session_state.ai_result is not None:
    st.subheader("🤖 AI 분석 결과")
    st.write(st.session_state.ai_result)
    st.divider()

    menu = st.text_input(
        "찾고 싶은 메뉴를 입력하세요.",
        placeholder="예: 알리오 올리오"
    )

    find_button = st.button("레시피 찾기", width="stretch")

    if find_button:
        encoded_menu = quote(menu)

        recipe_url = (
            "https://www.10000recipe.com/recipe/list.html"
            f"?q={encoded_menu}")

        youtube_url = (
            "https://www.youtube.com/results"
            f"?search_query={encoded_menu}+레시피")

        st.subheader(f"🔎 {menu} 레시피")
        st.link_button("🍳 만개의레시피에서 찾기",recipe_url,width="stretch")
        st.link_button("▶️ YouTube에서 찾기",youtube_url,width="stretch")