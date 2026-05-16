from ultralytics import YOLO

def train_model():
    """
    Demonstrates how to fine-tune YOLOv8 on the VisDrone dataset.
    Assumes the dataset has been preprocessed using data_prep.py 
    and the paths are set in visdrone.yaml.
    """
    # Load a pre-trained nano model
    model = YOLO('yolov8n.pt')

    # Train the model
    # epochs=50 is a good starting point for fine-tuning
    # imgsz=640 is standard, but drone images might benefit from higher res (e.g., 1024)
    results = model.train(
        data='visdrone.yaml', 
        epochs=50, 
        imgsz=640, 
        batch=16, 
        device='0', # Use '0' for GPU or 'cpu'
        name='visdrone_fine_tune'
    )
    
    print("Training finished.")
    return results

if __name__ == "__main__":
    print("Training script initialized. Run this to start fine-tuning on your dataset.")
    # train_model() # Uncomment to run
