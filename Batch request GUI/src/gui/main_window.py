from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                            QTextEdit, QLineEdit, QPushButton, QLabel,
                            QMessageBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from src.gui.settings_panel import SettingsPanel
from src.gui.batch_dialog import BatchRequestDialog
from src.api.client import APIClient

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("LLMs batch requests Chatbot")
        self.setMinimumSize(900, 600)
        
        # Initialize API client
        self.api_client = APIClient()
        
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Create chat display
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        font = QFont("Times New Roman", 10)
        self.chat_display.setFont(font)
        main_layout.addWidget(self.chat_display)
        
        # Create input area
        input_layout = QHBoxLayout()
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Type your message here...")
        self.input_field.returnPressed.connect(self.send_message)
        font = QFont("Times New Roman", 10)
        self.input_field.setFont(font)
        
        self.send_button = QPushButton("Send")
        self.send_button.clicked.connect(self.send_message)
        input_layout.addWidget(self.input_field)
        input_layout.addWidget(self.send_button)
        
        # Create control buttons
        button_layout = QHBoxLayout()
        self.settings_button = QPushButton("Settings")
        self.settings_button.clicked.connect(self.show_settings)
        self.batch_button = QPushButton("Batch Request")
        self.batch_button.clicked.connect(self.show_batch_dialog)
        button_layout.addWidget(self.settings_button)
        button_layout.addWidget(self.batch_button)
        
        # Add layouts to main layout
        main_layout.addLayout(input_layout)
        main_layout.addLayout(button_layout)
        
        # Initialize panels/dialogs
        self.settings_panel = None
        self.batch_dialog = None
        
        # Add welcome message
        self.display_system_message("Welcome to AI Chatbot! Configure your settings and start chatting.")
        
        # Check if API is configured
        if not self.api_client.load_config():
            self.display_system_message("Please configure your API settings to begin.")
        
    def send_message(self):
        """Handle sending a message"""
        message = self.input_field.text().strip()
        if not message:
            return
            
        # Check if API is configured
        if not self.api_client.config:
            if not self.api_client.load_config():  # Try reloading config
                QMessageBox.warning(
                    self,
                    "Warning",
                    "Please configure API settings first."
                )
                self.show_settings()
                return
            
        # Display user message
        self.display_user_message(message)
        self.input_field.clear()
        
        try:
            # Get AI response
            response = self.api_client.send_request(message)
            self.display_ai_message(response)
            
        except Exception as e:
            self.display_system_message(f"Error: {str(e)}")
            if "API configuration" in str(e):
                self.show_settings()
            
    def display_user_message(self, message):
        """Display a user message in the chat"""
        self.chat_display.append(f'<div style="text-align: right;"><b>You:</b> {message}</div>')
        
    def display_ai_message(self, message):
        """Display an AI message in the chat"""
        self.chat_display.append(f'<div style="text-align: left;"><b>AI:</b> {message}</div>')
        
    def display_system_message(self, message):
        """Display a system message in the chat"""
        self.chat_display.append(
            f'<div style="text-align: center; color: gray; font-style: italic;">{message}</div>'
        )
            
    def show_settings(self):
        """Show the settings panel"""
        if not self.settings_panel:
            self.settings_panel = SettingsPanel(self)
        self.settings_panel.show()
        
    def show_batch_dialog(self):
        """Show the batch request dialog"""
        # Check if API is configured
        if not self.api_client.config:
            if not self.api_client.load_config():  # Try reloading config
                QMessageBox.warning(
                    self,
                    "Warning",
                    "Please configure API settings first."
                )
                self.show_settings()
                return
            
        if not self.batch_dialog:
            self.batch_dialog = BatchRequestDialog(self.api_client, self)
        self.batch_dialog.show()
