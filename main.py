import asyncio
import sqlite3
from datetime import datetime, timedelta
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton, MDIconButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.slider import MDSlider
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.dialog import MDDialog
from kivy.clock import Clock
from kivy.lang import Builder
from playwright.async_api import async_playwright
from ai_generator import generate_post
from smart_analyzer import analyze_text, analyze_image, analyze_video
from avoid_blocking import get_random_delay, get_random_proxy
import os
from dotenv import load_dotenv
import random

# تحميل المتغيرات البيئية
load_dotenv()
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")

# تحميل أنماط KivyMD
Builder.load_file("assets/styles.kv")

# إعداد قاعدة البيانات
from database import init_db, update_interaction, get_last_interaction
init_db()

class HomeScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(MDLabel(
            text="Osra AI Social Automation",
            halign="center",
            pos_hint={"center_y": 0.9},
            font_style="H2"
        ))

        # زر بدء التفاعل
        self.start_button = MDRaisedButton(
            text="بدء التفاعل",
            pos_hint={"center_x": 0.5, "center_y": 0.7},
            size_hint=(0.5, 0.1),
            on_press=self.start_automation
        )
        self.add_widget(self.start_button)

        # زر إنشاء منشور ذكي
        self.generate_post_button = MDRaisedButton(
            text="إنشاء منشور ذكي",
            pos_hint={"center_x": 0.5, "center_y": 0.55},
            size_hint=(0.5, 0.1),
            on_press=self.generate_smart_post
        )
        self.add_widget(self.generate_post_button)

        # زر الإعدادات
        self.settings_button = MDIconButton(
            icon="cog",
            pos_hint={"center_x": 0.9, "center_y": 0.1},
            on_press=self.open_settings
        )
        self.add_widget(self.settings_button)

    async def start_automation(self, instance):
        platforms = ["twitter", "instagram", "facebook", "linkedin", "tiktok"]
        for platform in platforms:
            await self.interact_with_platform(platform)

    async def interact_with_platform(self, platform):
        delay = get_random_delay()  # فترات عشوائية لتجنب الحظر
        await asyncio.sleep(delay)

        proxy = get_random_proxy()  # استخدام Proxy عشوائي
        async with async_playwright() as p:
            browser = await p.chromium.launch(
                headless=False,
                proxy=proxy
            )
            page = await browser.new_page()

            # تسجيل الدخول حسب المنصة
            if platform == "twitter":
                await self.login_twitter(page)
                await self.interact_twitter(page)
            elif platform == "instagram":
                await self.login_instagram(page)
                await self.interact_instagram(page)
            elif platform == "facebook":
                await self.login_facebook(page)
                await self.interact_facebook(page)
            elif platform == "linkedin":
                await self.login_linkedin(page)
                await self.interact_linkedin(page)
            elif platform == "tiktok":
                await self.login_tiktok(page)
                await self.interact_tiktok(page)

            await browser.close()

    # ... (إضافة دوال تسجيل الدخول والتفاعل لكل منصة)
    # (يمكنك الرجوع إلى الكود السابق لإضافة هذه الدوال)

    def generate_smart_post(self, instance):
        topic = MDTextField(
            hint_text="ادخل موضوع المنشور",
            pos_hint={"center_x": 0.5, "center_y": 0.3},
            size_hint=(0.8, None)
        )
        dialog = MDDialog(
            title="إنشاء منشور ذكي",
            type="custom",
            content_cls=topic,
            buttons=[
                MDRaisedButton(text="إنشاء", on_press=lambda x: self.create_post(topic.text)),
                MDRaisedButton(text="إلغاء", on_press=lambda x: dialog.dismiss())
            ]
        )
        dialog.open()

    def create_post(self, topic):
        post_text = generate_post(topic)
        MDDialog(title="تم إنشاء المنشور", text=post_text).open()

    def open_settings(self, instance):
        from settings import SettingsScreen
        self.manager.add_widget(SettingsScreen(name="settings"))
        self.manager.current = "settings"

class SocialAutomationApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Blue"
        self.screen_manager = MDScreenManager()
        self.screen_manager.add_widget(HomeScreen(name="home"))
        return self.screen_manager

if __name__ == "__main__":
    SocialAutomationApp().run()
