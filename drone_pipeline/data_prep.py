import os
import glob
from PIL import Image

def convert_visdrone_to_yolo(visdrone_path, output_path):
    """
    Converts VisDrone annotations to YOLO format.
    
    VisDrone Format: <bbox_left>, <bbox_top>, <bbox_width>, <bbox_height>, <score>, <object_category>, <truncation>, <occlusion>
    YOLO Format: <class_id> <x_center> <y_center> <width> <height> (normalized)
    """
    
    # Class mapping: VisDrone -> YOLO
    # 1: pedestrian, 2: people -> 0 (Human)
    # 4: car, 5: van, 6: truck, 9: bus -> 1 (Car/Vehicle)
    class_map = {
        '1': 0, '2': 0,
        '4': 1, '5': 1, '6': 1, '9': 1
    }

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    # Assume VisDrone structure: VisDrone2019-DET-train/annotations/*.txt
    # and VisDrone2019-DET-train/images/*.jpg
    img_dir = os.path.join(visdrone_path, 'images')
    ann_dir = os.path.join(visdrone_path, 'annotations')

    for ann_file in glob.glob(os.path.join(ann_dir, '*.txt')):
        basename = os.path.basename(ann_file)
        img_file = os.path.join(img_dir, basename.replace('.txt', '.jpg'))
        
        if not os.path.exists(img_file):
            continue

        with Image.open(img_file) as img:
            width, height = img.size

        yolo_ann = []
        with open(ann_file, 'r') as f:
            for line in f:
                parts = line.strip().split(',')
                if len(parts) < 8:
                    continue
                
                left, top, w, h, score, category, trunc, occ = parts[:8]
                
                if category in class_map:
                    class_id = class_map[category]
                    
                    # Normalize coordinates
                    x_center = (float(left) + float(w) / 2) / width
                    y_center = (float(top) + float(h) / 2) / height
                    w_norm = float(w) / width
                    h_norm = float(h) / height
                    
                    yolo_ann.append(f"{class_id} {x_center:.6f} {y_center:.6f} {w_norm:.6f} {h_norm:.6f}")

        if yolo_ann:
            with open(os.path.join(output_path, basename), 'w') as f:
                f.write('\n'.join(yolo_ann))

if __name__ == "__main__":
    # Example usage:
    # convert_visdrone_to_yolo('VisDrone2019-DET-train', 'labels/train')
    print("Preprocessing script ready. Call convert_visdrone_to_yolo with dataset paths.")
