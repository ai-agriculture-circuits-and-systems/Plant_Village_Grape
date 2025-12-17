# Plant Village Grape

[![DOI](https://img.shields.io/badge/DOI-pending-lightgrey)](#citation)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-blue.svg)](https://creativecommons.org/licenses/by/4.0/)
[![Version](https://img.shields.io/badge/version-1.0.0-blue)](#changelog)

Grape leaf images labeled for disease classification. This dataset contains images of grape leaves with various diseases and healthy samples. This folder now follows the standardized layout used by `acfr-multifruit-2016`.

- Project page: `https://www.kaggle.com/datasets/abdallahalidev/plantvillage-dataset`
- Issue tracker: use this repo

## TL;DR
- Task: classification (five classes: `healthy`, `black_rot`, `esca`, `leaf_blight`, `background`)
- Modality: RGB
- Platform: handheld/field
- Real/Synthetic: real
- Images: 10,410 total
- Classes: 5
- Resolution: 256×256 pixels
- Annotations: COCO JSON (image-level via full-image boxes or object detection boxes)
- License: CC BY 4.0 (see License)
- Citation: see below

## Table of contents
- [Download](#download)
- [Dataset structure](#dataset-structure)
- [Sample images](#sample-images)
- [Annotation schema](#annotation-schema)
- [Stats and splits](#stats-and-splits)
- [Quick start](#quick-start)
- [Evaluation and baselines](#evaluation-and-baselines)
- [Datasheet (data card)](#datasheet-data-card)
- [Known issues and caveats](#known-issues-and-caveats)
- [License](#license)
- [Citation](#citation)
- [Changelog](#changelog)
- [Contact](#contact)

## Download
- Original dataset: `https://www.kaggle.com/datasets/abdallahalidev/plantvillage-dataset`
- This repo hosts structure and conversion scripts only; place the downloaded folders under this directory.
- Local license file: see `LICENSE` (Creative Commons Attribution 4.0).

## Dataset structure

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

## Sample images

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

## Annotation schema

### CSV format

Each image has a corresponding CSV file in `grapes/{subcategory}/csv/{image_name}.csv`:

```csv
#item,x,y,width,height,label
0,83,218,40,38,1
1,158,180,30,35,1
```

- Columns: `item`, `x`, `y`, `width`, `height`, `label`
- Coordinates: `(x, y)` is top-left corner, `width` and `height` in pixels
- Label: category ID (1=healthy, 2=black_rot, 3=esca, 4=leaf_blight, 0=background)

### COCO format

The COCO JSON files are generated by `scripts/convert_to_coco.py`:

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

### Label maps

The `grapes/labelmap.json` file defines the category mapping:

```json
[
  {"object_id": 0, "label_id": 0, "keyboard_shortcut": "0", "object_name": "background"},
  {"object_id": 1, "label_id": 1, "keyboard_shortcut": "1", "object_name": "healthy"},
  {"object_id": 2, "label_id": 2, "keyboard_shortcut": "2", "object_name": "black_rot"},
  {"object_id": 3, "label_id": 3, "keyboard_shortcut": "3", "object_name": "esca"},
  {"object_id": 4, "label_id": 4, "keyboard_shortcut": "4", "object_name": "leaf_blight"}
]
```

## Stats and splits

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

## Quick start

### Using COCO API

```python
from pycocotools.coco import COCO
import matplotlib.pyplot as plt

# Load annotations
coco = COCO('annotations/grapes_instances_train.json')

# Get image IDs
img_ids = coco.getImgIds()
print(f"Number of images: {len(img_ids)}")

# Get category IDs
cat_ids = coco.getCatIds()
print(f"Categories: {coco.loadCats(cat_ids)}")

# Load and display an image
img_id = img_ids[0]
img_info = coco.loadImgs(img_id)[0]
ann_ids = coco.getAnnIds(imgIds=img_id)
anns = coco.loadAnns(ann_ids)

print(f"Image: {img_info['file_name']}")
print(f"Annotations: {len(anns)}")
```

### Converting to COCO format

```bash
python scripts/convert_to_coco.py --root . --out annotations \
    --category grapes --splits train val test
```

### Dependencies

**Required:**
- Python 3.7+
- Pillow>=9.5

**Optional (for COCO API):**
- pycocotools>=2.0.7

Install with:
```bash
pip install -r requirements.txt
```

## Evaluation and baselines

- **Task**: Multi-class classification
- **Metrics**: Accuracy, Precision, Recall, F1-score
- **Baselines**: (To be added)

## Datasheet (data card)

### Motivation
This dataset was created to support research in plant disease detection and classification, specifically for grape leaf diseases. It is part of the larger Plant Village dataset collection.

### Composition
- **Image types**: RGB images of grape leaves
- **Categories**: 5 classes (healthy, black_rot, esca, leaf_blight, background)
- **Image format**: JPG
- **Resolution**: 256×256 pixels

### Collection process
Images were collected from various sources and processed to a standardized format. Some images may have been augmented or preprocessed.

### Preprocessing
- Images resized to 256×256 pixels
- Annotations converted to standardized CSV and COCO formats
- Dataset reorganized to follow standard structure

### Distribution
The dataset is available on Kaggle under the Plant Village dataset collection.

### Maintenance
This standardized version is maintained in this repository. For original dataset updates, refer to the Kaggle source.

## Known issues and caveats

1. **File naming**: Original images were renamed to `image (N).JPG` format during processing. Original filenames are preserved in JSON annotations as `pvc_filename` field.

2. **Background category**: The background category may not have JSON annotations, as it represents images without leaves.

3. **Split files**: The split files in `all/` directory use original Plant Village filenames. The reorganization script maps these to the new filenames using the `pvc_filename` field in JSON files.

4. **Coordinate system**: Bounding box coordinates use top-left origin (x, y) with width and height.

5. **Classification vs Detection**: This dataset can be used for both classification (using full-image bounding boxes) and object detection (using specific bounding boxes in CSV files).

## License

This dataset is released under the Creative Commons Attribution 4.0 International License (CC BY 4.0).

See `LICENSE` file for full license text.

Check the original dataset terms and cite appropriately.

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

- **V1.0.0** (2025-12-14): Initial standardized structure and COCO conversion utility
  - Reorganized dataset to follow standard structure with subcategory organization
  - Created CSV annotations from JSON files
  - Generated COCO format annotations
  - Added conversion scripts and documentation

## Contact

- **Maintainers**: Dataset standardization team
- **Original authors**: Plant Village project
- **Source**: `https://www.kaggle.com/datasets/abdallahalidev/plantvillage-dataset`
