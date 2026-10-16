import base64
from config import client

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

base64_image = encode_image("assets/ingredents.png")

print("AI가 사진을 뚫어져라 쳐다보고 있습니다...")

prompt = """
사진에서 실제로 보이는 음식 재료의 이름만 출력하세요.

규칙:
1. 재료 이름만 나열합니다.
2. 요리나 메뉴를 추천하지 않습니다.
3. 설명하지 않습니다.
4. 조리법을 말하지 않습니다.
5. 사진에 없는 재료를 추측하지 않습니다.

출력 예시:
토마토
양파
당근
"""

response = client.chat.completions.create(
    model="Qwen/Qwen2.5-VL-7B-Instruct",
    messages=[
        {
            "role": "user",
            # 비전 모델에게는 content에 문자열 대신 리스트를 보냅니다! (텍스트 + 이미지)
            "content": [
                {"type": "text", "text": prompt},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
            ]
        }
    ]
)

print("AI의 분석 결과:\n", response.choices[0].message.content)