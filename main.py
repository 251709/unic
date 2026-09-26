from math import sin, cos, radians
from tkinter import Canvas, Tk


def create_line_by_angle(canvas, x1, y1, length, angle_degrees, **kwargs):
    angle_radians = radians(angle_degrees)

    # считаем конечные координаты
    x2 = x1 + length * cos(angle_radians)
    y2 = y1 - length * sin(angle_radians)

    # рисуем линию и возвращаем ее
    return canvas.create_line(x1, y1, x2, y2, **kwargs)


def get_last_coords(canvas, line):
    return canvas.coords(line)[2], canvas.coords(line)[3]


def create_fractal_tree(
    canvas, 
    first_length=100, 
    k_l=0.7, 
    delta_angle=35, 
    depth=5, 
    line_style=None
):
    if line_style is None:
        line_style = {"fill": "blue", "width": 2}

    # создаем первую линию
    x1, y1, angle = 300, 600, 90
    first_line = create_line_by_angle(canvas, x1, y1, first_length, angle, **line_style)

    # рисуем от нее ветки
    x2, y2 = get_last_coords(canvas, first_line)
    create_fractal_branch(
        canvas, x2, y2, first_length, 90, k_l, delta_angle, depth, line_style
    )


def create_fractal_branch(
    canvas,
    x2,
    y2,
    length,
    angle,
    k_l=0.7,
    delta_angle=35,
    depth=5,
    line_style=None,
):
    if depth <= 0:
        return

    if line_style is None:
        line_style = {"fill": "blue", "width": 2}

    length *= k_l
    
    # рисуем линию от конца координат предыдущей
    left_line = create_line_by_angle(
        canvas, x2, y2, length, angle - delta_angle, **line_style
    )
    right_line = create_line_by_angle(
        canvas, x2, y2, length, angle + delta_angle, **line_style
    )

    # передаем рекурсию дальше
    create_fractal_branch(
        canvas, *get_last_coords(canvas, left_line), length, angle-delta_angle,
        k_l, delta_angle, depth - 1, line_style
    )
    create_fractal_branch(
        canvas, *get_last_coords(canvas, right_line), length, angle+delta_angle,
        k_l, delta_angle, depth - 1, line_style
    )


if __name__ == "__main__":
    root = Tk()
    root.geometry("600x600")

    canvas = Canvas(root, width=600, height=600, bg="white")
    canvas.pack()

    create_fractal_tree(
        canvas,
        first_length=140,
        k_l=0.7,
        delta_angle=15,
        depth=10,
        line_style={"fill": "darkgreen", "width": 3},
    )

    root.mainloop()