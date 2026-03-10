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

    def define_text_markup(self)\
        -> tuple[dict[str, tuple[int, int]], list[int], list[tuple[int, int]]]:
        
        values_len = len(self._values)
        deg_size = 360 / values_len

        degrees = [i * deg_size for i in range(values_len + 1)]
        border_coords = [self._circle.get_coords(deg) for deg in degrees]

        avg_degrees = []
        result = {}

        for txt, (i, deg) in zip(self._values, enumerate(degrees)):
            avg = (deg + degrees[i + 1]) / 2
            coords = self._circle.get_coords(avg, -(self._circle._radius / 3))

            avg_degrees.append(avg)
            result[txt] = coords

        return result, degrees, border_coords
    
    def place_text_markup(self):
        coords, _, bd_coords = self.define_text_markup()

        for key, value in coords.items():
            self.create_text(*value, text=key, anchor='center')

        # drawing borders
        for bdc in bd_coords:
            self.create_line(*self._circle._center, *bdc)

    def set_values(self, sequence):
        self._values = tuple(sequence)
