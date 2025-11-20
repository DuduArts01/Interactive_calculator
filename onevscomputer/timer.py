import time

class Timer:
    def __init__(self, start_seconds=60):
        self.time_left = start_seconds
        self.last_update = time.time()
        self.paused = False

    def update(self):
        """ Atualiza o cronômetro somente se não estiver pausado. """
        if self.paused:
            return self.time_left

        now = time.time()
        if now - self.last_update >= 1:
            self.time_left -= 1
            self.last_update = now

        return self.time_left

    def add_time(self, seconds):
        self.time_left += seconds

    def pause(self):
        self.paused = True

    def resume(self):
        self.paused = False
        self.last_update = time.time()

    def reset(self, start_seconds=60):
        self.time_left = start_seconds
        self.last_update = time.time()
        self.paused = False

    def get_time_string(self):
        minutes = self.time_left // 60
        seconds = self.time_left % 60
        return f"{minutes}:{seconds:02d}"
