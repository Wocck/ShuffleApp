import kivy
import random
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.checkbox import CheckBox
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.storage.jsonstore import JsonStore


kivy.require("2.0.0")


class MyRoot(BoxLayout):
    def __init__(self):
        super(MyRoot, self).__init__()
        self.store = JsonStore('player_data.json')
        self.player_list_layout = None
        self.checkboxes = None
        self.update_player_list()

    def update_player_list(self):
        player_names = self.load_players_to_list()
        self.player_list_layout = self.ids['player_list']

        # Clear any existing widgets in the GridLayout
        self.player_list_layout.clear_widgets()

        # Populate the GridLayout with player name Labels
        for name in player_names:
            box_layout = BoxLayout(orientation='horizontal', padding='5dp', size_hint=(None, None), width=400)
            player_checkbox = CheckBox(active=False, size=(80, 80), color=(0.65, 0.19, 0.47, 5))
            player_label = Label(text=name)
            player_checkbox.bind(active=self.increment_label)

            box_layout.add_widget(player_checkbox)
            box_layout.add_widget(player_label)
            self.player_list_layout.add_widget(box_layout)

    def increment_label(self, checkbox, value):
        if value:
            self.ids['count_label'].text = str(int(self.ids['count_label'].text) + 1)
        else:
            self.ids['count_label'].text = str(int(self.ids['count_label'].text) - 1)

    def load_players_to_list(self):
        if self.store.exists('players'):
            return self.store.get('players')['names']
        else:
            return []

    def add_player_action(self):
        if self.ids['add_player_input'].text == '':
            return
        player_name = self.ids['add_player_input'].text.rstrip()
        player_names = self.load_players_to_list()
        player_names.append(player_name)
        self.store.put('players', names=player_names)
        self.ids['add_player_input'].text = ""
        self.ids['count_label'].text = '0'
        self.update_player_list()

    def remove_player_action(self):
        player_name = self.ids["remove_player_input"].text.rstrip()
        player_names = self.load_players_to_list()
        if not player_names or player_name not in player_names:
            return
        player_names.remove(player_name)
        self.store.put('players', names=player_names)
        self.ids['remove_player_input'].text = ""
        self.update_player_list()

    def remove_all_players_action(self):
        player_names = self.load_players_to_list()
        if not player_names:
            return
        self.store.delete('players')
        self.ids['count_label'].text = '0'
        self.update_player_list()

    def shuffle_action(self):
        selected_players = []
        self.checkboxes = self.player_list_layout.children
        for checkbox in self.checkboxes:
            if checkbox.children[1].active:
                selected_players.append(checkbox.children[0].text)

        random.shuffle(selected_players)
        team1 = selected_players[:len(selected_players) // 2]
        team2 = selected_players[len(selected_players) // 2:]
        self.ids['team1_label'].text = 'Team1: ' + ', '.join(team1)
        self.ids['team2_label'].text = 'Team2: ' + ', '.join(team2)

    def select_all_players_action(self):
        checkboxes = self.player_list_layout.children
        for checkbox in checkboxes:
            checkbox.children[1].active = True
        self.ids['count_label'].text = str(len(checkboxes))


class TeamShuffle(App):
    def build(self):
        return MyRoot()


if __name__ == '__main__':
    app = TeamShuffle()
    app.run()
