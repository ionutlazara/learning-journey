CREATE SCHEMA TRAINING_FILES;

CREATE TABLE TRAINING_FILES.PDF_FILES (
	ID SERIAL PRIMARY KEY,
	SECTION_NAME VARCHAR(255),
	BUTTON_NAME VARCHAR(255),
	PDF_CONTENT BYTEA
);
