import streamlit as st
st.title("버튼 클릭 횟수")

count = 0

if st.button("클릭"):
    count = count+1    

st.write("현재 횟수:", count)