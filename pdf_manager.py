import psycopg2
from typing import Dict, Optional


class PDFManager:
    def __init__(self, db_config):
        # db_config is a dictionary with keys: dbname, user, password, host, port
        self.db_config = db_config
        self.conn = self._connect_to_db()

    def _connect_to_db(self):
        try:
            return psycopg2.connect(**self.db_config)
        except Exception as e:
            print(f"Failed to connect to database: {e}")
            return None

    def insert_pdf(self, section_name: str, button_name: str, pdf_data: bytes) -> bool:
        query = """
            INSERT INTO pdf_files (section_name, button_name, pdf_content)
            VALUES (%s, %s, %s)
        """
        with self.conn.cursor() as cur:
            try:
                cur.execute(query, (section_name, button_name, pdf_data))
            except Exception as e:
                print(f"Error inserting PDF: {e}")
                self.conn.rollback()
                return False
            else:
                self.conn.commit()
                return True

    def update_pdf(self, section_name: str, button_name: str, pdf_data: bytes) -> bool:
        query = """
            UPDATE pdf_files 
            SET pdf_content = %s 
            WHERE section_name = %s AND button_name = %s
        """
        with self.conn.cursor() as cur:
            try:
                cur.execute(query, (pdf_data, section_name, button_name))
            except Exception as e:
                print(f"Error updating PDF: {e}")
                self.conn.rollback()
                return False
            else:
                self.conn.commit()
                return True

    def delete_pdf(self, section_name: str, button_name: str) -> bool:
        query = """
            DELETE FROM pdf_files 
            WHERE section_name = %s AND button_name = %s
        """
        with self.conn.cursor() as cur:
            try:
                cur.execute(query, (section_name, button_name))
            except Exception as e:
                print(f"Error deleting PDF: {e}")
                self.conn.rollback()
                return False
            else:
                self.conn.commit()
                return True

    def get_pdf_content(self, section_name: str, button_name: str) -> Optional[bytes]:
        query = """
            SELECT pdf_content 
            FROM pdf_files 
            WHERE section_name = %s AND button_name = %s
        """
        with self.conn.cursor() as cur:
            cur.execute(query, (section_name, button_name))
            result = cur.fetchone()
            return result[0] if result else None

    def get_button_dict(self) -> Dict[str, Dict[str, bytes]]:
        query = "SELECT section_name, button_name FROM pdf_files"
        button_dict = {}
        with self.conn.cursor() as cur:
            cur.execute(query)
            for section_name, button_name in cur.fetchall():
                if section_name not in button_dict:
                    button_dict[section_name] = {}
                button_dict[section_name][button_name] = None  # PDF content not needed for sidebar display
        return button_dict

    def __del__(self):
        if self.conn:
            self.conn.close()
