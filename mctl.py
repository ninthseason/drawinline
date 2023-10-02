import numpy as np
import pyautogui as ag

ag.PAUSE = 0.01


def draw_trajectory(trajectory, bias):
    trajectory = np.array(trajectory) + bias
    start_point = trajectory[0]
    ag.moveTo(*start_point)
    # print("start at", start_point)
    ag.mouseDown(button='left')
    for i in trajectory[1:]:
        ag.moveTo(*i, duration=0)
    ag.mouseUp(button='left')


def move_trajectory(trajectory, bias):
    trajectory = np.array(trajectory) + bias
    ag.moveTo(*trajectory[0])
    for i in trajectory[1:]:
        ag.moveTo(*i, duration=0)


def draw_stroke(stroke, bias):
    for tau in stroke:
        draw_trajectory(tau, bias)


def move_stroke(stroke, bias):
    for tau in stroke:
        move_trajectory(tau, bias)


def test_draw(bias):
    trajectory = np.array([[0, 0], [100, 100]])
    draw_trajectory(trajectory, bias)


def test_move(bias):
    trajectory = np.array([[0, 0], [100, 100]]) + bias
    start_point = trajectory[0]
    ag.moveTo(*start_point)
    # print("start at", start_point)
    for i in trajectory[1:]:
        # print("to", i)\
        ag.keyDown()
        ag.moveTo(*i, duration=0)


if __name__ == '__main__':
    import time

    for i in [3, 2, 1]:
        print(i)
        time.sleep(1)
    window_bias = (344, 448)
    from imgprocess import file2stroke

    stroke = file2stroke(r"test.jpg", resize=(700, 700))
    # print(stroke)
    # print(len(draw_stroke), len(draw_stroke[0]))
    draw_stroke(stroke, window_bias)
    # test_draw(window_bias)
    # test_move(window_bias)
