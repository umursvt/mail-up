import QtQuick 2.15
import QtQuick.Controls 2.15

ApplicationWindow {
    visible: true
    width: 800
    height: 600
    title: "E-posta Gönderme Uygulaması"

   Rectangle {
        width: parent.width
        height: parent.height

        Column {
            spacing: 10
            anchors.centerIn: parent

            // ... (diğer bileşenler)

            Button {
                text: "E-posta Gönder"
                onClicked: sendEmail()
            }

            // Uyarı mesajı göstermek için bir Popup
            Popup {
                id: popupMessage
                modal: true
                contentItem: Rectangle {
                    width: parent.width * 0.7
                    height: parent.height * 0.3
                    color: "lightgray"
                    border.color: "black"
                    radius: 10

                    Text {
                        anchors.centerIn: parent
                        text: popupText
                        font.pixelSize: 18
                        wrapMode: Text.WordWrap
                    }

                    Button {
                        anchors.bottom: parent.bottom
                        width: parent.width
                        text: "Tamam"
                        onClicked: popupMessage.close()
                    }
                }
            }
        }
    }
}