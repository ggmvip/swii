#!/usr/bin/env python3
"""
PyZbar Baseline Testing
"""

import sys
import os
import time
from pyzbar.pyzbar import decode
from PIL import Image
from collections import defaultdict
import argparse


def test_pyzbar_baseline(dataset_path):
    """Test PyZbar decoding on dataset"""
    print("="*60)
    print("PYZBAR BASELINE TESTING")
    print("="*60)
    
    # Find all images
    image_files = []
    for ext in ['.jpg', '.jpeg', '.png']:
        image_files.extend([
            os.path.join(root, f)
            for root, dirs, files in os.walk(dataset_path)
            for f in files if f.lower().endswith(ext)
        ])
    
    if not image_files:
        print(f"No images found in {dataset_path}")
        return False
    
    print(f"Found {len(image_files)} images")
    
    # Statistics
    stats = defaultdict(lambda: {'success': 0, 'fail': 0, 'times': []})
    total_success = 0
    total_fail = 0
    
    # Test each image
    for img_path in image_files:
        try:
            img = Image.open(img_path)
            
            start = time.time()
            decoded = decode(img)
            elapsed = time.time() - start
            
            if decoded:
                code_type = decoded[0].type
                stats[code_type]['success'] += 1
                stats[code_type]['times'].append(elapsed)
                total_success += 1
            else:
                stats['UNKNOWN']['fail'] += 1
                total_fail += 1
                
        except Exception as e:
            print(f"Error processing {img_path}: {e}")
            total_fail += 1
    
    # Print results
    print("" + "="*60)
    print("RESULTS BY CODE TYPE")
    print("="*60)
    
    for code_type, data in stats.items():
        total = data['success'] + data['fail']
        if total > 0:
            success_rate = (data['success'] / total) * 100
            avg_time = sum(data['times']) / len(data['times']) if data['times'] else 0
            
            print(f"{code_type}:")
            print(f"  Success: {data['success']}/{total} ({success_rate:.1f}%)")
            print(f"  Average decode time: {avg_time*1000:.2f}ms")
    
    # Overall stats
    total = total_success + total_fail
    overall_rate = (total_success / total) * 100 if total > 0 else 0
    
    print("" + "="*60)
    print("OVERALL STATISTICS")
    print("="*60)
    print(f"Total images: {total}")
    print(f"Successfully decoded: {total_success} ({overall_rate:.1f}%)")
    print(f"Failed to decode: {total_fail}")
    
    return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset', default='data/test_images/', 
                       help='Path to dataset')
    args = parser.parse_args()
    
    success = test_pyzbar_baseline(args.dataset)
    sys.exit(0 if success else 1)
