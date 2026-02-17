import cv2
import time
import numpy as np
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent))

from model.tiny_yolo import TinyYolo
from utils.performance_monitor import PerformanceMonitor

def benchmark_model(test_images_dir, num_iterations=100):
    model = TinyYolo(classes=2, training=False)
    monitor = PerformanceMonitor()
    
    test_images = list(Path(test_images_dir).glob('*.jpg'))
    if not test_images:
        print(f"No test images found in {test_images_dir}")
        return
    
    print(f"Benchmarking with {len(test_images)} images")
    print(f"Running {num_iterations} iterations...\n")
    
    for i in range(num_iterations):
        test_img = test_images[i % len(test_images)]
        
        start = time.time()
        result = model.predict(test_img)
        duration = time.time() - start
        
        monitor.record_inference_time(duration)
        
        if (i + 1) % 10 == 0:
            print(f"Iteration {i+1}/{num_iterations}")
            monitor.print_stats()
    
    print("\nBenchmark Results:")
    print("=" * 50)
    stats = monitor.get_system_stats()
    print(f"Average inference time: {stats['avg_inference_ms']:.2f}ms")
    print(f"Throughput: {1000/stats['avg_inference_ms']:.1f} images/sec")
    print(f"CPU usage: {stats['cpu_percent']:.1f}%")
    print(f"Memory usage: {stats['memory_percent']:.1f}%")

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--images', default='tests/test_images')
    parser.add_argument('--iterations', type=int, default=100)
    args = parser.parse_args()
    
    benchmark_model(args.images, args.iterations)