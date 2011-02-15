import Qt 4.7

Rectangle {
    id: mainScreen
    color: "#ffffff"
    
    Component {
        id: viewDelegate
        Item {
            height: utterance.height + words.height + translations.height + 10

            Rectangle {
                id: utterance
                height: utt.height
                width: preUtt.width + utt.width
                Text {
                    id: preUtt
                    text: modelData.id
                    anchors.margins: 5
                    font.weight: Font.Bold
                    font.capitalization: Font.SmallCaps
                }
                Text {
                    id: utt
                    anchors.left: preUtt.right
                    anchors.margins: 5
                    text: modelData.utterance
                }
            }

            Row {
                id: words
                anchors.top: utterance.bottom
                spacing: 10
                
                Rectangle {
                    height: word.height + morpheme.height + gloss.height
                    width: Math.max(word.width, morpheme.width, gloss.width) + 10
                    Text {
                        id: word
                        text: "words"
                        font.capitalization: Font.SmallCaps
                        color: "#a0a0a0"
                    }
                    Text {
                        id: morpheme
                        anchors.top: word.bottom
                        text: "morph"
                        font.capitalization: Font.SmallCaps
                        color: "#a0a0a0"
                    }
                    Text {
                        id: gloss
                        anchors.top: morpheme.bottom
                        text: "gloss"
                        font.capitalization: Font.SmallCaps
                        color: "#a0a0a0"
                    }
                }
                
                Repeater { model: modelData.ilElements
                    Rectangle {
                        height: word.height + morpheme.height + gloss.height
                        width: Math.max(word.width, morpheme.width, gloss.width)
                        Text {
                            id: word
                            text: modelData[1]
                            color: modelData[4] ? "green" : "black"
                        }
                        Text {
                            id: morpheme
                            anchors.top: word.bottom
                            text: modelData[2]
                            font.italic: true
                            color: modelData[4] ? "green" : "black"
                        }
                        Text {
                            id: gloss
                            anchors.top: morpheme.bottom
                            text: modelData[3]
                            color: modelData[4] ? "green" : "black"
                        }
                    }
                }
            }
            
            Column {
                id: translations
                anchors.top: words.bottom
                Repeater { model: modelData.translations
                    Rectangle {
                        height: trans.height
                        width: preTrans.width + trans.width
                        Text {
                            id: preTrans
                            text: "trans"
                            anchors.margins: 5
                            color: "#a0a0a0"
                            font.capitalization: Font.SmallCaps
                        }
                        Text {
                            id: trans
                            anchors.left: preTrans.right
                            anchors.margins: 5
                            font.italic: true
                            text: modelData[1]
                        }
                    }
                }
            }
        }
    }
        
    ListView {
        anchors.fill: parent
        orientation: ListView.Vertical
        
        model: resultModel
        delegate: viewDelegate
    }
}