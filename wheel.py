from tkinter import Canvas
from circle import Circle
from threading import Thread
from random import randint
from time import sleep
sign = lambda n: 1 if n >= 1 else -1


class RandomWheel(Canvas):
    def __init__(self, center: tuple[int, int], rad: int, result_handle_func: callable,
                 random_range: tuple[int, int], values: tuple[str], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._circle = Circle(center, rad, -90)
        self._current_rot = 0
        self._values = list(values)
        self._random_range = random_range
        self._handle_func = result_handle_func
        self._is_launched = False

    def flip_wheel_state(self):
        self.delete('all')
        
        x1 = self._circle._center[0] - self._circle._radius
        y1 = self._circle._center[1] + self._circle._radius
        x2 = self._circle._center[0] + self._circle._radius
        y2 = self._circle._center[1] - self._circle._radius
        self.create_oval(x1, y1, x2, y2)
        
        self.create_line(
            *self._circle._center,
            *self._circle.get_coords(self._current_rot),
            arrow='last'
        )
        self.place_text_markup()
    
    def launch(self, speed: float, vector: int = -1):
        speed = 1 / speed

        def f():
            if not self._is_launched:
                time = randint(*self._random_range)
                self._is_launched = True

                while time > 0:
                    self._current_rot += vector * time
                    self.minimize_rads()
                    sleep(speed)

                    self.flip_wheel_state()
                    time -= 1

                self.define_val()
                self._is_launched = False

        Thread(target=f, daemon=True).start()

    def minimize_rads(self):
        while abs(self._current_rot) >= 360:
            self._current_rot -= 360 * sign(self._current_rot)

    def define_val(self):
        index = round(self._current_rot) * len(self._values) // 360
        self._handle_func(self._values[index])

    def place_text_markup(self):
        values_len = len(self._values)
        deg_size = 360 / values_len

        for i, txt in enumerate(self._values):
            deg = i * deg_size
            
            avg = (deg + (deg + deg_size)) / 2
            coords = self._circle.get_coords(avg, -(self._circle._radius / 3))
            bd_coords = self._circle.get_coords(deg)
    
            self.create_text(*coords, text=txt, anchor='center')
            self.create_line(*self._circle._center, *bd_coords)

    def set_values(self, sequence):
        self._values = tuple(sequence)
