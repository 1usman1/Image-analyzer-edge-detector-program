import time
from tkinter import *
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import numpy as np

# -------------------------------
# Window Setup
# -------------------------------
root = Tk()
root.title("Image Analyzer - Sobel Edge Detection")
root.geometry("950x550")
root.config(bg="#5E5E5E")

IMG_WIDTH = 350
IMG_HEIGHT = 350

original_img = None
generated_img = None

# -------------------------------
# Frames
# -------------------------------
left_frame = Frame(root, width=IMG_WIDTH, height=IMG_HEIGHT, bd=2, relief="solid", bg="gray")
left_frame.place(x=30, y=30)

right_frame = Frame(root, width=IMG_WIDTH, height=IMG_HEIGHT, bd=2, relief="solid", bg="gray")
right_frame.place(x=550, y=30)

# -------------------------------
# Image placeholders
# -------------------------------
left_label = Label(left_frame, text="Original Image", font=("Arial", 14))
left_label.place(relx=0.5, rely=0.5, anchor="center")

right_label = Label(right_frame, text="Processed Image", font=("Arial", 14))
right_label.place(relx=0.5, rely=0.5, anchor="center")

# -------------------------------
# Statistics label under processed image
# -------------------------------
stats_label = Label(
    root,
    text="Detected edge pixels: -\nEdge coverage: -\nThreshold: -\nImage size: -",
    font=("Arial", 11),
    bg="#5E5E5E",
    fg="white",
    justify="left",
    anchor="w"
)
stats_label.place(x=750, y=390)

# -------------------------------
# Threshold slider
# -------------------------------
threshold_slider = Scale(
    root,
    from_= 0,
    to = 255,
    orient=HORIZONTAL,
    label="threshold",
    length=138
)
threshold_slider.place(x=390,y=470)
threshold_slider.set(80)

# -------------------------------
# Load Image
# -------------------------------
def load_image():
    global original_img

    filename = filedialog.askopenfilename(
        title="Select Image",
        filetypes=[
            ("Image Files", "*.jpg *.jpeg *.png *.bmp *.gif"),
            ("All Files", "*.*")
        ]
    )

    if not filename:
        return

    original_img = Image.open(filename)
    original_img = original_img.resize((IMG_WIDTH, IMG_HEIGHT))

    original_tk = ImageTk.PhotoImage(original_img)

    left_label.config(image=original_tk, text="")
    left_label.image = original_tk

# -------------------------------
# Generate Sobel Edges
# -------------------------------
def generate_image():
    start = time.perf_counter()

    global generated_img

    if original_img is None:
        messagebox.showwarning(
            "No Image",
            "Please load an image first."
        )
        return

    gray = original_img.convert("L")
    img_array = np.array(gray, dtype=float)

    Gx = np.array([
        [-1, 0, 1],
        [-2, 0, 2],
        [-1, 0, 1]
    ])

    Gy = np.array([
        [-1, -2, -1],
        [ 0,  0,  0],
        [ 1,  2,  1]
    ])

    height, width = img_array.shape
    edge = np.zeros((height, width))

    for y in range(1, height - 1):
        for x in range(1, width - 1):
            region = img_array[y-1:y+2, x-1:x+2]

            sx = np.sum(region * Gx)
            sy = np.sum(region * Gy)

            edge[y, x] = np.sqrt(sx**2 + sy**2)

    max_val = edge.max()

    if max_val > 0:
        edge = (edge / max_val) * 255

    # Threshold
    threshold = threshold_slider.get()
    edge[edge < threshold] = 0
    edge[edge >= threshold] = 255

    edge = edge.astype(np.uint8)

    generated_img = Image.fromarray(edge)
    generated_tk = ImageTk.PhotoImage(generated_img)

    right_label.config(image=generated_tk, text="")
    right_label.image = generated_tk
    end = time.perf_counter()
    # -------------------------------
    # Image statistics
    # -------------------------------
    edge_pixels = np.count_nonzero(edge == 255)
    total_pixels = width * height
    edge_coverage = (edge_pixels / total_pixels) * 100

    stats_text = (
        f"Detected edge pixels: {edge_pixels:,}\n"
        f"Edge coverage: {edge_coverage:.1f}%\n"
        f"Threshold: {threshold}\n"
        f"Image size: {width} x {height}\n"
        f"Process time: {(end - start)*1000}"
    )
    stats_label.config(text=stats_text)

# -------------------------------
# Save Result
# -------------------------------
def save_image():
    if generated_img is None:
        messagebox.showwarning(
            "Nothing to Save",
            "Generate an image first."
        )
        return

    filename = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=[
            ("PNG Image", "*.png"),
            ("JPEG Image", "*.jpg"),
            ("All Files", "*.*")
        ]
    )

    if filename:
        generated_img.save(filename)
        messagebox.showinfo(
            "Saved",
            "Image saved successfully."
        )

# -------------------------------
# Buttons
# -------------------------------
load_button = Button(
    root,
    text="Load Image",
    command=load_image,
    font=("Arial", 12),
    width=15
)
load_button.place(x=180, y=430)

generate_button = Button(
    root,
    text="Generate Edges",
    command=generate_image,
    font=("Arial", 12),
    width=15
)
generate_button.place(x=390, y=430)

save_button = Button(
    root,
    text="Save Result",
    command=save_image,
    font=("Arial", 12),
    width=15
)
save_button.place(x=600, y=430)

# -------------------------------
# Start Program
# -------------------------------
root.mainloop()
