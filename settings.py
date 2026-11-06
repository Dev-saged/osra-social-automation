from kivymd.uix.screen import MDScreen
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.slider import MDSlider
from kivymd.uix.dialog import MDDialog

class SettingsScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(MDLabel(
            text="إعدادات النظام",
            halign="center",
            pos_hint={"center_y": 0.9},
            font_style="H3"
        ))

        # عدد الإعجابات
        self.likes_slider = MDSlider(
            min=1, max=20, value=5,
            pos_hint={"center_x": 0.5, "center_y": 0.7}
        )
        self.add_widget(self.likes_slider)

        # عدد التعليقات
        self.comments_slider = MDSlider(
            min=1, max=10, value=3,
            pos_hint={"center_x": 0.5, "center_y": 0.5}
        )
        self.add_widget(self.comments_slider)

        # زر الحفظ
        self.save_button = MDRaisedButton(
            text="حفظ الإعدادات",
            pos_hint={"center_x": 0.5, "center_y": 0.3},
            on_press=self.save_settings
        )
        self.add_widget(self.save_button)

    def save_settings(self, instance):
        likes = self.likes_slider.value
        comments = self.comments_slider.value
        MDDialog(
            title="تم الحفظ",
            text=f"عدد الإعجابات: {likes}
عدد التعليقات: {comments}"
        ).open()
