#!/usr/bin/python3
from pynput.mouse import Controller as MouseController
from pynput.keyboard import Key, Controller as KeyboardController
from screeninfo import get_monitors
from time import sleep
import numpy as np
import random

TIME_DELAY = 15
BROWSER_TAB_RANGE = (1, 9)

class MouseEvent:
    def _delay_decorator(function):
        def magic(self, *args, **kwargs) :
            sleep(0.5)
            function(self, *args, **kwargs)
        return magic

    def __init__(self) -> None:
        self.mouse_controller = MouseController()
        self.keyboard = KeyboardController()

        self.HEIGHT = get_monitors()[0].height
        self.WIDTH = get_monitors()[0].width
        self.CENTER = (int(self.WIDTH/2), int(self.HEIGHT/2))

    def move_to_center_position(self):
        self.move_to_position(self.mouse_controller.position, self.CENTER)

    def move_to_random_position(self):
        random_position = (random.randint(0, self.WIDTH),
                           random.randint(0, self.HEIGHT))
        self.move_to_position(self.mouse_controller.position, random_position)

    def move_to_position(self, start, end):
        points = self.get_point_list(start, end, 20)
        for point in points:
            self.mouse_controller.position = point
            sleep(0.03)

    def get_point_list(self, start, end, steps):
        number_of_points = steps
        xs = np.linspace(start[0], end[0], number_of_points)
        ys = np.linspace(start[1], end[1], number_of_points)
        point_list = []
        for i in range(len(xs)):
            point_list.append((int(xs[i]), int(ys[i])))

        return point_list

    @_delay_decorator
    def switch_window(self):
        with self.keyboard.pressed(Key.alt):
            self.keyboard.press(Key.tab)
            self.keyboard.release(Key.tab)

    @_delay_decorator
    def switch_browser_tabs(self, tab_number=int):
        with self.keyboard.pressed(Key.alt):
            self.keyboard.press(str(tab_number))
            sleep(0.5)
            self.keyboard.release(str(tab_number))

    @_delay_decorator
    def switch_next_tab(self):
        with self.keyboard.pressed(Key.ctrl):
            self.keyboard.press(Key.tab)
            sleep(0.5)
            self.keyboard.release(Key.tab)

    @_delay_decorator
    def scroll_down(self):
        # TODO: implement it in the future
        self.mouse_controller.scroll(0, -10)


def main():
    mouse_event = MouseEvent()
    old_tab_number = 0
    while True:
        sleep(TIME_DELAY)
        random_tab = random.randint(*BROWSER_TAB_RANGE)
        if old_tab_number == random_tab:
            mouse_event.switch_next_tab()
        else:
            mouse_event.switch_browser_tabs(random_tab)
            mouse_event.move_to_random_position()
            old_tab_number = random_tab


if __name__ == '__main__':
    main()
