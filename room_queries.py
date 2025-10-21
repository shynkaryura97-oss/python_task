# queries/room_queries.py
from datetime import datetime

class RoomQueries:
    def __init__(self, db_manager):
        self.db_manager = db_manager
    
    def get_rooms_with_student_count(self):
        query = """
        SELECT r.id, r.name, COUNT(s.id) as student_count
        FROM rooms r
        LEFT JOIN students s ON r.id = s.room_id
        GROUP BY r.id, r.name
        ORDER BY student_count DESC
        """
        return self.db_manager.execute_query(query)
    
    def get_rooms_with_min_avg_age(self, limit=5):
        query = """
        SELECT r.id, r.name, AVG(YEAR(CURDATE()) - YEAR(s.birthday)) as avg_age
        FROM rooms r
        JOIN students s ON r.id = s.room_id
        GROUP BY r.id, r.name
        ORDER BY avg_age ASC
        LIMIT %s
        """
        return self.db_manager.execute_query(query, (limit,))
    
    def get_rooms_with_max_age_difference(self, limit=5):
        query = """
        SELECT r.id, r.name, 
               MAX(YEAR(CURDATE()) - YEAR(s.birthday)) - MIN(YEAR(CURDATE()) - YEAR(s.birthday)) as age_diff
        FROM rooms r
        JOIN students s ON r.id = s.room_id
        GROUP BY r.id, r.name
        ORDER BY age_diff DESC
        LIMIT %s
        """
        return self.db_manager.execute_query(query, (limit,))
    
    def get_mixed_sex_rooms(self):
        query = """
        SELECT DISTINCT r.id, r.name
        FROM rooms r
        JOIN students s ON r.id = s.room_id
        GROUP BY r.id, r.name
        HAVING COUNT(DISTINCT s.sex) > 1
        """
        return self.db_manager.execute_query(query)
