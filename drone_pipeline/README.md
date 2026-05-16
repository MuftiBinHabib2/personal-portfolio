# 🚁 DroneVision AI: Aerial Analysis Pipeline

DroneVision AI is a high-performance computer vision pipeline designed for detecting and counting humans and vehicles in aerial drone imagery. Built with **YOLOv8** and optimized for the **VisDrone** dataset, this project features a stunning web dashboard for real-time analysis.

## 🚀 Quick Start

### 1. Prerequisites
- Python 3.8+
- Recommended: NVIDIA GPU with CUDA for faster inference (CPU works too!)

### 2. Installation
Clone the repository and install the dependencies:
```bash
git clone <your-repo-url>
cd drone_pipeline
pip install -r requirements.txt
```

### 3. Run the Web Dashboard
Launch the beautiful UI to interactively analyze your aerial photos:
```bash
python app.py
```
Then open **`http://127.0.0.1:5000`** in your browser.

### 4. Run the CLI Demo
To run a quick analysis on the sample image and save results:
```bash
python demo.py
```

## 🧠 Key Features

- **Object Detection**: Detects `Humans` and `Vehicles` (Cars, Vans, Trucks, Buses).
- **Human Counting**: Automated logic to count total pedestrians in the frame.
- **Aerial Optimization**: 
  - **CLAHE Enhancement**: Preprocesses images to improve contrast for tiny objects.
  - **High-Res Inference**: Runs at `1280px` to capture small details from distance.
  - **Object Tracking**: Bonus feature to track identities across video frames.
- **Modern UI**: A sleek, dark-themed dashboard with glassmorphic aesthetics.

## 📁 Project Structure

- `app.py`: Flask backend serving the dashboard API.
- `pipeline.py`: Core detection and preprocessing engine.
- `data_prep.py`: Utility to convert VisDrone dataset to YOLO format.
- `train.py`: Template for fine-tuning the model on custom drone data.
- `eval.py`: Performance evaluation script (mAP metrics).
- `templates/` & `static/`: Frontend dashboard assets.

## 📊 Dataset Context
This pipeline is designed for the **VisDrone** dataset. For optimal results in production, it is recommended to run `train.py` on the full VisDrone training set to fine-tune the model weights for nadir (top-down) perspectives.

---
Built with ❤️ using [Ultralytics YOLOv8](https://github.com/ultralytics/ultralytics).
