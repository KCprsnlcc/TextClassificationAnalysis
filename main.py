import os
import sys
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from transformers import pipeline
import mysql.connector
from datetime import datetime

# Database connection setup
db_config = {
    'user': 'root',  # default MySQL user
    'password': '',  # default MySQL password
    'host': '127.0.0.1',  # localhost
    'database': 'emotion_analysis'  # the database you created
}

# Function to insert analysis results into the database
def insert_results(input_text, emotions):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        query = "INSERT INTO analysis_results (input_text, neutral, sadness, happiness, fear, anger, surprise, disgust) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        values = (input_text, *emotions)
        cursor.execute(query, values)
        conn.commit()
        cursor.close()
        conn.close()
        show_notification("Analysis Result is in Database")
    except mysql.connector.Error as err:
        show_notification(f"Failed to insert data into database: {err}")

# Function to classify emotion
def classify_emotion():
    text = text_entry.get("1.0", tk.END).strip()
    if text:
        clear_results()
        predictions = classifier(text)[0]
        emotions = {emotion: 0.0 for emotion in specified_emotions}
        for prediction in predictions:
            label = prediction['label'].lower()
            if label in specified_emotions:
                emotions[label] = prediction['score']
        update_results(predictions)
        # Save results to database
        insert_results(text, list(emotions.values()))
    else:
        emotion_label.config(text="Please enter some text.", foreground='red')

# Function to show flat UI notification
def show_notification(message):
    notification_window = tk.Toplevel(root)
    notification_window.title("Notification")
    notification_window.configure(background="#1e272e")
    window_width = 400
    window_height = 100
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    notification_window.geometry(f"{window_width}x{window_height}+{x}+{y}")
    notification_window.resizable(False, False)
    notification_window.attributes("-topmost", True)
    notification_window.overrideredirect(True)
    notification_frame = tk.Frame(notification_window, bg="#1e272e")
    notification_frame.pack(fill="both", expand=True)
    message_label = ttk.Label(
        notification_frame,
        text=message,
        font=("Helvetica", 12),
        foreground="white",
        background="#1e272e"
    )
    message_label.pack(padx=10, pady=10)
    close_button = ttk.Button(
        notification_frame,
        text="Close",
        command=notification_window.destroy,
        style="Flat.TButton"
    )
    close_button.pack(padx=10, pady=10)
    style = ttk.Style(notification_window)
    style.theme_use("clam")
    style.configure("Toplevel", background="#1e272e")
    style.configure("TLabel", background="#1e272e", foreground="white")
    style.configure("Flat.TButton", background="#10ac84", foreground="white", font=("Helvetica", 12), borderwidth=0)

# Function to clear previous results
def clear_results():
    for widget in result_frame.winfo_children():
        widget.destroy()

# Function to display input text
# def display_input_text(text):
#     input_label = ttk.Label(result_frame, text=f"Input Text: {text}", font=("Helvetica", 12))
#     input_label.pack(anchor='center')

# Function to update results
def update_results(predictions):
    for prediction in predictions:
        label = ttk.Label(result_frame, text=f"{prediction['label']}: {prediction['score'] * 100:.2f}%",
                          font=("Helvetica", 12), background="#FFFFFF", foreground="#1e272e")
        label.pack(anchor='center')
        progress_color = get_progress_color(prediction['score'])
        progress = ttk.Progressbar(result_frame, style=f"{progress_color}.Horizontal.TProgressbar", length=400,
                                   mode='determinate')
        progress['value'] = prediction['score'] * 100
        progress.pack(pady=5, anchor='center')


# Function to get progress bar color based on score
def get_progress_color(score):
    if score >= 0.5:
        return "green"
    elif score >= 0.3:
        return "orange"
    else:
        return "red"

# Set TensorFlow environment variable to disable oneDNN custom operations
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

# Specify the path to the local model directory
local_model_directory = "transformermodel/"

# Load the emotion classification pipeline from the local directory
classifier = pipeline("text-classification", model=local_model_directory, top_k=None)

# Specify the emotions to classify
specified_emotions = ["neutral", "sadness", "happiness", "fear", "anger", "surprise", "disgust"]

# Create the main window
root = tk.Tk()
root.title("Emotion Classifier")
root.geometry("500x700")
root.configure(bg='#FFFFFF')

# Calculate the position to center the window
window_width = 500
window_height = 700
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2

# Set the window position
root.geometry(f"{window_width}x{window_height}+{x}+{y}")
root.overrideredirect(True)

# Header frame
header_frame = tk.Frame(root, bg="#1e272e")
header_frame.pack(side="top", fill="x")

# Get the base path for bundled files
if getattr(sys, 'frozen', False):
    base_path = sys._MEIPASS
else:
    base_path = os.path.abspath(".")

logo_path = os.path.join(base_path, "logo.png")
logo_img = Image.open(logo_path)
logo_img = logo_img.resize((50, 50))
logo = ImageTk.PhotoImage(logo_img)
logo_label = tk.Label(header_frame, image=logo, bg="#1e272e")
logo_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

title_description_frame = tk.Frame(header_frame, bg="#1e272e")
title_description_frame.grid(row=0, column=1, padx=10, pady=10, sticky="w")

title_label = ttk.Label(
    title_description_frame,
    text="Text Emotion Analysis",
    font=("Helvetica", 16),
    foreground="white",
    background="#1e272e"
)
title_label.grid(row=0, column=0, sticky="w")

description_label = ttk.Label(
    title_description_frame,
    text="Classify your emotion through text.",
    font=("Helvetica", 12),
    foreground="white",
    background="#1e272e"
)
description_label.grid(row=1, column=0, sticky="w")

# Configure styles
style = ttk.Style()
style.theme_use("clam")
style.configure("Flat.TButton", background="#10ac84", foreground="white", font=("Helvetica", 12), borderwidth=0)
style.configure("TLabel", background="#FFFFFF", font=("Helvetica", 12))
style.configure("green.Horizontal.TProgressbar", troughcolor='#CCCCCC', background='#10ac84', thickness=20)
style.configure("orange.Horizontal.TProgressbar", troughcolor='#CCCCCC', background='orange', thickness=20)
style.configure("red.Horizontal.TProgressbar", troughcolor='#CCCCCC', background='red', thickness=20)

# Create a text entry widget
text_entry = tk.Text(root, height=5, width=40, font=("Helvetica", 12), bd=0, highlightthickness=1,
                     highlightbackground="#CCCCCC")
text_entry.pack(padx=20, pady=20)

# Create a button to classify text
classify_button = ttk.Button(root, text="Classify Emotion", style="Flat.TButton", command=classify_emotion)
classify_button.pack(pady=10)

# Create a frame to display the progress bars
result_frame = tk.Frame(root, bg='#FFFFFF')
result_frame.pack(pady=(50, 20))

# Create a label to display the emotion status
emotion_label = ttk.Label(root, text="", font=("Helvetica", 12))
emotion_label.pack(pady=(0, 10))

# Start the main event loop
root.mainloop()
