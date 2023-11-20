from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QLabel, QVBoxLayout, QHBoxLayout
import qrcode
import pyshorteners
import os

class Home(QWidget):
    def __init__(self):
        super().__init__()
        self.counter = 1
        self.settings()
        self.initUI()
        self.submit.clicked.connect(self.connects)
        
    def initUI(self):
        self.input = QLineEdit()
        self.text = QLabel("Paste a URL here: ")
        self.alert = QLabel()
        self.input.setPlaceholderText("Paste here...")
        self.submit = QPushButton("Generate")
        
        self.master = QVBoxLayout()
        row1 = QHBoxLayout()

        row1.addWidget(self.text)
        row1.addWidget(self.input)
        self.master.addWidget(self.alert)
        self.master.addLayout(row1)
        self.master.addWidget(self.submit)
        self.setLayout(self.master)
    
    def connects(self):
        if self.submit.text() == "Generate":
            self.submit.setText("Reset")
            self.text.setText("Shortened URL:")
            self.create_url()
            self.create_QR()
        else:
            self.input.clear()
            self.alert.clear()
            self.text.setText("Paste a URL here: ")
            self.submit.setText("Generate")

    def create_QR(self):
        my_code = qrcode.make(self.input.text())
        my_code.save("code.png")
        self.save_image(my_code)

    def create_url(self):
        shortner = pyshorteners.Shortener()
        short_url = shortner.tinyurl.short(self.input.text())
        self.input.setText(short_url)

    def save_image(self, code):
        path = os.path.expanduser("~/Desktop")
        file_name = f"qr{self.counter}.png"
        file_path = os.path.join(path, file_name)
        
        try:
            code.save(file_path)
            self.alert.setText(f"QR code image saved to desktop as: {file_name}")
            self.counter += 1
        except Exception as e:
            self.alert.setText(f"Error saving QR code image: {str(e)}")
        
    def settings(self):
        self.setWindowTitle("ShortnerQR")
        self.resize(500, 100)

if __name__ == "__main__":
    app = QApplication([])
    main = Home()
    main.show()
    app.exec_()
