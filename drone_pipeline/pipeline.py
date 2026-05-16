import cv2
from ultralytics import YOLO
import numpy as np

class DroneAnalysisPipeline:
    def __init__(self, model_path='yolov8s.pt'):
        """
        Initializes the pipeline with a YOLOv8 model.
        Using yolov8s (Small) for better balance of speed and detection of small objects.
        """
        print(f"Initializing pipeline with model: {model_path}")
        self.model = YOLO(model_path)
        
        # Define classes we care about (mapping from COCO if using pre-trained)
        # COCO: 0 is person, 2 is car, 3 is motorcycle, 5 is bus, 7 is truck
        self.human_class = 0
        self.car_classes = [2, 3, 5, 7] 

    def analyze_image(self, image_path, output_path=None):
        """
        Detects humans and cars, counts humans, and visualizes results.
        """
        # Load image
        img = cv2.imread(image_path)
        if img is None:
            print(f"Error: Could not read image at {image_path}")
            return None

        # --- NEW: Contrast Enhancement for Tiny Objects ---
        # Apply CLAHE to help small objects stand out
        lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
        cl = clahe.apply(l)
        limg = cv2.merge((cl, a, b))
        enhanced_img = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)
        # --------------------------------------------------

        # Run inference with ultra-high resolution (1280px)
        results = self.model(enhanced_img, imgsz=1280)[0]
        
        human_count = 0
        car_count = 0
        
        # Process results
        for box in results.boxes:
            cls = int(box.cls[0])
            conf = float(box.conf[0])
            
            # Ultra-low threshold for tiny humans (0.10)
            # Cars are easier to detect, so we can keep them higher if needed, 
            # but let's be aggressive for now.
            if conf < 0.10: 
                continue
                
            label = ""
            color = (0, 0, 0)
            
            if cls == self.human_class:
                human_count += 1
                label = "Human"
                color = (0, 255, 0) # Green for humans
            elif cls in self.car_classes:
                car_count += 1
                label = "Car"
                color = (255, 0, 0) # Blue for cars
            else:
                continue

            # Draw bounding box
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
            cv2.putText(img, f"{label} {conf:.2f}", (x1, y1 - 10), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

        # Draw summary overlay
        overlay = img.copy()
        cv2.rectangle(overlay, (10, 10), (250, 80), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.6, img, 0.4, 0, img)
        
        cv2.putText(img, f"Total Humans: {human_count}", (20, 40), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        cv2.putText(img, f"Total Cars: {car_count}", (20, 70), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

        print(f"Analysis complete. Humans: {human_count}, Cars: {car_count}")
        
        if output_path:
            cv2.imwrite(output_path, img)
            print(f"Result saved to {output_path}")
            
        return img, {'human': human_count, 'car': car_count}

    def track_video(self, video_path, output_path):
        """
        Bonus: Object tracking on video.
        """
        print(f"Starting tracking on video: {video_path}")
        results = self.model.track(source=video_path, show=False, save=True, persist=True)
        print(f"Tracking complete. Results saved by YOLO internally.")
        return results

if __name__ == "__main__":
    # Example Pipeline Usage
    pipeline = DroneAnalysisPipeline()
    
    # In a real scenario, we'd provide a path to a drone image
    # pipeline.analyze_image('aerial_photo.jpg', 'output_detected.jpg')
    print("Pipeline script ready. Use analyze_image() for detection and counting.")
