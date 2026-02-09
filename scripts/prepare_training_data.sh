#!/bin/bash
# Complete data preparation pipeline for

set -e

echo "========================================="
echo "Data Preparation Pipeline"
echo "========================================="

# Dataset Split
echo "
[1/4] Splitting dataset..."
python3 preprocessing/prepare_dataset.py \
    --input data/curated_dataset/ \
    --output data/ \
    --train-ratio 0.7 \
    --val-ratio 0.15 \
    --test-ratio 0.15

echo "✓ Dataset split complete"

# TFRecord Generation
echo "
[2/4] Generating TFRecords..."
python3 preprocessing/convert_to_tfrecord.py

echo "✓ TFRecords generated"

# Test Augmentation
echo "
[3/4] Testing data augmentation..."
python3 preprocessing/augmentation.py --test

echo "✓ Augmentation pipeline validated"

# Validate Training Setup
echo "
[4/4] Validating training infrastructure..."
python3 scripts/validate_training.py

echo "
========================================="
echo "Data preparation complete!"
echo "========================================="
echo "
Generated files:"
echo "  - data/train.tf_record"
echo "  - data/val.tf_record"
echo "  - data/test.tf_record"
echo "
Next: Start training with"
