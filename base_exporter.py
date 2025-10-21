# exporters/base_exporter.py
from abc import ABC, abstractmethod

class BaseExporter(ABC):
    @abstractmethod
    def export(self, data):
        pass

# exporters/json_exporter.py
import json
from .base_exporter import BaseExporter

class JSONExporter(BaseExporter):
    def export(self, data):
        return json.dumps(data, indent=2, ensure_ascii=False, default=str)

# exporters/xml_exporter.py
import xml.etree.ElementTree as ET
from .base_exporter import BaseExporter

class XMLExporter(BaseExporter):
    def export(self, data):
        root = ET.Element('results')
        
        for query_name, results in data.items():
            query_element = ET.SubElement(root, query_name)
            
            for item in results:
                item_element = ET.SubElement(query_element, 'item')
                for key, value in item.items():
                    field_element = ET.SubElement(item_element, key)
                    field_element.text = str(value)
        
        return ET.tostring(root, encoding='unicode', method='xml')
