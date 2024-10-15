import os
import json
from typing import Dict, Any

class OutputFormatter:
    def __init__(self, output_dir: str):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def save_result(self, file_name: str, result: Dict[str, Any]):
        base_name = os.path.splitext(file_name)[0]
        output_path = os.path.join(self.output_dir, f"{base_name}_ocr_result.json")
        
        with open(output_path, 'w') as f:
            json.dump(result, f, indent=2)

    def save_metadata(self, file_name: str, metadata: Dict[str, Any]):
        base_name = os.path.splitext(file_name)[0]
        output_path = os.path.join(self.output_dir, f"{base_name}_metadata.json")
        
        with open(output_path, 'w') as f:
            json.dump(metadata, f, indent=2)
