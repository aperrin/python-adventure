import Qt 4.7
Item{
    id: item1
    width: 800
    height: 640

    signal positionRequired;

    function updatePosition(x, y) {
        souris.x = x
		souris.y = y
    }
	
	Rectangle{
		anchors.fill:parent
		color:"blue"
		}

	Rectangle {
		id: souris
		objectName:'plop'
		width: 60; height: 60
		x : width / 2;
		y : height / 2;
		color : 'red'

 }


}


