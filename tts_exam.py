import streamlit as st
import asyncio
import edge_tts

st.title("TTS 실습")

text = st.text_input("말할 내용을 입력하세요")

if st.button("재생") and text:
    output_file = "audio/output.mp3"

    async def make_tts():
        communicate = edge_tts.Communicate(
            text,
            "ko-KR-SunHiNeural"
        )
        await communicate.save(output_file)

    asyncio.run(make_tts())

    # Streamlit 화면에서 오디오 재생
    st.audio(output_file, format="audio/mp3", autoplay=True)