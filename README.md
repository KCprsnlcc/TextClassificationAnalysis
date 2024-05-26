# Emotion Classifier Application

## Overview

This is a desktop application that classifies emotions from text input using a pre-trained Transformer model. The application utilizes `tkinter` for the GUI, `Pillow` for image handling, and `transformers` from Hugging Face for text classification.

## Features

- **Text Input:** Users can input text into a text entry widget.
- **Emotion Classification:** Upon clicking the classify button, the application employs a Transformer model to classify the input text into different emotions.
- **Result Display:** The classified emotions are displayed along with their corresponding confidence scores, visually represented using progress bars.
- **Clear and User-Friendly Interface:** The GUI is simple and intuitive, featuring a header, text entry, and result display sections.

## Requirements

- Python 3.6 or higher
- Required Python libraries: `os`, `sys`, `tkinter`, `ttk`, `Pillow`, `transformers`

## Installation

1. **Clone the Repository:**
   ```sh
   git clone https://github.com/KCprsnlcc/TextClassificationAnalysis.git
   cd TextClassificationAnalysis
   ```

2. **Install Dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

3. **Ensure Model Directory:**
   Ensure the pre-trained Transformer model is available in the `transformermodel/` directory.

4. **Place Logo:**
   Ensure `logo.png` is in the base directory of the project.

## Usage

1. **Run the Application:**
   ```sh
   python main.py
   ```

2. **Enter Text:**
   Type the text you want to classify into the text entry widget.

3. **Classify Emotion:**
   Click the "Classify Emotion" button to see the classified emotions along with confidence scores.

## Code Explanation

### Main Components

1. **Import Statements:**
   Import necessary libraries and modules.
   ```python
   import os
   import sys
   import tkinter as tk
   from tkinter import ttk
   from PIL import Image, ImageTk
   from transformers import pipeline
   ```

2. **Function Definitions:**
   - **classify_emotion:** Classifies the input text and updates the results.
   - **clear_results:** Clears previous results.
   - **display_input_text:** Displays the input text.
   - **update_results:** Updates and displays new classification results.
   - **get_progress_color:** Returns the color for the progress bar based on the score.

3. **Environment Configuration:**
   Disable specific TensorFlow operations.
   ```python
   os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
   ```

4. **Load Model:**
   Load the emotion classification pipeline from the local directory.
   ```python
   classifier = pipeline("text-classification", model=local_model_directory, top_k=None)
   ```

5. **GUI Setup:**
   - **Main Window:** Configure the main window.
   - **Header Frame:** Create a header frame with a logo and title.
   - **Text Entry:** Create a text entry widget for user input.
   - **Classify Button:** Create a button to trigger emotion classification.
   - **Result Frame:** Create a frame to display classification results.
   - **Emotion Label:** Label to display messages or status.

6. **Start Main Event Loop:**
   Start the tkinter main event loop to run the application.
   ```python
   root.mainloop()
   ```

## Acknowledgements

- [Hugging Face](https://huggingface.co/) for providing the pre-trained Transformer models.
- [Python](https://www.python.org/) for being the programming language of choice.
- [tkinter](https://docs.python.org/3/library/tkinter.html) for the GUI framework.
- [Pillow](https://python-pillow.org/) for image handling capabilities.


