# Clipboard History Manager

**Clipboard History Manager** is a Python-based desktop application that allows users to track and manage their clipboard history. Built using PyQt6, the application provides a sleek GUI to store, view, edit, and manage clipboard items, including text and images. This tool is ideal for anyone who frequently uses copy-paste operations and wants an efficient way to manage multiple clipboard entries.

## Features

- **Clipboard Monitoring**: Automatically detects changes in the clipboard and stores text and images in history.
- **View and Edit**: Users can view and edit clipboard items directly within the app.
- **Formatting Toolbar**: Allows text formatting with options for bold, italic, and underline.
- **Item Management**: Clear history, copy, delete, or rearrange items for easy access.
- **Dark Theme UI**: A clean, modern interface with a dark theme for comfortable viewing.

## Prerequisites

1. **Python 3.7+**: Ensure Python is installed. [Download Python](https://www.python.org/downloads/)
2. **pip**: Package manager included with Python.

## Setup Instructions

### Step 1: Clone or Download the Repository

To get started, you can clone this repository with the following command:

```bash
git clone https://github.com/yourusername/clipboard-history-manager.git
```

Or download the repository as a ZIP and extract it.

### Step 2: Set Up a Virtual Environment

Navigate to the project directory:

```bash
cd clipboard-history-manager
```

Create a virtual environment (recommended to keep dependencies organized):

```bash
python -m venv screenshot-app
```

Activate the virtual environment:

- **Windows**:

    ```bash
    screenshot-app\Scripts\activate
    ```

- **macOS/Linux**:
  
    ```bash
    source screenshot-app/bin/activate
    ```

### Step 3: Install Dependencies

Install the required dependencies from `requirements.txt`:

```bash
pip install -r requirements.txt
```

### Step 4: Verify Icon Path

Make sure the `favicon.ico` file is present in the project’s root directory, as the application uses this icon in the main window. Update `app.py` if you place `favicon.ico` elsewhere.

### Step 5: Run the Application

To start the application, run:

```bash
python app.py
```

This will open the **Clipboard History Manager** GUI.

## How to Use Clipboard History Manager

1. **Clipboard Monitoring**: The app automatically tracks clipboard changes. When you copy text or images, they will be added to the history list.

2. **View Clipboard Items**: See your clipboard history in a list, displaying timestamps and previews.

3. **Edit Items**: Double-click any item in the history list to open it in the editor. You can make changes, apply text formatting, and save.

4. **Manage Clipboard Items**:
   - **Copy**: Select an item and use the "Copy Selected" button to recopy it to your clipboard.
   - **Delete**: Remove items you no longer need with the "Delete Selected" button.
   - **Clear History**: Clear all items in the clipboard history list.

5. **Status Updates**: The app provides real-time status messages, such as "Monitoring clipboard..." and "Item copied to clipboard."

## Folder Structure

The project files are organized as follows:

```plaintext
clipboard-history-manager/
├── app.py                  # Main application code
├── ClipboardHistory.spec    # PyInstaller specification file for building executable
├── favicon.ico             # Icon for the application
├── requirements.txt        # Project dependencies
├── LICENSE                 # License file
└── README.md               # Project documentation (this file)
```

## Building an Executable (Optional)

To create a standalone executable file for the application, use **PyInstaller**, which is already listed in `requirements.txt`.

1. **Install PyInstaller** if it’s not already installed:

    ```bash
    pip install pyinstaller
    ```

2. **Create the Executable**:

   Run the following command:

    ```bash
    pyinstaller --onefile --windowed --name "ClipboardHistoryManager" --icon="favicon.ico" app.py
    ```

   This will generate an executable in the `dist` folder. You can now run the application by launching the `ClipboardHistoryManager.exe` file.

## Troubleshooting

- **Clipboard Not Updating**: If clipboard history isn’t updating, ensure that the app is running in the foreground and check your system clipboard settings.
- **Icon Not Displaying**: Verify the `favicon.ico` path in `app.py`.
- **Dependency Issues**: Reinstall dependencies if the app does not launch.
- **Virtual Environment Issues**: If you encounter issues with activating the virtual environment, recreate it.

## Contributing

Feel free to open issues or submit pull requests for bug fixes or new features.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
