import time
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle
from kivy.clock import Clock as kivyClock
from kivy.uix.textinput import TextInput
from kivy.core.clipboard import Clipboard



# from kivy.core.window import Window
#
# Window.size = (280, 280 * (20 / 9))


class ColoredLabel(Label):
    def __init__(self, **kwargs):
        super(ColoredLabel, self).__init__(**kwargs)
        with self.canvas.before:
            Color(0, 0.65, 1, 1)  # Background color (orange)
            self.rect = Rectangle(pos=self.pos, size=self.size)
            self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size


class CustomClock(Label):
    def __init__(self, **kwargs):
        super(CustomClock, self).__init__(**kwargs)
        self.update_time()  # Initial update
        kivyClock.schedule_interval(self.update_time, 1)  # Schedule update every second

    def update_time(self, dt=None):
        self.text = time.strftime("%H:%M:%S")  # Update time
        self.font_size = min(self.size) * 0.45  # Adjust the multiplier as needed


class EpochClock(Label):
    def __init__(self, **kwargs):
        super(EpochClock, self).__init__(**kwargs)
        self.update_time()  # Initial update
        kivyClock.schedule_interval(self.update_time, 1)  # Schedule update every second

    def update_time(self, dt=None):
        self.text = str(round(time.time()))  # Update time
        self.font_size = min(self.size) * 0.35  # Adjust the multiplier as needed


class SmallGridLayout(GridLayout):
    def __init__(self, delay, **kwargs):
        super(SmallGridLayout, self).__init__(**kwargs)
        self.rows = 1
        self.cols = 100
        self.delay = int(delay)  # Convert delay to integer
        epoch_calculator1 = EpochCalculator(delay=self.delay)
        epoch_calculator2 = EpochCalculator(delay=self.delay)

        self.add_widget(epoch_calculator1)
        self.add_widget(epoch_calculator2)


class EpochCalculator(GridLayout):
    def __init__(self, delay=0, **kwargs):
        super(EpochCalculator, self).__init__(**kwargs)
        self.rows = 2
        self.cols = 1
        self.options = GridLayout(cols=2, rows=1)

        self.set_button = Button(text="set")
        self.set_button.bind(on_press=self.start_timer)
        self.options.add_widget(self.set_button)

        self.clear_button = Button(text="clear")
        self.clear_button.bind(on_press=self.clear_epoch)
        self.options.add_widget(self.clear_button)

        self.add_widget(self.options)

        self.epoch_label = TextInput(text="", readonly=True, multiline=True)
        self.epoch_label.bind(on_touch_down=self.copy_to_clipboard)  # Bind the touch event
        self.add_widget(self.epoch_label)

        self.delay = delay
        self.countdown_time = 0

        # Set font size to fill up the entire space
        self.epoch_label.bind(size=self.adjust_font_size)

    def adjust_font_size(self, instance, size):
        # Calculate the font size based on the minimum dimension of the widget
        min_dimension = min(size)
        font_size = min_dimension / 3  # Adjust as needed
        instance.font_size = font_size

    def start_timer(self, instance):
        if self.delay > 0:
            self.countdown_time = self.delay
            kivyClock.schedule_interval(self.update_timer, 1)
            self.epoch_label.text = str(self.countdown_time)
            self.epoch_label.font_size = 40
        else:
            self.set_epoch()

    def update_timer(self, dt):
        self.countdown_time -= 1
        if self.countdown_time <= 0:
            self.set_epoch()
            kivyClock.unschedule(self.update_timer)  # Stop the timer
        else:
            self.epoch_label.text = str(self.countdown_time)

    def set_epoch(self):
        if self.delay > 0:
            self.epoch_label.text = str(round(time.time()))
            self.epoch_label.font_size = 20

        else:
            self.epoch_label.text = str(round(time.time()) + self.delay)
            self.epoch_label.font_size = 20

    def clear_epoch(self, instance):
        self.epoch_label.text = ""

    def copy_to_clipboard(self, instance, touch):
        if instance.collide_point(*touch.pos):
            Clipboard.copy(instance.text)  # Copy the text to clipboard


class MyGrid(GridLayout):
    def __init__(self, **kwargs):
        super(MyGrid, self).__init__(**kwargs)
        self.cols = 2
        self.rows = 1

        self.info_grid = GridLayout(size_hint=(0.2, 1))
        self.info_grid.cols = 1
        self.info_grid.rows = 6

        labels = ["Clock:", "Epoch \nClock:", "+10:", "+0:", "-5:", "-10:"]
        for label_text in labels:
            self.info_grid.add_widget(ColoredLabel(text=label_text, color=(1, 0, 0, 1)))

        self.add_widget(self.info_grid)

        self.main_grid = GridLayout(size_hint=(0.8, 1))
        self.main_grid.rows = 6
        self.main_grid.cols = 1

        self.add_widget(self.main_grid)

        self.main_grid.add_widget(CustomClock())
        self.main_grid.add_widget(EpochClock())

        self.main_grid.add_widget(SmallGridLayout("+10"))
        self.main_grid.add_widget(SmallGridLayout("+0"))
        self.main_grid.add_widget(SmallGridLayout("-5"))
        self.main_grid.add_widget(SmallGridLayout("-10"))


class MyApp(App):
    def build(self):
        return MyGrid()


if __name__ == "__main__":
    MyApp().run()
