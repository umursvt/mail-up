import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl

class EditorWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        self.webview = QWebEngineView()

        self.webview.setHtml("""
            <html>
            <head>
                <script src="https://cdn.ckeditor.com/ckeditor5/36.0.1/classic/ckeditor.js"></script>
            </head>
            <body>
                <textarea id="editor"></textarea>
                <script>
                    ClassicEditor
                        .create(document.querySelector('#editor'), {
                            ckfinder: {
                                uploadUrl: '/upload'  // Yükleme URL'sini ayarlayın
                            }
                        })
                        .catch(error => {
                            console.error(error);
                        });
                </script>
            </body>
            </html>
        """)

        layout.addWidget(self.webview)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EditorWindow()
    window.show()
    sys.exit(app.exec_())
