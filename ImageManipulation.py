import tkinter as tk
from tkinter import filedialog
from tkinter import colorchooser
from PIL import Image, ImageOps, ImageTk, ImageFilter, ImageGrab
from tkinter import ttk
import numpy as np
import cv2

root = tk.Tk()
root.geometry("1000x600")
root.title("Let's Generate Some Images")
root.config(bg="Grey")

file_path = ""

def add_image():
    global file_path
    file_path = filedialog.askopenfilename(initialdir='C:\\Users\\user\\Files\\Pictures\\Screenshots') #update to your file path
    image = Image.open(file_path)
    width, height = int(image.width / 2), int(image.height / 2)
    image = image.resize((width, height), Image.LANCZOS)
    canvas.config(width=image.width, height=image.height)
    image = ImageTk.PhotoImage(image)
    canvas.image = image
    canvas.create_image(0, 0, image=image, anchor="nw")

def clear_canvas():
    canvas.delete("all")

def save_image():
    x0 = canvas.winfo_rootx()
    y0 = canvas.winfo_rooty()
    x1 = x0 + canvas.winfo_width()
    y1 = y0 + canvas.winfo_height()

    im = ImageGrab.grab((x0, y0, x1, y1))
    im.save('saveimage.png')
    im.show()


def apply_filter(filter_name):
    if filter_name == "Noise Removal":
        apply_noise_removal()
    elif filter_name == "Size down":
        size_down()
    elif filter_name == "Rotate":
        rotate()
    elif filter_name == "Emboss":
        emboss()
    elif filter_name == "Sharpen":
        sharpen()
    elif filter_name == "Facial Recognition":
        faces()

def remove_noise(image, intensity):
    # Apply Gaussian blur to remove noise
    denoised_image = cv2.GaussianBlur(image, (int(intensity), int(intensity)), 0)
    return denoised_image

def apply_noise_removal():
    global image
    if file_path and Image:
        intensity = intensity_slider.get()
        image = np.array(image)
        denoised_image = remove_noise(image, intensity)
        image = Image.fromarray(cv2.cvtColor(denoised_image, cv2.COLOR_BGR2RGB))
        add_image(image)

'''def display_image(image):
    photo = ImageTk.PhotoImage(image)
    canvas.config(width=image.width, height=image.height)
    canvas.image = photo
    canvas.create_image(0, 0, image=photo, anchor="nw")'''



        
def size_down():
    image = Image.open(file_path)
    width, height = int(image.width / 4), int(image.height / 4)
    image = image.resize((width, height), Image.LANCZOS)
    image = ImageTk.PhotoImage(image)
    canvas.image = image
    canvas.create_image(0, 0, image=image, anchor="nw")

def rotate():
    image = Image.open(file_path)
    width, height = int(image.width / 2), int(image.height / 2)
    image = image.resize((width, height), Image.LANCZOS)
    image = image.rotate(90)
    image = ImageTk.PhotoImage(image)
    canvas.image = image
    canvas.create_image(0, 0, image=image, anchor="nw")

def emboss():
    image = Image.open(file_path)
    width, height = int(image.width / 2), int(image.height / 2)
    image = image.resize((width, height), Image.LANCZOS)
    image = image.filter(ImageFilter.EMBOSS)
    image = ImageTk.PhotoImage(image)
    canvas.image = image
    canvas.create_image(0, 0, image=image, anchor="nw")

def sharpen():
    image = Image.open(file_path)
    width, height = int(image.width / 2), int(image.height / 2)
    image = image.resize((width, height), Image.LANCZOS)
    image = image.filter(ImageFilter.SHARPEN)
    image = ImageTk.PhotoImage(image)
    canvas.image = image
    canvas.create_image(0, 0, image=image, anchor="nw")

def faces():
    image = Image.open(file_path)
    width, height = int(image.width / 2), int(image.height / 2)
    image = image.resize((width, height), Image.LANCZOS)
    image = np.asarray(image)
    face_classifier = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    face = face_classifier.detectMultiScale(image, scaleFactor=1.1, minNeighbors=5, minSize=(40, 40))
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    for (x, y, w, h) in face:
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        # Get the region of interest (ROI) for the face
        # roi_gray = gray[y:y + h, x:x + w]
        roi_color = image[y:y + h, x:x + w]

        sharpened_face = cv2.detailEnhance(roi_color, sigma_s=10, sigma_r=0.15)

        # replace sharpened face image
        image[y:y + h, x:x + w] = sharpened_face
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = Image.fromarray(image)
    image = ImageTk.PhotoImage(image)
    canvas.image = image
    canvas.create_image(0, 0, image=image, anchor="nw")

left_frame = tk.Frame(root, width=200, height=600, bg="white")
left_frame.pack(side="left", fill="y")

canvas = tk.Canvas(root, width=750, height=600)
canvas.pack()

first_button = tk.Button(left_frame, text="Add Image", command=add_image, bg="white")
first_button.pack(pady=15)

clear_button = tk.Button(left_frame, text="Clear", command=clear_canvas, bg="#FF9797")
clear_button.pack(pady=10)

save_button = tk.Button(left_frame, text="Save Image", command=save_image, bg="lightblue")
save_button.pack(pady=15)

noise_removal_label = tk.Label(left_frame, text="Noise Removal", bg="white")
noise_removal_label.pack()

intensity_slider = tk.Scale(left_frame, from_=1, to=15, orient=tk.HORIZONTAL, label="Intensity")
intensity_slider.pack()


filter_label = tk.Label(left_frame, text="Image Interpolation", bg="white")
filter_label.pack()
filter_combobox = ttk.Combobox(left_frame, values=["Noise Removal", "Size down", "Rotate", "Emboss", "Sharpen" , "Facial Recognition"])
filter_combobox.pack()

filter_combobox.bind("<<ComboboxSelected>>", lambda event: apply_filter(filter_combobox.get()))

root.mainloop()