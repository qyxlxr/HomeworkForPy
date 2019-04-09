<<<<<<< HEAD
#!/usr/bin/env python3
""" From  turtle-example-suite     tdemo_yinyang.py

Another drawing suitable as a beginner's
programming example.

The small circles are drawn by the circle
command.
Modifier:Shawn Lee
"""
from turtle import *


# noinspection PyUnresolvedReferences
def yin(radius, color1, color2):
    """ From Demo,the half of TaiJi picture is drew by this function.
 It include three semicircle forming Outline and a full cirle.
  Three parameters is pen color、filled color and radius."""
    width(3)
    color("black", color1)
    begin_fill()
    circle(radius / 2., 180)
    circle(radius, 180)
    left(180)
    circle(-radius / 2., 180)
    end_fill()
    left(90)
    up()
    forward(radius * 0.35)
    right(90)
    down()
    color(color1, color2)
    begin_fill()
    circle(radius * 0.15)
    end_fill()
    left(90)
    up()
    backward(radius * 0.35)
    down()
    left(90)


def gradient(radius, use_color):
    """ The Function is aimed at a demo how make a animation by turtle.
    I used `tracer(0)` and `update()`  to control turtle's drawing.
    Two parameters is filled color and radius."""
    reset()
    a = pos()
    a = a - (0, radius)
    speed('fastest')
    hideturtle()
    setpos(a)
    color(use_color)
    begin_fill()
    circle(200)
    end_fill()


# noinspection PyUnresolvedReferences
def main():
    reset()
    loop_count = 0
    i = 0.001
    # speed('fast')
    speed('normal')
    yin(200, "black", "white")
    yin(200, "white", "black")
    hideturtle()
    tracer(0)
    while i:
        clear()
        if i < 1.1:
            left(i)
            yin(200, "black", "white")
            yin(200, "white", "black")
            i = i + 0.001
        elif i < 20:
            left(i)
            yin(200, "black", "white")
            yin(200, "white", "black")
            i = i ** 1.01
        else:
            loop_count = loop_count + 1
            grey = 0xDDDDDD - (0x010101 * (loop_count // 10))
            gradient(200, "#{:0>6x}".format(grey))
            if grey == 0:
                break
        update()
    reset()
    yin(200, "black", "white")
    yin(200, "white", "black")


if __name__ == '__main__':
    main()
=======
#!/usr/bin/env python3
""" From  turtle-example-suite     tdemo_yinyang.py

Another drawing suitable as a beginner's
programming example.

The small circles are drawn by the circle
command.
Modifier:Shawn Lee
"""
from turtle import *


# noinspection PyUnresolvedReferences
def yin(radius, color1, color2):
    """ From Demo,the half of TaiJi picture is drew by this function.
 It include three semicircle forming Outline and a full cirle.
  Three parameters is pen color、filled color and radius."""
    width(3)
    color("black", color1)
    begin_fill()
    circle(radius / 2., 180)
    circle(radius, 180)
    left(180)
    circle(-radius / 2., 180)
    end_fill()
    left(90)
    up()
    forward(radius * 0.35)
    right(90)
    down()
    color(color1, color2)
    begin_fill()
    circle(radius * 0.15)
    end_fill()
    left(90)
    up()
    backward(radius * 0.35)
    down()
    left(90)


def gradient(radius, use_color):
    """ The Function is aimed at a demo how make a animation by turtle.
    I used `tracer(0)` and `update()`  to control turtle's drawing.
    Two parameters is filled color and radius."""
    reset()
    a = pos()
    a = a - (0, radius)
    speed('fastest')
    hideturtle()
    setpos(a)
    color(use_color)
    begin_fill()
    circle(200)
    end_fill()


# noinspection PyUnresolvedReferences
def main():
    reset()
    loop_count = 0
    i = 0.001
    # speed('fast')
    speed('normal')
    yin(200, "black", "white")
    yin(200, "white", "black")
    hideturtle()
    tracer(0)
    while i:
        clear()
        if i < 1.1:
            left(i)
            yin(200, "black", "white")
            yin(200, "white", "black")
            i = i + 0.001
        elif i < 20:
            left(i)
            yin(200, "black", "white")
            yin(200, "white", "black")
            i = i ** 1.01
        else:
            loop_count = loop_count + 1
            grey = 0xDDDDDD - (0x010101 * (loop_count // 10))
            gradient(200, "#{:0>6x}".format(grey))
            if grey == 0:
                break
        update()
    reset()
    yin(200, "black", "white")
    yin(200, "white", "black")


if __name__ == '__main__':
    main()
>>>>>>> 935aad4963c03550332b91db00a33439606f5059
