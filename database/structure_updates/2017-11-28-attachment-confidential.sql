ALTER TABLE ATTACHMENT
ADD (
	IS_CONFIDENTIAL NUMBER(1, 0) DEFAULT 0 NOT NULL
);
