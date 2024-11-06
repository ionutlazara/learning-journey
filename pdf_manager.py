import base64
import sqlalchemy as sa
from typing import Dict, Optional


class PDFManager:
    def __init__(self, db_config):
        # db_config is a dictionary with keys: dbname, user, password, host, port
        self.db_config = db_config
        self.conn = self._connect_to_db()

    def _connect_to_db(self):
        try:
            engine = sa.create_engine(
                f"postgresql+psycopg2://{self.db_config['user']}:{self.db_config['password']}@{self.db_config['host']}:{self.db_config['port']}/{self.db_config['dbname']}"
            )
            return engine.connect()
        except Exception as e:
            print(f"Failed to connect to database: {e}")
            return None

    def insert_pdf(self, section_name: str, button_name: str, pdf_data: bytes, file_type: str) -> bool:
        query = sa.text(f"""
            INSERT INTO TRAINING_FILES.PDF_FILES (section_name, button_name, pdf_content, file_type) 
            VALUES (:section_name, :button_name, :pdf_data, :file_type)
        """)
        try:
            self.conn.execute(query, {
                "section_name": section_name,
                "button_name": button_name,
                "pdf_data": pdf_data,
                "file_type": file_type
            })
        except Exception as e:
            print(f"Error inserting file: {e}")
            self.conn.rollback()
            return False
        else:
            self.conn.commit()
            return True

    def update_pdf(self, section_name: str, button_name: str, pdf_data: bytes) -> bool:
        query = sa.text(f"""
            UPDATE TRAINING_FILES.PDF_FILES 
            SET pdf_content = :pdf_data 
            WHERE section_name = :section_name AND button_name = :button_name
        """)
        try:
            self.conn.execute(query, {
                "section_name": section_name,
                "button_name": button_name,
                "pdf_data": pdf_data,
            })
        except Exception as e:
            print(f"Error updating PDF: {e}")
            self.conn.rollback()
            return False
        else:
            self.conn.commit()
            return True

    def delete_pdf(self, section_name: str, button_name: str) -> bool:
        query = sa.text(f"""
            DELETE FROM TRAINING_FILES.PDF_FILES 
            WHERE section_name = :section_name AND button_name = :button_name
        """)
        try:
            self.conn.execute(query, {
                "section_name": section_name,
                "button_name": button_name
            })
        except Exception as e:
            print(f"Error deleting PDF: {e}")
            self.conn.rollback()
            return False
        else:
            self.conn.commit()
            return True

    def get_pdf_content(self, section_name: str, button_name: str) -> Optional[bytes]:
        query = sa.text(f"""
            SELECT pdf_content, file_type 
            FROM TRAINING_FILES.PDF_FILES 
            WHERE section_name = :section_name AND button_name = :button_name
        """)
        result = self.conn.execute(query, {
                "section_name": section_name,
                "button_name": button_name
            })
        for file_content, file_type in result.fetchall():
            if file_type == 'pdf':
                base64_file = base64.b64encode(bytes(file_content)).decode('utf-8')
            elif file_type == 'mp4':
                base64_file = bytes(file_content)

            return base64_file, file_type

    def get_button_dict(self) -> Dict[str, Dict[str, bytes]]:
        query = sa.text("SELECT section_name, button_name FROM TRAINING_FILES.PDF_FILES order by id asc")
        button_dict = {}
        result = self.conn.execute(query)
        for section_name, button_name in result.fetchall():
            if section_name not in button_dict:
                button_dict[section_name] = {}
            button_dict[section_name][
                button_name
            ] = None  # PDF content not needed for sidebar display

        return button_dict

    def __del__(self):
        if self.conn:
            self.conn.close()
