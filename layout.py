import kivy

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock

the_number = 10567567


class MyW(FloatLayout):
    global the_number

    def my_callback(self, dt):
        global the_number
        self.ids.label1.text = str(the_number)

        # my_label = MyW.ids(‘label1’)
        # my_label.text = str(the_number)
        print("read teh number here")
        the_number += 1

    def on_touch_down(self, touch):
        Clock.schedule_interval(self.my_callback, 2)
        if touch.is_double_tap:
            self.ids.label1.text = ""
            Clock.unschedule(self.my_callback)
            exit()


class layout(App):
    def build(self):
        return MyW()


if __name__ == "__main__":
    layout().run()