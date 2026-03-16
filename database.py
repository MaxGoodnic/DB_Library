import sqlite3
import psycopg2
from psycopg2.extras import RealDictCursor
from config import Config
from typing import Optional, Dict, Any, List

class DatabaseManager:
    def __init__(self, db_type: str = 'sqlite'):
        self.db_type = db_type
        self.connection = None
        
    def connect(self):
        if self.db_type == 'postgresql':
            return self._connect_postgresql()
        elif self.db_type == 'sqlite':
            return self._connect_sqlite()
        else:
            raise ValueError("Unsupported database type")
    
    def _connect_postgresql(self):
        try:
            self.connection = psycopg2.connect(**Config.POSTGRES_CONFIG)
            return self.connection
        except Exception as e:
            print(f"Error connecting to PostgreSQL: {e}")
            return None
    
    def _connect_sqlite(self):
        try:
            self.connection = sqlite3.connect(Config.SQLITE_DB)
            self.connection.row_factory = sqlite3.Row
            return self.connection
        except Exception as e:
            print(f"Error connecting to SQLite: {e}")
            return None
    
    def disconnect(self):
        if self.connection:
            self.connection.close()
            self.connection = None
    
    def execute_query(self, query: str, params: Optional[tuple] = None) -> List[Dict[str, Any]]:
        if not self.connection:
            self.connect()
        
        try:
            cursor = self.connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            if query.strip().upper().startswith('SELECT'):
                if self.db_type == 'postgresql':
                    result = [dict(row) for row in cursor.fetchall()]
                else:
                    result = [dict(row) for row in cursor.fetchall()]
                return result
            else:
                self.connection.commit()
                return [{"affected_rows": cursor.rowcount}]
                
        except Exception as e:
            if self.connection:
                self.connection.rollback()
            print(f"Error executing query: {e}")
            return []
    
    def execute_script(self, script_path: str):
        if not self.connection:
            self.connect()
        
        try:
            with open(script_path, 'r', encoding='utf-8') as file:
                script = file.read()
            
            cursor = self.connection.cursor()
            cursor.execute(script)
            self.connection.commit()
            print(f"Schema {script_path} executed successfully")
            
        except Exception as e:
            if self.connection:
                self.connection.rollback()
            print(f"Error executing script: {e}")
