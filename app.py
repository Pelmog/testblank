import streamlit as st

st.title("Number Adder")

# Input fields for two numbers
num1 = st.number_input("Enter first number", value=0.0)
num2 = st.number_input("Enter second number", value=0.0)

# Button to trigger addition
if st.button("Add Numbers"):
    result = num1 + num2
    st.success(f"Result: {result}")
    st.balloons()