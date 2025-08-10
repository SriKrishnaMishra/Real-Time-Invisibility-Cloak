import cv2
import numpy as np
import time
import tkinter as tk
from tkinter import ttk, messagebox
import threading
import json
import os
from datetime import datetime

class AdvancedInvisibilityCloak:
    def __init__(self):
        self.cap = None
        self.background = None
        self.is_running = False
        self.current_effect = "invisibility"
        self.color_ranges = {
            "red": {
                "lower1": np.array([0, 120, 50]),
                "upper1": np.array([10, 255, 255]),
                "lower2": np.array([170, 120, 50]),
                "upper2": np.array([180, 255, 255])
            },
            "green": {
                "lower1": np.array([40, 40, 40]),
                "upper1": np.array([80, 255, 255]),
                "lower2": np.array([40, 40, 40]),
                "upper2": np.array([80, 255, 255])
            },
            "blue": {
                "lower1": np.array([100, 50, 50]),
                "upper1": np.array([130, 255, 255]),
                "lower2": np.array([100, 50, 50]),
                "upper2": np.array([130, 255, 255])
            }
        }
        self.selected_color = "red"
        self.settings = self.load_settings()
        self.create_gui()
    
    def load_settings(self):
        """Load settings from JSON file"""
        try:
            with open('cloak_settings.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {
                "default_color": "red",
                "camera_index": 0,
                "sensitivity": 50,
                "smoothness": 5,
                "auto_save": False
            }
    
    def save_settings(self):
        """Save settings to JSON file"""
        with open('cloak_settings.json', 'w') as f:
            json.dump(self.settings, f, indent=4)
    
    def create_gui(self):
        """Create the main GUI window"""
        self.root = tk.Tk()
        self.root.title("Advanced Invisibility Cloak v2.0")
        self.root.geometry("400x600")
        self.root.configure(bg='#2c3e50')
        
        # Style configuration
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TButton', padding=10, font=('Arial', 10))
        style.configure('TLabel', background='#2c3e50', foreground='white', font=('Arial', 10))
        style.configure('TFrame', background='#2c3e50')
        
        # Main frame
        main_frame = ttk.Frame(self.root)
        main_frame.pack(padx=20, pady=20, fill='both', expand=True)
        
        # Title
        title_label = ttk.Label(main_frame, text="🧥 Advanced Invisibility Cloak", 
                               font=('Arial', 16, 'bold'))
        title_label.pack(pady=10)
        
        # Color selection
        color_frame = ttk.LabelFrame(main_frame, text="Cloak Color", padding=10)
        color_frame.pack(fill='x', pady=10)
        
        self.color_var = tk.StringVar(value=self.selected_color)
        for color in ["red", "green", "blue"]:
            ttk.Radiobutton(color_frame, text=color.title(), variable=self.color_var, 
                           value=color, command=self.on_color_change).pack(anchor='w')
        
        # Effect selection
        effect_frame = ttk.LabelFrame(main_frame, text="Special Effects", padding=10)
        effect_frame.pack(fill='x', pady=10)
        
        self.effect_var = tk.StringVar(value="invisibility")
        effects = [
            ("Invisibility", "invisibility"),
            ("Matrix Effect", "matrix"),
            ("Rainbow Trail", "rainbow"),
            ("Ghost Effect", "ghost"),
            ("Hologram", "hologram")
        ]
        
        for effect_name, effect_value in effects:
            ttk.Radiobutton(effect_frame, text=effect_name, variable=self.effect_var, 
                           value=effect_value, command=self.on_effect_change).pack(anchor='w')
        
        # Settings
        settings_frame = ttk.LabelFrame(main_frame, text="Settings", padding=10)
        settings_frame.pack(fill='x', pady=10)
        
        # Sensitivity slider
        ttk.Label(settings_frame, text="Color Sensitivity:").pack(anchor='w')
        self.sensitivity_var = tk.IntVar(value=self.settings.get("sensitivity", 50))
        sensitivity_scale = ttk.Scale(settings_frame, from_=0, to=100, 
                                     variable=self.sensitivity_var, orient='horizontal')
        sensitivity_scale.pack(fill='x', pady=5)
        
        # Smoothness slider
        ttk.Label(settings_frame, text="Smoothness:").pack(anchor='w')
        self.smoothness_var = tk.IntVar(value=self.settings.get("smoothness", 5))
        smoothness_scale = ttk.Scale(settings_frame, from_=1, to=10, 
                                    variable=self.smoothness_var, orient='horizontal')
        smoothness_scale.pack(fill='x', pady=5)
        
        # Auto-save checkbox
        self.auto_save_var = tk.BooleanVar(value=self.settings.get("auto_save", False))
        ttk.Checkbutton(settings_frame, text="Auto-save screenshots", 
                       variable=self.auto_save_var).pack(anchor='w', pady=5)
        
        # Control buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill='x', pady=20)
        
        ttk.Button(button_frame, text="🎥 Start Cloak", 
                  command=self.start_cloak).pack(fill='x', pady=5)
        ttk.Button(button_frame, text="⏹️ Stop Cloak", 
                  command=self.stop_cloak).pack(fill='x', pady=5)
        ttk.Button(button_frame, text="📸 Capture Background", 
                  command=self.capture_background).pack(fill='x', pady=5)
        ttk.Button(button_frame, text="💾 Save Settings", 
                  command=self.save_current_settings).pack(fill='x', pady=5)
        
        # Status
        self.status_var = tk.StringVar(value="Ready to start")
        status_label = ttk.Label(main_frame, textvariable=self.status_var, 
                                font=('Arial', 9))
        status_label.pack(pady=10)
        
        # Bind window close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def on_color_change(self):
        """Handle color selection change"""
        self.selected_color = self.color_var.get()
        self.status_var.set(f"Color changed to {self.selected_color}")
    
    def on_effect_change(self):
        """Handle effect selection change"""
        self.current_effect = self.effect_var.get()
        self.status_var.set(f"Effect changed to {self.current_effect}")
    
    def save_current_settings(self):
        """Save current settings"""
        self.settings.update({
            "default_color": self.selected_color,
            "sensitivity": self.sensitivity_var.get(),
            "smoothness": self.smoothness_var.get(),
            "auto_save": self.auto_save_var.get()
        })
        self.save_settings()
        messagebox.showinfo("Settings", "Settings saved successfully!")
    
    def capture_background(self):
        """Capture background in a separate thread"""
        if self.cap is None:
            self.cap = cv2.VideoCapture(0)
            if not self.cap.isOpened():
                messagebox.showerror("Error", "Could not open camera!")
                return
        
        self.status_var.set("Capturing background... Move out of view!")
        
        def capture_thread():
            time.sleep(3)  # Give user time to move
            background = None
            for i in range(30):
                ret, frame = self.cap.read()
                if ret:
                    background = cv2.flip(frame, 1)
            
            if background is not None:
                self.background = background
                self.status_var.set("Background captured successfully!")
                messagebox.showinfo("Success", "Background captured! You can now start the cloak.")
            else:
                self.status_var.set("Failed to capture background")
                messagebox.showerror("Error", "Failed to capture background")
        
        threading.Thread(target=capture_thread, daemon=True).start()
    
    def start_cloak(self):
        """Start the invisibility cloak effect"""
        if self.background is None:
            messagebox.showwarning("Warning", "Please capture background first!")
            return
        
        if self.is_running:
            messagebox.showinfo("Info", "Cloak is already running!")
            return
        
        self.is_running = True
        self.status_var.set("Cloak is running... Press 'q' to quit")
        
        def cloak_thread():
            self.run_cloak_effect()
        
        threading.Thread(target=cloak_thread, daemon=True).start()
    
    def stop_cloak(self):
        """Stop the invisibility cloak effect"""
        self.is_running = False
        self.status_var.set("Cloak stopped")
        if self.cap:
            self.cap.release()
            self.cap = None
    
    def run_cloak_effect(self):
        """Main cloak effect loop"""
        if self.cap is None:
            self.cap = cv2.VideoCapture(0)
        
        if not self.cap.isOpened():
            messagebox.showerror("Error", "Could not open camera!")
            return
        
        screenshot_count = 0
        
        while self.is_running:
            ret, frame = self.cap.read()
            if not ret:
                break
            
            frame = cv2.flip(frame, 1)
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            
            # Get color ranges
            color_range = self.color_ranges[self.selected_color]
            
            # Create mask
            if self.selected_color == "red":
                mask1 = cv2.inRange(hsv, color_range["lower1"], color_range["upper1"])
                mask2 = cv2.inRange(hsv, color_range["lower2"], color_range["upper2"])
                mask = mask1 + mask2
            else:
                mask = cv2.inRange(hsv, color_range["lower1"], color_range["upper1"])
            
            # Apply sensitivity
            sensitivity = self.sensitivity_var.get() / 100.0
            mask = cv2.threshold(mask, int(255 * sensitivity), 255, cv2.THRESH_BINARY)[1]
            
            # Apply smoothness
            smoothness = self.smoothness_var.get()
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (smoothness, smoothness))
            mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
            mask = cv2.GaussianBlur(mask, (smoothness, smoothness), 0)
            
            # Apply different effects
            if self.current_effect == "invisibility":
                final_output = self.apply_invisibility_effect(frame, mask)
            elif self.current_effect == "matrix":
                final_output = self.apply_matrix_effect(frame, mask)
            elif self.current_effect == "rainbow":
                final_output = self.apply_rainbow_effect(frame, mask)
            elif self.current_effect == "ghost":
                final_output = self.apply_ghost_effect(frame, mask)
            elif self.current_effect == "hologram":
                final_output = self.apply_hologram_effect(frame, mask)
            else:
                final_output = self.apply_invisibility_effect(frame, mask)
            
            # Display results
            cv2.imshow('Advanced Invisibility Cloak', final_output)
            cv2.imshow('Mask Debug', mask)
            
            # Handle key presses
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('s'):
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"cloak_screenshot_{timestamp}_{screenshot_count}.jpg"
                cv2.imwrite(filename, final_output)
                screenshot_count += 1
                self.status_var.set(f"Screenshot saved: {filename}")
            
            # Auto-save
            if self.auto_save_var.get() and screenshot_count % 100 == 0:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"auto_save_{timestamp}.jpg"
                cv2.imwrite(filename, final_output)
        
        cv2.destroyAllWindows()
        self.stop_cloak()
    
    def apply_invisibility_effect(self, frame, mask):
        """Apply basic invisibility effect"""
        mask_inv = cv2.bitwise_not(mask)
        background_part = cv2.bitwise_and(self.background, self.background, mask=mask)
        frame_part = cv2.bitwise_and(frame, frame, mask=mask_inv)
        return cv2.add(background_part, frame_part)
    
    def apply_matrix_effect(self, frame, mask):
        """Apply Matrix-style digital rain effect"""
        # Create green digital rain effect
        height, width = frame.shape[:2]
        matrix_effect = np.zeros_like(frame)
        
        # Add green digital rain
        for i in range(0, width, 20):
            for j in range(0, height, 30):
                if np.random.random() > 0.7:
                    cv2.putText(matrix_effect, "01", (i, j), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
        
        # Blend with original effect
        mask_3channel = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR) / 255.0
        invisibility_result = self.apply_invisibility_effect(frame, mask)
        return (invisibility_result * (1 - mask_3channel) + 
                matrix_effect * mask_3channel).astype(np.uint8)
    
    def apply_rainbow_effect(self, frame, mask):
        """Apply rainbow trail effect"""
        # Create rainbow colors
        height, width = frame.shape[:2]
        rainbow = np.zeros_like(frame)
        
        for i in range(height):
            hue = int((i / height) * 180)
            color = tuple(int(x) for x in cv2.cvtColor(np.uint8([[[hue, 255, 255]]]), 
                                                      cv2.COLOR_HSV2BGR)[0, 0])
            rainbow[i, :] = color
        
        # Blend with original effect
        mask_3channel = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR) / 255.0
        invisibility_result = self.apply_invisibility_effect(frame, mask)
        return (invisibility_result * (1 - mask_3channel) + 
                rainbow * mask_3channel).astype(np.uint8)
    
    def apply_ghost_effect(self, frame, mask):
        """Apply ghost/transparency effect"""
        # Create ghost effect with transparency
        ghost_frame = frame.copy()
        ghost_frame = cv2.addWeighted(ghost_frame, 0.3, self.background, 0.7, 0)
        
        # Blend with original effect
        mask_3channel = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR) / 255.0
        invisibility_result = self.apply_invisibility_effect(frame, mask)
        return (invisibility_result * (1 - mask_3channel) + 
                ghost_frame * mask_3channel).astype(np.uint8)
    
    def apply_hologram_effect(self, frame, mask):
        """Apply hologram effect with glitch"""
        # Create hologram effect
        holo_frame = frame.copy()
        
        # Add blue tint
        holo_frame[:, :, 0] = holo_frame[:, :, 0] * 0.5  # Reduce blue
        holo_frame[:, :, 1] = holo_frame[:, :, 1] * 0.8  # Reduce green
        holo_frame[:, :, 2] = holo_frame[:, :, 2] * 1.2  # Enhance red
        
        # Add scan lines
        for i in range(0, holo_frame.shape[0], 4):
            holo_frame[i:i+2, :] = [255, 255, 255]
        
        # Blend with original effect
        mask_3channel = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR) / 255.0
        invisibility_result = self.apply_invisibility_effect(frame, mask)
        return (invisibility_result * (1 - mask_3channel) + 
                holo_frame * mask_3channel).astype(np.uint8)
    
    def on_closing(self):
        """Handle window closing"""
        self.stop_cloak()
        self.save_current_settings()
        self.root.destroy()
    
    def run(self):
        """Start the GUI application"""
        self.root.mainloop()

if __name__ == "__main__":
    app = AdvancedInvisibilityCloak()
    app.run()
