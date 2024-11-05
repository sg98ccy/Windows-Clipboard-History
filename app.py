from PyQt6.QtWidgets import (QApplication, QMainWindow, QListWidget, QListWidgetItem, 
                             QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QLabel, 
                             QDialog, QTextEdit, QScrollArea, QToolBar)
from PyQt6.QtGui import QPixmap, QImage, QIcon, QTextCharFormat, QFont, QAction, QTextDocument, QTextImageFormat
from PyQt6.QtCore import Qt, QSize, QMimeData, QBuffer, QByteArray, QUrl
import sys
import time
import os

# Set the path for the favicon icon
FAVICON_PATH = os.path.abspath("favicon.ico")

class ClipboardHistoryItem:
    def __init__(self, content, content_type, timestamp):
        self.content = content
        self.content_type = content_type
        self.timestamp = timestamp

class CustomListWidget(QListWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("""
            QListWidget {
                background-color: #2E2E2E;
                border: none;
                border-radius: 10px;
                padding: 5px;
            }
            QListWidget::item {
                background-color: #3A3A3A;
                color: #E0E0E0;
                border-radius: 5px;
                margin-bottom: 5px;
                padding: 8px;
            }
            QListWidget::item:selected {
                background-color: #4A4A4A;
            }
            QListWidget::item:hover {
                background-color: #454545;
            }
        """)

class StyledButton(QPushButton):
    def __init__(self, text, icon_path=None):
        super().__init__(text)
        self.setStyleSheet("""
            QPushButton {
                background-color: #4A4A4A;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 5px;
                font-weight: bold;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #5A5A5A;
            }
            QPushButton:pressed {
                background-color: #3A3A3A;
            }
        """)
        if icon_path:
            self.setIcon(QIcon(icon_path))
            self.setIconSize(QSize(18, 18))
        self.setCursor(Qt.CursorShape.PointingHandCursor)

class ItemEditDialog(QDialog):
    def __init__(self, item, parent=None):
        super().__init__(parent)
        self.item = item
        self.setWindowTitle("Edit Clipboard Item")
        self.setGeometry(200, 200, 600, 400)
        self.setStyleSheet("""
            QDialog {
                background-color: #2E2E2E;
                color: #E0E0E0;
            }
            QTextEdit {
                background-color: #3A3A3A;
                color: #E0E0E0;
                border: none;
                border-radius: 5px;
                padding: 10px;
                font-size: 13px;
            }
            QLabel {
                color: #E0E0E0;
                font-size: 14px;
            }
            QToolBar {
                background-color: #3A3A3A;
                border: none;
                padding: 5px;
            }
            QToolBar QToolButton {
                background-color: #4A4A4A;
                color: white;
                border: none;
                padding: 5px;
                border-radius: 3px;
            }
            QToolBar QToolButton:hover {
                background-color: #5A5A5A;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setSpacing(10)

        # Add timestamp label
        timestamp_label = QLabel(f"Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(item.timestamp))}")
        layout.addWidget(timestamp_label)

        # Create toolbar for text formatting options
        toolbar = QToolBar()
        layout.addWidget(toolbar)

        # Add text formatting actions
        bold_action = QAction(QIcon("icons/bold.png"), "Bold", self)
        bold_action.triggered.connect(self.toggle_bold)
        toolbar.addAction(bold_action)

        italic_action = QAction(QIcon("icons/italic.png"), "Italic", self)
        italic_action.triggered.connect(self.toggle_italic)
        toolbar.addAction(italic_action)

        underline_action = QAction(QIcon("icons/underline.png"), "Underline", self)
        underline_action.triggered.connect(self.toggle_underline)
        toolbar.addAction(underline_action)

        # Create text edit widget for editing content
        self.content_edit = QTextEdit()
        if item.content_type == "text":
            self.content_edit.setHtml(item.content)
        elif item.content_type == "image":
            cursor = self.content_edit.textCursor()
            image_format = QTextImageFormat()
            image = QImage()
            image.loadFromData(item.content)
            image_format.setWidth(image.width())
            image_format.setHeight(image.height())
            buffer = QBuffer()
            buffer.open(QBuffer.OpenModeFlag.WriteOnly)
            image.save(buffer, "PNG")
            image_data = buffer.data().toBase64().data()
            image_format.setName(f"data:image/png;base64,{image_data.decode()}")
            cursor.insertImage(image_format)
        layout.addWidget(self.content_edit)

        # Add save and cancel buttons
        button_layout = QHBoxLayout()
        save_button = StyledButton("Save")
        save_button.clicked.connect(self.accept)
        cancel_button = StyledButton("Cancel")
        cancel_button.clicked.connect(self.reject)
        
        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)
        layout.addLayout(button_layout)

    def toggle_bold(self):
        self.toggle_format('font-weight', 'bold', 'normal')

    def toggle_italic(self):
        self.toggle_format('font-style', 'italic', 'normal')

    def toggle_underline(self):
        self.toggle_format('text-decoration', 'underline', 'none')

    def toggle_format(self, format_type, format_value, default_value):
        cursor = self.content_edit.textCursor()
        char_format = cursor.charFormat()
        
        if format_type == 'font-weight':
            if char_format.fontWeight() == QFont.Weight.Bold:
                char_format.setFontWeight(QFont.Weight.Normal)
            else:
                char_format.setFontWeight(QFont.Weight.Bold)
        elif format_type == 'font-style':
            char_format.setFontItalic(not char_format.fontItalic())
        elif format_type == 'text-decoration':
            char_format.setFontUnderline(not char_format.fontUnderline())
        
        cursor.setCharFormat(char_format)
        self.content_edit.setTextCursor(cursor)

    def get_edited_content(self):
        return self.content_edit.toHtml()

class ClipboardHistoryApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Clipboard History")
        self.setGeometry(100, 100, 600, 500)
        self.setWindowIcon(QIcon(FAVICON_PATH))
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1E1E1E;
            }
            QLabel {
                color: #E0E0E0;
            }
        """)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        self.layout.setSpacing(10)
        self.layout.setContentsMargins(15, 15, 15, 15)

        self.title_label = QLabel("Clipboard History")
        self.title_label.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            margin-bottom: 15px;
            color: #E0E0E0;
        """)
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.title_label)

        self.history_list = CustomListWidget()
        self.history_list.itemDoubleClicked.connect(self.edit_item)
        self.layout.addWidget(self.history_list)

        self.button_layout = QHBoxLayout()
        self.clear_button = StyledButton("Clear History", "icons/trash.png")
        self.clear_button.clicked.connect(self.clear_history)
        self.button_layout.addWidget(self.clear_button)

        self.copy_button = StyledButton("Copy Selected", "icons/copy.png")
        self.copy_button.clicked.connect(self.copy_selected_item)
        self.button_layout.addWidget(self.copy_button)

        self.delete_button = StyledButton("Delete Selected", "icons/delete.png")
        self.delete_button.clicked.connect(self.delete_selected_item)
        self.button_layout.addWidget(self.delete_button)

        self.layout.addLayout(self.button_layout)

        self.status_label = QLabel("Monitoring clipboard...")
        self.status_label.setStyleSheet("color: #808080; font-style: italic; margin-top: 10px; font-size: 12px;")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.status_label)

        self.clipboard_history = []

        # Connect to clipboard dataChanged signal for immediate updates
        QApplication.clipboard().dataChanged.connect(self.check_clipboard)

    def check_clipboard(self):
        try:
            clipboard = QApplication.clipboard()
            mime_data = clipboard.mimeData()

            if mime_data.hasHtml():
                content = mime_data.html()
                content_type = "text"
            elif mime_data.hasText():
                content = mime_data.text()
                content_type = "text"
            elif mime_data.hasImage():
                image = mime_data.imageData()
                buffer = QBuffer()
                buffer.open(QBuffer.OpenModeFlag.WriteOnly)
                image.save(buffer, "PNG")
                content = buffer.data()
                content_type = "image"
            else:
                return

            timestamp = time.time()
            
            # Check if the content already exists in the history
            existing_item = next((item for item in self.clipboard_history if item.content == content), None)
            
            if existing_item:
                # Move the existing item to the top
                self.clipboard_history.remove(existing_item)
                self.clipboard_history.append(existing_item)
                existing_item.timestamp = timestamp
                
                # Remove the old item from the list widget
                for i in range(self.history_list.count()):
                    if self.history_list.item(i).data(Qt.ItemDataRole.UserRole) == existing_item:
                        self.history_list.takeItem(i)
                        break
                
                # Add the item to the top of the list
                self.add_item_to_list(existing_item)
            else:
                # Add new item
                item = ClipboardHistoryItem(content, content_type, timestamp)
                self.clipboard_history.append(item)
                self.add_item_to_list(item)

        except Exception as e:
            self.status_label.setText(f"Error: {str(e)}")

    def add_item_to_list(self, item):
        list_item = QListWidgetItem()
        if item.content_type == "text":
            doc = QTextDocument()
            doc.setHtml(item.content)
            preview = doc.toPlainText().replace('\n', ' ')[:40] + "..." if len(doc.toPlainText()) > 40 else doc.toPlainText()
            list_item.setText(f"{time.strftime('%H:%M:%S', time.localtime(item.timestamp))}: {preview}")
        elif item.content_type == "image":
            list_item.setText(f"{time.strftime('%H:%M:%S', time.localtime(item.timestamp))}: [Image]")
            pixmap = QPixmap()
            pixmap.loadFromData(item.content)
            scaled_pixmap = pixmap.scaled(30, 30, Qt.AspectRatioMode.KeepAspectRatio, 
                                        Qt.TransformationMode.SmoothTransformation)
            list_item.setIcon(QIcon(scaled_pixmap))

        list_item.setData(Qt.ItemDataRole.UserRole, item)
        self.history_list.insertItem(0, list_item)
        self.history_list.setCurrentItem(list_item)  # Select the newly added item

    def clear_history(self):
        self.clipboard_history.clear()
        self.history_list.clear()
        self.status_label.setText("History cleared")

    def copy_selected_item(self):
        selected_items = self.history_list.selectedItems()
        if selected_items:
            item = selected_items[0].data(Qt.ItemDataRole.UserRole)
            
            clipboard = QApplication.clipboard()
            mime_data = QMimeData()
            if item.content_type == "text":
                mime_data.setHtml(item.content)
                doc = QTextDocument()
                doc.setHtml(item.content)
                mime_data.setText(doc.toPlainText())
            elif item.content_type == "image":
                mime_data.setImageData(QImage.fromData(item.content))
            
            clipboard.setMimeData(mime_data)
            self.status_label.setText("Item copied to clipboard")

    def delete_selected_item(self):
        selected_items = self.history_list.selectedItems()
        if selected_items:
            index = self.history_list.row(selected_items[0])
            item = self.history_list.item(index).data(Qt.ItemDataRole.UserRole)
            self.clipboard_history.remove(item)
            self.history_list.takeItem(index)
            self.status_label.setText("Item deleted from history")

    def edit_item(self, list_item):
        item = list_item.data(Qt.ItemDataRole.UserRole)
        
        dialog = ItemEditDialog(item, self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            edited_content = dialog.get_edited_content()
            item.content = edited_content
            item.content_type = "text"  # Treat all edited content as text (HTML)
            item.timestamp = time.time()  # Update the timestamp

            # Remove the item from its current position
            
            self.clipboard_history.remove(item)
            self.history_list.takeItem(self.history_list.row(list_item))

            # Add the edited item to the top of the list
            self.clipboard_history.append(item)
            self.add_item_to_list(item)

            # Set the edited content as the current clipboard content
            clipboard = QApplication.clipboard()
            mime_data = QMimeData()
            mime_data.setHtml(edited_content)
            doc = QTextDocument()
            doc.setHtml(edited_content)
            mime_data.setText(doc.toPlainText())
            clipboard.setMimeData(mime_data)
            
            self.status_label.setText("Item edited successfully, moved to top, and set as current clipboard content")

def exception_hook(exctype, value, traceback):
    print(f"An exception occurred: {exctype.__name__}: {value}")
    sys.__excepthook__(exctype, value, traceback)

sys.excepthook = exception_hook

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ClipboardHistoryApp()
    window.show()
    sys.exit(app.exec())