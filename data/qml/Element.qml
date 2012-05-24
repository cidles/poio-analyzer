import Qt 4.7

Column {
    
    Row {
        id: utterance
        spacing: 10
        Text {
            id: preUtt
            text: modelData.id
            anchors.margins: 5
            font.weight: Font.Bold
            font.capitalization: Font.SmallCaps
        }
        Text {
            id: utt
            anchors.margins: 5
            font.weight: Font.Bold
            text: modelData.utterance
        }
    }

    Row {
        id: words
        spacing: 20
        
        Column {
            Text {
                id: word
                text: "words"
                font.capitalization: Font.SmallCaps
                color: "#a0a0a0"
            }
            Text {
                id: morpheme
                text: "morph"
                font.capitalization: Font.SmallCaps
                color: "#a0a0a0"
            }
            Text {
                id: gloss
                text: "gloss"
                font.capitalization: Font.SmallCaps
                color: "#a0a0a0"
            }
        }
    
        Repeater { model: modelData.ilElements
            Column {
                Text {
                    id: word
                    text: modelData[1]
                    color: modelData[4] ? "green" : "black"
                }
                Text {
                    id: morpheme
                    text: modelData[2]
                    font.italic: true
                    color: modelData[4] ? "green" : "black"
                }
                Text {
                    id: gloss
                    text: modelData[3]
                    color: modelData[4] ? "green" : "black"
                }
            }
        }
    }

    Column {
        id: translations
        Repeater { model: modelData.translations
            Row {
                spacing: 20
                Text {
                    id: preTrans
                    text: "trans"
                    color: "#a0a0a0"
                    font.capitalization: Font.SmallCaps
                }
                Text {
                    id: trans
                    font.italic: true
                    text: modelData[1]
                }
            }
        }
    }
}
