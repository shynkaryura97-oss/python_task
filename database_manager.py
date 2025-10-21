# database/database_manager.py
import mysql.connector
from config.settings import DB_CONFIG

class DatabaseManager:
    def __init__(self):
        self.connection = None
        self.connect()
    
    def connect(self):
        try:
            self.connection = mysql.connector.connect(**DB_CONFIG)
        except mysql.connector.Error as e:
            print(f"Error connecting to MySQL: {e}")
            raise
    
    def initialize_database(self):
        with open('src/database/schema.sql', 'r') as file:
            schema_sql = file.read()
        
        cursor = self.connection.cursor()
        for statement in schema_sql.split(';'):
            if statement.strip():
                cursor.execute(statement)
        self.connection.commit()
        cursor.close()
    
    def create_indexes(self):
        cursor = self.connection.cursor()
        
        # Индексы для оптимизации запросов
        indexes = [
            "CREATE INDEX IF NOT EXISTS idx_students_room_id ON students(room_id)",
            "CREATE INDEX IF NOT EXISTS idx_students_birthday ON students(birthday)",
            "CREATE INDEX IF NOT EXISTS idx_students_sex ON students(sex)",
            "CREATE INDEX IF NOT EXISTS idx_rooms_id ON rooms(id)"
        ]
        
        for index_sql in indexes:
            cursor.execute(index_sql)
        
        self.connection.commit()
        cursor.close()
    
    def execute_query(self, query, params=None):
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute(query, params or ())
        result = cursor.fetchall()
        cursor.close()
        return result
    
    def close(self):
        if self.connection:
            self.connection.close()
