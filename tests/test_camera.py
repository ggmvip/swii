#!/usr/bin/env python3
"""
Camera Hardware Validation
"""

import sys
import cv2
from utils.camera_utils import init_camera, test_camera_capture


def test_camera():
    """Test camera hardware"""
    print("="*60)
    print("CAMERA HARDWARE VALIDATION")
    print("="*60)
    
    # Initialize camera
    print("[TEST 1] Initializing camera...")
    camera, platform = init_camera()
    
    if not camera.isOpened():
        print("FAILED: Camera not opened")
        return False
    
    print(f"✓ Camera opened on platform: {platform}")
    
    # Test frame capture
    print("[TEST 2] Testing frame capture...")
    success, result = test_camera_capture(camera, num_frames=30)
    
    if not success:
        print(f"FAILED: {result}")
        camera.release()
        return False
    
    print(f"✓ Capture successful")
    print(f"  Average capture time: {result['avg_capture_time']*1000:.2f}ms")
    print(f"  Estimated FPS: {result['estimated_fps']:.1f}")
    print(f"  Frame shape: {result['frame_shape']}")
    
    # Check target specs
    target_fps = 30
    target_latency = 100  # ms
    
    actual_latency = result['avg_capture_time'] * 1000
    
    print("[TEST 3] Checking specifications...")
    if result['estimated_fps'] >= target_fps * 0.9:  # 90% of target
        print(f"✓ FPS meets target ({target_fps} FPS)")
    else:
        print(f"⚠ FPS below target: {result['estimated_fps']:.1f} < {target_fps}")
    
    if actual_latency < target_latency:
        print(f"✓ Latency meets target (<{target_latency}ms)")
    else:
        print(f"⚠ Latency above target: {actual_latency:.1f}ms")
    
    camera.release()
    
    print("" + "="*60)
    print("CAMERA VALIDATION COMPLETE")
    print("="*60)
    
    return True


if __name__ == "__main__":
    success = test_camera()
    sys.exit(0 if success else 1)
