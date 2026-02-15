import unittest
import cv2
import numpy as np
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent))

from model.tiny_yolo import TinyYolo
from barcode import get_barcode

class TestBarcodeDetection(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.model = TinyYolo(classes=2, training=False)
        cls.test_images = Path('tests/test_images')
    
    def test_yolo_loads(self):
        self.assertIsNotNone(self.model)
    
    def test_barcode_detection(self):
        test_img = self.test_images / 'barcode_sample.jpg'
        if test_img.exists():
            result = self.model.predict(str(test_img))
            self.assertIsNotNone(result)
    
    def test_qr_detection(self):
        test_img = self.test_images / 'qr_sample.jpg'
        if test_img.exists():
            result = self.model.predict(str(test_img))
            self.assertIsNotNone(result)
    
    def test_pyzbar_decode(self):
        test_img = self.test_images / 'barcode_sample.jpg'
        if test_img.exists():
            code_data, code_type, _ = get_barcode(test_img)
            self.assertIsNotNone(code_data)

if __name__ == '__main__':
    unittest.main()