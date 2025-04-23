import time
import pandas as pd
import matplotlib.pyplot as plt
from nba_api.stats.endpoints import LeagueDashTeamStats

def fetch_total_3pta(season: str) -> int:
    """
    Fetches the total number of 3-point attempts across all teams for a given NBA season.
    
    Args:
        season: Season in 'YYYY-YY' format, e.g., '1979-80'.
        
    Returns:
        Sum of FG3A (3-point attempts) for the entire league that season.
    """
    # be polite with the API
    time.sleep(0.6)
    stats = LeagueDashTeamStats(
        season=season,
        season_type_all_star='Regular Season',
        per_mode_detailed='Totals'    # <-- changed this line
    )
    df = stats.get_data_frames()[0]
    return int(df['FG3A'].sum())


def compute_3pta_intervals(start_year: int, end_year: int, interval_years: int = 5) -> pd.DataFrame:
    """
    Computes total 3-point attempts in year intervals.
    
    Args:
        start_year: First season start year (e.g., 1970 for 1970-71).
        end_year: Last season start year (e.g., 2023 for 2023-24).
        interval_years: Size of each interval in years.
        
    Returns:
        DataFrame with columns ['Interval', 'Total_3PT_Attempts'].
    """
    # Build list of seasons
    seasons = [f"{y}-{str(y+1)[2:]}" for y in range(start_year, end_year + 1)]
    
    results = []
    for i in range(0, len(seasons), interval_years):
        group = seasons[i:i + interval_years]
        total = sum(fetch_total_3pta(season) for season in group)
        start = int(group[0].split('-')[0])
        end = int(group[-1].split('-')[0])
        results.append({
            'Interval': f"{start}-{end}",
            'Total_3PT_Attempts': total
        })
        
    return pd.DataFrame(results)

def plot_3pta(df: pd.DataFrame):
    """
    Plots total 3-point attempts by interval.
    """
    plt.figure()
    plt.plot(df['Interval'], df['Total_3PT_Attempts'])
    plt.title('Total 3PT Attempts by NBA Season Intervals')
    plt.xlabel('Season Interval')
    plt.ylabel('Total 3PT Attempts')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    # Adjust interval_years between 5 and 10 as desired
    df_intervals = compute_3pta_intervals(start_year=1995, end_year=2024, interval_years=3)
    print(df_intervals)
    plot_3pta(df_intervals)