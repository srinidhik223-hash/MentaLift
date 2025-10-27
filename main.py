import json, os
from datetime import datetime
from textblob import TextBlob
import matplotlib.pyplot as plt

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.slider import Slider
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.popup import Popup

SESSION_FILE = "session.json"

# ------------------- Suggestion Logic -------------------
def get_suggestions(mood, stress, anxiety, sleep, notes):
    suggestions = []
    if mood <= 3:
        suggestions.extend([
            "Talk to a friend or family member.",
            "Go for a walk outdoors.",
            "Write your thoughts in a journal."
        ])
    elif mood <= 6:
        suggestions.extend([
            "Do something creative you enjoy.",
            "Listen to uplifting music.",
            "Spend time on a hobby."
        ])
    else:
        suggestions.extend([
            "Maintain your positive habits.",
            "Share your positivity with someone.",
            "Keep up your exercise routine."
        ])
    if stress >= 7 or anxiety >= 7:
        suggestions.append("Practice deep breathing for 5–10 minutes.")
    elif stress >= 5 or anxiety >= 5:
        suggestions.append("Take a short break to relax.")
    if sleep < 5:
        suggestions.append("Aim for at least 7–8 hours of sleep.")
    if notes.strip():
        sentiment = TextBlob(notes).sentiment.polarity
        if sentiment < -0.3:
            suggestions.append("Consider talking to a counselor.")
        elif sentiment > 0.3:
            suggestions.append("Keep up the positive mindset!")
    return [f"{i+1}. {s}" for i, s in enumerate(suggestions)]

# ------------------- Status Calculation -------------------
def get_status(mood, stress, anxiety, sleep):
    if mood >= 7 and stress <= 3 and anxiety <= 3 and sleep >= 7:
        return "Calm"
    elif stress >= 7 and anxiety >= 7:
        return "Anxious"
    elif mood <= 3 and sleep <= 4:
        return "Tired"
    elif mood <= 4:
        return "Low"
    elif stress >= 6:
        return "Stressed"
    else:
        return "Balanced"

# ------------------- Storage Functions -------------------
def save_entry(username, mood, stress, anxiety, sleep, status, notes):
    entry = {
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "mood": mood,
        "stress": stress,
        "anxiety": anxiety,
        "sleep": sleep,
        "status": status,
        "notes": notes,
        "score": (mood + sleep) - (stress + anxiety),
        "suggestions": get_suggestions(mood, stress, anxiety, sleep, notes)
    }
    filename = f"{username}_data.json"
    if os.path.exists(filename):
        with open(filename, "r") as f:
            history = json.load(f)
    else:
        history = []
    history.append(entry)
    with open(filename, "w") as f:
        json.dump(history, f, indent=4)

def load_history(username):
    filename = f"{username}_data.json"
    if os.path.exists(filename):
        with open(filename, "r") as f:
            return json.load(f)
    return []

# ------------------- Session Management -------------------
def save_session(username):
    with open(SESSION_FILE, "w") as f:
        json.dump({"username": username}, f)

def load_session():
    if os.path.exists(SESSION_FILE):
        with open(SESSION_FILE, "r") as f:
            return json.load(f).get("username")
    return None

def clear_session():
    if os.path.exists(SESSION_FILE):
        os.remove(SESSION_FILE)

# ------------------- Screens -------------------

# ---- Welcome Screen ----
class WelcomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation="vertical", padding=20, spacing=20)

        # Icon image
        try:
            logo = Image(source="icon.png", size_hint=(1, 0.4), allow_stretch=True)
            layout.add_widget(logo)
        except Exception as e:
            print("⚠ Could not load welcome icon:", e)

        # App title
        layout.add_widget(Label(text="MentaLift", font_size=32, bold=True, size_hint=(1, 0.2)))

        # Buttons
        btn = Button(text="Check My Mental Status", size_hint=(1, 0.15), background_color=(0.2,0.6,1,1))
        btn.bind(on_press=lambda x: setattr(self.manager, "current", "login"))
        layout.add_widget(btn)

        about_btn = Button(text="About MentaLift", size_hint=(1, 0.15))
        about_btn.bind(on_press=lambda x: self.show_about())
        layout.add_widget(about_btn)

        self.add_widget(layout)

    def show_about(self):
        content = Label(text="MentaLift – Your digital companion for mental well-being.\nDesigned to monitor mental status and provide daily insights.")
        popup = Popup(title="About MentaLift", content=content, size_hint=(0.8,0.5))
        popup.open()

# ---- Login Screen ----
class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation="vertical", padding=20, spacing=10)

        # App title
        layout.add_widget(Label(text="MentaLift", font_size=32, bold=True, size_hint=(1, 0.2)))

        # Icon below title
        try:
            logo = Image(source="icon.png", size_hint=(1, 0.3), allow_stretch=True)
            layout.add_widget(logo)
        except Exception as e:
            print("⚠ Could not load login icon:", e)

        # Username & Password
        self.username = TextInput(hint_text="Enter Username", size_hint=(1, 0.15))
        self.password = TextInput(hint_text="Enter Password", password=True, size_hint=(1, 0.15))
        login_btn = Button(text="Login / Register", size_hint=(1, 0.15), background_color=(0.2, 0.6, 1, 1))
        login_btn.bind(on_press=self.login)

        layout.add_widget(self.username)
        layout.add_widget(self.password)
        layout.add_widget(login_btn)
        self.add_widget(layout)

    def login(self, instance):
        username = self.username.text.strip()
        if username:
            save_session(username)
            self.manager.current = "home"
            self.manager.get_screen("home").username = username

# ---- Home Screen ----
class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.username = None
        self.layout = BoxLayout(orientation="vertical", spacing=10, padding=10)

        self.layout.add_widget(Label(text="Log Your Mental Health", font_size=22, size_hint=(1, 0.1)))
        self.mood_slider = self.make_slider("Mood")
        self.stress_slider = self.make_slider("Stress")
        self.anxiety_slider = self.make_slider("Anxiety")
        self.sleep_slider = self.make_slider("Sleep Quality")

        self.notes = TextInput(hint_text="Write additional notes...", size_hint=(1, 0.3))
        self.layout.add_widget(self.notes)

        btn = Button(text="Submit & Get Suggestions", size_hint=(1, 0.2), background_color=(0.2, 0.6, 1, 1))
        btn.bind(on_press=self.submit)
        self.layout.add_widget(btn)

        self.results = Label(text="", size_hint=(1, 1))
        scroll = ScrollView(size_hint=(1, 1))
        scroll.add_widget(self.results)
        self.layout.add_widget(scroll)

        self.history_btn = Button(text="View History", size_hint=(1, 0.15))
        self.history_btn.bind(on_press=lambda x: setattr(self.manager, "current", "history"))
        self.layout.add_widget(self.history_btn)

        self.logout_btn = Button(text="Logout", size_hint=(1, 0.15), background_color=(1, 0.2, 0.2, 1))
        self.logout_btn.bind(on_press=self.logout)
        self.layout.add_widget(self.logout_btn)

        self.add_widget(self.layout)

    def make_slider(self, text):
        box = BoxLayout(orientation="vertical", size_hint=(1, 0.2))
        label = Label(text=f"{text}: 5", size_hint=(1, 0.3))
        slider = Slider(min=1, max=10, value=5, step=1, size_hint=(1, 0.3))
        slider.bind(value=lambda inst, val: setattr(label, "text", f"{text}: {int(val)}"))
        box.add_widget(label)
        box.add_widget(slider)
        self.layout.add_widget(box)
        return slider

    def submit(self, instance):
        mood = int(self.mood_slider.value)
        stress = int(self.stress_slider.value)
        anxiety = int(self.anxiety_slider.value)
        sleep = int(self.sleep_slider.value)
        notes = self.notes.text

        status = get_status(mood, stress, anxiety, sleep)
        suggestions = get_suggestions(mood, stress, anxiety, sleep, notes)

        save_entry(self.username, mood, stress, anxiety, sleep, status, notes)

        self.results.text = f"Status: {status}\n\nSuggestions:\n" + "\n".join(suggestions)

    def logout(self, instance):
        clear_session()
        self.manager.current = "login"

# ---- History Screen ----
class HistoryScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation="vertical", padding=10, spacing=10)

        # Icon image at top of history screen
        try:
            logo = Image(source="icon.png", size_hint=(1, 0.2), allow_stretch=True)
            self.layout.add_widget(logo)
        except Exception as e:
            print("⚠ Could not load history icon:", e)

        self.layout.add_widget(Label(text="Mental Well-being History", font_size=22, size_hint=(1, 0.1)))

        # Scroll area for graph & entries
        self.scroll_area = ScrollView(size_hint=(1, 0.7))
        self.content_layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.content_layout.bind(minimum_height=self.content_layout.setter('height'))
        self.scroll_area.add_widget(self.content_layout)
        self.layout.add_widget(self.scroll_area)

        back_btn = Button(text="Back", size_hint=(1, 0.15))
        back_btn.bind(on_press=lambda x: setattr(self.manager, "current", "home"))
        self.layout.add_widget(back_btn)

        self.add_widget(self.layout)

    def on_pre_enter(self):
        username = self.manager.get_screen("home").username
        history = load_history(username)
        self.content_layout.clear_widgets()

        if history:
            # Graph
            dates = [datetime.strptime(h["date"], "%Y-%m-%d %H:%M") for h in history]
            scores = [h["score"] for h in history]

            plt.clf()
            plt.figure(figsize=(7, 3))
            plt.plot(dates, scores, marker="o", linestyle="-", color="#4C84FF")
            plt.xlabel("Date")
            plt.ylabel("Mental Well-being Score")
            plt.title(f"Mental Health Trend - {username}")
            plt.grid(True, linestyle="--", alpha=0.6)
            plt.xticks(rotation=45)
            plt.tight_layout()

            graph_path = f"{username}_graph.png"
            plt.savefig(graph_path)
            self.content_layout.add_widget(Image(source=graph_path, size_hint_y=None, height=300))

            # Entries
            for h in history:
                entry_text = (
                    f"Date: {h['date']}\n"
                    f"Mood: {h['mood']} | Stress: {h['stress']} | Anxiety: {h['anxiety']} | Sleep: {h['sleep']}\n"
                    f"Status: {h['status']}\n"
                    f"Notes: {h['notes']}\n"
                    f"Suggestions:\n" + "\n".join(h["suggestions"]) + "\n" + "-"*40
                )
                self.content_layout.add_widget(Label(text=entry_text, size_hint_y=None, height=200))
        else:
            self.content_layout.add_widget(Label(text="No history yet."))

# ------------------- App -------------------
class MentalHealthApp(App):
    def build(self):
        sm = ScreenManager()
        saved_user = load_session()
        sm.add_widget(WelcomeScreen(name="welcome"))
        sm.add_widget(LoginScreen(name="login"))
        sm.add_widget(HomeScreen(name="home"))
        sm.add_widget(HistoryScreen(name="history"))

        if saved_user:
            home_screen = sm.get_screen("home")
            home_screen.username = saved_user
            sm.current = "home"
        else:
            sm.current = "welcome"  # start with welcome screen

        return sm

if __name__ == "__main__":
    MentalHealthApp().run()
