# Import necessary libraries and modules
import random
import tkinter as tk
from tkinter.simpledialog import askstring

# Define a class representing a player
class Player:
    def __init__(self, name, team, points=0):
        self.name = name
        self.team = team
        self.points = points

# Define a class representing a fantasy team
class FantasyTeam:
    def __init__(self):
        self.players = []

    # Method to add a player to the fantasy team
    def add_player(self, player):
        if len(self.players) < 11:
            self.players.append(player)

    # Method to remove a player from the fantasy team
    def remove_player(self, player):
        self.players.remove(player)

    # Method to calculate the total points of the fantasy team
    def calculate_points(self):
        total_points = sum(player.points for player in self.players)
        return total_points

# Define the main application class
class intern:
    def __init__(self, root):
        self.root = root
        self.root.title("Cricket Fantasy League")
        # Initialize sample players and an instance of the FantasyTeam class
        self.players = self.generate_sample_players()
        self.fantasy_team = FantasyTeam()

        # Create Listboxes for player and team display
        self.player_listbox = tk.Listbox(root, selectmode=tk.SINGLE, width=50, height=15)
        self.player_listbox.pack(side=tk.LEFT, pady=10)

        # Create Calculate Points button
        self.calculate_button = tk.Button(root, text="Calculate Points", command=self.calculate_points)
        self.calculate_button.pack(pady=10)
        self.calculate_button["state"] = "disabled"  # Disable the Calculate Points button initially

        # Create Listbox for displaying selected team
        self.team_listbox = tk.Listbox(root, selectmode=tk.SINGLE, width=50, height=15)
        self.team_listbox.pack(side=tk.RIGHT, pady=10)

        # Create Save Team button
        self.save_button = tk.Button(root, text="Save Team", command=self.save_team)
        self.save_button.pack(pady=10)
        self.save_button["state"] = "disabled"  # Disable the Save Team button initially

        # Initialize variables to track state
        self.prompt_shown = False  # Variable to track if the prompt has been shown
        self.saved_team = False  # Variable to track if the team has been saved

        # Bind double-click events to add or remove players
        self.player_listbox.bind("<Double-1>", self.add_remove_player)
        self.team_listbox.bind("<Double-1>", self.add_remove_player)

        # Populate listboxes
        self.populate_player_listbox()
        self.populate_team_listbox()

    # Method to generate sample players for teams A and B
    def generate_sample_players(self):
        team_a_players = ["Ruturaj Gaikwad", "Ambati Rayudu", "Faf du Plessis", "Deepak Chahar", "Matheesha Pathirana",
                          "Josh Hazlewood", "Moeen Ali", "Virat Kohli", "Mahipal Lomror", "Finn Allen", "Glenn Maxwell"]
        team_b_players = ["Suyash Prabhudessai", "Tushar Deshpande", "Mukesh Chowdhary", "Siddharth Kaul", "Akash Deep",
                          "Karn Sharma", "Shivam Dube", "Anuj Rawat", "Dinesh Karthik", "DJ Bravo", "MS Dhoni"]
        return [Player(name, "Team A", random.randint(10, 100)) for name in team_a_players] + [
            Player(name, "Team B", random.randint(10, 100)) for name in team_b_players]

    # Method to populate the player listbox
    def populate_player_listbox(self):
        self.player_listbox.delete(0, tk.END)
        for player in self.players:
            self.player_listbox.insert(tk.END, f"{player.name} - {player.team} - Points: {player.points}")

    # Method to add or remove a player on double-click
    def add_remove_player(self, event):
        selected_index = None
        if event.widget == self.player_listbox:
            selected_index = self.player_listbox.curselection()
        elif event.widget == self.team_listbox:
            selected_index = self.team_listbox.curselection()

        if selected_index:
            selected_player = self.players[selected_index[0]] if event.widget == self.player_listbox else \
                self.fantasy_team.players[selected_index[0]]

        if self.saved_team:
            return  # If the team is saved, do not allow modifications
        if event.widget == self.player_listbox:
            if len(self.fantasy_team.players) < 11:
                self.fantasy_team.add_player(selected_player)
                self.players.remove(selected_player)
                self.team_listbox.insert(tk.END,
                                         f"{selected_player.name} -{selected_player.team} - Points: {selected_player.points}")
                self.player_listbox.delete(selected_index)
                if len(self.fantasy_team.players) == 11:
                    self.show_team_name_prompt()
        elif event.widget == self.team_listbox:
            self.fantasy_team.remove_player(selected_player)
            self.players.append(selected_player)
            self.player_listbox.insert(tk.END,
                                       f"{selected_player.name} -{selected_player.team} - Points: {selected_player.points}")
            self.team_listbox.delete(selected_index)
        if len(self.fantasy_team.players) == 11:
            self.calculate_button["state"] = "normal"
            self.save_button["state"] = "normal"
        else:
            self.calculate_button["state"] = "disabled"
            self.save_button["state"] = "disabled"
            self.populate_player_listbox()
            self.populate_team_listbox()

    # Method to show the team name prompt after selecting 11 players
    def show_team_name_prompt(self):
        team_name = askstring("Team Name", "Enter your team name:")
        if team_name:
            self.fantasy_team.name = team_name
            self.show_info_dialog(f"Team '{self.fantasy_team.name}' saved successfully!")
            self.saved_team = True
            self.prompt_shown = True
            self.calculate_button["state"] = "disabled"  # Disable Calculate Points button after saving
            self.save_button["state"] = "disabled"  # Disable Save Team button after saving
        else:
            self.show_warning_dialog("Please enter a team name.")

    # Method to save the team
    def save_team(self):
        if len(self.fantasy_team.players) == 11:
            team_name = askstring("Team Name", "Enter your team name:")
            if team_name:
                self.fantasy_team.name = team_name
                self.show_info_dialog(f"Team '{self.fantasy_team.name}' saved successfully!")
                self.saved_team = True  # Set the saved_team flag to True
                self.prompt_shown = True
                self.calculate_button["state"] = "normal"  # Enable Calculate Points button after saving
                self.save_button["state"] = "disabled"  # Disable Save Team button after saving
            else:
                self.show_warning_dialog("Please enter a team name.")
        else:
            self.show_warning_dialog("Please select exactly 11 players before saving the team.")

    # Method to calculate points for the saved team
    def calculate_points(self):
        if self.saved_team:
            total_points = self.fantasy_team.calculate_points()
            self.show_info_dialog(f"Total points for {self.fantasy_team.name}: {total_points}")
        else:
            self.show_warning_dialog("Please save your team before calculating points.")

    # Method to populate the team listbox
    def populate_team_listbox(self):
        self.team_listbox.delete(0, tk.END)
        for player in self.fantasy_team.players:
            self.team_listbox.insert(tk.END, f"{player.name} - {player.team} - Points: {player.points}")

    # Method to display an information dialog
    def show_info_dialog(self, message):
        dialog = tk.Toplevel(self.root)
        dialog.title("Information")
        label = tk.Label(dialog, text=message, width=70, height=10)
        label.pack(padx=20, pady=20)

    # Method to display a warning dialog
    def show_warning_dialog(self, message):
        dialog = tk.Toplevel(self.root)
        dialog.title("Warning")
        label = tk.Label(dialog, text=message, width=70, height=10)
        label.pack(padx=20, pady=20)

# Define the main function to run the application
def main():
    root = tk.Tk()
    app = intern(root)
    root.mainloop()

# Check if the script is being run as the main program
if __name__ == "__main__":
    main()
