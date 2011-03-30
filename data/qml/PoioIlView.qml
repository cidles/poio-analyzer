import Qt 4.7

Rectangle {

    id: mainScreen
    color: "#ffffff"
    property alias currentFileIndex: view.currentIndex

    ListView {
        id: view
        property int maxWidth: 0

        anchors.fill: parent
        spacing: 10
        contentWidth: 10000
        anchors.margins: 10
        highlightMoveDuration: 1
        highlightMoveSpeed: 30000
        
        model: resultModel
        delegate: Column {
            spacing: 10
            Text {
                font.underline: true
                font.weight: Font.Bold
                font.pointSize: 14
                text: modelData.filename
            }
            Column {
                spacing: 10
                Repeater {
                    model: modelData.utterances
                    delegate: Utterance {}
                }
            }
        }
    }

    ScrollBar {
        target: view
    }

    ScrollBarV {
        target: view
    }

}