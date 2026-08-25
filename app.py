from tkinter import *
from PIL import Image, ImageTk
import numpy as np

root = Tk()
root.title("Image Analyzer")
root.geometry("900x500")

# Image size
IMG_WIDTH = 350
IMG_HEIGHT = 350

# Load original image
original_img = Image.open(r"D:\image analyzer\Image analyzer github\example image.jpg")
original_img = original_img.resize((IMG_WIDTH, IMG_HEIGHT))

# Convert for Tkinter
original_tk = ImageTk.PhotoImage(original_img)

# Left image label
left_label = Label(root, image=original_tk, relief="solid", bd=2)
left_label.place(x=30, y=30)

# Right image label
right_label = Label(root)
right_label.place(x=520, y=30)


def generate_image():

    # Convert image to grayscale NumPy array
    gray = original_img.convert("L")
    img_array = np.array(gray, dtype=float)

    # Sobel kernels
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

    # Apply Sobel convolution
    for y in range(1, height - 1):
        for x in range(1, width - 1):

            region = img_array[y-1:y+2, x-1:x+2]

            sx = np.sum(region * Gx)
            sy = np.sum(region * Gy)

            edge[y, x] = np.sqrt(sx**2 + sy**2)

    # Normalize to 0-255
    edge = (edge / edge.max()) * 255
    edge = edge.astype(np.uint8)

    # Convert back to PIL Image
    generated_img = Image.fromarray(edge)

    # Convert to Tkinter image
    generated_tk = ImageTk.PhotoImage(generated_img)

    right_label.config(image=generated_tk, relief="solid", bd=2)
    right_label.image = generated_tk  # Prevent garbage collection


generate_button = Button(
    root,
    text="Generate Edges",
    command=generate_image,
    font=("Arial", 12)
)

generate_button.place(x=380, y=420)

root.mainloop()
