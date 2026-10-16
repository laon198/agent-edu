import streamlit as st
import random


POKEMONS = [
    {"name": "피카츄", "image": "assets/pikachu.png"},
    {"name": "이브이", "image": "assets/eevee.png"},
    {"name": "파이리", "image": "assets/charmander.png"},
]

st.title("포켓몬 이름 맞추기")

# 처음 실행할 때 포켓몬 하나 선택
if "pokemon" not in st.session_state:
    st.session_state.pokemon = random.choice(POKEMONS)

pokemon = st.session_state.pokemon

# 포켓몬 이미지 출력
st.image(pokemon["image"], width=200)

# 사용자 답 입력
answer = st.text_input("이 포켓몬 이름은?")
