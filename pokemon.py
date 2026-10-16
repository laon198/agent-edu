import streamlit as st
import random
import asyncio
import edge_tts
from pathlib import Path

POKEMONS = [
    {"name": "피카츄", "image": "assets/pikachu.png"},
    {"name": "이브이", "image": "assets/eevee.png"},
    {"name": "파이리", "image": "assets/charmander.png"},
]

st.title("포켓몬 이름 맞추기")

# 오디오 저장 폴더
AUDIO_DIR = Path("audio")
AUDIO_DIR.mkdir(exist_ok=True)

if "pokemon" not in st.session_state:
    st.session_state.pokemon = random.choice(POKEMONS)

pokemon = st.session_state.pokemon

st.image(pokemon["image"], width=200)

answer = st.text_input("이 포켓몬 이름은?")

async def make_tts(text, output_file):
    communicate = edge_tts.Communicate(
        text,
        "ko-KR-SunHiNeural"
    )
    await communicate.save(str(output_file))


if st.button("정답 확인"):

    if answer.strip() == pokemon["name"]:

        message = "정답입니다!"
        st.success(message)

        output_file = AUDIO_DIR / "correct.mp3"

        asyncio.run(
            make_tts(message, output_file)
        )

        st.audio(
            str(output_file),
            format="audio/mp3",
            autoplay=True
        )

    else:

        message = f"틀렸습니다. 정답은 {pokemon['name']}입니다."
        st.error(message)

        output_file = AUDIO_DIR / "wrong.mp3"

        asyncio.run(
            make_tts(message, output_file)
        )

        st.audio(
            str(output_file),
            format="audio/mp3",
            autoplay=True
        )