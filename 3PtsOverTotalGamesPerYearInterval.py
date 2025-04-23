import time
import pandas as pd
import matplotlib.pyplot as plt
from nba_api.stats.endpoints import LeagueDashTeamStats

def fetch_total_3pta(season: str) -> int:
    time.sleep(0.6)
    stats = LeagueDashTeamStats(
        season=season,
        season_type_all_star='Regular Season',
        per_mode_detailed='Totals'
    )
    df = stats.get_data_frames()[0]
    return int(df['FG3A'].sum())

def fetch_total_games(season: str) -> int:
    time.sleep(0.6)
    stats = LeagueDashTeamStats(
        season=season,
        season_type_all_star='Regular Season',
        per_mode_detailed='Totals'
    )
    df = stats.get_data_frames()[0]
    # GP is counted per team, so divide by 2 to get actual games
    return int(df['GP'].sum()) // 2

def compute_interval_stats(start_year: int, end_year: int, interval_years: int = 5) -> pd.DataFrame:
    seasons = [f"{y}-{str(y+1)[2:]}" for y in range(start_year, end_year + 1)]
    rows = []
    for i in range(0, len(seasons), interval_years):
        group = seasons[i:i + interval_years]
        total_3pta  = sum(fetch_total_3pta(season)  for season in group)
        total_games = sum(fetch_total_games(season) for season in group)
        rows.append({
            'Interval':         f"{int(group[0].split('-')[0])}-{int(group[-1].split('-')[0])}",
            '3PT_per_Game':     total_3pta / total_games
        })
    return pd.DataFrame(rows)

def plot_3pta_per_game(df: pd.DataFrame):
    plt.figure()
    plt.plot(df['Interval'], df['3PT_per_Game'], marker='o')
    plt.title('Average 3-Point Attempts per Game by Interval')
    plt.xlabel('Season Interval')
    plt.ylabel('3PT Attempts per Game')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    df_stats = compute_interval_stats(start_year=1995, end_year=2024, interval_years=3)
    print(df_stats)
    plot_3pta_per_game(df_stats)
