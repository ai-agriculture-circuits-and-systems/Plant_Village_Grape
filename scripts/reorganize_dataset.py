#!/usr/bin/env python3
"""
重组 Plant Village Grape 数据集为标准结构
"""
import os
import json
import shutil
from pathlib import Path
from collections import defaultdict

# 类别映射：原始目录名 -> 新子类别名
CATEGORY_MAPPING = {
    'Grape___healthy': 'healthy',
    'Grape___Black_rot': 'black_rot',
    'Grape___Esca_(Black_Measles)': 'esca',
    'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)': 'leaf_blight',
    'Background_without_leaves': 'background'
}

# 子类别到 label_id 的映射
SUBCATEGORY_TO_LABEL = {
    'background': 0,
    'healthy': 1,
    'black_rot': 2,
    'esca': 3,
    'leaf_blight': 4
}

def convert_json_to_csv(json_file, csv_file, category_id):
    """将 JSON 标注转换为 CSV 格式"""
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    annotations = data.get('annotations', [])
    if not annotations:
        # 如果没有标注，创建空 CSV 文件
        with open(csv_file, 'w', encoding='utf-8') as f:
            f.write('#item,x,y,width,height,label\n')
        return
    
    # 写入 CSV 文件
    with open(csv_file, 'w', encoding='utf-8') as f:
        f.write('#item,x,y,width,height,label\n')
        for idx, ann in enumerate(annotations):
            bbox = ann.get('bbox', [0, 0, 0, 0])
            x, y, width, height = bbox
            f.write(f'{idx},{x},{y},{width},{height},{category_id}\n')

def copy_files(src_dir, dst_dir, pattern='*', subdir='without_augmentation'):
    """复制文件从源目录到目标目录"""
    src_path = Path(src_dir) / subdir
    dst_path = Path(dst_dir)
    
    if not src_path.exists():
        print(f"Warning: {src_path} does not exist, skipping...")
        return []
    
    dst_path.mkdir(parents=True, exist_ok=True)
    copied_files = []
    
    for ext in ['.JPG', '.jpg', '.json']:
        for src_file in src_path.glob(f'*{ext}'):
            dst_file = dst_path / src_file.name
            shutil.copy2(src_file, dst_file)
            copied_files.append(src_file.name)
    
    return copied_files

def create_labelmap(output_file):
    """创建 labelmap.json 文件"""
    labelmap = []
    
    # 背景类别
    labelmap.append({
        "object_id": 0,
        "label_id": 0,
        "keyboard_shortcut": "0",
        "object_name": "background"
    })
    
    # 其他类别
    for subcat, label_id in sorted(SUBCATEGORY_TO_LABEL.items(), key=lambda x: x[1]):
        if label_id == 0:  # 跳过背景，已添加
            continue
        labelmap.append({
            "object_id": label_id,
            "label_id": label_id,
            "keyboard_shortcut": str(label_id),
            "object_name": subcat
        })
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(labelmap, f, indent=2, ensure_ascii=False)

def parse_split_files(all_dir, grapes_dir):
    """解析划分文件并创建新的划分文件"""
    split_files = ['train.txt', 'val.txt', 'test.txt']
    pvc_to_stem = {}  # pvc_filename -> (子类别, 新文件名stem)
    
    # 扫描所有 JSON 文件，建立 pvc_filename 到新文件名的映射
    for old_cat, new_subcat in CATEGORY_MAPPING.items():
        json_dir = grapes_dir / new_subcat / 'json'
        if not json_dir.exists():
            continue
        
        for json_file in json_dir.glob('*.json'):
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if data.get('images') and len(data['images']) > 0:
                        pvc_filename = data['images'][0].get('pvc_filename', '')
                        if pvc_filename:
                            stem = json_file.stem
                            pvc_to_stem[pvc_filename] = (new_subcat, stem)
            except Exception as e:
                print(f"Warning: Failed to parse {json_file}: {e}")
                continue
    
    print(f"建立了 {len(pvc_to_stem)} 个文件名映射")
    
    # 处理每个划分文件
    for split_file in split_files:
        old_split = Path(all_dir) / split_file
        if not old_split.exists():
            continue
        
        # 按子类别分组
        subcat_files = defaultdict(list)
        matched_count = 0
        unmatched_count = 0
        
        with open(old_split, 'r', encoding='utf-8') as f:
            for line in f:
                filename = line.strip()
                if filename in pvc_to_stem:
                    subcat, new_stem = pvc_to_stem[filename]
                    subcat_files[subcat].append(new_stem)
                    matched_count += 1
                else:
                    unmatched_count += 1
        
        print(f"  {split_file}: 匹配 {matched_count} 个, 未匹配 {unmatched_count} 个")
        
        # 为每个子类别创建划分文件
        for subcat, files in subcat_files.items():
            sets_dir = Path(grapes_dir) / subcat / 'sets'
            sets_dir.mkdir(parents=True, exist_ok=True)
            
            split_path = sets_dir / split_file
            with open(split_path, 'w', encoding='utf-8') as f:
                for file_stem in sorted(files):
                    f.write(f'{file_stem}\n')
            
            print(f"    Created {split_path} with {len(files)} images")

def main():
    root_dir = Path(__file__).parent.parent
    grapes_dir = root_dir / 'grapes'
    
    print("开始重组数据集...")
    
    # 1. 复制图像和 JSON 文件
    for old_cat, new_subcat in CATEGORY_MAPPING.items():
        print(f"\n处理类别: {old_cat} -> {new_subcat}")
        
        old_dir = root_dir / old_cat
        new_images_dir = grapes_dir / new_subcat / 'images'
        new_json_dir = grapes_dir / new_subcat / 'json'
        
        # 复制图像文件
        print(f"  复制图像文件到 {new_images_dir}")
        image_files = copy_files(old_dir, new_images_dir, subdir='without_augmentation')
        print(f"    复制了 {len([f for f in image_files if f.endswith(('.JPG', '.jpg'))])} 个图像文件")
        
        # 复制 JSON 文件
        print(f"  复制 JSON 文件到 {new_json_dir}")
        json_files = copy_files(old_dir, new_json_dir, subdir='without_augmentation')
        print(f"    复制了 {len([f for f in json_files if f.endswith('.json')])} 个 JSON 文件")
        
        # 2. 从 JSON 生成 CSV 文件
        print(f"  生成 CSV 标注文件...")
        category_id = SUBCATEGORY_TO_LABEL[new_subcat]
        csv_dir = grapes_dir / new_subcat / 'csv'
        csv_dir.mkdir(parents=True, exist_ok=True)
        
        json_dir = Path(new_json_dir)
        csv_count = 0
        for json_file in json_dir.glob('*.json'):
            stem = json_file.stem
            csv_file = csv_dir / f'{stem}.csv'
            convert_json_to_csv(json_file, csv_file, category_id)
            csv_count += 1
        
        print(f"    生成了 {csv_count} 个 CSV 文件")
    
    # 3. 创建 labelmap.json
    print("\n创建 labelmap.json...")
    labelmap_file = grapes_dir / 'labelmap.json'
    create_labelmap(labelmap_file)
    print(f"  已创建 {labelmap_file}")
    
    # 4. 创建划分文件
    print("\n创建数据集划分文件...")
    parse_split_files(root_dir / 'all', grapes_dir)
    
    # 5. 创建 all.txt 文件
    print("\n创建 all.txt 文件...")
    for subcat in CATEGORY_MAPPING.values():
        images_dir = grapes_dir / subcat / 'images'
        sets_dir = grapes_dir / subcat / 'sets'
        sets_dir.mkdir(parents=True, exist_ok=True)
        
        # 获取所有图像文件名（不含扩展名）
        image_stems = set()
        for img_file in images_dir.glob('*.JPG'):
            image_stems.add(img_file.stem)
        for img_file in images_dir.glob('*.jpg'):
            image_stems.add(img_file.stem)
        
        all_file = sets_dir / 'all.txt'
        with open(all_file, 'w', encoding='utf-8') as f:
            for stem in sorted(image_stems):
                f.write(f'{stem}\n')
        
        print(f"  已创建 {all_file} with {len(image_stems)} images")
    
    print("\n数据集重组完成！")

if __name__ == '__main__':
    main()
