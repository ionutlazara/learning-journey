import streamlit as st
from pdf_manager import PDFManager


class AppManager:
    def __init__(self, db_config, render_manager):
        self.pdf_manager = PDFManager(db_config)
        self.render_manager = render_manager
        self.button_dict = self.pdf_manager.get_button_dict()
        self.setup_sidebar()

    def setup_sidebar(self):
        st.sidebar.title("Basic Data Engineering Journey")

        for section, buttons in self.button_dict.items():
            with st.sidebar.expander(section):
                for button in buttons.keys():
                    if st.button(button):
                        st.session_state['button_clicked'] = (section, button)

        # Divider and manage buttons
        st.sidebar.markdown("---")
        st.sidebar.subheader("Manage PDFs")
        if st.sidebar.button("Upload"):
            st.session_state['action'] = 'upload'
        if st.sidebar.button("Edit"):
            st.session_state['action'] = 'edit'
        if st.sidebar.button("Delete"):
            st.session_state['action'] = 'delete'

    @st.cache_data
    def get_cached_pdf(self, section: str, button: str) -> bytes:
        """Fetch PDF content from the database and cache it by section and button."""
        return self.pdf_manager.get_pdf_content(section, button)

    def main_panel_content(self):
        """Display the main content based on clicked button or action."""
        st.title("Main Content")
        if "button_clicked" in st.session_state:
            section, button = st.session_state['button_clicked']
            pdf_data = self.get_cached_pdf(section, button)
            if pdf_data:
                self.render_manager.display_pdf(pdf_data, "pdf_template.html")
            else:
                st.write("No PDF content available for this section.")

        # Handle additional actions for upload, edit, delete
        if st.session_state.get("action") == "upload":
            self.upload_pdf()
        elif st.session_state.get("action") == "edit":
            self.edit_pdf()
        elif st.session_state.get("action") == "delete":
            self.delete_pdf()

    def upload_pdf(self):
        """Handle the upload PDF action."""
        st.subheader("Upload a New PDF")
        new_section = st.text_input("Section Name")
        new_button = st.text_input("Button Name")
        pdf_file = st.file_uploader("Choose a PDF file", type=["pdf"])

        if st.button("Submit Upload"):
            if new_section and new_button and pdf_file:
                pdf_data = pdf_file.read()
                success = self.pdf_manager.insert_pdf(new_section, new_button, pdf_data)
                if success:
                    st.success("PDF uploaded successfully!")
                    st.session_state['action'] = None
                else:
                    st.error("Failed to upload PDF.")

    def edit_pdf(self):
        """Handle the edit PDF action."""
        st.subheader("Edit Existing PDF")
        section = st.selectbox("Select Section", options=self.button_dict.keys())
        button = st.selectbox("Select Button", options=self.button_dict[section].keys())
        pdf_file = st.file_uploader("Choose a new PDF file", type=["pdf"])

        if st.button("Submit Edit"):
            if section and button and pdf_file:
                pdf_data = pdf_file.read()
                success = self.pdf_manager.update_pdf(section, button, pdf_data)
                if success:
                    st.success("PDF updated successfully!")
                    st.session_state['action'] = None
                    st.cache_data.clear()
                else:
                    st.error("Failed to update PDF.")

    def delete_pdf(self):
        """Handle the delete PDF action."""
        st.subheader("Delete PDF")
        section = st.selectbox("Select Section", options=self.button_dict.keys())
        button = st.selectbox("Select Button", options=self.button_dict[section].keys())

        if st.button("Confirm Delete"):
            success = self.pdf_manager.delete_pdf(section, button)
            if success:
                st.success("PDF deleted successfully!")
                st.session_state['action'] = None
                st.cache_data.clear()
            else:
                st.error("Failed to delete PDF.")
