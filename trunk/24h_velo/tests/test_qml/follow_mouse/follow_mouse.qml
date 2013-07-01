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

        source:"./images/ampoule_eteinte.png"

 }
