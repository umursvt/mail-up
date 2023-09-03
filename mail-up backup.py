import sys
import smtplib
import os
import mimetypes
import pandas as pd
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QTextEdit, QPushButton, QVBoxLayout, QWidget, QFileDialog, QMessageBox
from PyQt5.QtGui import QFont
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime

class EmailApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.sender_label = QLabel("Gönderen E-posta:")
        self.sender_input = QLineEdit("sender mail adresi")
        self.subject_label = QLabel("Konu:")
        self.subject_input = QLineEdit()
        self.body_label = QLabel("İçerik:")
      
        self.attach_label_button = QPushButton("Maile Ek Yükle")
        self.any_label = QLabel("")
        self.delete_all = QPushButton("")
        self.delete_all.setEnabled(False)
        self.body_input = QTextEdit(self)
        self.body_input3 = QTextEdit(self)
        self.body_input.setStyleSheet(
            "QTextEdit {"
            "   backgroundColor: #e0e0e0 "
            "   border: 5px solid #d0d0d0;"
            "   padding: 5px;"
            "   border-radius: 5px;"
            "   font-size: 16px;"
            "   color: #333;"
            "}"
        )
        self.body_input3.setStyleSheet(
            "QTextEdit {"
            "   backgroundColor: #e0e0e0 "
            "   border: 5px solid #d0d0d0;"
            "   padding: 5px;"
            "   border-radius: 5px;"
            "   font-size: 16px;"
            "   color: #333;"
            "}"
        )
        font = QFont("New York Times", 12)
        self.body_input.setFont(font)
        self.attach_image_button = QPushButton("Resim Ekle")
        
        self.resim_label = QLabel("")
        self.send_button = QPushButton("E-posta Gönder")

        self.attach_label_button.clicked.connect(self.attach_any)
        self.send_button.clicked.connect(self.send_email)
        self.attach_image_button.clicked.connect(self.attach_image)
        self.delete_all.clicked.connect(self.delete_all_function)

        layout = QVBoxLayout()
        layout.addWidget(self.sender_label)
        layout.addWidget(self.sender_input)
        layout.addWidget(self.any_label)
        layout.addWidget(self.delete_all)
        layout.addWidget(self.attach_label_button)
        layout.addWidget(self.subject_label)
        layout.addWidget(self.subject_input)
        layout.addWidget(self.body_label)
        layout.addWidget(self.body_input)
        layout.addWidget(self.resim_label)
        layout.addWidget(self.attach_image_button)
      
        layout.addWidget(self.body_input3)
        layout.addWidget(self.send_button)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.setWindowTitle("E-posta Gönderme Uygulaması")
        self.setGeometry(550, 200, 900, 700)

        self.attached_any_data = {}
        self.attached_image_data = None
        self.send_count = 0
        self.total_send = 0
        self.update_send_info()

    def update_send_info(self):
        self.send_button.setText(f"E-posta Gönder ({self.send_count}/{self.total_send})")

    def attach_any(self):
        file_dialog = QFileDialog()
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_paths, _ = file_dialog.getOpenFileNames(
            self, "Dosya Seç", "", "Tüm Dosyalar ( *.pdf *.pptx *.xlsx *.pdf *.doc *.docx *.jpg *.png *.jpeg *.gif);;Tüm Dosyalar (*)", options=options,
        )
        for file_path in file_paths:
            if file_path:
                with open(file_path, "rb") as file:
                    file_data = file.read()
                    file_name = os.path.basename(file_path)
                    self.attached_any_data[file_name] = file_data
        self.update_attached_labels()

    def attach_image(self):
        file_dialog = QFileDialog()
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_path, _ = file_dialog.getOpenFileName(
            self, "Resim Seç", "", "Resim Dosyaları (*.jpeg *.jpg *.png *.gif);;Tüm Dosyalar (*)", options=options,
        )
        if file_path:
            self.resim_label.setText(f"Resim Dosyası Maile Eklendi: {file_path}")
            with open(file_path, "rb") as image_file:
                self.attached_image_data = image_file.read()

    def update_attached_labels(self):
        self.attached_files = list(self.attached_any_data.keys())
        self.any_label.setText("Dosyalar Maile Eklendi:\n" + "\n".join(self.attached_files))
        if len(self.attached_files) > 0:
            self.delete_all.setEnabled(True)
            self.delete_all.setText("Hepsini Sil")
        else:
            self.delete_all.setEnabled(False)
            self.delete_all.setText("")

    def delete_all_function(self):
        self.attached_any_data.clear()
        self.update_attached_labels()

    def send_email(self):
        # if not self.body_input.toPlainText():
        #     QMessageBox.warning(self, "Uyarı", "Lütfen mailinize mesaj yazınız.")
        #     return

        read_excel = pd.read_excel("deneme.xlsx")
        self.total_send = len(read_excel)
        self.send_count = 0
        self.update_send_info()

        try:
            smtp_server = "smtp.eu.mailgun.org"
            smtp_port = 587
            email_address = "mail bolumu"
            email_password = "sifre bolumu "

            for index, row in read_excel.iterrows():
                self.send_count += 1
                self.update_send_info()

                name = row["isimler"]
                mail = row["mailler"]
                receiver_email = mail
                subject = self.subject_input.text()
                body = f"Sayın {name},\n"
                body2 = "\n" + self.body_input.toPlainText() + "\n"
                

                msg = MIMEMultipart()
                msg["From"] = "info@mg.howdenturkey.net"
                msg["To"] = receiver_email
                msg["Subject"] = subject

                for file_path, file_data in self.attached_any_data.items():
                    mime_type, _ = mimetypes.guess_type(file_path)
                    attachment = MIMEApplication(file_data, _subtype=mime_type.split("/")[1])
                    attachment.add_header("Content-Disposition", f'attachment; filename="{file_path}"')
                    msg.attach(attachment)

                if self.attached_image_data:
                    image_part = MIMEImage(self.attached_image_data, name="attached_image.jpg")
                    msg.attach(image_part)
                    pic = f'<p><img class="photo" src="cid:attached_image.jpg"></p>'
                    body2 += pic
                html_content = f'''
                    <html>
                    <head>
                    <style>
                    @import url('https://fonts.googleapis.com/css2?family=Manrope:wght@200;300&display=swap');
                                    .photo {{
                                        width: 75%;
                                    }}
                                    .main-body {{
                                        font-family: Roboto, sans-serif; 
                                        font-size: 14px;
                                    }}
                    </style>
                    </head>
                    <body>
                    <p><span >{body}</span></p>
                    <p>Howden Türkiye olarak sigorta sektörü ile ilgili güncel bilgilerin yer aldığı  “HowdenLife” dergimizin Temmuz-Ağustos-Eylül 2023 sayısı yayında…</p>
                 
                    <p>Howden Grup’taki son gelişmeler, Deprem sonrası öne çıkan Dask konusunda Türk Reasürans Genel Müdürü Selva Eren ile yaptığımız röportaj, penetrasyon oranı ve primlerin değerlendirilmesi, Tekne Sigortası ile ilgili ayrıntıları ve Sürdürülebilirlik ve Sigorta konusunu ele alıyoruz.</p>
                  
                    <p>https://www.howden.ist/2023-temmuz/</p>
                        <div class="photo" > {body2} </div> 
                         
                    <p>Dijital dergimiz aynı zamanda "Turkcell Dergilik" uygulamasında da yer almaktadır.</p>
                    <p>Keyifli okumalar,</p>
                    <p>Saygılarımızla,</p>
                    <p>Howden Türkiye</p>
                    </body> 
                    </html>
                '''
                msg.attach(MIMEText(html_content, "html"))

                server = smtplib.SMTP(smtp_server, smtp_port)
                server.starttls()
                server.login(email_address, email_password)
                server.sendmail(email_address, receiver_email, msg.as_string())
                server.quit()

                now = datetime.now()
                timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
                read_excel.at[index, "konu"] = self.subject_input.text()
                read_excel.at[index, "Gönderilme Tarihi"] = timestamp
                read_excel.at[index, "Gönderildi mi?"] = "Evet"

                QMessageBox.information(self, "Bilgi", "Mailler başarıyla gönderildi.")
                print(f'Mail başarılı bir şekilde gönderildi: {index, row}')
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"E-posta gönderilirken bir hata oluştu: {str(e)}")
            now = datetime.now()
            timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
            read_excel.at[index, "konu"] = self.subject_input.text()
            read_excel.at[index, "Gönderilme Tarihi"] = timestamp
            read_excel.at[index, "Gönderildi mi?"] = "Hayır"
            read_excel.to_excel("deneme.xlsx", index=False)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EmailApp()
    window.show()
    sys.exit(app.exec_())
