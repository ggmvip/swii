import cv2
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent))

from barcode import get_barcode

def validate_dataset(data_dir):
    data_path = Path(data_dir)
    
    print(f"Validating dataset at: {data_path}\n")
    
    stats = {
        'total': 0,
        'decoded': 0,
        'failed': 0,
        'by_type': {}
    }
    
    for img_file in data_path.glob('**/*.jpg'):
        stats['total'] += 1
        
        code_data, code_type, _ = get_barcode(img_file)
        
        if code_data:
            stats['decoded'] += 1
            stats['by_type'][code_type] = stats['by_type'].get(code_type, 0) + 1
        else:
            stats['failed'] += 1
            print(f"Failed to decode: {img_file.name}")
    
    print("\nValidation Results:")
    print("=" * 50)
    print(f"Total images: {stats['total']}")
    print(f"Successfully decoded: {stats['decoded']}")
    print(f"Failed: {stats['failed']}")
    print(f"Success rate: {stats['decoded']/stats['total']*100:.1f}%")
    print("\nBy code type:")
    for code_type, count in stats['by_type'].items():
        print(f"  {code_type}: {count}")

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--data', default='data')
    args = parser.parse_args()
    
    validate_dataset(args.data)