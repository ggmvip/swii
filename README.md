# Barcode & QR Code Detection System

A deep learning system that detects and decodes barcodes and QR codes using a custom-trained Tiny YOLO v3 model, PyZbar, and the OpenFoodFacts API. Runs locally or via a Hugging Face cloud inference endpoint, with support for desktop, NVIDIA Jetson Nano, and Raspberry Pi.

---

## Project Description

The pipeline works in three stages:

1. **Detection** — A Tiny YOLO v3 model (2 classes: `Barcode`, `QR`) processes images at 416×416 resolution and outputs bounding boxes.
2. **Decoding** — PyZbar reads the detected code from the image and returns the raw data string and code type.
3. **Product Lookup** — If the decoded data is numeric, the OpenFoodFacts API is queried to retrieve product information.

The trained model is exported to ONNX format for CPU inference via `onnxruntime`. A Gradio app (`app.py`) exposes the pipeline as a web interface. A live camera mode (`hg_cloud_inference.py`) adds motion-triggered scanning and logs detections to CSV.

---

## Repository Structure

```
swii/
├── app.py                    # Gradio web app (ONNX inference + PyZbar + OpenFoodFacts)
├── barcode.py                # PyZbar decoding helper
├── camera_app.py             # Live camera application
├── hg_cloud_inference.py     # Motion-triggered camera detector (cloud or local inference)
├── export_yolo_to_onnx.py    # Convert trained .h5 weights to ONNX format
├── platform_config.py        # Auto-detects platform and camera source (Jetson/RPi/Desktop)
├── settings.py               # Model and training configuration
├── streamlit.py              # (Legacy) Streamlit app
├── test_detection.py         # End-to-end test suite (8 tests)
├── requirements.txt          # Python dependencies
├── docker_requirements.txt   # Docker-specific dependencies
├── Dockerfile                # Docker image definition
├── run_docker.sh             # Docker run helper script
├── data/                     # Datasets, model weights, TFRecords
├── model/                    # TinyYolo model definition (tiny_yolo.py)
├── notebooks/                # Training and experimentation notebooks
├── preprocessing/            # Dataset preparation scripts
├── scripts/                  # Utility scripts
├── sparkfun/                 # SparkFun hardware integration
└── docs/                     # Documentation
```

---

## Prerequisites

- Python 3.12+
- `libzbar0` (Linux) or `zbar` (Mac) for PyZbar
- Trained ONNX model file: `yolo_barcode_detector.onnx` (generated from `export_yolo_to_onnx.py`)
- For Jetson Nano: TensorFlow must be installed separately (see `requirements.txt` notes)
- For Raspberry Pi: use `opencv-python-headless` instead of `opencv-python`

---

## Installation

**1. Install system dependency for PyZbar**

Linux:
```bash
sudo apt-get install libzbar0
```

Mac (requires Homebrew):
```bash
brew install zbar
```

Windows: zbar DLLs are bundled with the Python wheels automatically.

**2. Clone the repository**

```bash
git clone https://github.com/ggmvip/swii.git
cd swii
```

**3. Install Python dependencies**

```bash
pip install -r requirements.txt
```

---

## Running the Gradio App

`app.py` is the main inference entry point. It loads the ONNX model, runs detection via ONNX Runtime (CPU), decodes with PyZbar, and queries OpenFoodFacts.

```bash
python app.py
```

The Gradio interface opens in your browser. Upload an image and the app returns a JSON result:

```json
{
  "status": "success",
  "code_data": "3017620422003",
  "code_type": "EAN13",
  "product_name": "Nutella",
  "confidence": 1.0
}
```

**Note:** The ONNX model file `yolo_barcode_detector.onnx` must be present in the project root. Generate it with `export_yolo_to_onnx.py` after training (see Training section).

---

## Live Camera Mode

`hg_cloud_inference.py` runs continuous camera detection with motion triggering. It can route inference to a Hugging Face Space (cloud) or run locally.

```bash
python hg_cloud_inference.py
```

**Configuration (top of file):**

| Variable | Default | Description |
|---|---|---|
| `USE_CLOUD_INFERENCE` | `True` | Set to `False` to use local TinyYolo model |
| `CLOUD_SPACE_ID` | `fotonlink/barcode-detector` | Hugging Face Space ID |
| `MOTION_SENSITIVITY` | `25` | Pixel difference threshold (lower = more sensitive) |
| `MOTION_AREA_THRESHOLD` | `500` | Pixel count required to trigger a scan |
| `UPLOAD_COOLDOWN` | `2.0` | Seconds between cloud uploads |

Detection logs are saved to `logs/csvs/` and captured frames to `logs/images/`. Press `q` to quit.

---

## Configuration

`settings.py` contains all model and training parameters. Key values:

```python
class Settings:
    model = {
        "size": 416,             # Input image size
        "score_threshold": 0.5,  # Detection confidence threshold
        "iou_threshold": 0.3,    # Non-maximum suppression threshold
        "max_boxes": 5,
        "weights": "data/model/yolov3_train_class2_final.weights.h5",
    }
    train = {
        "batch_size": 32,
        "learning_rate": 1e-3,
        "epochs": 100,
        "weights_num_classes": 80,   # Pretrained COCO weights (transfer learning)
        "train_dataset": "data/train_barcode_qr.tf_record",
        "val_dataset":   "data/val_barcode_qr.tf_record",
        "classes": "data/classes.csv",
        "pretrained_weights": "checkpoints/yolov3-tiny.weights.h5",
        "final_weights": "data/model/yolov3_train_final_2class.weights.h5",
    }

    class_names = ["Barcode", "QR"]
```

Adjust `score_threshold` and `iou_threshold` to tune detection sensitivity before running the app.

---

## Platform & Camera Auto-Detection

`platform_config.py` auto-detects your hardware and selects the appropriate camera source. No manual configuration needed in most cases.

| Platform | Auto-Detection Method | Camera Source |
|---|---|---|
| NVIDIA Jetson | `/etc/nv_tegra_release` | CSI (GStreamer) → USB fallback |
| Raspberry Pi | `/proc/device-tree/model` | USB auto-scan |
| Desktop | Default | USB auto-scan (`/dev/video*`) |

**Environment variable overrides:**

```bash
# Override platform
export PLATFORM_OVERRIDE=jetson   # or 'rpi', 'desktop'

# Override camera source
export CAMERA_SOURCE=0            # Camera index or GStreamer pipeline string

# Force USB even on Jetson
export FORCE_USB=1
```

**Quick camera test:**

```bash
python platform_config.py
```

---

## Training

**1. Prepare your dataset** (place images in `data/curated_dataset/`)

```bash
python preprocessing/prepare_dataset.py
```

**2. Convert to TFRecord format**

```bash
python preprocessing/convert_to_tfrecord.py
```

**3. Train the model**

Training configuration is set in `settings.py`. Run training via the notebooks in `notebooks/` or directly using the model module:

```python
from model.tiny_yolo import TinyYolo

model = TinyYolo(classes=2, training=True)
```

**4. Export trained weights to ONNX**

Once training is complete and weights are saved to `data/model/yolov3_train_class2_final.weights.h5`:

```bash
python export_yolo_to_onnx.py
```

This generates `yolo_barcode_detector.onnx` in the project root, which is loaded by `app.py`.

---

## Testing

`test_detection.py` runs 8 end-to-end tests covering imports, platform detection, model loading, camera access, barcode decoding, CSV logging, model inference, and API connectivity.

```bash
python test_detection.py
```

Example output:

```
╔════════════════════════════════════════════════════════════╗
║     Barcode/QR Detection System - Testing Suite           ║
╚════════════════════════════════════════════════════════════╝

  ✓ PASS: Package Imports
  ✓ PASS: Platform Detection
  ✓ PASS: Model Loading
  ✓ PASS: Camera Access
  ✓ PASS: Barcode/QR Decoding
  ✓ PASS: CSV Logging
  ✓ PASS: Model Inference
  ✓ PASS: API Connection

  Total: 8/8 tests passed
```

---

## Docker

A `Dockerfile` and `run_docker.sh` are provided for containerised deployment.

```bash
# Build image
docker build -t barcode-detector .

# Run with the helper script
bash run_docker.sh
```

For Jetson Nano, TensorFlow must be installed from NVIDIA's embedded package index. See the notes in `requirements.txt`.

---

## Dependencies

Core packages from `requirements.txt`:

| Package | Version |
|---|---|
| tensorflow | 2.16.1 |
| opencv-python | 4.10.0.84 |
| Pillow | 11.3.0 |
| pyzbar | 0.1.9 |
| onnx | 1.17.0 |
| tf2onnx | 1.16.1 |
| onnxruntime | (latest) |
| gradio_client | (latest) |
| numpy | 1.26.4 |
| requests | 2.32.5 |
| streamlit | 1.50.0 |
| tensorboard | 2.16.1 |

---

## References

- Keras Tiny YOLO v3 implementation: https://github.com/zzh8829/yolov3-tf2
- OpenFoodFacts API: https://world.openfoodfacts.org
- Hugging Face Space (cloud inference): https://huggingface.co/spaces/fotonlink/barcode-detector