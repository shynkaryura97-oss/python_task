# main.py
import argparse
import json
from database.database_manager import DatabaseManager
from data_loader.data_loader import DataLoader
from queries.room_queries import RoomQueries
from exporters.json_exporter import JSONExporter
from exporters.xml_exporter import XMLExporter

class RoomStudentsProcessor:
    def __init__(self, db_manager):
        self.db_manager = db_manager
        self.queries = RoomQueries(db_manager)
    
    def process(self, output_format='json'):
        results = {}
        
        # Выполняем все запросы
        results['rooms_student_count'] = self.queries.get_rooms_with_student_count()
        results['rooms_min_avg_age'] = self.queries.get_rooms_with_min_avg_age(5)
        results['rooms_max_age_diff'] = self.queries.get_rooms_with_max_age_difference(5)
        results['mixed_sex_rooms'] = self.queries.get_mixed_sex_rooms()
        
        # Экспортируем результаты
        if output_format.lower() == 'xml':
            exporter = XMLExporter()
        else:
            exporter = JSONExporter()
            
        return exporter.export(results)

def main():
    parser = argparse.ArgumentParser(description='Process room and student data')
    parser.add_argument('--students', required=True, help='Path to students file')
    parser.add_argument('--rooms', required=True, help='Path to rooms file')
    parser.add_argument('--format', choices=['json', 'xml'], default='json', help='Output format')
    
    args = parser.parse_args()
    
    # Инициализация базы данных
    db_manager = DatabaseManager()
    db_manager.initialize_database()
    
    # Загрузка данных
    data_loader = DataLoader(db_manager)
    data_loader.load_rooms(args.rooms)
    data_loader.load_students(args.students)
    
    # Создание индексов для оптимизации
    db_manager.create_indexes()
    
    # Обработка и экспорт
    processor = RoomStudentsProcessor(db_manager)
    result = processor.process(args.format)
    
    print(result)

if __name__ == '__main__':
    main()
