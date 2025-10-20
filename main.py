from nba_api.stats.endpoints import playergamelog as PGL
from nba_api.stats.endpoints import playercareerstats
from nba_api.stats.static import players
import pandas as pd
import matplotlib.pyplot as plt
import tkinter as tk
import threading


class Player:
    def __init__(self, playerName):
        self.playerName = playerName 
        self.player_id = (players.find_players_by_full_name(playerName))[0]['id']
        self.gameLog = PGL.PlayerGameLog(self.player_id, season='2024-25')



    def displayStats(self):
        df = self.gameLog.get_data_frames()[0]
        averages = df[['PTS','REB', 'AST']].mean()
        print(averages)

    def to_df(self):
        return self.gameLog.get_data_frames()[0]
    
    def to_df_int(self, amt):
        return (self.gameLog.get_data_frames()[0]).head(amt).iloc[::-1]
    
    def getGamesPlayedThisSeason(self):
        # Fetch the game log data
        df = self.gameLog.get_data_frames()[0]
        
        # The number of unique game dates gives us the number of games played
        num_games = df['GAME_DATE'].nunique()
        return int(num_games)

# Show Player Averages
def showAverages(Player, amt):

    playerData = Player.to_df_int(amt)
    
    # Draw Window
    window = tk.Tk()
    window.title(f'{Player.playerName} Averages')
    window.geometry("300x200+1300+200")

    # Points
    label_pts = tk.Label(window, text=f"Points: {playerData["PTS"].mean():.1f}", font=("Arial", 12))
    label_pts.pack(pady=1)

    # Rebounds
    label_pts = tk.Label(window, text=f"Rebounds: {playerData["REB"].mean():.1f}", font=("Arial", 12))
    label_pts.pack(pady=1)

    # Assists
    label_pts = tk.Label(window, text=f"Assists: {playerData["AST"].mean():.1f}", font=("Arial", 12))
    label_pts.pack(pady=1)

    window.mainloop()


# Plot the graph
def plotGraph(Player, amt):
    playerData = Player.to_df_int(amt)

    playerData['GAME_DATE'] = pd.to_datetime(playerData['GAME_DATE'])

    plt.figure(figsize=(12, 6))

    for x in playerData['GAME_DATE']:
        plt.axvline(x=x, color='gray', linestyle='--', linewidth=0.7, alpha=0.4)

    for stat, marker in zip(['PTS', 'REB', 'AST'], ['o', 's', '^']):
        plt.plot(playerData['GAME_DATE'], playerData[stat], marker=marker, label=stat)
        for i, value in enumerate(playerData[stat]):
            plt.text(playerData['GAME_DATE'].iloc[i], value + 0.5, f"{value:.0f}", 
                    ha='center', va='bottom', fontsize=8)
    

    plt.gcf().autofmt_xdate()
    
    plt.legend(loc='best')
    plt.xlabel("Date ")
    plt.tight_layout()
    plt.get_current_fig_manager().window.geometry("+100+200")
    plt.show()

def main(playerName, amt):
    lebron = Player(playerName)
    
    # Run the plotGraph function in a separate thread
    averages_thread = threading.Thread(target=showAverages, args=(lebron, amt))
    averages_thread.start()

    # Run the showAverages function in the main thread (since Tkinter requires it)
    plotGraph(lebron, amt)

# Example Usage
main("Lebron James", 10)
                  
