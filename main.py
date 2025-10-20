from nba_api.stats.endpoints import playercareerstats
from nba_api.stats.endpoints import playergamelog as PGL
from nba_api.stats.static import players
import pandas as pd
import matplotlib.pyplot as plt


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
    

def plotGraph(amt, Player):
    plter = Player.to_df_int(amt)

    plter['GAME_DATE'] = pd.to_datetime(plter['GAME_DATE'])

    plt.figure(figsize=(12, 6))

    for x in plter['GAME_DATE']:
        plt.axvline(x=x, color='gray', linestyle='--', linewidth=0.7, alpha=0.4)

    for stat, marker in zip(['PTS', 'REB', 'AST'], ['o', 's', '^']):
        plt.plot(plter['GAME_DATE'], plter[stat], marker=marker, label=stat)
        for i, value in enumerate(plter[stat]):
            plt.text(plter['GAME_DATE'].iloc[i], value + 0.5, f"{value:.0f}", 
                    ha='center', va='bottom', fontsize=8)
    
    plt.gcf().autofmt_xdate()
    
    plt.legend(loc='upper right')
    plt.xlabel("Date ")
    plt.tight_layout()
    plt.show()

giannis = Player("Giannis Antetokounmpo")
plotGraph(10,giannis)