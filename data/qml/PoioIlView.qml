import Qt 4.7

Rectangle {

    id: mainScreen
    color: "#ffffff"

    Column {
        id: list
        
        anchors.fill: parent
        spacing: 10
        anchors.margins: 5
        
        Repeater {
            id: repeater
            model: resultModel
            Column {
                spacing: 10
                
                Text {
                    id: filename
                    property int yPos: mapFromItem(null, 0, 0).y
                    font.underline: true
                    font.weight: Font.Bold
                    font.pointSize: 14
                    text: modelData.filename
                    onYPosChanged: console.log(yPos)
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
    }

}