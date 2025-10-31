# ECCode IME - Simple Chinese Input Method

Welcome to the ECCode IME project! This Python-based input method allows users to type Chinese characters using ECCode, a component-based Chinese input method. The system supports both **Simplified** and **Traditional** Chinese characters and enables efficient character selection.

This project uses the **ECCode** dataset and **Tkinter** for the user interface.

## **Features**

- **ECCode-based Input**: Type ECCode combinations to select Chinese characters.
- **Live Candidate Suggestions**: As you type the ECCode, candidates are suggested in real-time.
- **Commit from List**: Select characters from the live suggestions (1–9 or Space/Enter to commit).
- **Committed Text**: All selected characters appear in the **Composed Text** area.
- **Reverse Lookup**: Search for ECCode combinations by entering a character.
- **Clear Button**: Clears the input field and the committed text area.
- **Copy & Save**: Save the composed text or copy it to the clipboard.
- Loads the ECCode mapping dataset (`eccode_dataset.xlsx`).
- Lets you type ECCode codes (e.g., `yh` → `一`, `zkii` → `中`).
- You can load a different Excel dataset at any time.

---

## **Getting Started**

### 1. **Clone or Download the Project**
Clone or download this repository to your local machine. If you prefer cloning it, use the following command:

```bash
git clone https://github.com/mahimalmuntashir/eccode-ime.git
```

### 2. **Install Dependencies**
Ensure you have Python 3.9+ installed on your system. Then, install the required libraries by running:

```bash
pip install -r requirements.txt
```
This will install the necessary libraries:

pandas (for reading and processing the ECCode dataset)

openpyxl (for working with Excel files)

tkinter (for the graphical user interface)

### 3. **Download the ECCode Dataset**
You can load a dataset of ECCode mappings. If not already included in the repository, you can download it from a public source or create your own in Excel. The dataset should be in the following format:

A column with Chinese characters.

Columns containing the ECCode combinations for each character.

Make sure the dataset is in Excel format (.xlsx) and named eccode_dataset.xlsx, or place your dataset in the same folder as the Python script and select it through the interface.

## **How to Run**
Set Up a Virtual Environment (Optional but recommended):

```bash
python -m venv myvenv
myvenv\Scripts\activate  # For Windows
source myvenv/bin/activate  # For macOS/Linux
Install Dependencies:
```

```bash
pip install pandas openpyxl
Run the Application:
```

```bash
python eccode_ime.py
```

## **How to Use**
### 1. Running the Program
After installing dependencies and ensuring the dataset is ready, you can run the program by executing the command above. The application will launch with the following features:

Input Code Field: Type ECCode (e.g., yh, zkii) into the input field.

Candidate List: Characters corresponding to your input will be shown in a list. You can select a character by clicking or using number keys (1–9).

Committed Text Area: All characters you commit will appear in the text area. This area is read-only, and users cannot directly edit it.

History Strip: A history of committed characters is shown at the top of the window.

Reverse Lookup: Enter a Chinese character in the "Reverse Lookup" field to see all the ECCode mappings for that character.

### 2. Buttons and Actions
Load Excel: Load a different ECCode dataset from your computer.

Save Text: Save your composed text to a file.

Clear: Clears the input field and the committed text area.

Copy: Copies the committed text to your clipboard.

Help: Provides instructions for using the program.

## **Shortcuts**
1–9: Select the corresponding candidate from the list.

Space / Enter: Commit the first candidate from the list.

Esc: Clear the current code in the input field.

## **File Structure**
```graphql
 
ecocode-ime/
│
├── eccode_ime.py              # Main Python file for running the IME
├── eccode_dataset.xlsx        # The ECCode dataset (Chinese character mappings)
├── requirements.txt           # List of required Python libraries
└── README.md                  # Instructions on how to use the project
```

## **Dataset Format**
The app expects an Excel file with the following structure:

A column named “汉字” containing the character.

One or more unnamed columns (e.g., “Unnamed: 5”, “Unnamed: 6”, …) containing ECCode combinations.

The app concatenates these code columns into a single lowercase code string.

## **Troubleshooting**
### 1. No Dataset Loaded
If the app opens with no dataset:

Click “Load Excel…” and select the eccode_dataset.xlsx file.

### 2. Missing Libraries (pandas/openpyxl)
If you encounter an error related to pandas or openpyxl, you can install the required libraries by running:

```bash
pip install pandas openpyxl
```

Frequently Asked Questions (FAQ)
### 1. How do I add my own dataset?
If you want to use your own ECCode dataset:

Ensure it is in Excel (.xlsx) format.

The dataset should have two columns: one for Chinese characters and one for ECCode combinations.

After modifying the dataset, click "Load Excel..." within the application to upload your file.

### 2. Can I use this on Windows/Mac/Linux?
Yes! This program is cross-platform and will work on any system with Python 3.9+ and the required libraries installed.

### 3. Is there a mobile version?
Currently, this is a desktop-only application built using Tkinter. To use it on mobile, you would need to adapt the code for mobile platforms like Android or iOS, which would involve using frameworks like Kivy or BeeWare.

### 4. How do I contribute to this project?
If you want to contribute, feel free to fork the repository, make your changes, and submit a pull request. Please ensure that your changes are well-documented and tested.

## **License**
This project is licensed under the MIT License - see the LICENSE file for details. 
