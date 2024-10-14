import streamlit as st
import base64
from typing import Dict
from config_settings import settings
from jinja2 import Environment, FileSystemLoader


# Initialize Jinja2 environment and load templates from the current directory
env = Environment(loader=FileSystemLoader('./templates'))

st.session_state.selected_pdf = None


# Function to load and render HTML template using Jinja2
def render_template(template_name: str, **context: Dict):
    template = env.get_template(template_name)
    return template.render(context)


# Function to load and apply external CSS file
def local_css():
    with open("./styles/styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# Function to display PDF in an iframe
def display_pdf(file_path: str, template: str):
    with open(file_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')

        html_content = render_template(
            template_name=template, 
            pdf_data=base64_pdf,
        )
        st.markdown(html_content, unsafe_allow_html=True)


# Sidebar with multiple expandable sections
st.sidebar.title("Journey to Data Engineer")

for section, buttons in settings.items():
    with st.sidebar.expander(section):
        for button, file in buttons.items():
            if st.button(button):
                st.session_state.selected_pdf = file  # Store the file path directly in session state

local_css()

# Main panel content - Dynamically display based on the clicked button
if st.session_state.selected_pdf:
    # Display the PDF in an iframe with relative sizing
    display_pdf(st.session_state.selected_pdf, "pdf_container.html")
else:
    st.write("Please click a button from the sidebar.")
