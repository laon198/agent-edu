import streamlit as st
import base64
import asyncio
import edge_tts
from openai import OpenAI

# -------------------------
# Qwen 서버 연결
# -------------------------
client = OpenAI(
    base_url="https://testse.store/v1",
    api_key="lab-vllm-secret-key-2026"
)

# -------------------------
# 이미지 Base64 변환
# -------------------------
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(
            image_file.read()
        ).decode("utf-8")


# -------------------------
# TTS 생성
# -------------------------
async def make_tts(text):
    communicate = edge_tts.Communicate(
        text,
        "ko-KR-SunHiNeural"
    )
    await communicate.save("output.mp3")


# -------------------------
# Streamlit 화면
# -------------------------
st.title("AI 관광지 해설")

image_path = "./assets/top.png"

st.image(
    image_path,
    caption="관광지 사진",
    width=500
)

if st.button("AI에게 물어보기"):

    base64_image = encode_image(image_path)

    with st.spinner("AI가 사진을 분석하고 있습니다..."):

        response = client.chat.completions.create(
            model="Qwen/Qwen2.5-VL-7B-Instruct",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": """
                            이 사진 속 관광지 또는 문화유적을 분석해줘.
                            김천에 있는 문화유적이야,
                            관광객에게 설명하듯이 한국어로
                            2~3문장 정도로 간단하게 설명해줘.
                            """
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
            ],
            max_tokens=150
        )

    result = response.choices[0].message.content

    st.subheader("AI 설명")
    st.write(result)

    # AI 결과를 음성으로 변환
    asyncio.run(make_tts(result))

    # 브라우저에서 음성 재생
    st.audio(
        "output.mp3",
        format="audio/mp3",
        autoplay=True
    )