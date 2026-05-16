import os
from pipeline import DroneAnalysisPipeline

def run_demo():
    # 1. Initialize the pipeline
    # This will download the yolov8n.pt weights automatically on first run
    pipeline = DroneAnalysisPipeline(model_path='yolov8n.pt')
    
    # 2. Path to our generated sample image
    # Note: Replace with the actual filename if needed, or I'll try to find it
    sample_img = r'C:\Users\User\.gemini\antigravity\brain\b7b43445-370b-4846-aa15-754bcd2d8af3\drone_aerial_sample_1778912658067.png'
    output_img = 'demo_results.png'
    
    if not os.path.exists(sample_img):
        print(f"Sample image not found at {sample_img}. Please check the path.")
        return

    # 3. Run analysis
    print("Running detection on sample drone image...")
    img, counts = pipeline.analyze_image(sample_img, output_path=output_img)
    human_count = counts['human']
    
    print("-" * 30)
    print(f"DEMO COMPLETE")
    print(f"Humans detected: {human_count}")
    print(f"Results saved to: {os.path.abspath(output_img)}")
    print("-" * 30)

if __name__ == "__main__":
    run_demo()
