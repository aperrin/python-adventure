import Qt 4.7
Rectangle{
    id: rect1
    width: 1000
    height: 1000
    property int sep_x: 1000;
    property int sep_y: 500;

    property string st_amp1: "./images/ampoule_allumee.png"
    property string st_amp2: "./images/ampoule_allumee.png"
    property string st_amp3: "./images/ampoule_allumee.png"
    property string st_amp4: "./images/ampoule_allumee.png"

    color: "black"


 Image {
     id: amp1
     width: 200; height: 200/420*698
     x : 350
     y : 100
     source: st_amp1
 }


 Image {
     id: amp2
     width: 200; height: 200/420*698
     x : amp1.x + sep_x
     y : amp1.y

        source: st_amp2
 }

 Image {
     id: amp3
     width: 200; height: 200/420*698
     x : amp1.x
     y : amp1.y + sep_y

        source: st_amp3
 }


 Image {
     id: amp4
     width: 200; height: 200/420*698
     x : amp1.x + sep_x
     y : amp1.y + sep_y

        source: st_amp4
 }
}



Image {
    id: amp2
    width: size_x; height: size_y
    x : 350
    y : 100
    source: st_amp1
}

Image {
    id: amp3
    width: size_x; height: size_y
    x : 350
    y : 100
    source: st_amp1
}

Image {
    id: amp4
    width: size_x; height: size_y
    x : 350
    y : 100
    source: st_amp1
}

Image {
    id: amp5
    width: size_x; height: size_y
    x : 350
    y : 100
    source: st_amp1
}

Image {
    id: amp6
    width: size_x; height: size_y
    x : 350
    y : 100
    source: st_amp1
}

Image {
    id: amp7
    width: size_x; height: size_y
    x : 350
    y : 100
    source: st_amp1
}

Image {
    id: amp8
    width: size_x; height: size_y
    x : 350
    y : 100
    source: st_amp1
}

Image {
    id: amp9
    width: size_x; height: size_y
    x : 350
    y : 100
    source: st_amp1
}

Image {
    id: amp10
    width: size_x; height: size_y
    x : 350
    y : 100
    source: st_amp1
}

Image {
    id: amp11
    width: size_x; height: size_y
    x : 350
    y : 100
    source: st_amp1
}

Image {
    id: amp12
    width: size_x; height: size_y
    x : 350
    y : 100
    source: st_amp1
}

Image {
    id: amp13
    width: size_x; height: size_y
    x : 350
    y : 100
    source: st_amp1
}

Image {
    id: amp14
    width: size_x; height: size_y
    x : 350
    y : 100
    source: st_amp1
}

Image {
    id: amp15
    width: size_x; height: size_y
    x : 350
    y : 100
    source: st_amp1
}

Image {
    id: amp16
    width: size_x; height: size_y
    x : 350
    y : 100
    source: st_amp1
}

Image {
    id: amp17
    width: size_x; height: size_y
    x : 350
    y : 100
    source: st_amp1
}

Image {
    id: amp18
    width: size_x; height: size_y
    x : 350
    y : 100
    source: st_amp1
}

Image {
    id: amp19
    width: size_x; height: size_y
    x : 350
    y : 100
    source: st_amp1
}

Image {
    id: amp20
    width: size_x; height: size_y
    x : 350
    y : 100
    source: st_amp1
}

Image {
    id: amp21
    width: size_x; height: size_y
    x : 350
    y : 100
    source: st_amp1
}

Image {
    id: amp22
    width: size_x; height: size_y
    x : 350
    y : 100
    source: st_amp1
}

Image {
    id: amp23
    width: size_x; height: size_y
    x : 350
    y : 100
    source: st_amp1
}

Image {
    id: amp24
    width: size_x; height: size_y
    x : 350
    y : 100
    source: st_amp1
}
