    import QtQuick 1.0
     
    Rectangle {
        id: page
        width: 500; height: 200
        color: "lightgray"
	
		Text {
			id: plopText
			text : "plop"
			anchors.horizontalCenter: page.horizontalCenter
			y : 100		
		}     

        Text {
            id: helloText
            text: "Hello world!"
            y: 30
            anchors.horizontalCenter: page.horizontalCenter
            font.pointSize: 24; font.bold: true
     
            MouseArea { id: mouseArea; anchors.fill: parent }
     
            states: State {
                name: "down"; when: mouseArea.pressed == true
                PropertyChanges { target: helloText; y: 160; rotation: 360; color: "red" }
            }
     
            transitions: Transition {
                from: ""; to: "down"; reversible: true
                ParallelAnimation {
                    NumberAnimation { properties: "y,rotation"; duration: 1000; easing.type: Easing.InOutQuad }
                    ColorAnimation { duration: 2000 }
                }
            }
        }
     
        Grid {
            id: colorPicker
            x: 4; anchors.bottom: page.bottom; anchors.bottomMargin: 4
            rows: 2; columns: 3; spacing: 3
     
            Cell { cellColor: "red"; onClicked: helloText.color = cellColor }
            Cell { cellColor: "green"; onClicked: helloText.color = cellColor }
            Cell { cellColor: "blue"; onClicked: helloText.color = cellColor }
            Cell { cellColor: "yellow"; onClicked: helloText.color = cellColor }
            Cell { cellColor: "steelblue"; onClicked: helloText.color = cellColor }
            Cell { cellColor: "black"; onClicked: helloText.color = cellColor }
        }
    }


