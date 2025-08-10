import cv2
import numpy as np

def test_camera():
    """Test if camera and OpenCV are working properly"""
    print("🧪 Testing Camera and OpenCV...")
    
    # Test OpenCV import
    print(f"✅ OpenCV version: {cv2.__version__}")
    print(f"✅ NumPy version: {np.__version__}")
    
    # Test camera
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("❌ Error: Could not open camera")
        return False
    
    print("✅ Camera opened successfully!")
    
    # Capture a test frame
    ret, frame = cap.read()
    if ret:
        print(f"✅ Frame captured successfully! Size: {frame.shape}")
        
        # Display the frame
        cv2.imshow('Camera Test', frame)
        print("📷 Press any key to close the test window...")
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        print("❌ Error: Could not capture frame")
        return False
    
    cap.release()
    print("✅ Camera test completed successfully!")
    return True

if __name__ == "__main__":
    test_camera()
