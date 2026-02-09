# sweii

**Reverse Vending Machine Project**

## Quick Start

### Prerequisites

- Python 3.8+
- NVIDIA Jetson Nano (or GPU-enabled system)
- Camera (CSI or USB)
- 10GB+ disk space
- Curated dataset

### 1. Environment Setup

```bash
# Clone repository
git clone https://github.com/ggmvip/swii.git
cd swii

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run environment setup script
bash scripts/setup_environment.sh
```

### 2. Configuration

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your settings
nano .env
```

### 3. Docker Setup

```bash
# Build Docker image
docker-compose build

# Test Docker container
docker-compose run --rm barcode-detector python3 --version

# Run with GPU and camera access
docker-compose up
```

---

### Development Environment Setup

**Script**: `scripts/setup_environment.sh`

```bash
bash scripts/setup_environment.sh
```

### Docker Environment for Jetson

**Files**: `Dockerfile`, `docker-compose.yml`

```bash
docker-compose build
docker-compose run --rm barcode-detector bash
```

### Camera Hardware Validation

**Test**: `tests/test_camera.py`

```bash
python3 tests/test_camera.py
```

### Current YOLO Model Evaluation

**Test**: `tests/test_model_baseline.py`

```bash
python3 tests/test_model_baseline.py --dataset data/test_images/
```

### PyZbar Baseline Testing

**Test**: `tests/test_pyzbar_baseline.py`

```bash
python3 tests/test_pyzbar_baseline.py --dataset data/test_images/
```

### OpenFoodFacts API Wrapper

**Module**: `api/openfoodfacts.py`

```python
from api.openfoodfacts import OpenFoodFactsClient

client = OpenFoodFactsClient()
product = client.get_product_info("3017620422003")
print(product)
```

### Dataset Split for Training

**Script**: `preprocessing/prepare_dataset.py`

```bash
python3 preprocessing/prepare_dataset.py \
    --input data/curated_dataset/ \
    --output data/ \
    --train-ratio 0.7 \
    --val-ratio 0.15 \
    --test-ratio 0.15
```

### TFRecord Generation Pipeline

**Script**: `preprocessing/convert_to_tfrecord.py`

```bash
python3 preprocessing/convert_to_tfrecord.py
```

### Data Augmentation Pipeline

**Module**: `preprocessing/augmentation.py`

```python
from preprocessing.augmentation import AugmentationPipeline

augmentor = AugmentationPipeline()
augmented_image = augmentor.augment(image, bboxes)
```

### Training Configuration Setup

**File**: `config/settings.py`

Edit `config/settings.py` to configure training parameters.

### Training Infrastructure Validation

**Script**: `scripts/validate_training.py`

```bash
python3 scripts/validate_training.py
```

### API Caching Layer

**Module**: `api/cache.py`

```python
from api.openfoodfacts import OpenFoodFactsClient

client = OpenFoodFactsClient(use_cache=True)
product = client.get_product_info("3017620422003")  # Cached
```

---

## Running All Tests

### Run Baseline Tests

```bash
python3 scripts/run_baseline_tests.py
```

### Prepare Training Data

```bash
bash scripts/prepare_training_data.sh
```

### Validate Training Setup

```bash
python3 scripts/validate_training.py
```
