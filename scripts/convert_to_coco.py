#!/usr/bin/env python3
"""
Convert Plant Village Grape dataset annotations to COCO JSON format.
Supports multi-class classification (healthy, black_rot, esca, leaf_blight, background).
Structure: grapes/{subcategory}/ subdirectories.
"""

import argparse
import csv
import json
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from PIL import Image

# 子类别列表
SUBCATEGORIES = ['healthy', 'black_rot', 'esca', 'leaf_blight', 'background']

# 子类别到 label_id 的映射
SUBCATEGORY_TO_LABEL = {
    'background': 0,
    'healthy': 1,
    'black_rot': 2,
    'esca': 3,
    'leaf_blight': 4
}

def read_split_list(split_file: Path) -> List[str]:
    """Read image base names (without extension) from a split file."""
    if not split_file.exists():
        return []
    lines = [line.strip() for line in split_file.read_text(encoding="utf-8").splitlines()]
    return [line for line in lines if line]

def image_size(image_path: Path) -> Tuple[int, int]:
    """Return (width, height) for an image path using PIL."""
    try:
        with Image.open(image_path) as img:
            return img.width, img.height
    except Exception as e:
        print(f"Warning: Failed to get size for {image_path}: {e}")
        return 256, 256  # Default size

def parse_csv_boxes(csv_path: Path) -> List[Dict]:
    """Parse a single CSV file and return bounding boxes with category IDs."""
    if not csv_path.exists():
        return []
    
    boxes = []
    with csv_path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                # Support multiple column name variants
                x = float(row.get('x', row.get('xc', row.get('x_center', 0))))
                y = float(row.get('y', row.get('yc', row.get('y_center', 0))))
                width = float(row.get('width', row.get('w', row.get('dx', 0))))
                height = float(row.get('height', row.get('h', row.get('dy', 0))))
                label = int(row.get('label', row.get('class', row.get('category_id', 1))))
                
                if width > 0 and height > 0:
                    boxes.append({
                        'bbox': [x, y, width, height],
                        'area': width * height,
                        'category_id': label
                    })
            except (ValueError, KeyError):
                continue
    
    return boxes

def collect_annotations_for_split(
    category_root: Path,
    split: str,
) -> Tuple[List[Dict], List[Dict], List[Dict]]:
    """Collect COCO dictionaries for images, annotations, and categories.
    Supports structure: grapes/{subcategory}/ subdirectories.
    """
    # Try to read split file from any subcategory (they should all have the same split)
    # Use the first available subcategory's split file
    split_file = None
    for subcat in SUBCATEGORIES:
        test_split = category_root / subcat / "sets" / f"{split}.txt"
        if test_split.exists():
            split_file = test_split
            break
    
    image_stems = set(read_split_list(split_file)) if split_file else set()
    
    if not image_stems:
        # Fall back to all images if no split file
        for subcat in SUBCATEGORIES:
            images_dir = category_root / subcat / "images"
            if images_dir.exists():
                image_stems.update({p.stem for p in images_dir.glob("*.png")})
                image_stems.update({p.stem for p in images_dir.glob("*.jpg")})
                image_stems.update({p.stem for p in images_dir.glob("*.JPG")})
                image_stems.update({p.stem for p in images_dir.glob("*.bmp")})
    
    images: List[Dict] = []
    anns: List[Dict] = []
    
    # Build categories from labelmap.json if available
    categories: List[Dict] = []
    labelmap_path = category_root / "labelmap.json"
    if labelmap_path.exists():
        with open(labelmap_path, 'r', encoding='utf-8') as f:
            labelmap = json.load(f)
            for item in labelmap:
                if item['object_id'] > 0:  # Skip background (id=0)
                    categories.append({
                        "id": item['object_id'],
                        "name": item['object_name'],
                        "supercategory": "grape"
                    })
    else:
        # Fallback: create categories from subcategories
        for subcat in SUBCATEGORIES:
            label_id = SUBCATEGORY_TO_LABEL.get(subcat, 0)
            if label_id > 0:  # Skip background
                categories.append({
                    "id": label_id,
                    "name": subcat,
                    "supercategory": "grape"
                })
    
    image_id_counter = 1
    ann_id_counter = 1
    
    # Check all subcategory directories
    for stem in sorted(image_stems):
        img_path = None
        subcategory = None
        csv_path = None
        
        # Try each subcategory directory
        for subcat in SUBCATEGORIES:
            subcat_dir = category_root / subcat
            for ext in ['.png', '.jpg', '.JPG', '.PNG', '.bmp', '.BMP']:
                test_path = subcat_dir / 'images' / f"{stem}{ext}"
                if test_path.exists():
                    img_path = test_path
                    subcategory = subcat
                    csv_path = subcat_dir / 'csv' / f"{stem}.csv"
                    break
            if img_path:
                break
        
        if not img_path:
            continue
        
        width, height = image_size(img_path)
        images.append({
            "id": image_id_counter,
            "file_name": f"grapes/{subcategory}/images/{img_path.name}",
            "width": width,
            "height": height,
        })
        
        # Get category_id from subcategory
        category_id = SUBCATEGORY_TO_LABEL.get(subcategory, 1)
        
        if csv_path and csv_path.exists():
            boxes = parse_csv_boxes(csv_path)
            if boxes:
                # Use boxes from CSV
                for box in boxes:
                    anns.append({
                        "id": ann_id_counter,
                        "image_id": image_id_counter,
                        "category_id": box['category_id'],
                        "bbox": box['bbox'],
                        "area": box['area'],
                        "iscrowd": 0,
                    })
                    ann_id_counter += 1
            else:
                # No boxes in CSV, create full-image annotation for classification
                anns.append({
                    "id": ann_id_counter,
                    "image_id": image_id_counter,
                    "category_id": category_id,
                    "bbox": [0, 0, width, height],
                    "area": width * height,
                    "iscrowd": 0,
                })
                ann_id_counter += 1
        else:
            # No CSV file, create full-image annotation for classification
            anns.append({
                "id": ann_id_counter,
                "image_id": image_id_counter,
                "category_id": category_id,
                "bbox": [0, 0, width, height],
                "area": width * height,
                "iscrowd": 0,
            })
            ann_id_counter += 1
        
        image_id_counter += 1
    
    return images, anns, categories

def build_coco_dict(
    images: List[Dict],
    anns: List[Dict],
    categories: List[Dict],
    description: str,
) -> Dict:
    """Build a complete COCO dict from components."""
    return {
        "info": {
            "year": 2025,
            "version": "1.0.0",
            "description": description,
            "url": "https://www.kaggle.com/datasets/abdallahalidev/plantvillage-dataset",
        },
        "images": images,
        "annotations": anns,
        "categories": categories,
        "licenses": [],
    }

def convert(
    root: Path,
    out_dir: Path,
    category: str,
    splits: List[str],
) -> None:
    """Convert selected category and splits to COCO JSON files."""
    out_dir.mkdir(parents=True, exist_ok=True)
    
    category_root = root / category
    
    for split in splits:
        images, anns, categories = collect_annotations_for_split(
            category_root, split
        )
        desc = f"Plant Village Grape {category} {split} split"
        coco = build_coco_dict(images, anns, categories, desc)
        out_path = out_dir / f"{category}_instances_{split}.json"
        out_path.write_text(json.dumps(coco, indent=2), encoding="utf-8")
        print(f"Generated: {out_path} ({len(images)} images, {len(anns)} annotations)")

def main():
    parser = argparse.ArgumentParser(description="Convert Plant Village Grape annotations to COCO JSON")
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parent.parent,
        help="Dataset root directory",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=None,
        help="Output directory for COCO JSON files (default: <root>/annotations)",
    )
    parser.add_argument(
        "--category",
        type=str,
        default="grapes",
        help="Category name (default: grapes)",
    )
    parser.add_argument(
        "--splits",
        nargs="+",
        default=["train", "val", "test"],
        choices=["train", "val", "test"],
        help="Dataset splits to generate (default: train val test)",
    )
    
    args = parser.parse_args()
    
    if args.out is None:
        args.out = args.root / "annotations"
    
    convert(
        root=args.root,
        out_dir=args.out,
        category=args.category,
        splits=args.splits,
    )

if __name__ == "__main__":
    main()
