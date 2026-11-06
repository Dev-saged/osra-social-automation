import asyncio
import sqlite3
from datetime import datetime, timedelta
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton
from kivy.clock import Clock
from playwright.async_api import async_playwright
from mistralai.client import MistralClient
import os
from dotenv import load_dotenv
import random

# تحميل المتغيرات البيئية
load_dotenv()
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")

# إعداد قاعدة البيانات
def init_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS interactions (
            platform TEXT,
            last_interaction TIMESTAMP,
            likes INTEGER DEFAULT 0,
            comments INTEGER DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

init_db()

class SocialAutomationApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Blue"

        # الشاشة الرئيسية
        self.screen = MDScreen()
        self.label = MDLabel(
            text="Osra AI Social Automation",
            halign="center",
            pos_hint={"center_y": 0.8},
            font_style="H3"
        )
        self.start_button = MDRaisedButton(
            text="بدء التفاعل",
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            size_hint=(0.5, 0.1),
            on_press=self.start_automation
        )
        self.screen.add_widget(self.label)
        self.screen.add_widget(self.start_button)
        return self.screen

    async def start_automation(self, instance):
        platforms = ["twitter", "instagram", "facebook", "linkedin"]
        for platform in platforms:
            await self.interact_with_platform(platform)

    async def interact_with_platform(self, platform):
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=False)
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

            await browser.close()

    # تسجيل الدخول حسب المنصة
    async def login_twitter(self, page):
        await page.goto("https://twitter.com/login")
        await page.fill('input[autocomplete="username"]', os.getenv("TWITTER_USERNAME"))
        await page.click('div[role="button"]')
        await page.wait_for_timeout(2000)
        await page.fill('input[autocomplete="current-password"]', os.getenv("TWITTER_PASSWORD"))
        await page.click('div[role="button"]')
        await page.wait_for_timeout(5000)

    async def login_instagram(self, page):
        await page.goto("https://www.instagram.com/accounts/login/")
        await page.fill('input[name="username"]', os.getenv("INSTAGRAM_USERNAME"))
        await page.fill('input[name="password"]', os.getenv("INSTAGRAM_PASSWORD"))
        await page.click('button[type="submit"]')
        await page.wait_for_timeout(5000)

    async def login_facebook(self, page):
        await page.goto("https://www.facebook.com/login/")
        await page.fill('input[name="email"]', os.getenv("FACEBOOK_EMAIL"))
        await page.fill('input[name="pass"]', os.getenv("FACEBOOK_PASSWORD"))
        await page.click('button[name="login"]')
        await page.wait_for_timeout(5000)

    async def login_linkedin(self, page):
        await page.goto("https://www.linkedin.com/login/")
        await page.fill('input[name="session_key"]', os.getenv("LINKEDIN_EMAIL"))
        await page.fill('input[name="session_password"]', os.getenv("LINKEDIN_PASSWORD"))
        await page.click('button[type="submit"]')
        await page.wait_for_timeout(5000)

    # التفاعل حسب المنصة
    async def interact_twitter(self, page):
        posts = await page.query_selector_all('article')
        for post in posts[:5]:
            await post.hover()
            await page.wait_for_timeout(random.randint(3000, 7000))  # فترات عشوائية

            # إعجاب
            like_button = await post.query_selector('div[data-testid="like"]')
            if like_button:
                await like_button.click()
                await self.update_interaction("twitter", "likes")
                await page.wait_for_timeout(random.randint(2000, 5000))

            # تعليق ذكي
            post_text = await post.text_content()
            response = self.generate_response(post_text)
            if response:
                comment_box = await page.query_selector('div[data-testid="tweetTextarea_0"]')
                if comment_box:
                    await comment_box.fill(response)
                    await comment_box.press("Enter")
                    await self.update_interaction("twitter", "comments")
                    await page.wait_for_timeout(random.randint(3000, 6000))

    async def interact_instagram(self, page):
        posts = await page.query_selector_all('div[role="button"]')
        for post in posts[:3]:
            await post.click()
            await page.wait_for_timeout(random.randint(3000, 7000))

            # إعجاب
            like_button = await page.query_selector('span[aria-label="Like"]')
            if like_button:
                await like_button.click()
                await self.update_interaction("instagram", "likes")
                await page.wait_for_timeout(random.randint(2000, 5000))

            # تعليق
            post_text = await page.text_content('h1')
            response = self.generate_response(post_text)
            if response:
                comment_box = await page.query_selector('textarea')
                if comment_box:
                    await comment_box.fill(response)
                    await comment_box.press("Enter")
                    await self.update_interaction("instagram", "comments")
                    await page.wait_for_timeout(random.randint(3000, 6000))

    # ... (يمكن إضافة تفاعل Facebook وLinkedIn بنفس الطريقة)

    def generate_response(self, post_text):
        """توليد رد ذكي باستخدام Mistral AI Tiny"""
        client = MistralClient(api_key=MISTRAL_API_KEY)
        response = client.chat(
            model="mistral-tiny",
            messages=[{"role": "user", "content": f"حلل هذا المنشور واكتب رد ذكي: {post_text}"}]
        )
        return response.choices[0].message.content

    def update_interaction(self, platform, action):
        """تحديث آخر تفاعل في قاعدة البيانات"""
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO interactions (platform, last_interaction, likes, comments)
            VALUES (?, datetime('now'), COALESCE(likes, 0) + 1, COALESCE(comments, 0) + 1)
        ''', (platform,))
        conn.commit()
        conn.close()

if __name__ == "__main__":
    SocialAutomationApp().run()
