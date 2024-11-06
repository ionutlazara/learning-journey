import streamlit as st
from pdf_manager import PDFManager
from config_settings import db_config


@st.cache_resource
def get_cached_pdf(section: str, button: str) -> bytes:
    """Fetch PDF content from the database and cache it by section and button."""
    pdf_manager = PDFManager(db_config)
    return pdf_manager.get_pdf_content(section, button)


class AppManager:
    def __init__(self, db_config, render_manager):
        self.pdf_manager = PDFManager(db_config)
        self.render_manager = render_manager
        self.button_dict = self.pdf_manager.get_button_dict()
        self.setup_sidebar()

        # Initialize session state if not already present
        if "page" not in st.session_state:
            st.session_state.page = "main"  # Start on the main page by default

    def setup_sidebar(self):
        st.sidebar.title("Basic Data Engineering Journey")

        for section, buttons in self.button_dict.items():
            with st.sidebar.expander(section):
                for button in buttons.keys():
                    if st.button(button):
                        st.session_state.page = 'main'
                        st.session_state['button_clicked'] = (section, button)

        # Divider and manage buttons
        st.sidebar.markdown("---")
        st.sidebar.subheader("Manage PDFs")
        if st.sidebar.button("Upload"):
            st.session_state.page = 'upload'   
        if st.sidebar.button("Edit"):
            st.session_state.page = 'edit'       
        if st.sidebar.button("Delete"):
            st.session_state.page = 'delete'   

    def main_panel_content(self):
        """Display the main content based on clicked button or action."""
        if st.session_state.page == "main":
            self.display_pdf_content()

        elif st.session_state.page == "upload":
            self.upload_pdf()

        elif st.session_state.page == "edit":
            self.edit_pdf()

        elif st.session_state.page == "delete":
            self.delete_pdf()

    def display_pdf_content(self):
        """Display the PDF content when a button is clicked."""
        if "button_clicked" in st.session_state:
            section, button = st.session_state['button_clicked']
            pdf_data = get_cached_pdf(section, button)
            if pdf_data:
                self.render_manager.display_pdf(pdf_data, "pdf_container.html")
            else:
                st.write("No PDF content available for this section.")

    def upload_pdf(self):
        """Handle the upload PDF action."""
        st.subheader("Upload a New PDF")
        new_section = st.text_input("Section Name")
        new_button = st.text_input("Button Name")
        pdf_file = st.file_uploader("Choose a PDF file", type=["pdf"])

        if st.button("Submit Upload"):
            if new_section and new_button and pdf_file:
                pdf_data = pdf_file.getvalue()
                success = self.pdf_manager.insert_pdf(new_section, new_button, pdf_data)
                if success:
                    st.success("PDF uploaded successfully!")
                    st.session_state.page = 'main'
                else:
                    st.error("Failed to upload PDF.")

    def edit_pdf(self):
        """Handle the edit PDF action."""
        st.subheader("Edit Existing PDF")
        if self.button_dict:
            section = st.selectbox("Select Section", options=self.button_dict.keys())
            button = st.selectbox("Select Button", options=self.button_dict[section].keys())
            pdf_file = st.file_uploader("Choose a new PDF file", type=["pdf"])

            if st.button("Submit Edit"):
                if section and button and pdf_file:
                    pdf_data = pdf_file.getvalue()
                    success = self.pdf_manager.update_pdf(section, button, pdf_data)
                    if success:
                        st.success("PDF updated successfully!")
                        st.session_state.page = 'main'
                        st.cache_resource.clear()
                    else:
                        st.error("Failed to update PDF.")
        else:
            st.write("No Sections available.")

    def delete_pdf(self):
        """Handle the delete PDF action."""
        st.subheader("Delete PDF")
        if self.button_dict:
            section = st.selectbox("Select Section", options=self.button_dict.keys())
            button = st.selectbox("Select Button", options=self.button_dict[section].keys())

            if st.button("Confirm Delete"):
                success = self.pdf_manager.delete_pdf(section, button)
                if section and button:
                    if success:
                        st.success("PDF deleted successfully!")
                        st.session_state.page = 'main'
                        st.cache_resource.clear()
                    else:
                        st.error("Failed to delete PDF.")            
        else:
            st.write("No Sections available.")
