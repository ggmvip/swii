import numpy as np
import os

class Settings:
    """
    Configuration settings for barcode/QR detection system
    """
    
    model = {
        "size":                 416,  # image size - model w/ square images
        "anchors":              np.array([(10, 14), (23, 27), (37, 58),
                                        (81, 82), (135, 169), (344, 319)],
                                        np.float32) / 416,
        "masks":                np.array([[3, 4, 5], [0, 1, 2]]),
        "score_threshold":      float(os.getenv('YOLO_CONFIDENCE', 0.5)),
        "iou_threshold":        float(os.getenv('YOLO_IOU', 0.3)),
        "max_boxes":            5,
        "weights":              os.getenv('MODEL_PATH', 
                                         "data/model/yolov3_train_class2_final.weights.h5"),
    }
    
    train = {
        "batch_size":           int(os.getenv('BATCH_SIZE', 32)),
        "learning_rate":        float(os.getenv('LEARNING_RATE', 1e-3)),
        "epochs":               int(os.getenv('EPOCHS', 100)),
        "weights_num_classes":  80,  # Transfer learning with different nb classes
        
        # Updated paths for Week 2 TFRecords
        "train_dataset":        os.getenv('TRAIN_TFRECORD', "data/train.tf_record"),
        "val_dataset":          os.getenv('VAL_TFRECORD', "data/val.tf_record"),
        "test_dataset":         os.getenv('TEST_TFRECORD', "data/test.tf_record"),
        
        "classes":              "data/classes.csv",
        "pretrained_weights":   "checkpoints/yolov3-tiny.weights.h5",  
        "final_weights":        "data/model/yolov3_train_final_2class.weights.h5",
        "checkpoints":          os.getenv('CHECKPOINT_DIR', "checkpoints/") + "yolov3_train_2class_{epoch}.weights.h5",
        "logs":                 os.getenv('LOG_DIR', "logs/"),
        "run_eagerly":          True  # Set to True for debugging
    }
    
    # Class names for barcode/QR detection
    class_names = ["Barcode", "QR"]
    
    # Week 2: Data augmentation settings
    augmentation = {
        "enabled":              True,
        "brightness_range":     (0.8, 1.2),
        "contrast_range":       (0.8, 1.2),
        "rotation_range":       15,  # degrees
        "horizontal_flip":      True,
        "zoom_range":           (0.9, 1.1),
        "apply_to_training":    True,
        "apply_to_validation":  False,
    }
    
    # Camera settings
    camera = {
        "width":                int(os.getenv('CAMERA_WIDTH', 1280)),
        "height":               int(os.getenv('CAMERA_HEIGHT', 720)),
        "fps":                  int(os.getenv('CAMERA_FPS', 30)),
    }
    
    # API settings
    api = {
        "openfoodfacts_timeout": int(os.getenv('OPENFOODFACTS_TIMEOUT', 5)),
        "cache_enabled":         os.getenv('API_CACHE_ENABLED', 'true').lower() == 'true',
        "cache_ttl":             int(os.getenv('API_CACHE_TTL', 3600)),
        "cache_max_size":        500,
    }
