import json
import os
import random
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.core.window import Window
from kivy.metrics import dp

SAVE_FILE = "clicker_save.json"
ADMIN_PASSWORD = "admin"

# ============================================================
# ТЕМЫ ОФОРМЛЕНИЯ
# ============================================================
THEMES = {
    "classic": {
        "name": "Классическая",
        "bg": (0.11, 0.15, 0.20, 1),
        "panel_bg": (0.15, 0.18, 0.25, 1),
        "text": (0.9, 0.9, 0.9, 1),
        "coins": (1, 0.85, 0, 1),
        "stats": (0.7, 0.8, 0.9, 1),
        "click_btn": (0.9, 0.5, 0.1, 1),
        "upgrade_btn": (0.2, 0.8, 0.4, 1),
        "upgrade_btn_disabled": (0.35, 0.35, 0.35, 1),
        "admin_btn": (0.5, 0.2, 0.5, 1),
        "reset_btn": (0.7, 0.2, 0.2, 1),
        "prestige_btn": (0.5, 0.2, 0.7, 1),
        "prestige_text": (0.8, 0.6, 1, 1),
        "icon": (0.9, 0.7, 0.3, 1),
        "ach_done": (0.3, 1, 0.5, 1),
        "ach_lock": (0.6, 0.6, 0.6, 1),
    },
    "light": {
        "name": "Светлая",
        "bg": (0.95, 0.95, 0.97, 1),
        "panel_bg": (1, 1, 1, 1),
        "text": (0.2, 0.2, 0.2, 1),
        "coins": (0.9, 0.6, 0, 1),
        "stats": (0.4, 0.4, 0.5, 1),
        "click_btn": (1, 0.6, 0.2, 1),
        "upgrade_btn": (0.1, 0.7, 0.3, 1),
        "upgrade_btn_disabled": (0.7, 0.7, 0.7, 1),
        "admin_btn": (0.6, 0.3, 0.6, 1),
        "reset_btn": (0.8, 0.3, 0.3, 1),
        "prestige_btn": (0.6, 0.3, 0.8, 1),
        "prestige_text": (0.5, 0.2, 0.7, 1),
        "icon": (0.8, 0.6, 0.2, 1),
        "ach_done": (0.2, 0.8, 0.4, 1),
        "ach_lock": (0.7, 0.7, 0.7, 1),
    },
    "neon": {
        "name": "Неоновая",
        "bg": (0.05, 0.05, 0.08, 1),
        "panel_bg": (0.1, 0.1, 0.15, 1),
        "text": (0.9, 0.9, 1, 1),
        "coins": (0, 1, 0.8, 1),
        "stats": (0.6, 0.6, 0.9, 1),
        "click_btn": (0.2, 0.9, 0.9, 1),
        "upgrade_btn": (0.9, 0.2, 0.9, 1),
        "upgrade_btn_disabled": (0.3, 0.3, 0.4, 1),
        "admin_btn": (0.9, 0.9, 0, 1),
        "reset_btn": (1, 0.2, 0.4, 1),
        "prestige_btn": (0.9, 0, 0.9, 1),
        "prestige_text": (0.9, 0.5, 1, 1),
        "icon": (0, 1, 0.8, 1),
        "ach_done": (0, 1, 0.8, 1),
        "ach_lock": (0.4, 0.4, 0.5, 1),
    },
    "retro": {
        "name": "Ретро",
        "bg": (0.85, 0.75, 0.6, 1),
        "panel_bg": (0.9, 0.8, 0.65, 1),
        "text": (0.3, 0.2, 0.1, 1),
        "coins": (0.7, 0.4, 0.1, 1),
        "stats": (0.4, 0.3, 0.2, 1),
        "click_btn": (0.8, 0.5, 0.2, 1),
        "upgrade_btn": (0.5, 0.6, 0.3, 1),
        "upgrade_btn_disabled": (0.6, 0.55, 0.5, 1),
        "admin_btn": (0.6, 0.4, 0.3, 1),
        "reset_btn": (0.7, 0.3, 0.2, 1),
        "prestige_btn": (0.5, 0.3, 0.4, 1),
        "prestige_text": (0.4, 0.2, 0.3, 1),
        "icon": (0.6, 0.4, 0.2, 1),
        "ach_done": (0.4, 0.6, 0.2, 1),
        "ach_lock": (0.6, 0.55, 0.5, 1),
    },
    "space": {
        "name": "Космическая",
        "bg": (0.08, 0.05, 0.15, 1),
        "panel_bg": (0.12, 0.08, 0.2, 1),
        "text": (0.85, 0.85, 1, 1),
        "coins": (0.6, 0.8, 1, 1),
        "stats": (0.7, 0.7, 0.9, 1),
        "click_btn": (0.4, 0.3, 0.8, 1),
        "upgrade_btn": (0.3, 0.7, 0.9, 1),
        "upgrade_btn_disabled": (0.25, 0.25, 0.35, 1),
        "admin_btn": (0.7, 0.4, 0.9, 1),
        "reset_btn": (0.9, 0.3, 0.5, 1),
        "prestige_btn": (0.6, 0.4, 0.9, 1),
        "prestige_text": (0.8, 0.7, 1, 1),
        "icon": (0.7, 0.8, 1, 1),
        "ach_done": (0.5, 1, 0.8, 1),
        "ach_lock": (0.5, 0.5, 0.6, 1),
    },
}


# ============================================================
# ВСПЛЫВАЮЩИЙ ТЕКСТ
# ============================================================
class FloatingText(Widget):
    def __init__(self, text, x, y, color=(1, 0.85, 0, 1), **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (dp(140), dp(40))
        self.pos = (x - 70, y)
        self._removed = False

        self.label = Label(
            text=str(text),
            font_size=dp(24),
            bold=True,
            color=color,
            halign="center",
            valign="middle",
            markup=True
        )
        self.label.bind(size=self.label.setter('text_size'))
        self.add_widget(self.label)

        try:
            anim = Animation(
                pos=(self.pos[0], self.pos[1] + dp(120)),
                opacity=0,
                duration=1.0,
                transition='out_quad'
            )
            anim.bind(on_complete=self._on_done)
            anim.start(self)
        except Exception:
            pass

    def _on_done(self, *args):
        if self._removed:
            return
        self._removed = True
        try:
            if self.parent:
                self.parent.remove_widget(self)
        except Exception:
            pass


# ============================================================
# УВЕДОМЛЕНИЕ О ДОСТИЖЕНИИ
# ============================================================
class AchievementPopup(FloatLayout):
    def __init__(self, title, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (1, None)
        self.height = dp(60)
        self.pos_hint = {'top': 1}

        with self.canvas:
            from kivy.graphics import Color, Rectangle
            Color(0.1, 0.6, 0.3, 0.95)
            self.bg = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=lambda *a: setattr(self.bg, 'size', self.size))
        self.bind(pos=lambda *a: setattr(self.bg, 'pos', self.pos))

        box = BoxLayout(orientation='horizontal', padding=dp(10), spacing=dp(10))
        box.add_widget(Label(
            text=f"🏆 {title}",
            font_size=dp(14), bold=True,
            halign="left", valign="middle"
        ))
        self.add_widget(box)

        Clock.schedule_once(lambda dt: self._hide(), 3.0)

    def _hide(self):
        try:
            anim = Animation(pos_hint={'top': -0.1}, duration=0.5)
            anim.bind(on_complete=lambda *a: self.parent.remove_widget(self)
                      if self.parent else None)
            anim.start(self)
        except Exception:
            pass


# ============================================================
# КАРТОЧКА УЛУЧШЕНИЯ
# ============================================================
class UpgradeCard(BoxLayout):
    def __init__(self, game, upgrade, idx, **kwargs):
        super().__init__(orientation='horizontal',
                         size_hint_y=None, height=dp(65),
                         spacing=dp(8), padding=dp(8),
                         **kwargs)
        self.game = game
        self.upgrade = upgrade
        self.idx = idx

        self.icon = Label(
            text=upgrade['icon'],
            font_size=dp(18), bold=True,
            size_hint_x=None, width=dp(40),
            halign="center", valign="middle"
        )
        self.icon.bind(size=self.icon.setter('text_size'))
        self.add_widget(self.icon)

        info = BoxLayout(orientation='vertical', spacing=dp(1))
        self.name_label = Label(
            text="", font_size=dp(11), bold=True,
            halign="left", valign="middle"
        )
        self.name_label.bind(size=self.name_label.setter('text_size'))
        self.desc_label = Label(
            text="", font_size=dp(10),
            halign="left", valign="middle"
        )
        self.desc_label.bind(size=self.desc_label.setter('text_size'))
        info.add_widget(self.name_label)
        info.add_widget(self.desc_label)
        self.add_widget(info)

        self.buy_btn = Button(
            text="Купить", font_size=dp(11),
            size_hint_x=None, width=dp(75)
        )
        self.buy_btn.bind(on_press=lambda b: self.game.buy_upgrade(idx))
        self.add_widget(self.buy_btn)

        self.update_state()

    def update_state(self):
        try:
            cost = self.game.get_cost(self.upgrade)
            can_buy = self.game.coins >= cost
            theme = THEMES[self.game.current_theme]
            self.buy_btn.disabled = not can_buy
            self.buy_btn.background_color = theme["upgrade_btn"] if can_buy else theme["upgrade_btn_disabled"]
            self.name_label.text = f"{self.upgrade['name']}  [Ур.{self.upgrade['level']}]"
            self.desc_label.text = f"{cost:,} | {upgrade_desc(self.upgrade)}".replace(",", " ")
        except Exception:
            pass


def upgrade_desc(upg):
    t, v = upg["type"], upg["value"]
    if t == "click": return f"+{v}/клик"
    if t == "auto":  return f"+{v}/сек"
    if t == "crit":  return f"+{v}% крит x5"
    if t == "luck":  return f"+{v}% удача x10"
    if t == "multi": return f"x{v} ко всему"
    if t == "auto_click": return f"{v} автоклик/с"
    return ""


# ============================================================
# АДМИН-ПАНЕЛЬ
# ============================================================
class AdminPanel(FloatLayout):
    def __init__(self, game, **kwargs):
        super().__init__(**kwargs)
        self.game = game

        with self.canvas:
            from kivy.graphics import Color, Rectangle
            Color(0, 0, 0, 0.8)
            self.bg = Rectangle(size=Window.size)
        self.bind(size=lambda *a: setattr(self.bg, 'size', Window.size))

        panel = BoxLayout(
            orientation='vertical',
            size_hint=(0.9, 0.9),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            spacing=dp(6), padding=dp(12)
        )
        with panel.canvas.before:
            from kivy.graphics import Color, Rectangle
            Color(0.15, 0.18, 0.25, 1)
            panel.bg = Rectangle(size=panel.size, pos=panel.pos)
        panel.bind(size=lambda *a: setattr(panel.bg, 'size', panel.size))
        panel.bind(pos=lambda *a: setattr(panel.bg, 'pos', panel.pos))

        panel.add_widget(Label(
            text="[ АДМИН-ПАНЕЛЬ ]",
            font_size=dp(18), bold=True,
            color=(1, 0.5, 0.5, 1),
            size_hint_y=None, height=dp(30)
        ))

        self.cheat_label = Label(
            text="Читы: ВЫКЛ", font_size=dp(12),
            color=(1, 0.7, 0.7, 1),
            size_hint_y=None, height=dp(22)
        )
        panel.add_widget(self.cheat_label)

        actions = [
            ("+1K монет", lambda: self._add(1000)),
            ("+100K монет", lambda: self._add(100000)),
            ("+1M монет", lambda: self._add(1000000)),
            ("Установить монеты", self._show_set),
            ("+10 престиж-очков", lambda: self._add_prestige(10)),
            ("x10 буст на 60с", lambda: self._boost(10, 60)),
            ("x100 буст на 30с", lambda: self._boost(100, 30)),
            ("Открыть все улучшения", self._unlock_all),
            ("Сбросить цены", self._reset_prices),
            ("ВКЛ/ВЫКЛ автоклик", self._toggle_auto),
            ("Полный сброс", self._full_reset),
        ]

        scroll = ScrollView(size_hint_y=1)
        btn_box = BoxLayout(orientation='vertical', spacing=dp(5),
                            size_hint_y=None,
                            height=dp(38) * len(actions))
        btn_box.bind(minimum_height=btn_box.setter('height'))

        for text, action in actions:
            btn = Button(
                text=text, font_size=dp(12),
                background_color=(0.3, 0.4, 0.6, 1),
                size_hint_y=None, height=dp(38)
            )
            btn.bind(on_press=lambda b, a=action: self._safe(a))
            btn_box.add_widget(btn)

        scroll.add_widget(btn_box)
        panel.add_widget(scroll)

        close_btn = Button(
            text="Закрыть", font_size=dp(13), bold=True,
            background_color=(0.7, 0.2, 0.2, 1),
            size_hint_y=None, height=dp(40)
        )
        close_btn.bind(on_press=lambda b: game.close_admin())
        panel.add_widget(close_btn)

        self.add_widget(panel)

    def _safe(self, fn):
        try:
            fn()
        except Exception as e:
            print("Admin error:", e)

    def _add(self, n):
        self.game.coins += n
        self.game.update_ui()

    def _add_prestige(self, n):
        self.game.prestige_points += n
        self.game.recalc_stats()
        self.game.update_ui()

    def _show_set(self):
        try:
            popup = Popup(title='Монеты', size_hint=(0.8, 0.35),
                          background_color=(0.2, 0.2, 0.3, 1))
            box = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(8))
            inp = TextInput(hint_text='Число', input_filter='int',
                            font_size=dp(16), multiline=False)
            box.add_widget(inp)

            def apply(_):
                try:
                    self.game.coins = int(inp.text)
                    self.game.update_ui()
                    popup.dismiss()
                except Exception:
                    pass
            box.add_widget(Button(text='OK', on_press=apply,
                                  background_color=(0.2, 0.7, 0.3, 1)))
            popup.content = box
            popup.open()
        except Exception:
            pass

    def _boost(self, mult, sec):
        self.game.temp_multiplier = mult
        self.cheat_label.text = f"Буст: x{mult} ({sec}с)"
        Clock.schedule_once(lambda dt: self._end_boost(), sec)

    def _end_boost(self):
        self.game.temp_multiplier = 1
        self.cheat_label.text = "Буст: ВЫКЛ"
        self.game.update_ui()

    def _unlock_all(self):
        for u in self.game.upgrades:
            u["level"] = max(u["level"], 1)
        self.game.recalc_stats()
        self.game.update_ui()

    def _reset_prices(self):
        for u in self.game.upgrades:
            u["level"] = 0
        self.game.recalc_stats()
        self.game.update_ui()

    def _toggle_auto(self):
        self.game.auto_click_enabled = not self.game.auto_click_enabled
        self.cheat_label.text = f"Автоклик: {'ВКЛ' if self.game.auto_click_enabled else 'ВЫКЛ'}"

    def _full_reset(self):
        self.game.reset_game()
        self.cheat_label.text = "Читы: ВЫКЛ"


# ============================================================
# ГЛАВНОЕ ПРИЛОЖЕНИЕ
# ============================================================
class ClickerApp(App):
    def build(self):
        self.current_theme = "classic"
        self.load_theme()
        self.apply_theme()

        Window.clearcolor = THEMES[self.current_theme]["bg"]

        # Состояние
        self.coins = 0
        self.click_power = 1
        self.auto_click_power = 0
        self.total_clicks = 0
        self.crit_chance = 0
        self.luck_chance = 0
        self.global_multiplier = 1
        self.temp_multiplier = 1
        self.auto_click_enabled = False
        self.admin_panel = None

        # Престиж
        self.prestige_points = 0
        self.prestige_multiplier = 1.0
        self.total_earned_all_time = 0

        # Достижения
        self.achievements = {
            "first_click":    {"name": "Первый клик",       "done": False, "check": lambda: self.total_clicks >= 1},
            "clicks_100":     {"name": "100 кликов",        "done": False, "check": lambda: self.total_clicks >= 100},
            "clicks_1000":    {"name": "1000 кликов",       "done": False, "check": lambda: self.total_clicks >= 1000},
            "coins_1k":       {"name": "1,000 монет",       "done": False, "check": lambda: self.coins >= 1000},
            "coins_100k":     {"name": "100,000 монет",     "done": False, "check": lambda: self.coins >= 100000},
            "coins_1m":       {"name": "1,000,000 монет",   "done": False, "check": lambda: self.coins >= 1000000},
            "first_prestige": {"name": "Первый престиж",    "done": False, "check": lambda: self.prestige_points >= 1},
            "prestige_10":    {"name": "10 престиж-очков",  "done": False, "check": lambda: self.prestige_points >= 10},
            "auto_100":       {"name": "100/сек автодоход", "done": False, "check": lambda: self.auto_click_power >= 100},
        }

        self.upgrades = [
            {"name": "Сила клика",    "icon": "[+]",  "base_cost": 15,
             "type": "click", "value": 1,  "level": 0},
            {"name": "Автокликер",    "icon": "[A]",  "base_cost": 50,
             "type": "auto",  "value": 1,  "level": 0},
            {"name": "Двойной клик",  "icon": "[x2]", "base_cost": 200,
             "type": "click", "value": 5,  "level": 0},
            {"name": "Фабрика",       "icon": "[F]",  "base_cost": 1000,
             "type": "auto",  "value": 10, "level": 0},
            {"name": "Крит. удар",    "icon": "[!]",  "base_cost": 500,
             "type": "crit",  "value": 5,  "level": 0},
            {"name": "Удача",         "icon": "[?]",  "base_cost": 800,
             "type": "luck",  "value": 3,  "level": 0},
            {"name": "Шахта",         "icon": "[M]",  "base_cost": 5000,
             "type": "auto",  "value": 50, "level": 0},
            {"name": "Банк",          "icon": "[B]",  "base_cost": 25000,
             "type": "auto",  "value": 200, "level": 0},
            {"name": "Лаборатория",   "icon": "[L]",  "base_cost": 100000,
             "type": "multi", "value": 2,  "level": 0},
            {"name": "Портал",        "icon": "[P]",  "base_cost": 500000,
             "type": "auto",  "value": 1000, "level": 0},
            {"name": "Алмаз. шахта",  "icon": "[D]",  "base_cost": 2500000,
             "type": "auto",  "value": 5000, "level": 0},
            {"name": "Робоклик",      "icon": "[R]",  "base_cost": 10000,
             "type": "auto_click", "value": 1, "level": 0},
        ]

        self.load_game()

        root = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(6))

        # Счётчик
        self.coins_label = Label(
            text="0", font_size=dp(40), bold=True,
            size_hint_y=None, height=dp(50)
        )
        root.add_widget(self.coins_label)

        self.coins_word_label = Label(
            text="монет", font_size=dp(13),
            size_hint_y=None, height=dp(18)
        )
        root.add_widget(self.coins_word_label)

        # Престиж
        self.prestige_label = Label(
            text=f"Престиж: {self.prestige_points} очк. (x{self.prestige_multiplier:.2f})",
            font_size=dp(11),
            size_hint_y=None, height=dp(18)
        )
        root.add_widget(self.prestige_label)

        # Статистика
        self.stats_label = Label(
            text="", font_size=dp(10),
            size_hint_y=None, height=dp(18)
        )
        root.add_widget(self.stats_label)

        # Клик-область
        click_area = FloatLayout(size_hint_y=None, height=dp(150))
        self.click_btn = Button(
            text="КЛИК", font_size=dp(32), bold=True,
            background_normal='',
            size_hint=(0.6, 0.8),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        self.click_btn.bind(on_press=self.on_click)
        click_area.add_widget(self.click_btn)
        root.add_widget(click_area)
        self.click_area = click_area

        # Кнопка престижа
        self.prestige_btn = Button(
            text="[★] Престиж (сброс за очки)",
            font_size=dp(12), bold=True,
            size_hint_y=None, height=dp(35)
        )
        self.prestige_btn.bind(on_press=lambda b: self.do_prestige())
        root.add_widget(self.prestige_btn)

        # Достижения
        self.ach_title = Label(
            text="--- Достижения ---",
            font_size=dp(12), bold=True,
            size_hint_y=None, height=dp(20)
        )
        root.add_widget(self.ach_title)

        ach_scroll = ScrollView(size_hint_y=None, height=dp(50),
                                do_scroll_x=True, do_scroll_y=False)
        self.ach_box = BoxLayout(orientation='horizontal',
                                 size_hint_x=None,
                                 width=dp(150) * len(self.achievements),
                                 spacing=dp(5), padding=dp(5))
        self.ach_box.bind(minimum_width=self.ach_box.setter('width'))
        self.ach_labels = {}
        for key, ach in self.achievements.items():
            lbl = Label(
                text=f"[{'+' if ach['done'] else '-'}] {ach['name']}",
                font_size=dp(10), bold=True,
                size_hint_x=None, width=dp(140),
                halign="center", valign="middle"
            )
            lbl.bind(size=lbl.setter('text_size'))
            self.ach_labels[key] = lbl
            self.ach_box.add_widget(lbl)
        ach_scroll.add_widget(self.ach_box)
        root.add_widget(ach_scroll)

        # Улучшения
        self.upg_title = Label(
            text="--- Улучшения ---",
            font_size=dp(12), bold=True,
            size_hint_y=None, height=dp(20)
        )
        root.add_widget(self.upg_title)

        scroll = ScrollView(size_hint_y=1)
        self.upgrades_layout = BoxLayout(
            orientation='vertical', size_hint_y=None,
            spacing=dp(5), padding=dp(3)
        )
        self.upgrades_layout.bind(minimum_height=self.upgrades_layout.setter('height'))
        self.upgrade_cards = []
        for i, upg in enumerate(self.upgrades):
            card = UpgradeCard(self, upg, i)
            self.upgrade_cards.append(card)
            self.upgrades_layout.add_widget(card)
        scroll.add_widget(self.upgrades_layout)
        root.add_widget(scroll)

        # Нижние кнопки
        bottom = BoxLayout(size_hint_y=None, height=dp(40), spacing=dp(6))
        self.theme_btn = Button(text="[🎨 Темы]", font_size=dp(11))
        self.theme_btn.bind(on_press=lambda b: self.show_themes())
        bottom.add_widget(self.theme_btn)

        self.admin_btn = Button(text="[ Админ]", font_size=dp(11))
        self.admin_btn.bind(on_press=lambda b: self.open_admin())
        bottom.add_widget(self.admin_btn)

        self.reset_btn = Button(text="[X] Сброс", font_size=dp(11))
        self.reset_btn.bind(on_press=lambda b: self.reset_game())
        bottom.add_widget(self.reset_btn)
        root.add_widget(bottom)

        # Таймеры
        self._clock_auto = Clock.schedule_interval(self.auto_tick, 1.0)
        self._clock_save = Clock.schedule_interval(lambda dt: self.save_game(), 5.0)
        self._clock_auto_click = Clock.schedule_interval(self.autoclick_tick, 1.0)
        self._clock_ach = Clock.schedule_interval(self.check_achievements, 2.0)

        self.update_ui()
        return root

    # ---------- ТЕМЫ ----------
    def load_theme(self):
        try:
            if os.path.exists(SAVE_FILE):
                with open(SAVE_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                self.current_theme = data.get("theme", "classic")
        except Exception:
            pass

    def save_theme(self):
        try:
            if os.path.exists(SAVE_FILE):
                with open(SAVE_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
            else:
                data = {}
            data["theme"] = self.current_theme
            with open(SAVE_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f)
        except Exception:
            pass

    def apply_theme(self):
        theme = THEMES[self.current_theme]
        Window.clearcolor = theme["bg"]

        if hasattr(self, 'root'):
            try:
                # Основные цвета
                self.coins_label.color = theme["coins"]
                self.coins_word_label.color = theme["text"]
                self.prestige_label.color = theme["prestige_text"]
                self.stats_label.color = theme["stats"]
                self.ach_title.color = theme["text"]
                self.upg_title.color = theme["text"]

                # Кнопки
                self.click_btn.background_color = theme["click_btn"]
                self.prestige_btn.background_color = theme["prestige_btn"]
                self.theme_btn.background_color = theme["admin_btn"]
                self.admin_btn.background_color = theme["admin_btn"]
                self.reset_btn.background_color = theme["reset_btn"]

                # Достижения
                for key, ach in self.achievements.items():
                    lbl = self.ach_labels.get(key)
                    if lbl:
                        lbl.color = theme["ach_done"] if ach["done"] else theme["ach_lock"]

                # Карточки улучшений
                for card in self.upgrade_cards:
                    card.icon.color = theme["icon"]
                    card.name_label.color = theme["text"]
                    card.desc_label.color = theme["stats"]
                    card.update_state()
            except Exception as e:
                print("Theme apply error:", e)

    def show_themes(self):
        try:
            popup = Popup(title='Выбор темы', size_hint=(0.85, 0.7),
                          background_color=(0.2, 0.2, 0.3, 1))
            box = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(8))

            scroll = ScrollView(size_hint_y=1)
            themes_box = BoxLayout(orientation='vertical', size_hint_y=None,
                                   height=dp(50) * len(THEMES), spacing=dp(6))
            themes_box.bind(minimum_height=themes_box.setter('height'))

            for key, theme_data in THEMES.items():
                btn = Button(
                    text=f"{theme_data['name']} {'[✓]' if key == self.current_theme else ''}",
                    font_size=dp(13), bold=True,
                    background_color=theme_data["bg"],
                    color=theme_data["text"],
                    size_hint_y=None, height=dp(45)
                )

                def select_theme(k=key):
                    self.current_theme = k
                    self.apply_theme()
                    self.save_theme()
                    popup.dismiss()

                btn.bind(on_press=lambda b, k=key: select_theme(k))
                themes_box.add_widget(btn)

            scroll.add_widget(themes_box)
            box.add_widget(scroll)
            popup.content = box
            popup.open()
        except Exception as e:
            print("Themes error:", e)

    # ---------- КЛИК ----------
    def on_click(self, instance):
        try:
            base = self.click_power
            earned = base

            is_crit = random.randint(1, 100) <= self.crit_chance
            is_luck = random.randint(1, 100) <= self.luck_chance

            if is_crit:
                earned *= 5
            if is_luck:
                earned *= 10

            earned = int(earned * self.global_multiplier *
                         self.temp_multiplier * self.prestige_multiplier)
            if earned < 1:
                earned = 1

            self.coins += earned
            self.total_clicks += 1
            self.total_earned_all_time += earned

            try:
                anim = Animation(
                    pos_hint={'center_x': 0.5, 'center_y': 0.45},
                    duration=0.08
                ) + Animation(
                    pos_hint={'center_x': 0.5, 'center_y': 0.5},
                    duration=0.12
                )
                anim.start(instance)
            except Exception:
                pass

            try:
                pos = instance.to_window(*instance.center)
                color = (1, 0.3, 0.3, 1) if is_crit else (0.3, 1, 0.5, 1) if is_luck else THEMES[self.current_theme]["coins"]
                suffix = " КРИТ!" if is_crit else " УДАЧА!" if is_luck else ""
                txt = f"+{earned:,}{suffix}".replace(",", " ")
                self.click_area.add_widget(FloatingText(txt, pos[0], pos[1], color))
            except Exception:
                pass

            self.update_ui()
        except Exception as e:
            print("Click error:", e)

    # ---------- ПОКУПКА ----------
    def buy_upgrade(self, idx):
        try:
            upg = self.upgrades[idx]
            cost = self.get_cost(upg)
            if self.coins >= cost:
                self.coins -= cost
                upg["level"] += 1
                self.recalc_stats()
                self.update_ui()
        except Exception as e:
            print("Buy error:", e)

    def get_cost(self, upg):
        return int(upg["base_cost"] * (1.15 ** upg["level"]))

    def recalc_stats(self):
        self.click_power = 1
        self.auto_click_power = 0
        self.crit_chance = 0
        self.luck_chance = 0
        self.global_multiplier = 1

        for u in self.upgrades:
            lvl = u["level"]
            if lvl == 0:
                continue
            if u["type"] == "click":
                self.click_power += u["value"] * lvl
            elif u["type"] == "auto":
                self.auto_click_power += u["value"] * lvl
            elif u["type"] == "crit":
                self.crit_chance += u["value"] * lvl
            elif u["type"] == "luck":
                self.luck_chance += u["value"] * lvl
            elif u["type"] == "multi":
                self.global_multiplier *= (u["value"] ** lvl)

        self.prestige_multiplier = 1.0 + 0.1 * self.prestige_points

    # ---------- АВТОДОХОД ----------
    def auto_tick(self, dt):
        try:
            if self.auto_click_power > 0:
                earned = int(self.auto_click_power *
                             self.global_multiplier *
                             self.temp_multiplier *
                             self.prestige_multiplier)
                self.coins += earned
                self.total_earned_all_time += earned
                self.update_ui()
        except Exception:
            pass

    def autoclick_tick(self, dt):
        if not self.auto_click_enabled:
            return
        try:
            self.on_click(self.click_btn)
        except Exception:
            pass

    # ---------- ПРЕСТИЖ ----------
    def do_prestige(self):
        try:
            earned = int(self.total_earned_all_time / 10000)
            if earned < 1:
                self._show_msg("Нужно заработать 10,000 монет для престижа")
                return

            popup = Popup(
                title=f'Престиж: получить {earned} очк.?',
                size_hint=(0.8, 0.4),
                background_color=(0.3, 0.2, 0.4, 1)
            )
            box = BoxLayout(orientation='vertical', padding=dp(12), spacing=dp(10))
            box.add_widget(Label(
                text=(f"Сбросить монеты и улучшения,\n"
                      f"но получить +{earned} престиж-очков\n"
                      f"(x{1.0 + 0.1 * (self.prestige_points + earned):.2f} ко всему доходу)"),
                font_size=dp(13), halign="center"
            ))
            btns = BoxLayout(size_hint_y=None, height=dp(40), spacing=dp(10))

            def confirm(_):
                self.prestige_points += earned
                self.coins = 0
                self.total_earned_all_time = 0
                for u in self.upgrades:
                    u["level"] = 0
                self.recalc_stats()
                self.update_ui()
                self.save_game()
                popup.dismiss()

            def cancel(_):
                popup.dismiss()

            btn_yes = Button(text="Да", background_color=(0.2, 0.7, 0.3, 1))
            btn_yes.bind(on_press=confirm)
            btn_no = Button(text="Нет", background_color=(0.7, 0.2, 0.2, 1))
            btn_no.bind(on_press=cancel)
            btns.add_widget(btn_yes)
            btns.add_widget(btn_no)
            box.add_widget(btns)
            popup.content = box
            popup.open()
        except Exception as e:
            print("Prestige error:", e)

    # ---------- ДОСТИЖЕНИЯ ----------
    def check_achievements(self, dt):
        try:
            for key, ach in self.achievements.items():
                if ach["done"]:
                    continue
                if ach["check"]():
                    ach["done"] = True
                    self._show_achievement(ach["name"])
                    self.save_game()
        except Exception:
            pass

    def _show_achievement(self, name):
        try:
            popup = AchievementPopup(name)
            self.root.add_widget(popup)
        except Exception:
            pass

    def _show_msg(self, text):
        try:
            popup = Popup(title='Инфо', size_hint=(0.8, 0.3),
                          background_color=(0.2, 0.2, 0.3, 1))
            box = BoxLayout(orientation='vertical', padding=dp(10))
            box.add_widget(Label(text=text, font_size=dp(13), halign="center"))
            box.add_widget(Button(text='OK', on_press=lambda b: popup.dismiss(),
                                  background_color=(0.3, 0.5, 0.8, 1)))
            popup.content = box
            popup.open()
        except Exception:
            pass

    # ---------- АДМИН ----------
    def open_admin(self):
        try:
            popup = Popup(title='Пароль админа', size_hint=(0.8, 0.35),
                          background_color=(0.2, 0.2, 0.3, 1))
            box = BoxLayout(orientation='vertical', padding=dp(12), spacing=dp(8))
            inp = TextInput(hint_text='Пароль', font_size=dp(16), multiline=False)
            box.add_widget(inp)

            def check(_):
                if inp.text == ADMIN_PASSWORD:
                    popup.dismiss()
                    self.show_admin_panel()
                else:
                    inp.text = ''
                    inp.hint_text = 'Неверно!'
            box.add_widget(Button(text='Войти', on_press=check,
                                  background_color=(0.3, 0.5, 0.8, 1)))
            popup.content = box
            popup.open()
        except Exception as e:
            print("Admin open error:", e)

    def show_admin_panel(self):
        if self.admin_panel:
            return
        self.admin_panel = AdminPanel(self)
        self.root.add_widget(self.admin_panel)

    def close_admin(self):
        if self.admin_panel:
            try:
                self.root.remove_widget(self.admin_panel)
            except Exception:
                pass
            self.admin_panel = None

    # ---------- UI ----------
    def update_ui(self):
        try:
            self.coins_label.text = f"{int(self.coins):,}".replace(",", " ")
            mult = self.global_multiplier * self.temp_multiplier * self.prestige_multiplier
            self.stats_label.text = (
                f"Клик:+{self.click_power} Авто:+{self.auto_click_power}/с "
                f"Крит:{self.crit_chance}% Удача:{self.luck_chance}% x{mult:.1f}"
            )
            self.prestige_label.text = (
                f"Престиж: {self.prestige_points} очк. (x{self.prestige_multiplier:.2f})"
            )
            for card in self.upgrade_cards:
                card.update_state()
            for key, ach in self.achievements.items():
                lbl = self.ach_labels.get(key)
                if lbl:
                    lbl.text = f"[{'+' if ach['done'] else '-'}] {ach['name']}"
                    theme = THEMES[self.current_theme]
                    lbl.color = theme["ach_done"] if ach["done"] else theme["ach_lock"]
        except Exception as e:
            print("UI error:", e)

    # ---------- СОХРАНЕНИЕ ----------
    def save_game(self):
        try:
            data = {
                "coins": self.coins,
                "total_clicks": self.total_clicks,
                "total_earned_all_time": self.total_earned_all_time,
                "prestige_points": self.prestige_points,
                "upgrades": [u["level"] for u in self.upgrades],
                "achievements": {k: v["done"] for k, v in self.achievements.items()},
                "theme": self.current_theme
            }
            with open(SAVE_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f)
        except Exception as e:
            print("Save error:", e)

    def load_game(self):
        try:
            if not os.path.exists(SAVE_FILE):
                return
            with open(SAVE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.coins = data.get("coins", 0)
            self.total_clicks = data.get("total_clicks", 0)
            self.total_earned_all_time = data.get("total_earned_all_time", 0)
            self.prestige_points = data.get("prestige_points", 0)
            for i, lvl in enumerate(data.get("upgrades", [])):
                if i < len(self.upgrades):
                    self.upgrades[i]["level"] = lvl
            saved_ach = data.get("achievements", {})
            for k, v in saved_ach.items():
                if k in self.achievements:
                    self.achievements[k]["done"] = v
            self.recalc_stats()
        except Exception as e:
            print("Load error:", e)

    def reset_game(self):
        try:
            if os.path.exists(SAVE_FILE):
                os.remove(SAVE_FILE)
            self.coins = 0
            self.total_clicks = 0
            self.total_earned_all_time = 0
            self.prestige_points = 0
            self.current_theme = "classic"
            for u in self.upgrades:
                u["level"] = 0
            for ach in self.achievements.values():
                ach["done"] = False
            self.recalc_stats()
            self.apply_theme()
            self.update_ui()
        except Exception as e:
            print("Reset error:", e)


if __name__ == "__main__":
    ClickerApp().run()