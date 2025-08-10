# Invisibility Cloak Project

This project creates a git init effect using computer vision and OpenCV. It works by detecting a specific colored cloth/object and replacing it with the background captured earlier.

## Features

- **Basic Version**: Simple red cloak detection with basic masking
- **Advanced Version**: Multiple color options (Red, Green, Blue) with improved filtering and screenshot capability

## Requirements

- Webcam
- Colored cloth/object (red, green, or blue)

## Installation

### Option 1: Using Virtual Environment (Recommended)
```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Option 2: Global Installation
```bash
pip install opencv-python numpy
```

### Test Installation
```bash
python test_camera.py
```

## How to Run

1. Run the main script:
```bash
python invisibility_cloak.py
```

2. Choose your version:
   - **Version 1**: Basic version (red cloak only)
   - **Version 2**: Advanced version (multiple colors)

3. Follow the on-screen instructions:
   - Move out of camera view for background capture
   - Put on your colored cloak
   - Press 'q' to quit
   - Press 's' to save screenshot (advanced version only)

## How It Works

1. **Background Capture**: The program captures the background without you in the frame
2. **Color Detection**: Uses HSV color space to detect the specified colored cloth
3. **Masking**: Creates a mask of the detected color and its inverse
4. **Blending**: Combines the background (where cloak is detected) with the current frame (where cloak is not detected)
5. **Display**: Shows the final result with the invisibility effect

## Tips for Best Results

- Use a bright, solid-colored cloth
- Ensure good lighting conditions
- Keep the background static during capture
- Avoid wearing clothes of the same color as your cloak
- For red cloak, use a bright red cloth for better detection

## Troubleshooting

### Common Issues:

1. **ModuleNotFoundError: No module named 'cv2'**
   - Solution: Install OpenCV in your virtual environment
   ```bash
   .venv\Scripts\activate
   pip install opencv-python numpy
   ```

2. **Camera not opening**
   - Make sure your webcam is connected and not being used by another application
   - Try running `python test_camera.py` to test camera access
   - Check if your camera drivers are up to date

3. **Poor color detection**
   - Adjust lighting conditions (bright, even lighting works best)
   - Try a different colored cloth (bright red, green, or blue)
   - Use the advanced version for better filtering

4. **Flickering effect**
   - The advanced version has better filtering to reduce this issue
   - Adjust the smoothness setting in the advanced version

5. **Virtual Environment Issues**
   - Make sure you're in the correct directory
   - Activate the virtual environment before running the project
   - If using VS Code, select the correct Python interpreter

## Controls

- **'q'**: Quit the application
- **'s'**: Save screenshot (advanced version only)

## Files

- `invisibility_cloak.py`: Main application file
- `requirements.txt`: Python dependencies
- `README.md`: This file
