import json
import pandas as pd
import os
from datetime import datetime
import glob

def load_team_data(folder_path):
    """
    Load all JSON files from the specified folder and return a list of all matches
    """
    all_matches = []
    
    # Get all JSON files in the folder
    json_files = glob.glob(os.path.join(folder_path, "*.json"))
    
    for json_file in json_files:
        team_name = os.path.splitext(os.path.basename(json_file))[0]
        
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                team_data = json.load(f)
                
            # Add team name to each match record
            for match in team_data:
                match['team'] = team_name
                all_matches.append(match)
                
        except Exception as e:
            print(f"Error reading {json_file}: {str(e)}")
    
    return all_matches

def flatten_statistics(match_data):
    """
    Convert match statistics from nested format to flat columns
    """
    flattened = {
        'team': match_data.get('team', ''),
        'match_id': match_data.get('id', ''),
        'tournament': match_data.get('tournament', ''),
        'date': match_data.get('day', ''),
        'home_team': match_data.get('homeTeam', ''),
        'away_team': match_data.get('awayTeam', ''),
        'home_score': match_data.get('homeScore', ''),
        'away_score': match_data.get('awayScore', ''),
        'is_home': match_data.get('homeTeam', '') == match_data.get('team', ''),
        'opponent': match_data.get('awayTeam', '') if match_data.get('homeTeam', '') == match_data.get('team', '') else match_data.get('homeTeam', ''),
        'goals_for': match_data.get('homeScore', '') if match_data.get('homeTeam', '') == match_data.get('team', '') else match_data.get('awayScore', ''),
        'goals_against': match_data.get('awayScore', '') if match_data.get('homeTeam', '') == match_data.get('team', '') else match_data.get('homeScore', ''),
    }
    
    # Add result
    try:
        goals_for = int(flattened['goals_for'])
        goals_against = int(flattened['goals_against'])
        if goals_for > goals_against:
            flattened['result'] = 'Win'
        elif goals_for < goals_against:
            flattened['result'] = 'Loss'
        else:
            flattened['result'] = 'Draw'
    except:
        flattened['result'] = 'Unknown'
    
    # Flatten statistics
    statistics = match_data.get('statistics', [])
    for stat in statistics:
        stat_name = stat.get('name', '').replace(' ', '_').lower()
        
        # Get team's value (home or away based on team position)
        if flattened['is_home']:
            team_value = stat.get('home', '')
            opponent_value = stat.get('away', '')
        else:
            team_value = stat.get('away', '')
            opponent_value = stat.get('home', '')
        
        flattened[f'{stat_name}_team'] = team_value
        flattened[f'{stat_name}_opponent'] = opponent_value
    
    return flattened

def create_excel_file(folder_path, output_filename=None):
    """
    Convert all JSON files in folder to Excel file
    """
    if not os.path.exists(folder_path):
        print(f"Error: Folder '{folder_path}' does not exist")
        return False
    
    # Load all match data
    print(f"Loading data from {folder_path}...")
    all_matches = load_team_data(folder_path)
    
    if not all_matches:
        print("No match data found!")
        return False
    
    print(f"Found {len(all_matches)} matches total")
    
    # Flatten all matches
    flattened_matches = []
    for match in all_matches:
        flattened_match = flatten_statistics(match)
        flattened_matches.append(flattened_match)
    
    # Create DataFrame
    df = pd.DataFrame(flattened_matches)
    
    # Sort by team and date
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values(['team', 'date'])
    
    # Generate output filename if not provided
    if not output_filename:
        folder_name = os.path.basename(folder_path)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_filename = f"{folder_name}_stats_{timestamp}.xlsx"
    
    # Create Excel file with multiple sheets
    with pd.ExcelWriter(output_filename, engine='openpyxl') as writer:
        # All matches sheet
        df.to_excel(writer, sheet_name='All Matches', index=False)
        
        # Summary sheet by team
        summary_df = create_team_summary(df)
        summary_df.to_excel(writer, sheet_name='Team Summary', index=False)
        
        # Individual team sheets
        teams = df['team'].unique()
        for team in teams:
            team_df = df[df['team'] == team].copy()
            # Clean sheet name (Excel has restrictions)
            clean_team_name = team.replace('/', '_').replace('\\', '_')[:31]
            team_df.to_excel(writer, sheet_name=clean_team_name, index=False)
    
    print(f"Excel file created: {output_filename}")
    print(f"Sheets created:")
    print(f"  - All Matches ({len(df)} matches)")
    print(f"  - Team Summary ({len(teams)} teams)")
    for team in teams:
        matches_count = len(df[df['team'] == team])
        print(f"  - {team} ({matches_count} matches)")
    
    return True

def create_team_summary(df):
    """
    Create a summary DataFrame with team statistics
    """
    summary_data = []
    
    for team in df['team'].unique():
        team_df = df[df['team'] == team]
        
        # Basic stats
        matches = len(team_df)
        wins = len(team_df[team_df['result'] == 'Win'])
        draws = len(team_df[team_df['result'] == 'Draw'])
        losses = len(team_df[team_df['result'] == 'Loss'])
        
        try:
            goals_for = team_df['goals_for'].astype(int).sum()
            goals_against = team_df['goals_against'].astype(int).sum()
            goal_difference = goals_for - goals_against
        except:
            goals_for = goals_against = goal_difference = 0
        
        points = wins * 3 + draws
        
        summary = {
            'team': team,
            'matches': matches,
            'wins': wins,
            'draws': draws,
            'losses': losses,
            'goals_for': goals_for,
            'goals_against': goals_against,
            'goal_difference': goal_difference,
            'points': points
        }
        
        # Add average statistics if available
        numeric_columns = team_df.select_dtypes(include=['number']).columns
        for col in numeric_columns:
            if col.endswith('_team') and col not in ['goals_for', 'goals_against']:
                avg_value = team_df[col].mean()
                summary[f'avg_{col}'] = round(avg_value, 2)
        
        summary_data.append(summary)
    
    summary_df = pd.DataFrame(summary_data)
    summary_df = summary_df.sort_values('points', ascending=False)
    
    return summary_df

def main():
    """
    Main function to run the conversion
    """
    # Default folder path
    folder_path = "Premier League"
    
    # Check if folder exists
    if not os.path.exists(folder_path):
        print(f"Premier League folder not found. Please make sure the folder exists.")
        print("Available folders:")
        for item in os.listdir('.'):
            if os.path.isdir(item):
                print(f"  - {item}")
        return
    
    # Create Excel file
    success = create_excel_file(folder_path)
    
    if success:
        print("\nConversion completed successfully!")
    else:
        print("\nConversion failed!")

if __name__ == "__main__":
    main()
