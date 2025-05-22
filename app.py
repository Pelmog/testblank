import streamlit as st
import pandas as pd
from datetime import datetime

st.title("Ticker-Tape Calculator")
st.markdown("""
<style>
    .stButton>button {
        width: 100%;
        height: 50px;
        font-size: 20px;
        font-weight: bold;
    }
    div[data-testid="stVerticalBlock"] > div:has(div.stButton) {
        text-align: center;
        padding: 0px;
        margin: 0px;
    }
    .digit-button>button {
        background-color: #f0f2f6;
    }
    .operation-button>button {
        background-color: #ffd8b1;
    }
    .clear-button>button {
        background-color: #ffb1b1;
    }
    .equal-button>button {
        background-color: #b1ffc8;
    }
    div[data-testid="stHorizontalBlock"] {
        gap: 5px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "calculations" not in st.session_state:
    st.session_state.calculations = []
    st.session_state.current_value = 0.0
    st.session_state.operation_history = []
    st.session_state.input_buffer = ""
    st.session_state.waiting_for_operand = False
    st.session_state.last_operation = None

def add_digit(digit):
    st.session_state.input_buffer += str(digit)

def add_decimal():
    if "." not in st.session_state.input_buffer:
        if st.session_state.input_buffer == "":
            st.session_state.input_buffer = "0."
        else:
            st.session_state.input_buffer += "."

def clear_buffer():
    st.session_state.input_buffer = ""

def backspace():
    st.session_state.input_buffer = st.session_state.input_buffer[:-1]

def get_buffer_value():
    if st.session_state.input_buffer == "":
        return 0.0
    return float(st.session_state.input_buffer)

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

def perform_operation(operation=None):
    if st.session_state.input_buffer == "" and operation is not None:
        # Just changing the operation
        st.session_state.last_operation = operation
        return
    
    input_value = get_buffer_value()
    
    if not st.session_state.waiting_for_operand:
        # First operand, just store it
        st.session_state.current_value = input_value
        st.session_state.waiting_for_operand = True
        clear_buffer()
        st.session_state.last_operation = operation
        return
    
    # Perform the pending operation
    if st.session_state.last_operation == "+":
        result = st.session_state.current_value + input_value
        add_to_history("+", input_value, result)
    elif st.session_state.last_operation == "-":
        result = st.session_state.current_value - input_value
        add_to_history("-", input_value, result)
    elif st.session_state.last_operation == "×":
        result = st.session_state.current_value * input_value
        add_to_history("×", input_value, result)
    elif st.session_state.last_operation == "÷":
        if input_value != 0:
            result = st.session_state.current_value / input_value
            add_to_history("÷", input_value, result)
        else:
            st.error("Cannot divide by zero!")
            return
    
    clear_buffer()
    st.session_state.last_operation = operation
    
    # If equals was pressed (operation is None), reset waiting state
    if operation is None:
        st.session_state.waiting_for_operand = False

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
    
    st.session_state.waiting_for_operand = False
    st.session_state.last_operation = None
    clear_buffer()

# Main layout
col1, col2 = st.columns([3, 1])

with col1:
    # Display area
    display_col1, display_col2 = st.columns([3, 1])
    
    with display_col1:
        st.subheader("Current Value: " + str(st.session_state.current_value))
        
        # Display the input buffer or 0
        display_value = st.session_state.input_buffer if st.session_state.input_buffer else "0"
        st.markdown(f"""
        <div style="background-color: white; padding: 10px; border-radius: 5px; 
                   border: 1px solid #ddd; text-align: right; font-size: 24px; 
                   font-family: monospace; margin-bottom: 10px;">
            {display_value}
        </div>
        """, unsafe_allow_html=True)
    
    with display_col2:
        if st.session_state.last_operation:
            st.markdown(f"""
            <div style="background-color: #ffd8b1; padding: 10px; border-radius: 5px; 
                       border: 1px solid #ddd; text-align: center; font-size: 24px; 
                       font-family: monospace; margin-bottom: 10px;">
                {st.session_state.last_operation}
            </div>
            """, unsafe_allow_html=True)
    
    # Calculator buttons
    # Row 1: 7, 8, 9, ÷
    row1_1, row1_2, row1_3, row1_4 = st.columns(4)
    with row1_1:
        if st.button("7", key="btn7", help="Number 7"):
            add_digit(7)
    with row1_2:
        if st.button("8", key="btn8", help="Number 8"):
            add_digit(8)
    with row1_3:
        if st.button("9", key="btn9", help="Number 9"):
            add_digit(9)
    with row1_4:
        if st.button("÷", key="btnDiv", help="Divide"):
            perform_operation("÷")
    
    # Row 2: 4, 5, 6, ×
    row2_1, row2_2, row2_3, row2_4 = st.columns(4)
    with row2_1:
        if st.button("4", key="btn4", help="Number 4"):
            add_digit(4)
    with row2_2:
        if st.button("5", key="btn5", help="Number 5"):
            add_digit(5)
    with row2_3:
        if st.button("6", key="btn6", help="Number 6"):
            add_digit(6)
    with row2_4:
        if st.button("×", key="btnMul", help="Multiply"):
            perform_operation("×")
    
    # Row 3: 1, 2, 3, -
    row3_1, row3_2, row3_3, row3_4 = st.columns(4)
    with row3_1:
        if st.button("1", key="btn1", help="Number 1"):
            add_digit(1)
    with row3_2:
        if st.button("2", key="btn2", help="Number 2"):
            add_digit(2)
    with row3_3:
        if st.button("3", key="btn3", help="Number 3"):
            add_digit(3)
    with row3_4:
        if st.button("-", key="btnSub", help="Subtract"):
            perform_operation("-")
    
    # Row 4: 0, ., =, +
    row4_1, row4_2, row4_3, row4_4 = st.columns(4)
    with row4_1:
        if st.button("0", key="btn0", help="Number 0"):
            add_digit(0)
    with row4_2:
        if st.button(".", key="btnDot", help="Decimal point"):
            add_decimal()
    with row4_3:
        if st.button("=", key="btnEq", help="Calculate result"):
            perform_operation(None)
    with row4_4:
        if st.button("+", key="btnAdd", help="Add"):
            perform_operation("+")
    
    # Row 5: Clear, Backspace
    row5_1, row5_2 = st.columns(2)
    with row5_1:
        if st.button("C", key="btnClear", help="Clear all"):
            st.session_state.calculations = []
            st.session_state.current_value = 0.0
            st.session_state.operation_history = []
            st.session_state.input_buffer = ""
            st.session_state.waiting_for_operand = False
            st.session_state.last_operation = None
    with row5_2:
        if st.button("⌫", key="btnBack", help="Backspace"):
            backspace()

with col2:
    # Rollback controls
    st.subheader("Rollback")
    steps_to_rollback = st.number_input("Steps", min_value=1, max_value=len(st.session_state.calculations) if st.session_state.calculations else 1, value=1, step=1)
    
    if st.button("Rollback", key="btnRollback") and st.session_state.calculations:
        rollback(steps_to_rollback)
        st.rerun()

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