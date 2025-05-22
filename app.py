import streamlit as st
import pandas as pd
from datetime import datetime

st.title("Ticker-Tape Calculator")

if "calculations" not in st.session_state:
    st.session_state.calculations = []
    st.session_state.current_value = 0.0
    st.session_state.operation_history = []

def add_to_history(operation, value, result):
    timestamp = datetime.now().strftime("%H:%M:%S")
    st.session_state.calculations.append({
        "timestamp": timestamp,
        "operation": operation,
        "value": value,
        "result": result
    })
    st.session_state.operation_history.append(f"{operation} {value}")
    st.session_state.current_value = result

def rollback(steps):
    if steps <= 0 or steps > len(st.session_state.calculations):
        return
    
    # Remove the last 'steps' entries
    for _ in range(steps):
        if st.session_state.calculations:
            st.session_state.calculations.pop()
            st.session_state.operation_history.pop()
    
    # Update current value to the last calculation result, or 0 if empty
    if st.session_state.calculations:
        st.session_state.current_value = st.session_state.calculations[-1]["result"]
    else:
        st.session_state.current_value = 0.0

col1, col2 = st.columns([3, 1])

with col1:
    # Display current value
    st.subheader(f"Current Value: {st.session_state.current_value}")
    
    # Input for new value
    input_value = st.number_input("Enter a number", value=0.0, key="input_number")
    
    # Operation buttons
    col_add, col_sub, col_mul, col_div = st.columns(4)
    
    with col_add:
        if st.button("Add (+)"):
            result = st.session_state.current_value + input_value
            add_to_history("+", input_value, result)
    
    with col_sub:
        if st.button("Subtract (-)"):
            result = st.session_state.current_value - input_value
            add_to_history("-", input_value, result)
    
    with col_mul:
        if st.button("Multiply (×)"):
            result = st.session_state.current_value * input_value
            add_to_history("×", input_value, result)
    
    with col_div:
        if st.button("Divide (÷)"):
            if input_value != 0:
                result = st.session_state.current_value / input_value
                add_to_history("÷", input_value, result)
            else:
                st.error("Cannot divide by zero!")
    
    # Clear button
    if st.button("Clear (C)"):
        st.session_state.calculations = []
        st.session_state.current_value = 0.0
        st.session_state.operation_history = []
        st.experimental_rerun()

with col2:
    # Rollback controls
    st.subheader("Rollback")
    steps_to_rollback = st.number_input("Steps", min_value=1, max_value=len(st.session_state.calculations) if st.session_state.calculations else 1, value=1, step=1)
    
    if st.button("Rollback") and st.session_state.calculations:
        rollback(steps_to_rollback)
        st.experimental_rerun()

# Display ticker tape
st.subheader("Ticker Tape")
if st.session_state.calculations:
    df = pd.DataFrame(st.session_state.calculations)
    st.dataframe(df, use_container_width=True)
else:
    st.info("No calculations yet. Start by performing an operation.")

# Display operation history
st.subheader("Operation History")
if st.session_state.operation_history:
    history_text = " → ".join(st.session_state.operation_history)
    st.code(f"0 → {history_text} = {st.session_state.current_value}")
else:
    st.info("No operations performed yet.")