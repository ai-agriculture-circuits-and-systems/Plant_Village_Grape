# Plant Village Grape

[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-green?logo=creativecommons&logoColor=white)](https://creativecommons.org/licenses/by/4.0/)
[![Version](https://img.shields.io/badge/version-1.0.0-blue?logo=semver&logoColor=white)](https://github.com/your-repo/Plant_Village_Grape)
[![GitHub stars](https://img.shields.io/github/stars/your-repo/Plant_Village_Grape?style=flat&logo=github&label=Stars&color=orange&labelColor=orange&logoColor=white)](https://github.com/your-repo/Plant_Village_Grape)
[![GitHub forks](https://img.shields.io/github/forks/your-repo/Plant_Village_Grape?style=flat&logo=github&label=Forks&color=yellow&labelColor=yellow&logoColor=white)](https://github.com/your-repo/Plant_Village_Grape)
[![GitHub watchers](https://img.shields.io/github/watchers/your-repo/Plant_Village_Grape?style=flat&logo=github&label=Watchers&color=cyan&labelColor=cyan&logoColor=white)](https://github.com/your-repo/Plant_Village_Grape)
[![GitHub issues](https://img.shields.io/github/issues/your-repo/Plant_Village_Grape?style=flat&logo=github&label=Issues&color=red&labelColor=red&logoColor=white)](https://github.com/your-repo/Plant_Village_Grape/issues)
[![GitHub pull requests](https://img.shields.io/github/issues-pr/your-repo/Plant_Village_Grape?style=flat&logo=github&label=PRs&color=lime&labelColor=lime&logoColor=white)](https://github.com/your-repo/Plant_Village_Grape/pulls)
[![GitHub contributors](https://img.shields.io/github/contributors/your-repo/Plant_Village_Grape?style=flat&logo=github&label=Contributors&color=purple&labelColor=purple&logoColor=white)](https://github.com/your-repo/Plant_Village_Grape/graphs/contributors)
[![GitHub last commit](https://img.shields.io/github/last-commit/your-repo/Plant_Village_Grape?style=flat&logo=github&label=Last%20Commit&color=gray&labelColor=gray&logoColor=white)](https://github.com/your-repo/Plant_Village_Grape/commits)
[![DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.xxxxx-indigo?logo=doi&logoColor=white)](https://doi.org/10.5281/zenodo.xxxxx)

Grape leaf images labeled for disease classification. This dataset contains images of grape leaves with various diseases and healthy samples. This folder now follows the standardized layout used by `acfr-multifruit-2016`.

- **Project page**: `https://www.kaggle.com/datasets/abdallahalidev/plantvillage-dataset`
- **Original paper**: `https://arxiv.org/abs/1511.08060`
- **Dataset repository**: `https://www.kaggle.com/datasets/abdallahalidev/plantvillage-dataset`

## TL;DR

- **Task**: Classification, Object Detection
- **Modality**: RGB
- **Platform**: Ground
- **Real/Synthetic**: Real
- **Images**: 10,410 labeled images
- **Classes**: 5 categories
  - `healthy`: 846 images
  - `black_rot`: 2,360 images
  - `esca`: 2,766 images
  - `leaf_blight`: 2,152 images
  - `background`: 2,286 images
- **Resolution**: 256×256 pixels
- **Annotations**: COCO JSON (image-level via full-image boxes or object detection boxes)
- **Total annotations**: 10,410 (one per image for classification)
- **License**: CC BY 4.0 (see LICENSE)
- **Citation**: See below

## Table of Contents
- [Download](#download)
- [Dataset Structure](#dataset-structure)
- [Sample Images](#sample-images)
- [Annotation Schema](#annotation-schema)
- [Stats and Splits](#stats-and-splits)
- [Quick Start](#quick-start)
- [Evaluation and Baselines](#evaluation-and-baselines)
- [Datasheet (Data Card)](#datasheet-data-card)
- [Known Issues and Caveats](#known-issues-and-caveats)
- [License](#license)
- [Citation](#citation)
- [Changelog](#changelog)
- [Contact](#contact)

## Download

- **Original dataset**: `https://www.kaggle.com/datasets/abdallahalidev/plantvillage-dataset`
- **This repository**: Hosts structure and conversion scripts only; place the downloaded folders under this directory.
- **Local license file**: See `LICENSE` (CC BY 4.0).

## Dataset Structure

This dataset follows the standardized dataset structure specification with subcategory organization:

```
Plant_Village_Grape/
├── grapes/
│   ├── healthy/              # Healthy grape leaf images
│   │   ├── csv/              # CSV annotations per image
│   │   ├── json/             # Original JSON annotations
│   │   ├── images/           # Healthy images
│   │   └── sets/             # Dataset splits
│   ├── black_rot/            # Black rot disease images
│   │   ├── csv/
│   │   ├── json/
│   │   ├── images/
│   │   └── sets/
│   ├── esca/                 # Esca (Black Measles) disease images
│   │   ├── csv/
│   │   ├── json/
│   │   ├── images/
│   │   └── sets/
│   ├── leaf_blight/          # Leaf blight (Isariopsis Leaf Spot) images
│   │   ├── csv/
│   │   ├── json/
│   │   ├── images/
│   │   └── sets/
│   ├── background/           # Background images without leaves
│   │   ├── csv/
│   │   ├── images/
│   │   └── sets/
│   ├── labelmap.json        # Label mapping
│   └── sets/                 # (Optional) Combined dataset splits
├── annotations/              # COCO format JSON (generated)
│   ├── grapes_instances_train.json
│   ├── grapes_instances_val.json
│   └── grapes_instances_test.json
├── scripts/
│   ├── reorganize_dataset.py # Dataset reorganization script
│   └── convert_to_coco.py    # COCO conversion script
├── LICENSE
├── README.md
└── requirements.txt
```

- Splits: `grapes/{subcategory}/sets/train.txt`, `grapes/{subcategory}/sets/val.txt`, `grapes/{subcategory}/sets/test.txt` list image basenames (no extension). If missing, all images are used.

## Sample Images

Below are example images for each category in this dataset. Paths are relative to this README location.

<table>
  <tr>
    <th>Category</th>
    <th>Sample</th>
  </tr>
  <tr>
    <td><strong>Healthy</strong></td>
    <td>
      <img src="grapes/healthy/images/image (100).JPG" alt="Healthy example" width="260"/>
      <div align="center"><code>grapes/healthy/images/image (100).JPG</code></div>
    </td>
  </tr>
  <tr>
    <td><strong>Black Rot</strong></td>
    <td>
      <img src="grapes/black_rot/images/image (100).JPG" alt="Black rot example" width="260"/>
      <div align="center"><code>grapes/black_rot/images/image (100).JPG</code></div>
    </td>
  </tr>
  <tr>
    <td><strong>Esca (Black Measles)</strong></td>
    <td>
      <img src="grapes/esca/images/image (100).JPG" alt="Esca example" width="260"/>
      <div align="center"><code>grapes/esca/images/image (100).JPG</code></div>
    </td>
  </tr>
  <tr>
    <td><strong>Leaf Blight</strong></td>
    <td>
      <img src="grapes/leaf_blight/images/image (100).JPG" alt="Leaf blight example" width="260"/>
      <div align="center"><code>grapes/leaf_blight/images/image (100).JPG</code></div>
    </td>
  </tr>
  <tr>
    <td><strong>Background</strong></td>
    <td>
      <img src="grapes/background/images/image (1).JPG" alt="Background example" width="260"/>
      <div align="center"><code>grapes/background/images/image (1).JPG</code></div>
    </td>
  </tr>
</table>

## Annotation Schema

- **CSV per-image schema** (stored under `grapes/{subcategory}/csv/` folder):
  - Columns: `item, x, y, width, height, label`
  - Coordinates: `(x, y)` is top-left corner, `width` and `height` in pixels
  - Label: category ID (1=healthy, 2=black_rot, 3=esca, 4=leaf_blight, 0=background)
  
- **COCO-style** (generated):

```json
{
  "info": {
    "year": 2025,
    "version": "1.0.0",
    "description": "Plant Village Grape grapes train split"
  },
  "images": [
    {
      "id": 1,
      "file_name": "grapes/healthy/images/image (100).JPG",
      "width": 256,
      "height": 256
    }
  ],
  "annotations": [
    {
      "id": 1,
      "image_id": 1,
      "category_id": 1,
      "bbox": [0, 0, 256, 256],
      "area": 65536,
      "iscrowd": 0
    }
  ],
  "categories": [
    {"id": 1, "name": "healthy", "supercategory": "grape"},
    {"id": 2, "name": "black_rot", "supercategory": "grape"},
    {"id": 3, "name": "esca", "supercategory": "grape"},
    {"id": 4, "name": "leaf_blight", "supercategory": "grape"}
  ]
}
```

- **Label maps**: `grapes/labelmap.json` defines the category mapping:

```json
[
  {"object_id": 0, "label_id": 0, "keyboard_shortcut": "0", "object_name": "background"},
  {"object_id": 1, "label_id": 1, "keyboard_shortcut": "1", "object_name": "healthy"},
  {"object_id": 2, "label_id": 2, "keyboard_shortcut": "2", "object_name": "black_rot"},
  {"object_id": 3, "label_id": 3, "keyboard_shortcut": "3", "object_name": "esca"},
  {"object_id": 4, "label_id": 4, "keyboard_shortcut": "4", "object_name": "leaf_blight"}
]
```

## Stats and Splits

### Image counts by category

| Category | Images |
|----------|--------|
| Healthy | 846 |
| Black Rot | 2,360 |
| Esca | 2,766 |
| Leaf Blight | 2,152 |
| Background | 2,286 |
| **Total** | **10,410** |

### Dataset splits

Splits provided via `grapes/{subcategory}/sets/*.txt`. You may define your own splits by editing those files.

| Split | Images (approximate) |
|-------|---------------------|
| Train | ~534 |
| Val | ~112 |
| Test | ~751 |

Note: The splits are distributed across all subcategories. Each subcategory has its own split files.

## Quick Start

### Using COCO API

```python
from pycocotools.coco import COCO
import json

# Load COCO annotations
coco = COCO('annotations/grapes_instances_train.json')

# Get all image IDs
img_ids = coco.getImgIds()
print(f"Total images: {len(img_ids)}")

# Get all category IDs
cat_ids = coco.getCatIds()
categories = [coco.loadCats([id])[0]['name'] for id in cat_ids]
print(f"Categories: {categories}")

# Load a specific image and its annotations
img_id = img_ids[0]
img_info = coco.loadImgs([img_id])[0]
ann_ids = coco.getAnnIds(imgIds=[img_id])
anns = coco.loadAnns(ann_ids)

print(f"Image: {img_info['file_name']}")
print(f"Size: {img_info['width']}x{img_info['height']}")
print(f"Annotations: {len(anns)}")
```

### Converting to COCO format

If you need to regenerate COCO annotations from CSV files:

```bash
python scripts/convert_to_coco.py --root . --out annotations \
    --category grapes --splits train val test
```

### Dependencies

**Required**:
- `Pillow>=9.5` (for image processing)

**Optional**:
- `pycocotools>=2.0.7` (for COCO API)

Install with:
```bash
pip install -r requirements.txt
```

## Evaluation and Baselines

- **Primary metric**: 
  - Classification: Accuracy, Precision, Recall, F1-score (per class and macro-averaged)
  - Object Detection: mAP@[.50:.95], mAP@.50, mAP@.75
- **Baseline results**: (to be added)

## Datasheet (Data Card)

### Motivation

This dataset was created to support research in plant disease detection and classification, specifically for grape leaf diseases, which is crucial for automated disease detection in agricultural applications.

### Composition

The dataset consists of:
- **Image types**: RGB images of grape leaves
- **Categories**: 5 classes (healthy, black_rot, esca, leaf_blight, background)
- **Annotation format**: Image-level classification annotations (via full-image bounding boxes) and object-level detection annotations

### Collection Process

- **Source**: Images collected from various sources and processed to a standardized format
- **Annotation tool**: Images annotated for classification and detection tasks
- **Validation**: Images resized to 256×256 pixels

### Preprocessing

- Images resized to 256×256 pixels
- Annotations converted to standardized CSV and COCO formats
- Dataset reorganized to follow standard structure

### Distribution

- Dataset is distributed under CC BY 4.0 license
- Original data available on Kaggle under the Plant Village dataset collection
- This repository provides standardized structure and conversion scripts

### Maintenance

- Dataset structure has been standardized according to the dataset structure specification
- COCO format annotations are generated from CSV files using the provided conversion script

## Known Issues and Caveats

1. **File naming**: Original images were renamed to `image (N).JPG` format during processing. Original filenames are preserved in JSON annotations as `pvc_filename` field.

2. **Background category**: The background category may not have JSON annotations, as it represents images without leaves.

3. **Split files**: The split files in `all/` directory use original Plant Village filenames. The reorganization script maps these to the new filenames using the `pvc_filename` field in JSON files.

4. **Coordinate system**: Bounding box coordinates use top-left origin (x, y) with width and height.

5. **Classification vs Detection**: This dataset can be used for both classification (using full-image bounding boxes) and object detection (using specific bounding boxes in CSV files).

## License

This dataset is licensed under the Creative Commons Attribution 4.0 International License (CC BY 4.0).

Check the original dataset terms and cite appropriately.

See `LICENSE` file for full license text.

## Citation

If you use this dataset, please cite:

```bibtex
@misc{plantvillage_grape,
  title={Plant Village Grape Dataset},
  author={Plant Village},
  year={2025},
  url={https://www.kaggle.com/datasets/abdallahalidev/plantvillage-dataset},
  note={Standardized structure version}
}
```

Original Plant Village dataset citation:
```bibtex
@article{plantvillage,
  title={Plant Village Dataset},
  author={Hughes, David and Salathé, Marcel},
  journal={arXiv preprint arXiv:1511.08060},
  year={2015}
}
```

## Changelog

- **V1.0.0** (2025): Initial standardized structure and COCO conversion utility

## Contact

- **Maintainers**: Open to contributions via issue tracker
- **Original authors**: Plant Village Contributors (David Hughes, Marcel Salathé)
- **Source**: `https://www.kaggle.com/datasets/abdallahalidev/plantvillage-dataset`
