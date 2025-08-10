# Invisibility Cloak Project

This project creates a real-time invisibility cloak effect using computer vision and OpenCV. It works by detecting a specific colored cloth/object and replacing it with the background captured earlier.

## Features

- **Basic Version**: Simple red cloak detection with basic masking
- **Advanced Version**: Multiple color options (Red, Green, Blue) with improved filtering and screenshot capability

## Requirements

- Python 3.7 or higher
- Webcam
- Colored cloth/object (red, green, or blue)

## Installation

1. Install the required packages:
```bash
pip install -r requirements.txt
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

- **Camera not opening**: Make sure your webcam is connected and not being used by another application
- **Poor detection**: Adjust lighting or try a different colored cloth
- **Flickering**: The advanced version has better filtering to reduce this issue

## Controls

- **'q'**: Quit the application
- **'s'**: Save screenshot (advanced version only)

## Files

- `invisibility_cloak.py`: Main application file
- `requirements.txt`: Python dependencies
- `README.md`: This file
