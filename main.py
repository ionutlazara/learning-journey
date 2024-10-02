import streamlit as st


button_dict = {
    "Python Programming": ["Installation and Setup", "Variables"],
    "SQL Basics": ["Tables", "Views"],
}


# Function to handle button clicks
def handle_button_click(section, button):
    st.session_state.button_clicked = f"{section} - {button}"


# Initialize session state to track clicked buttons
if "button_clicked" not in st.session_state:
    st.session_state.button_clicked = None

# Sidebar with multiple expandable sections
st.sidebar.title("Basic Data Engineering Journey")

for section, buttons in button_dict.items():
    with st.sidebar.expander(section):
        for button in buttons:
            if st.button(button):
                handle_button_click(section, button)

# Main panel content - Dynamically display based on the clicked button
st.title("Main Content")

if st.session_state.button_clicked:
    st.write(f"You clicked: {st.session_state.button_clicked}")
    # Add more content for each button as needed
else:
    st.write("Please click a button from the sidebar.")
