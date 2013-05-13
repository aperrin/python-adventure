import Qt 4.7
Item{
    id: item1
    width: 800
    height: 640
	
	Rectangle{
anchors.fill:parent
color:"blue"
}

 Image {
     id: souris
     width: 60; height: 60

	x : width / 2;
	y : height / 2;

	source:"./reticule.png"

 }


     MouseArea {
	hoverEnabled: true
         anchors.fill: parent
         onMousePositionChanged: {souris.x = mouse.x - souris.width / 2, souris.y = mouse.y - souris.height / 2}
     }
}


