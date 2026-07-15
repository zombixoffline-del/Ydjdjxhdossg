from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle, Ellipse
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.core.image import Image as CoreImage
import math
import os

class GameWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.player_x = 0.0
        self.player_y = 0.0
        self.speed = 150.0

        # Загрузка фона, если есть
        self.bg_texture = None
        if os.path.exists('background.png'):
            try:
                self.bg_texture = CoreImage('background.png').texture
                self.bg_texture.wrap = 'repeat'
                self.tw = self.bg_texture.width
                self.th = self.bg_texture.height
            except:
                self.bg_texture = None
        else:
            print("background.png не найден, будет залит цветом")

        # Джойстик
        self.joystick_center = (100, 100)
        self.joystick_radius = 60
        self.knob_radius = 25
        self.knob_pos = (100, 100)
        self.touch_id = None
        self.dir_x = 0.0
        self.dir_y = 0.0

        # Клавиатура (для ПК)
        self.keys = set()
        self._keyboard = Window.request_keyboard(None, self)
        self._keyboard.bind(on_key_down=self._on_key_down)
        self._keyboard.bind(on_key_up=self._on_key_up)

        Clock.schedule_interval(self.update, 1/60)

    def _on_key_down(self, _, keycode, __, ___):
        self.keys.add(keycode[1])
    def _on_key_up(self, _, keycode):
        self.keys.discard(keycode[1])

    def on_touch_down(self, touch):
        dx = touch.x - self.joystick_center[0]
        dy = touch.y - self.joystick_center[1]
        if dx*dx + dy*dy <= (self.joystick_radius + 30)**2:
            self.touch_id = touch.uid
            self._update_knob(touch.x, touch.y)
            return True
        return super().on_touch_down(touch)

    def on_touch_move(self, touch):
        if touch.uid == self.touch_id:
            self._update_knob(touch.x, touch.y)
            return True
        return super().on_touch_move(touch)

    def on_touch_up(self, touch):
        if touch.uid == self.touch_id:
            self.touch_id = None
            self.knob_pos = self.joystick_center
            self.dir_x = 0.0
            self.dir_y = 0.0
            return True
        return super().on_touch_up(touch)

    def _update_knob(self, x, y):
        vx = x - self.joystick_center[0]
        vy = y - self.joystick_center[1]
        dist = math.hypot(vx, vy)
        if dist > self.joystick_radius:
            vx = vx / dist * self.joystick_radius
            vy = vy / dist * self.joystick_radius
            dist = self.joystick_radius
        self.knob_pos = (self.joystick_center[0] + vx, self.joystick_center[1] + vy)
        if dist > 0:
            self.dir_x = vx / self.joystick_radius
            self.dir_y = vy / self.joystick_radius
        else:
            self.dir_x = 0.0
            self.dir_y = 0.0

    def update(self, dt):
        # Управление с клавиатуры (без изменений)
        kx = ky = 0
        s = self.speed * dt
        if 'w' in self.keys or 'up' in self.keys:   ky += s
        if 's' in self.keys or 'down' in self.keys: ky -= s
        if 'a' in self.keys or 'left' in self.keys: kx -= s
        if 'd' in self.keys or 'right' in self.keys: kx += s

        # Управление с джойстика (ИНВЕРТИРУЕМ Y)
        jx = self.dir_x * self.speed * dt
        jy = -self.dir_y * self.speed * dt   # <-- вот здесь инверсия

        move_x = kx + jx
        move_y = ky + jy

        if move_x != 0 or move_y != 0:
            self.player_x += move_x
            self.player_y += move_y

        # Рисование
        self.canvas.clear()
        with self.canvas:
            # Фон
            if self.bg_texture:
                w, h = self.width, self.height
                u0 = -self.player_x / self.tw
                v0 = -self.player_y / self.th
                u1 = u0 + w / self.tw
                v1 = v0 + h / self.th
                Rectangle(texture=self.bg_texture, pos=(0,0), size=(w,h),
                          tex_coords=(u0,v0, u1,v0, u1,v1, u0,v1))
            else:
                Color(0.2, 0.6, 0.2, 1)
                Rectangle(pos=(0,0), size=(self.width, self.height))

            # Игрок (синяя точка)
            Color(0, 0, 1, 1)
            Ellipse(pos=(self.width/2 - 10, self.height/2 - 10), size=(20,20))

            # Джойстик
            Color(0.3, 0.3, 0.3, 0.6)
            Ellipse(pos=(self.joystick_center[0] - self.joystick_radius,
                         self.joystick_center[1] - self.joystick_radius),
                    size=(self.joystick_radius*2, self.joystick_radius*2))
            Color(0.4, 0.7, 1, 0.9)
            Ellipse(pos=(self.knob_pos[0] - self.knob_radius,
                         self.knob_pos[1] - self.knob_radius),
                    size=(self.knob_radius*2, self.knob_radius*2))


class GameApp(App):
    def build(self):
        return GameWidget()

if __name__ == '__main__':
    GameApp().run()