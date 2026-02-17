import yaml
from pathlib import Path

class ConfigLoader:
    def __init__(self, config_path='config/settings.yaml'):
        self.config_path = Path(config_path)
        self.config = self._load_config()
    
    def _load_config(self):
        if not self.config_path.exists():
            return self._default_config()
        
        with open(self.config_path, 'r') as f:
            return yaml.safe_load(f)
    
    def _default_config(self):
        return {
            'camera': {
                'width': 1280,
                'height': 720,
                'fps': 30
            },
            'model': {
                'weights_path': 'data/model/yolov3_train_class2_final.weights.h5',
                'confidence_threshold': 0.5,
                'iou_threshold': 0.5
            },
            'logging': {
                'csv_dir': 'logs/csvs',
                'images_dir': 'logs/images',
                'log_level': 'INFO'
            },
            'api': {
                'openfoodfacts_timeout': 5,
                'max_retries': 3
            }
        }
    
    def get(self, key_path):
        keys = key_path.split('.')
        value = self.config
        for key in keys:
            value = value.get(key)
            if value is None:
                return None
        return value