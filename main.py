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
from kivy.uix.modalview import ModalView
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.storage.jsonstore import JsonStore

# --- App Data (This is the app's permanent offline database) ---

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

ACHIEVEMENT_LIST = {
    'Consistency': [
        { 'id': 'c1', 'title': 'First Workout!', 'description': 'Complete your first activity.'},
        { 'id': 'c2', 'title': 'One Week Strong', 'description': 'Complete a full week of planned workouts.'},
        { 'id': 'c3', 'title': '30-Day Hustle', 'description': 'Complete 30 workouts.'},
    ],
    'Weight Loss': [
        { 'id': 'w1', 'title': 'On the Board', 'description': 'Lose your first 10 lbs.'},
        { 'id': 'w2', 'title': '25 Down', 'description': 'Lose a total of 25 lbs.'},
        { 'id': 'w3', 'title': 'Halfway There!', 'description': 'Lose 35 lbs, halfway to your goal.'},
    ]
}


# --- Helper Functions ---
def get_today_string():
    return datetime.now().strftime("%Y-%m-%d")

def get_week_number(start_date):
    if not start_date: return 1
    # Handle both datetime objects and ISO format strings
    if isinstance(start_date, str):
        try:
            start_date = datetime.fromisoformat(start_date)
        except ValueError:
            return 1 # Or handle error appropriately
            
    if start_date.tzinfo:
        start_date = start_date.replace(tzinfo=None)
    
    diff = datetime.now() - start_date
    week = (diff.days // 7) + 1
    return max(1, week)


# --- Kivy Screen Definitions using Builder ---
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
            AwardsScreen:
                name: 'awards'
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
                text: 'Awards'
                on_release: app.root.ids.sm.current = 'awards'
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
        
        GridLayout:
            cols: 1
            size_hint_y: None
            height: dp(180) # Increased height for inputs and button
            spacing: dp(10)
            padding: dp(10)
            
            TextInput:
                id: meal_name_input
                hint_text: 'Meal Name'
                multiline: False
                
            TextInput:
                id: calories_input
                hint_text: 'Calories'
                input_filter: 'int'
                multiline: False

            TextInput:
                id: protein_input
                hint_text: 'Protein (g)'
                input_filter: 'int'
                multiline: False
            
            Button:
                text: 'Log Meal'
                on_release: app.log_meal()

        ScrollView:
            GridLayout:
                id: meal_list
                cols: 1
                size_hint_y: None
                height: self.minimum_height
                spacing: dp(5)

<AwardsScreen>:
    ScrollView:
        GridLayout:
            cols: 1
            padding: dp(10)
            spacing: dp(10)
            size_hint_y: None
            height: self.minimum_height
            id: awards_grid

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
            spacing: dp(10)
            Label:
                text: 'This is an offline version of the app.'
            Label:
                text: 'User data is saved locally on this device.'
            Label:
                text: 'Version 0.7'

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
                markup: True
        Button:
            text: 'Close'
            size_hint_y: None
            height: dp(50)
            on_release: root.dismiss()
"""

Builder.load_string(KIVY_LAYOUT_STRING)

# --- Screen Class Definitions ---

class MainScreen(BoxLayout): pass
class DashboardScreen(Screen):
    def on_enter(self, *args): App.get_running_app().update_dashboard()
class WorkoutScreen(Screen):
    def on_enter(self, *args): App.get_running_app().update_workout_plan()
class NutritionScreen(Screen):
    def on_enter(self, *args): App.get_running_app().update_meal_list()
class AwardsScreen(Screen):
    def on_enter(self, *args): App.get_running_app().update_awards_screen()
class SettingsScreen(Screen): pass
class WorkoutPopup(ModalView): pass

# --- The Main Application Class ---

class FitnessApp(App):

    def build(self):
        # Using Kivy's JsonStore for simple offline data persistence.
        # This creates a file in the app's user data directory.
        self.store = JsonStore(os.path.join(self.user_data_dir, 'fitness_data.json'))
        
        # Initialize data if the store is empty
        if not self.store.exists('profile'):
            self.store.put('profile',
                startDate=(datetime.now() - timedelta(days=30)).isoformat(),
                startWeight=304,
                goalWeight=235,
                unlockedAchievements={}
            )
        
        today = get_today_string()
        if not self.store.exists(today):
             self.store.put(today, meals=[])

        Window.clearcolor = (0.15, 0.15, 0.15, 1)
        
        Clock.schedule_once(self.update_all_screens, 0)
        return MainScreen()

    def update_all_screens(self, *args):
        self.update_dashboard()
        self.update_workout_plan()
        self.update_meal_list()
        self.update_awards_screen()

    def create_info_card(self, title, value):
        card = BoxLayout(orientation='vertical', size_hint_y=None, height=dp(100), padding=dp(10),
                         canvas_before=[Builder.load_string('''
Color:
    rgba: .2, .2, .2, 1
RoundedRectangle:
    pos: self.pos
    size: self.size
    radius: [dp(10)]
''')])
        card.add_widget(Label(text=title, color=(0.7, 0.7, 0.7, 1), font_size='16sp'))
        card.add_widget(Label(text=str(value), bold=True, font_size='22sp'))
        return card

    def update_dashboard(self):
        grid = self.root.ids.sm.get_screen('dashboard').ids.dashboard_grid
        grid.clear_widgets()

        profile = self.store.get('profile')
        current_week = get_week_number(profile['startDate'])
        plan_index = min(current_week // 4, len(MONTHLY_PLAN_DATA) - 1)
        plan = MONTHLY_PLAN_DATA[plan_index]
        
        today = get_today_string()
        if self.store.exists(today):
            meals_data = self.store.get(today)['meals']
            total_calories = sum(meal['calories'] for meal in meals_data)
            total_protein = sum(meal['protein'] for meal in meals_data)
        else:
            total_calories = 0
            total_protein = 0

        grid.add_widget(self.create_info_card("Current Week", current_week))
        grid.add_widget(self.create_info_card("Current Phase", plan['phase']))
        grid.add_widget(self.create_info_card("Calorie Target", f"{plan['calories']} kcal"))
        grid.add_widget(self.create_info_card("Protein Target", f"{plan['protein']} g"))
        grid.add_widget(self.create_info_card("Calories Logged", total_calories))
        grid.add_widget(self.create_info_card("Protein Logged", total_protein))

    def update_workout_plan(self):
        grid = self.root.ids.sm.get_screen('workout').ids.workout_grid
        grid.clear_widgets()
        
        for day_info in WEEKLY_SCHEDULE:
            day_workout = WORKOUTS_DATA.get(day_info['type'], {})
            day_card = BoxLayout(padding=dp(10), size_hint_y=None, height=dp(80))
            info_layout = BoxLayout(orientation='vertical')
            info_layout.add_widget(Label(text=day_info['day'], font_size='18sp', bold=True, halign='left', text_size=(Window.width * 0.5, None)))
            info_layout.add_widget(Label(text=day_info['type'], color=(0.8, 0.8, 0.8, 1), halign='left', text_size=(Window.width * 0.5, None)))
            day_card.add_widget(info_layout)
            btn = Button(text='View', size_hint_x=0.3)
            btn.bind(on_release=lambda x, workout=day_workout: self.show_workout_popup(workout))
            day_card.add_widget(btn)
            grid.add_widget(day_card)

    def show_workout_popup(self, workout_info):
        popup = WorkoutPopup()
        details_text = f"[b]{workout_info.get('type', 'N/A')}[/b]\\n\\n"
        
        if workout_info.get('type') == 'Strength':
            details_text += f"Reps in Reserve (RIR): {workout_info.get('rir', 'N/A')}\\n\\n"
            for exercise in workout_info.get('exercises', []):
                details_text += f"- {exercise['name']}: {exercise['sets']} sets of {exercise['reps']} reps\\n"
        else:
            details_text += workout_info.get('details', 'No details available.')
        
        popup.ids.workout_details_label.text = details_text
        popup.open()

    def log_meal(self):
        nutrition_screen = self.root.ids.sm.get_screen('nutrition')
        meal_name = nutrition_screen.ids.meal_name_input.text
        calories = nutrition_screen.ids.calories_input.text
        protein = nutrition_screen.ids.protein_input.text

        if not meal_name or not calories or not protein: return

        try:
            today = get_today_string()
            if not self.store.exists(today):
                self.store.put(today, meals=[])

            meals_data = self.store.get(today)
            meals_data['meals'].append({
                'name': meal_name, 'calories': int(calories), 'protein': int(protein)
            })
            self.store.put(today, meals=meals_data['meals'])
            
            nutrition_screen.ids.meal_name_input.text = ''
            nutrition_screen.ids.calories_input.text = ''
            nutrition_screen.ids.protein_input.text = ''
            
            self.update_meal_list()
            self.update_dashboard()

        except ValueError:
            print("Calories and Protein must be numbers.")

    def update_meal_list(self):
        meal_list_grid = self.root.ids.sm.get_screen('nutrition').ids.meal_list
        meal_list_grid.clear_widgets()
        
        today = get_today_string()
        if self.store.exists(today):
            meals = self.store.get(today)['meals']
        else:
            meals = []
        
        if not meals:
            meal_list_grid.add_widget(Label(text="No meals logged for today.", size_hint_y=None, height=dp(50)))
            return

        for meal in meals:
            meal_list_grid.add_widget(Label(
                text=f"{meal['name']}: {meal['calories']} kcal, {meal['protein']}g protein",
                size_hint_y=None, height=dp(40)
            ))

    def update_awards_screen(self):
        grid = self.root.ids.sm.get_screen('awards').ids.awards_grid
        grid.clear_widgets()
        
        profile = self.store.get('profile')
        unlocked = profile.get('unlockedAchievements', {})

        for category, achievements in ACHIEVEMENT_LIST.items():
            grid.add_widget(Label(text=category, font_size='20sp', bold=True, size_hint_y=None, height=dp(40)))
            for ach in achievements:
                status = "Unlocked" if ach['id'] in unlocked else "Locked"
                award_text = f"[b]{ach['title']}[/b] ({status})\\n{ach['description']}"
                award_label = Label(text=award_text, markup=True, size_hint_y=None, height=dp(60))
                grid.add_widget(award_label)


if __name__ == '__main__':
    FitnessApp().run()
