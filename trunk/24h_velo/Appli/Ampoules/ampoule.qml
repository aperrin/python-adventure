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
