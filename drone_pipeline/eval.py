from ultralytics import YOLO

def evaluate_model(model_path='visdrone_fine_tune/weights/best.pt'):
    """
    Evaluates the fine-tuned model on the validation set.
    Outputs metrics like mAP@50 and mAP@50-95.
    """
    try:
        model = YOLO(model_path)
    except Exception:
        print(f"Could not load custom model at {model_path}. Using base model for demo.")
        model = YOLO('yolov8n.pt')

    # Validate the model
    metrics = model.val(data='visdrone.yaml')
    
    print(f"mAP@50: {metrics.box.map50:.4f}")
    print(f"mAP@50-95: {metrics.box.map:.4f}")
    
    return metrics

if __name__ == "__main__":
    print("Evaluation script ready.")
    # evaluate_model()
