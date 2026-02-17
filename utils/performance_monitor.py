import time
import psutil
from collections import deque

class PerformanceMonitor:
    def __init__(self, window_size=100):
        self.fps_history = deque(maxlen=window_size)
        self.inference_times = deque(maxlen=window_size)
        self.last_time = time.time()
        self.frame_count = 0
    
    def update_fps(self):
        current_time = time.time()
        fps = 1.0 / (current_time - self.last_time)
        self.fps_history.append(fps)
        self.last_time = current_time
        self.frame_count += 1
    
    def record_inference_time(self, duration):
        self.inference_times.append(duration)
    
    def get_average_fps(self):
        if not self.fps_history:
            return 0
        return sum(self.fps_history) / len(self.fps_history)
    
    def get_average_inference_time(self):
        if not self.inference_times:
            return 0
        return sum(self.inference_times) / len(self.inference_times)
    
    def get_system_stats(self):
        return {
            'cpu_percent': psutil.cpu_percent(),
            'memory_percent': psutil.virtual_memory().percent,
            'avg_fps': self.get_average_fps(),
            'avg_inference_ms': self.get_average_inference_time() * 1000
        }
    
    def print_stats(self):
        stats = self.get_system_stats()
        print(f"FPS: {stats['avg_fps']:.1f} | "
              f"Inference: {stats['avg_inference_ms']:.1f}ms | "
              f"CPU: {stats['cpu_percent']:.1f}% | "
              f"RAM: {stats['memory_percent']:.1f}%")