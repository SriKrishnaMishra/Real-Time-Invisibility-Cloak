import cv2
import numpy as np
import time

def create_invisibility_cloak():
    # Initialize the camera
    cap = cv2.VideoCapture(0)
    
    # Check if camera opened successfully
    if not cap.isOpened():
        print("Error: Could not open camera")
        return
    
    # Give camera some time to adjust
    print("Preparing invisibility cloak...")
    print("Please move out of the camera view!")
    
    # Capture the background for 3 seconds
    time.sleep(3)
    background = None
    
    # Capture background frames
    for i in range(30):
        ret, background = cap.read()
        if not ret:
            print("Error: Could not read from camera")
            cap.release()
            return
    
    # Flip background for mirror effect
    background = cv2.flip(background, 1)
    
    print("Background captured! Now put on your 'cloak' (red colored cloth/object)")
    print("Press 'q' to quit")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
            
        # Flip frame for mirror effect
        frame = cv2.flip(frame, 1)
        
        # Convert BGR to HSV for better color detection
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # Define range for red color (you can adjust these values)
        # Red color has two ranges in HSV
        lower_red1 = np.array([0, 120, 50])
        upper_red1 = np.array([10, 255, 255])
        lower_red2 = np.array([170, 120, 50])
        upper_red2 = np.array([180, 255, 255])
        
        # Create masks for red color
        mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
        mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
        mask = mask1 + mask2
        
        # Morphological operations to clean up the mask
        kernel = np.ones((3, 3), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_DILATE, kernel)
        
        # Create inverse mask
        mask_inv = cv2.bitwise_not(mask)
        
        # Apply masks to create the invisibility effect
        # Part 1: Take only region of the cloak from background
        background_part = cv2.bitwise_and(background, background, mask=mask)
        
        # Part 2: Take only region without cloak from current frame
        frame_part = cv2.bitwise_and(frame, frame, mask=mask_inv)
        
        # Combine both parts
        final_output = cv2.add(background_part, frame_part)
        
        # Display the result
        cv2.imshow('Invisibility Cloak', final_output)
        cv2.imshow('Mask', mask)  # Show mask for debugging
        
        # Break the loop on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # Release everything
    cap.release()
    cv2.destroyAllWindows()

def create_invisibility_cloak_advanced():
    """
    Advanced version with color selection and better filtering
    """
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Error: Could not open camera")
        return
    
    print("Advanced Invisibility Cloak")
    print("Choose your cloak color:")
    print("1. Red")
    print("2. Green") 
    print("3. Blue")
    
    choice = input("Enter choice (1-3): ")
    
    # Define color ranges based on choice
    if choice == '1':  # Red
        lower1 = np.array([0, 120, 50])
        upper1 = np.array([10, 255, 255])
        lower2 = np.array([170, 120, 50])
        upper2 = np.array([180, 255, 255])
        color_name = "Red"
    elif choice == '2':  # Green
        lower1 = np.array([40, 40, 40])
        upper1 = np.array([80, 255, 255])
        lower2 = lower1  # Green has single range
        upper2 = upper1
        color_name = "Green"
    elif choice == '3':  # Blue
        lower1 = np.array([100, 50, 50])
        upper1 = np.array([130, 255, 255])
        lower2 = lower1  # Blue has single range
        upper2 = upper1
        color_name = "Blue"
    else:
        print("Invalid choice, using Red")
        lower1 = np.array([0, 120, 50])
        upper1 = np.array([10, 255, 255])
        lower2 = np.array([170, 120, 50])
        upper2 = np.array([180, 255, 255])
        color_name = "Red"
    
    print(f"Selected {color_name} cloak")
    print("Please move out of camera view for background capture...")
    time.sleep(3)
    
    # Capture background
    background = None
    for i in range(30):
        ret, background = cap.read()
        if not ret:
            print("Error: Could not read from camera")
            cap.release()
            return
    
    background = cv2.flip(background, 1)
    
    print(f"Background captured! Put on your {color_name} cloak")
    print("Press 'q' to quit, 's' to save screenshot")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
            
        frame = cv2.flip(frame, 1)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # Create color mask
        if choice == '1':  # Red needs two ranges
            mask1 = cv2.inRange(hsv, lower1, upper1)
            mask2 = cv2.inRange(hsv, lower2, upper2)
            mask = mask1 + mask2
        else:
            mask = cv2.inRange(hsv, lower1, upper1)
        
        # Advanced morphological operations
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.dilate(mask, kernel, iterations=2)
        
        # Smooth the mask to reduce flickering
        mask = cv2.GaussianBlur(mask, (5, 5), 0)
        
        # Convert mask to 3 channels for blending
        mask_3channel = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR) / 255.0
        
        # Blend the images
        final_output = frame * (1 - mask_3channel) + background * mask_3channel
        final_output = final_output.astype(np.uint8)
        
        # Display results
        cv2.imshow('Invisibility Cloak - Advanced', final_output)
        cv2.imshow('Original', frame)
        
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('s'):
            cv2.imwrite('invisibility_screenshot.jpg', final_output)
            print("Screenshot saved as 'invisibility_screenshot.jpg'")
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    print("Invisibility Cloak Project")
    print("1. Basic Version")
    print("2. Advanced Version")
    
    choice = input("Choose version (1 or 2): ")
    
    if choice == '2':
        create_invisibility_cloak_advanced()
    else:
        create_invisibility_cloak()
