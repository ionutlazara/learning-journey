import streamlit as st
import base64


button_dict = {
    "Python Programming": {
        "Introduction": "python_programming/Introduction.pdf",
        "Control Flow Tools": "python_programming/Control_Flow_Tools.pdf"
    },
    "SQL Basics": {
        "Tables": "",
        "Views": ""
    },
}


# Function to display PDF in an iframe
def display_pdf(file_path):
    with open(file_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    pdf_display = f'''
    <style>
        .pdf-container {{
            display: flex;
            justify-content: space-between;  /* Button on right, iframe on left */
            align-items: flex-start;  /* Align both at the top */
            margin-left: -29%;  /* Move iframe and button together to the left */
            width: 200%;  /* Relative width for the entire container */
        }}
        iframe {{
            width: 80%;  /* Relative width for the iframe */
            height: 89vh;  /* Relative height: 89% of the viewport height */
        }}
    </style>
    <div class="pdf-container">
        <iframe src="data:application/pdf;base64,{base64_pdf}" type="application/pdf"></iframe>
    </div>
    '''
    st.markdown(pdf_display, unsafe_allow_html=True)


# Sidebar with multiple expandable sections
st.sidebar.title("Basic Data Engineering Journey")

for section, buttons in button_dict.items():
    with st.sidebar.expander(section):
        for button, file in buttons.items():
            if st.button(button):
                st.session_state.selected_pdf = file  # Store the file path directly in session state

# Main panel content - Dynamically display based on the clicked button
if st.session_state.selected_pdf:
    # Display the PDF in an iframe with relative sizing
    display_pdf(st.session_state.selected_pdf)
else:
    st.write("Please click a button from the sidebar.")
