from math import sqrt
from functools import partial

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Line
from kivy.clock import Clock
from kivy.gesture import Gesture, GestureDatabase
from kivy.properties import ObjectProperty


# TODO: This is a nice generic class that is going to go into it's own package
# and possibly belongs in Kivy
class GestureBox(BoxLayout):

    gesture_timeout = 200
    gesture_distance = 100

    # used internally to store a touch and
    # dispatch it if the touch does not turn into a gesture
    _touch = ObjectProperty(None, allownone=True)

    def __init__(self, *args, **kwargs):
        super(GestureBox, self).__init__(*args, **kwargs)
        self.gestures = GestureDatabase()

    def add_gesture(self, name, gesture_str):
        gesture = self.gestures.str_to_gesture(gesture_str)
        gesture.name = name
        self.gestures.add_gesture(gesture)
        self.register_event_type('on_gesture_' + name)

    def on_touch_down(self, touch):
        if not self.collide_point(*touch.pos):
            touch.ud[self._get_uid('cavoid')] = True
            return
        if self._touch:
            return super(GestureBox, self).on_touch_down(touch)
        self._touch = touch
        uid = self._get_uid()
        touch.grab(self)
        touch.ud[uid] = {
            'mode': 'unknown',
            'time': touch.time_start}
        Clock.schedule_once(self._change_touch_mode,
                self.gesture_timeout / 1000.)
        touch.ud['gesture_line'] = Line(points=(touch.x, touch.y))
        return True

    def on_touch_move(self, touch):
        if self._get_uid('cavoid') in touch.ud:
            return
        if self._touch is not touch:
            super(GestureBox, self).on_touch_move(touch)
            return self._get_uid() in touch.ud
        if touch.grab_current is not self:
            return True
        ud = touch.ud[self._get_uid()]
        if ud['mode'] == 'unknown':
            dx = abs(touch.ox - touch.x)
            dy = abs(touch.oy - touch.y)
            distance = sqrt(dx * dx + dy * dy)

            if distance > self.gesture_distance:
                Clock.unschedule(self._change_touch_mode)
                ud['mode'] = 'gesture'

        try:
            touch.ud['gesture_line'].points += [touch.x, touch.y]
        except KeyError:
            pass

        return True

    def on_touch_up(self, touch):
        if self._get_uid('cavoid') in touch.ud:
            return
        if self in [x() for x in touch.grab_list]:
            touch.ungrab(self)
            self._touch = None
            ud = touch.ud[self._get_uid()]
            if ud['mode'] == 'unknown':
                Clock.unschedule(self._change_touch_mode)
                super(GestureBox, self).on_touch_down(touch)
                Clock.schedule_once(partial(self._do_touch_up, touch), .1)
            else:
                gesture = Gesture()
                gesture.add_stroke(
                    zip(touch.ud['gesture_line'].points[::2],
                        touch.ud['gesture_line'].points[1::2]))
                gesture.normalize()
                match = self.gestures.find(gesture, minscore=0.70)
                if match:
                    self.dispatch('on_gesture_' + match[1].name)
                else:
                    # FIXME: If the gesture isn't recognized, it should
                    # probably be propogated to the child
                    pass
                return True

        else:
            if self._touch is not touch and self.uid not in touch.ud:
                super(GestureBox, self).on_touch_up(touch)
        return self._get_uid() in touch.ud

    def _do_touch_up(self, touch, *largs):
        super(GestureBox, self).on_touch_up(touch)
        # don't forget about grab event!
        for x in touch.grab_list[:]:
            touch.grab_list.remove(x)
            x = x()
            if not x:
                continue
            touch.grab_current = x
            super(GestureBox, self).on_touch_up(touch)
        touch.grab_current = None
        gesture = Gesture()
        gesture.add_stroke(
            zip(touch.ud['gesture_line'].points[::2],
                touch.ud['gesture_line'].points[1::2]))
        gesture.normalize()
        match = self.gestures.find(gesture, minscore=0.70)
        if match:
            self.dispatch('on_gesture_' + match[1].name)
        return True

    def _change_touch_mode(self, *largs):
        if not self._touch:
            return
        uid = self._get_uid()
        touch = self._touch
        ud = touch.ud[uid]
        if ud['mode'] == 'unknown':
            touch.ungrab(self)
            self._touch = None
            touch.push()
            touch.apply_transform_2d(self.to_widget)
            touch.apply_transform_2d(self.to_parent)
            super(GestureBox, self).on_touch_down(touch)
            touch.pop()
            return

    def _get_uid(self, prefix='sv'):
        return '{0}.{1}'.format(prefix, self.uid)