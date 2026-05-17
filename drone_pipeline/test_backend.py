import requests
import os

def test_backend():
    url = 'http://127.0.0.1:5000/analyze'
    # Create a dummy image for testing
    import numpy as np
    import cv2
    img = np.zeros((100, 100, 3), dtype=np.uint8)
    cv2.imwrite('test_img.jpg', img)
    
    with open('test_img.jpg', 'rb') as f:
        files = {'image': f}
        try:
            print(f"Sending request to {url}...")
            r = requests.post(url, files=files)
            print(f"Status Code: {r.status_code}")
            print(f"Response: {r.text[:200]}")
        except Exception as e:
            print(f"Request failed: {e}")

if __name__ == "__main__":
    test_backend()
