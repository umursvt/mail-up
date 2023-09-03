import sys
import os
import requests
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QTextEdit, QPushButton, QVBoxLayout, QWidget, QFileDialog
from PyQt5.QtGui import QFont

class EmailApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.sender_label = QLabel("Gönderen E-posta:")
        self.sender_input = QLineEdit("info@mg.howdenturkey.net")
        self.receiver_label = QLabel("Alıcı E-posta:")
        self.receiver_input = QLineEdit("egemen.vatansever@howden.com.tr")
        self.subject_label = QLabel("Konu:")
        self.subject_input = QLineEdit("deneme22")
        self.body_label = QLabel("İçerik:")
        self.body_input = QTextEdit()
        self.attach_label_button = QPushButton("Dosya Ekle")
        self.attach_label_button.clicked.connect(self.attach_any)
        self.send_button = QPushButton("E-posta Gönder")
        self.send_button.clicked.connect(self.send_email)  # Burada self.send_email işlevini bağla

        layout = QVBoxLayout()
        layout.addWidget(self.sender_label)
        layout.addWidget(self.sender_input)
        layout.addWidget(self.receiver_label)
        layout.addWidget(self.receiver_input)
        layout.addWidget(self.subject_label)
        layout.addWidget(self.subject_input)
        layout.addWidget(self.body_label)
        layout.addWidget(self.body_input)
        layout.addWidget(self.attach_label_button)
        layout.addWidget(self.send_button)

        central_widget = QWidget()
        central_widget.setLayout(layout)

        self.setCentralWidget(central_widget)
        self.setWindowTitle("E-posta Gönderme Uygulaması")
        self.setGeometry(550, 200, 400, 400)
        self.attached_any_data = []

    def attach_any(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        files, _ = QFileDialog.getOpenFileNames(self, "Dosya Seç", "", "Tüm Dosyalar (*)", options=options)
        if files:
            self.attached_any_data.extend(files)

    def send_email(self):
        api_key = "sifre"
        domain = "domain"
        sender = self.sender_input.text()
        receiver = self.receiver_input.text()
        subject = self.subject_input.text()
        body = self.body_input.toPlainText()

        response = requests.post(
            f"https://api.mailgun.net/v3/{domain}/messages",
            auth=("api", api_key),
            data={
                "from": sender,
                "to": receiver,
                "subject": subject,
                "text": body
            }
        )
        print(response)

        if response.status_code == 200:
            print("E-posta başarıyla gönderildi.")
        else:
            print("E-posta gönderilirken bir hata oluştu.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EmailApp()
    window.show()
    sys.exit(app.exec_())
