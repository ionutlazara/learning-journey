from jinja2 import Environment, FileSystemLoader
import streamlit as st
from typing import Dict


class RenderManager:
    def __init__(self, css_path: str, template_dir: str):
        self.env = Environment(loader=FileSystemLoader(template_dir))
        self.css_path = css_path
        self.load_css()

    def load_css(self):
        """Load and apply external CSS file."""
        with open(self.css_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    def render_template(self, template_name: str, **context: Dict):
        """Load and render an HTML template using Jinja2."""
        template = self.env.get_template(template_name)
        return template.render(context)

    def display_pdf(self, file_data: bytes, template: str):
        """Display PDF in an iframe with styling using a Jinja2 HTML template."""
        html_content = self.render_template(template_name=template, file_data=file_data)
        st.markdown(html_content, unsafe_allow_html=True)
