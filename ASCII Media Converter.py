## DEPENDENCIES ##

import cv2 # type: ignore
import numpy as np # type: ignore   
import os
import tkinter as tk
from tkinter import filedialog, messagebox
import threading


## VARIABLE ##

ASCII_CHARS = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\^`'. "
# Reversed chain " .'`^\",:;Il!i><~+_-?][}{1)(|\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"

## CLASS ##

class ASCIIConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Convertisseur ASCII")
        self.root.geometry("500x500")
        
        # Status label
        self.status_label = tk.Label(root, text="Select an option below", font=("Arial", 12))
        self.status_label.pack(pady=10)
        
        # Mode selection
        self.mode_var = tk.StringVar(value="file")
        tk.Label(root, text="Choose Mode:", font=("Arial", 10)).pack()
        tk.Radiobutton(root, text="Convert File (Image/Video)", variable=self.mode_var, value="file", command=self.update_ui).pack()
        tk.Radiobutton(root, text="Convert Webcam (Real-Time)", variable=self.mode_var, value="webcam", command=self.update_ui).pack()
        
        # File type selection (for file mode)
        self.file_type_var = tk.StringVar(value="image")
        self.file_type_frame = tk.Frame(root)
        tk.Label(self.file_type_frame, text="File Type:").pack(side=tk.LEFT)
        tk.Radiobutton(self.file_type_frame, text="Image", variable=self.file_type_var, value="image").pack(side=tk.LEFT)
        tk.Radiobutton(self.file_type_frame, text="Video", variable=self.file_type_var, value="video").pack(side=tk.LEFT)
        
        # File selection frame
        self.file_frame = tk.Frame(root)
        self.file_frame.pack(pady=10)
        
        tk.Label(self.file_frame, text="Input File:").grid(row=0, column=0, padx=5)
        self.input_entry = tk.Entry(self.file_frame, width=40)
        self.input_entry.grid(row=0, column=1, padx=5)
        tk.Button(self.file_frame, text="Browse", command=self.browse_input).grid(row=0, column=2, padx=5)
        
        tk.Label(self.file_frame, text="Output File:").grid(row=1, column=0, padx=5)
        self.output_entry = tk.Entry(self.file_frame, width=40)
        self.output_entry.grid(row=1, column=1, padx=5)
        tk.Button(self.file_frame, text="Browse", command=self.browse_output).grid(row=1, column=2, padx=5)
        
        # ASCII settings
        tk.Label(root, text="ASCII Width:").pack()
        self.width_entry = tk.Entry(root)
        self.width_entry.insert(0, "80")
        self.width_entry.pack()
        
        tk.Label(root, text="ASCII Height:").pack()
        self.height_entry = tk.Entry(root)
        self.height_entry.insert(0, "60")
        self.height_entry.pack()
        
        # FPS settings (for videos)
        self.fps_label = tk.Label(root, text="FPS (for videos):")
        self.fps_label.pack()
        self.fps_entry = tk.Entry(root)
        self.fps_entry.insert(0, "30")
        self.fps_entry.pack()
        
        # Convert button
        self.convert_button = tk.Button(root, text="Convert", command=self.start_conversion, font=("Arial", 12))
        self.convert_button.pack(pady=20)
        
        # Webcam control
        self.webcam_thread = None
        self.webcam_running = False

        # Initial UI update
        self.update_ui()
    
    def update_ui(self):
        mode = self.mode_var.get()
        if mode == "file":
            self.file_type_frame.pack(pady=5)
            self.file_frame.pack(pady=10)
            self.fps_label.pack()
            self.fps_entry.pack()
            self.convert_button.pack(pady=20)
        else:
            self.file_type_frame.pack_forget()
            self.file_frame.pack_forget()
            self.fps_label.pack_forget()
            self.fps_entry.pack_forget()
            self.convert_button.pack_forget()
            self.webcam_button = tk.Button(root, text="Convert Webcam", command=self.start_webcam)
            self.webcam_button.pack(pady=20)
    
    def browse_input(self):
        file_path = filedialog.askopenfilename(title="Select Input File", filetypes=[("All Files", "*.*")])
        if file_path:
            self.input_entry.delete(0, tk.END)
            self.input_entry.insert(0, file_path)
    
    def browse_output(self):
        file_type = self.file_type_var.get()
        if file_type == "image":
            defaultextension = ".jpg"
            filetypes = [("JPG files", "*.jpg"), ("PNG files", "*.png"), ("All Files", "*.*")]
        else:
            defaultextension = ".mp4"
            filetypes = [("MP4 files", "*.mp4"), ("AVI files", "*.avi"), ("All Files", "*.*")]
        file_path = filedialog.asksaveasfilename(title="Select Output File", defaultextension=defaultextension, filetypes=filetypes)
        if file_path:
            self.output_entry.delete(0, tk.END)
            self.output_entry.insert(0, file_path)
    
    def start_conversion(self):
        try:
            ascii_width = int(self.width_entry.get())
            ascii_height = int(self.height_entry.get())
            fps = int(self.fps_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Invalid ASCII width, height, or FPS. Please enter integers.")
            return
        
        input_path = self.input_entry.get()
        output_path = self.output_entry.get()
        if not input_path or not output_path:
            messagebox.showerror("Error", "Please select input and output files.")
            return
        
        if not os.path.isfile(input_path):
            messagebox.showerror("Error", "Input file does not exist.")
            return
        
        file_type = self.file_type_var.get()
        self.status_label.config(text="Converting...")
        if file_type == 'video':
            threading.Thread(target=convert_video_to_ascii, args=(input_path, output_path, ascii_width, ascii_height, fps, self.status_label)).start()
        elif file_type == 'image':
            threading.Thread(target=convert_image_to_ascii, args=(input_path, output_path, ascii_width, ascii_height, self.status_label)).start()
    
    def start_webcam(self):
        try:
            ascii_width = int(self.width_entry.get())
            ascii_height = int(self.height_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Invalid ASCII width or height. Please enter integers.")
            return
        
        if self.webcam_running:
            self.webcam_running = False
            self.webcam_button.config(text="Convert Webcam")
            self.status_label.config(text="Webcam stopped.")
        else:
            self.webcam_running = True
            self.webcam_button.config(text="Stop Webcam")
            self.status_label.config(text="Starting webcam...")
            self.webcam_thread = threading.Thread(target=self.run_webcam, args=(ascii_width, ascii_height))
            self.webcam_thread.start()
    
    def run_webcam(self, ascii_width, ascii_height):
        convert_webcam_to_ascii(ascii_width, ascii_height, self.status_label)
        self.webcam_running = False
        self.webcam_button.config(text="Convert Webcam")
        self.status_label.config(text="Webcam stopped.")

## FONCTIONS ##

def frame_to_ascii(frame, width=80, height=60, font_scale=0.5, thickness=1, max_width=None, max_height=None):
    """
    Convert a single frame (or image) to an ASCII art image.
    - Resize the frame to the specified width and height.
    - Map each pixel block to an ASCII character.
    - Create a new image with the ASCII text drawn on it.
    - If max_width and max_height are provided, scale font to fit within those dimensions.
    """
    # Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Resize to the desired ASCII grid size
    resized = cv2.resize(gray, (width, height), interpolation=cv2.INTER_LINEAR)
    
    # Calculate scaling if max dimensions are provided
    scale = 1.0
    if max_width is not None and max_height is not None:
        desired_width = width * 10
        desired_height = height * 20
        scale = min(max_width / desired_width, max_height / desired_height) if desired_width > 0 and desired_height > 0 else 1.0
    
    # Adjust font_scale and thickness based on scale
    adjusted_font_scale = font_scale * scale
    adjusted_thickness = max(1, int(thickness * scale))
    
    # Calculate character dimensions based on scale
    char_width = 10 * scale
    char_height = 20 * scale
    
    # Create a blank white image for the ASCII art with adjusted size
    ascii_image = np.ones((int(height * char_height), int(width * char_width), 3), dtype=np.uint8) * 255
    
    # Font settings
    font = cv2.FONT_HERSHEY_SIMPLEX
    
    # For each position in the grid, get the average intensity and map to ASCII char
    for y in range(height):
        for x in range(width):
            intensity = resized[y, x]
            # Map intensity (0-255) to ASCII index
            char_index = int((intensity / 255) * (len(ASCII_CHARS) - 1))
            char = ASCII_CHARS[char_index]
            
            # Position to draw the text, adjusted for scale
            pos = (int(x * char_width), int(y * char_height + char_height * 0.75))  # Adjust baseline
            
            # Draw the character in black on white background
            cv2.putText(ascii_image, char, pos, font, adjusted_font_scale, (0, 0, 0), adjusted_thickness, cv2.LINE_AA)
    
    return ascii_image

def convert_video_to_ascii(input_video_path, output_video_path, ascii_width=80, ascii_height=60, fps=30, status_label=None):
    """
    Convert a video to ASCII art video.
    Maximum ASCII resolution: 300x200.
    Adjusts ASCII width/height to preserve the video's aspect ratio.
    """
    # Open the input video to get frame size
    cap = cv2.VideoCapture(input_video_path)
    if not cap.isOpened():
        messagebox.showerror("Error", "Could not open video.")
        return
    
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    cap.release()
    
    # Adjust ASCII width and height to match the video's aspect ratio
    ratio = frame_width / frame_height
    adjusted_ascii_width = min(ascii_width, int(ascii_height * ratio))
    adjusted_ascii_height = min(ascii_height, int(ascii_width / ratio))
    
    # Cap ASCII resolution for videos
    adjusted_ascii_width = min(adjusted_ascii_width, 300)
    adjusted_ascii_height = min(adjusted_ascii_height, 200)
    
    # Re-open the video for processing
    cap = cv2.VideoCapture(input_video_path)
    
    # Define output video properties (ASCII art size)
    output_width = adjusted_ascii_width * 10
    output_height = adjusted_ascii_height * 20
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec for MP4
    out = cv2.VideoWriter(output_video_path, fourcc, fps, (output_width, output_height))
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Convert frame to ASCII art
        ascii_frame = frame_to_ascii(frame, adjusted_ascii_width, adjusted_ascii_height)
        
        # Write the ASCII frame to output video
        out.write(ascii_frame)
    
    # Release resources
    cap.release()
    out.release()
    cv2.destroyAllWindows()
    if status_label:
        status_label.config(text=f"ASCII art video saved to {output_video_path}")
    messagebox.showinfo("Success", f"ASCII art video saved to {output_video_path}")

def convert_image_to_ascii(input_image_path, output_image_path, ascii_width=80, ascii_height=60, status_label=None):
    """
    Convert an image to ASCII art image.
    Adjusts ASCII width/height to preserve the image's aspect ratio.
    """
    # Read the input image to get size
    image = cv2.imread(input_image_path)
    if image is None:
        messagebox.showerror("Error", "Could not open image.")
        return
    
    frame_height, frame_width = image.shape[:2]
    
    # Adjust ASCII width and height to match the image's aspect ratio
    ratio = frame_width / frame_height
    adjusted_ascii_width = min(ascii_width, int(ascii_height * ratio))
    adjusted_ascii_height = min(ascii_height, int(ascii_width / ratio))
    
    # Convert image to ASCII art using the same frame_to_ascii function
    ascii_image = frame_to_ascii(image, adjusted_ascii_width, adjusted_ascii_height)
    
    # Save the ASCII art image
    cv2.imwrite(output_image_path, ascii_image)
    if status_label:
        status_label.config(text=f"ASCII art image saved to {output_image_path}")
    messagebox.showinfo("Success", f"ASCII art image saved to {output_image_path}")

def convert_webcam_to_ascii(ascii_width=80, ascii_height=60, status_label=None):
    """
    Convert real-time video from webcam to ASCII art and display it.
    Press 'q' to quit.
    Adjusts ASCII width/height to match the camera's aspect ratio and scales font/window if needed.
    """
    # Open the webcam (default camera, index 0)
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        messagebox.showerror("Error", "Could not open webcam.")
        return
    
    # Get initial frame to determine size
    ret, frame = cap.read()
    if not ret:
        messagebox.showerror("Error", "Failed to capture initial frame from webcam.")
        cap.release()
        return
    
    frame_height, frame_width = frame.shape[:2]
    
    # Adjust ASCII width and height to match the camera's aspect ratio
    adjusted_ascii_width = min(ascii_width, int(ascii_height * 1.77))
    adjusted_ascii_height = min(ascii_height, int(ascii_width / 1.77))
    
    print("Adjusted ASCII size to {adjusted_ascii_width}x{adjusted_ascii_height} to match camera ratio. Press 'q' to quit.")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            messagebox.showerror("Error", "Failed to capture frame from webcam.")
            break
        
        # Convert frame to ASCII art with adjusted dimensions and scaling
        ascii_frame = frame_to_ascii(frame, adjusted_ascii_width, adjusted_ascii_height, max_width=1920, max_height=1080)
        
        # Display the ASCII art frame
        cv2.imshow('Real-Time ASCII Art', ascii_frame)
        
        # Resize the window to match the ASCII art dimensions
        cv2.resizeWindow('Real-Time ASCII Art', ascii_frame.shape[1], ascii_frame.shape[0])
        
        # Break on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # Release resources
    cap.release()
    cv2.destroyAllWindows()
    if status_label:
        status_label.config(text="Webcam ASCII art conversion stopped.")


## MAIN ##

if __name__ == "__main__":
    root = tk.Tk()
    app = ASCIIConverterApp(root)
    root.mainloop()