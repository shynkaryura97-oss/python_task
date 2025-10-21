# data_loader/data_loader.py
import json

class DataLoader:
    def __init__(self, db_manager):
        self.db_manager = db_manager
    
    def load_rooms(self, file_path):
        with open(file_path, 'r') as file:
            rooms_data = json.load(file)
        
        cursor = self.db_manager.connection.cursor()
        for room in rooms_data:
            cursor.execute(
                "INSERT IGNORE INTO rooms (id, name) VALUES (%s, %s)",
                (room['id'], room['name'])
            )
        self.db_manager.connection.commit()
        cursor.close()
    
    def load_students(self, file_path):
        with open(file_path, 'r') as file:
            students_data = json.load(file)
        
        cursor = self.db_manager.connection.cursor()
        for student in students_data:
            cursor.execute(
                """INSERT IGNORE INTO students 
                   (id, birthday, sex, name, room_id) 
                   VALUES (%s, %s, %s, %s, %s)""",
                (student['id'], student['birthday'], student['sex'], 
                 student['name'], student['room'])
            )
        self.db_manager.connection.commit()
        cursor.close()
