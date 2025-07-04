# app/storage/database.py
import sqlite3
from uuid import uuid4
import json

class Database:
    def __init__(self):
        self.conn = sqlite3.connect("invoices.db")
        self.create_tables()
        
    def create_tables(self):
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS invoices (
                    id TEXT PRIMARY KEY,
                    filename TEXT,
                    data TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
    def store(self, data: dict, filename: str) -> str:
        doc_id = str(uuid4())
        with self.conn:
            self.conn.execute(
                "INSERT INTO invoices (id, filename, data) VALUES (?, ?, ?)",
                (doc_id, filename, json.dumps(data))
            )
        return doc_id