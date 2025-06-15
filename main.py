import os
from datetime import datetime, timedelta

# Kivy UI Components
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.uix.modalview import ModalView
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.metrics import dp

# Firebase Integration
# NOTE: This uses the Python Firebase Admin SDK.
# It requires a service account key to run.
# The GitHub Actions workflow will handle this.
try:
    import firebase_admin
    from firebase_admin import credentials, firestore
except ImportError:
    # This is a fallback for local testing without firebase
    firebase_admin = None
    print("WARNING: firebase_admin library not found. App will run in mock mode.")


# --- App Data (Mirrors the React App's data) ---

MONTHLY_PLAN_DATA = [
  { 'month': 1, 'calories': 2230, 'protein': 205, 'phase': 1, 'neat': '7,000-8,000 steps' },
  { 'month': 2, 'calories': 2180, 'protein': 200, 'phase': 2, 'neat': '8,000-9,000 steps' },
  { 'month': 3, 'calories': 2130, 'protein': 195, 'phase': 3, 'neat': '8,000-10,000 steps' },
  { 'month': 4, 'calories': 2080, 'protein': 190, 'phase': 3, 'neat': '8,000-10,000 steps' },
  { 'month': 5, 'calories': 2030, 'protein': 185, 'phase': 4, 'neat': '10,000+ steps' },
  { 'month': 6, 'calories': 1980, 'protein': 180, 'phase': 4, 'neat': '10,000+ steps' },
  { 'month': 7, 'calories': 1930, 'protein': 175, 'phase': 4, 'neat': '10,000+ steps' },
  { 'month': 8, 'calories': 1880, 'protein': 170, 'phase': 5, 'neat': '10,000+ steps' },
  { 'month': 9, 'calories': 1850, 'protein': 168, 'phase': 5, 'neat': '10,000+ steps' },
  { 'month': 10, 'calories': 1820, 'protein': 165, 'phase': 5, 'neat': '10,000+ steps' },
]

WORKOUTS_DATA = {
    'Full Body A': { 'type': 'Strength', 'rir': 3, 'exercises': [ { 'name': 'Dumbbell Goblet Squats', 'sets': '3', 'reps': '10-15' }, { 'name': 'Push-ups', 'sets': '3', 'reps': 'AMRAP' }, { 'name': 'Single-Arm DB Rows', 'sets': '3', 'reps': '10-12/arm' }, { 'name': 'Dumbbell RDLs', 'sets': '3', 'reps': '12-15' }, { 'name': 'Dumbbell OHP', 'sets': '3', 'reps': '10-15' }, { 'name': 'Plank', 'sets': '3', 'reps': '30-60s' }, ]},
    'Full Body B': { 'type': 'Strength', 'rir': 3, 'exercises': [ { 'name': 'Dumbbell Lunges', 'sets': '3', 'reps': '8-12/leg' }, { 'name': 'Dumbbell Floor Press', 'sets': '3', 'reps': '10-15' }, { 'name': 'Bent-Over Two-DB Row', 'sets': '3', 'reps': '10-15' }, { 'name': 'Dumbbell Hammer Curls', 'sets': '2', 'reps': '12-15' }, { 'name': 'Dumbbell Triceps Kickbacks', 'sets': '2', 'reps': '12-15' }, { 'name': 'Bird-Dog', 'sets': '3', 'reps': '10-12/side' }, ]},
    'Cardio': { 'type': 'Cardio', 'details': "LISS Cardio for 25-35 minutes at a conversational pace (RPE 3-4)." },
    'Rest': { 'type': 'Rest', 'details': "Full rest day. Focus on recovery, hydration, and sleep." }
}

WEEKLY_SCHEDULE = [
    { 'day': 'Monday', 'type': 'Full Body A' }, { 'day': 'Tuesday', 'type': 'Cardio' }, { 'day': 'Wednesday', 'type': 'Rest' }, { 'day': 'Thursday', 'type': 'Cardio' }, { 'day': 'Friday', 'type': 'Full Body B' }, { 'day': 'Saturday', 'type': 'Cardio' }, { 'day': 'Sunday', 'type': 'Rest' }
]

# --- Helper Functions ---
def get_today_string():
    return datetime.now().strftime("%Y-%m-%d")

def get_week_number(start_date):
    if not start_date: return 1
    # Ensure start_date is timezone-naive for comparison
    if start_date.tzinfo:
        start_date = start_date.replace(tzinfo=None)
    diff = datetime.now() - start_date
    week = (diff.days // 7) + 1
    return max(1, week) # Ensure week is at least 1


# --- Kivy Screen Definitions using Builder ---
# This is a string that defines the layout of all screens in a Kivy-specific language.
# It makes the Python code cleaner by separating layout from logic.

KIVY_LAYOUT_STRING = """
<MainScreen>:
    BoxLayout:
        orientation: 'vertical'
        ScreenManager:
            id: sm
            DashboardScreen:
                name: 'dashboard'
            WorkoutScreen:
                name: 'workout'
            NutritionScreen:
                name: 'nutrition'
            SettingsScreen:
                name: 'settings'
        BoxLayout:
            size_hint_y: None
            height: dp(60)
            canvas.before:
                Color:
                    rgba: 0.1, 0.1, 0.1, 1
                Rectangle:
                    pos: self.pos
                    size: self.size
            Button:
                text: 'Dashboard'
                on_release: app.root.ids.sm.current = 'dashboard'
            Button:
                text: 'Workouts'
                on_release: app.root.ids.sm.current = 'workout'
            Button:
                text: 'Nutrition'
                on_release: app.root.ids.sm.current = 'nutrition'
            Button:
                text: 'Settings'
                on_release: app.root.ids.sm.current = 'settings'

<DashboardScreen>:
    ScrollView:
        GridLayout:
            cols: 1
            size_hint_y: None
            height: self.minimum_height
            padding: dp(10)
            spacing: dp(10)

            Label:
                text: 'AMS Transformation Dashboard'
                font_size: '24sp'
                size_hint_y: None
                height: dp(40)

            GridLayout:
                cols: 2
                spacing: dp(10)
                size_hint_y: None
                height: self.minimum_height

                # Dashboard Widgets will be added here from Python code
                id: dashboard_grid

<WorkoutScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: dp(10)
        spacing: dp(10)
        Label:
            text: 'Weekly Workout Plan'
            font_size: '24sp'
            size_hint_y: None
            height: dp(40)
        ScrollView:
            GridLayout:
                id: workout_grid
                cols: 1
                size_hint_y: None
                height: self.minimum_height
                spacing: dp(5)

<NutritionScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: dp(10)
        spacing: dp(10)
        Label:
            text: 'Daily Nutrition Log'
            font_size: '24sp'
            size_hint_y: None
            height: dp(40)
        # More nutrition widgets would go here
        Label:
            text: 'Nutrition logging coming soon!'

<SettingsScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: dp(10)
        spacing: dp(10)
        Label:
            text: 'Settings'
            font_size: '24sp'
            size_hint_y: None
            height: dp(40)
        GridLayout:
            cols: 1
            id: settings_grid
            # Settings info will be added here

<WorkoutPopup>:
    title: "Workout Details"
    size_hint: 0.9, 0.9
    BoxLayout:
        orientation: 'vertical'
        padding: dp(10)
        ScrollView:
            Label:
                id: workout_details_label
                text: ''
                size_hint_y: None
                height: self.texture_size[1]
                text_size: self.width, None
        Button:
            text: 'Close'
            size_hint_y: None
            height: dp(50)
            on_release: root.dismiss()
"""

Builder.load_string(KIVY_LAYOUT_STRING)

# --- Screen Class Definitions ---

class MainScreen(BoxLayout):
    pass

class DashboardScreen(Screen):
    def on_enter(self, *args):
        # This method is called every time the screen is shown
        app = App.get_running_app()
        app.update_dashboard()

class WorkoutScreen(Screen):
    def on_enter(self, *args):
        app = App.get_running_app()
        app.update_workout_plan()

class NutritionScreen(Screen):
    pass

class SettingsScreen(Screen):
    def on_enter(self, *args):
        app = App.get_running_app()
        app.update_settings()

class WorkoutPopup(ModalView):
    pass

# --- The Main Application Class ---

class FitnessApp(App):

    def build(self):
        self.db = None
        self.user_id = "user_01" # Hardcoded for simplicity
        self.profile_data = {}
        self.daily_data = {}
        
        # This is the Kivy way of setting colors and styles
        Window.clearcolor = (0.15, 0.15, 0.15, 1) # Dark gray background
        
        # Initialize Firebase if the library is available
        if firebase_admin:
            try:
                # IMPORTANT: The serviceAccountKey.json must be present for this to work.
                # In the GitHub Actions workflow, this will be provided via a secret.
                cred_path = 'serviceAccountKey.json'
                if os.path.exists(cred_path):
                    cred = credentials.Certificate(cred_path)
                    firebase_admin.initialize_app(cred)
                    self.db = firestore.client()
                    print("Firebase initialized successfully.")
                else:
                    print(f"WARNING: '{cred_path}' not found. Firebase will not be used.")
            except Exception as e:
                print(f"ERROR: Could not initialize Firebase: {e}")
        
        # Load data from Firebase when the app starts
        Clock.schedule_once(self.load_initial_data, 1)

        return MainScreen()

    def load_initial_data(self, *args):
        """Fetches the user's profile and daily data from Firestore."""
        if not self.db:
            print("Running in mock mode. No data will be fetched.")
            self.profile_data = {
                'startDate': datetime.now() - timedelta(days=14),
                'startWeight': 304,
                'goalWeight': 235
            }
            self.daily_data = {
                get_today_string(): {'calories': 1200, 'protein': 150}
            }
            self.update_all_screens()
            return

        try:
            # Fetch profile
            profile_ref = self.db.collection('users').document(self.user_id).collection('profile').document('main')
            profile_doc = profile_ref.get()
            if profile_doc.exists:
                self.profile_data = profile_doc.to_dict()
                print("Profile data loaded.")
            else:
                print("No profile found. Creating a default one.")
                # Create a default profile if one doesn't exist
                self.profile_data = {
                    'startDate': datetime.now(),
                    'startWeight': 304.0,
                    'goalWeight': 235.0
                }
                profile_ref.set(self.profile_data)

            # Fetch all daily data documents
            daily_ref = self.db.collection('users').document(self.user_id).collection('dailyData').stream()
            self.daily_data = {doc.id: doc.to_dict() for doc in daily_ref}
            print(f"Loaded {len(self.daily_data)} daily data entries.")
            
            # Update all screens with the new data
            self.update_all_screens()

        except Exception as e:
            print(f"Error loading initial data from Firebase: {e}")

    def update_all_screens(self):
        """Calls the update method for each screen."""
        self.update_dashboard()
        self.update_workout_plan()
        self.update_settings()

    def create_info_card(self, title, value):
        """Helper function to create a consistent looking card widget."""
        card = BoxLayout(orientation='vertical', size_hint_y=None, height=dp(100), padding=dp(10))
        card.add_widget(Label(text=title, color=(0.7, 0.7, 0.7, 1), font_size='16sp'))
        card.add_widget(Label(text=str(value), bold=True, font_size='22sp'))
        return card

    def update_dashboard(self):
        """Populates the dashboard screen with current data."""
        grid = self.root.ids.sm.get_screen('dashboard').ids.dashboard_grid
        grid.clear_widgets()

        if not self.profile_data:
            grid.add_widget(Label(text="Loading profile..."))
            return

        current_week = get_week_number(self.profile_data.get('startDate'))
        plan = MONTHLY_PLAN_DATA[min(current_week // 4, len(MONTHLY_PLAN_DATA) - 1)]
        today_data = self.daily_data.get(get_today_string(), {})

        grid.add_widget(self.create_info_card("Current Week", current_week))
        grid.add_widget(self.create_info_card("Current Phase", plan['phase']))
        grid.add_widget(self.create_info_card("Calorie Target", f"{plan['calories']} kcal"))
        grid.add_widget(self.create_info_card("Protein Target", f"{plan['protein']} g"))
        
        calories_today = today_data.get('calories', 0)
        protein_today = today_data.get('protein', 0)
        
        grid.add_widget(self.create_info_card("Calories Logged", calories_today))
        grid.add_widget(self.create_info_card("Protein Logged", protein_today))

    def update_workout_plan(self):
        """Populates the workout screen with the weekly schedule."""
        grid = self.root.ids.sm.get_screen('workout').ids.workout_grid
        grid.clear_widgets()
        
        for day_info in WEEKLY_SCHEDULE:
            day_workout = WORKOUTS_DATA.get(day_info['type'], {})
            
            day_card = BoxLayout(padding=dp(10), size_hint_y=None, height=dp(80))
            
            info_layout = BoxLayout(orientation='vertical')
            info_layout.add_widget(Label(text=day_info['day'], font_size='18sp', bold=True, halign='left'))
            info_layout.add_widget(Label(text=day_info['type'], color=(0.8, 0.8, 0.8, 1), halign='left'))
            
            day_card.add_widget(info_layout)
            
            # Pass the full workout info to the popup function
            btn = Button(text='View', size_hint_x=0.3)
            btn.bind(on_release=lambda x, workout=day_workout: self.show_workout_popup(workout))
            day_card.add_widget(btn)

            grid.add_widget(day_card)

    def show_workout_popup(self, workout_info):
        """Displays a popup with details of the selected workout."""
        popup = WorkoutPopup()
        details_text = f"[b]{workout_info.get('type', 'N/A')}[/b]\n\n"
        
        if workout_info.get('type') == 'Strength':
            details_text += f"Reps in Reserve (RIR): {workout_info.get('rir', 'N/A')}\n\n"
            for exercise in workout_info.get('exercises', []):
                details_text += f"- {exercise['name']}: {exercise['sets']} sets of {exercise['reps']} reps\n"
        else:
            details_text += workout_info.get('details', 'No details available.')
        
        popup.ids.workout_details_label.text = details_text
        popup.open()

    def update_settings(self):
        """Populates the settings screen with profile information."""
        grid = self.root.ids.sm.get_screen('settings').ids.settings_grid
        grid.clear_widgets()

        if not self.profile_data:
            grid.add_widget(Label(text="Loading profile..."))
            return
            
        start_date = self.profile_data.get('startDate')
        if hasattr(start_date, 'strftime'):
             start_date_str = start_date.strftime('%Y-%m-%d')
        else:
            # Handle case where date might be a string already
            start_date_str = str(start_date)

        grid.add_widget(Label(text=f"User ID: {self.user_id}"))
        grid.add_widget(Label(text=f"Start Date: {start_date_str}"))
        grid.add_widget(Label(text=f"Start Weight: {self.profile_data.get('startWeight')} lbs"))
        grid.add_widget(Label(text=f"Goal Weight: {self.profile_data.get('goalWeight')} lbs"))


if __name__ == '__main__':
    FitnessApp().run()
