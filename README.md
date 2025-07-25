# SofaScore API Stats

A Python application that fetches comprehensive football statistics from the SofaScore API for various tournaments and teams. The application collects detailed match statistics and exports them to JSON files for analysis.

## Features

- 🏆 **Multiple Tournament Support**: Champions League, Europa League, Premier League, Bundesliga, La Liga, Serie A, Championship, and Brasileirão
- 📊 **Comprehensive Statistics**: Collects 37+ different match statistics including shots, passes, possession, defensive actions, and more
- 🎯 **Team-Specific Data**: Generates individual JSON files for each team containing all their match statistics
- ⚙️ **Customizable**: Easy to configure which statistics to collect via the `options.py` file
- 🔄 **Automated Processing**: Processes all teams in a tournament automatically

## Installation

1. **Clone the repository**:
```bash
git clone https://github.com/victorstdev/sofascore-api-stats.git
cd sofascore-api-stats
```

2. **Create a virtual environment** (recommended):
```bash
python -m venv venv
```

3. **Activate the virtual environment**:
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`

4. **Install dependencies**:
```bash
pip install -r requirements.txt
```

## Usage

Simply run the main script:

```bash
python main.py
```

The application will:
1. Display a menu to choose from available tournaments
2. Fetch the latest season data for the selected tournament
3. Get all teams in the tournament
4. Process each team's matches and collect statistics
5. Save the data as JSON files in a folder named after the tournament

## Supported Tournaments

- **Champions League** (ID: 1462)
- **Europa League** (ID: 10908)
- **Premier League** (ID: 1)
- **Bundesliga** (ID: 42)
- **Brasileirão** (ID: 83)
- **La Liga** (ID: 36)
- **Serie A Tim** (ID: 33)
- **Championship** (ID: 2)

## Statistics Collected

The application collects statistics across 8 different categories:

### Expected Goals
- Expected goals

### Possession
- Ball possession

### Shots
- Total shots, Shots on target, Shots off target, Blocked shots

### Match Events (TVData)
- Corner kicks, Offsides, Fouls, Red cards, Free kicks, Throw-ins, Goal kicks

### Advanced Shooting
- Big chances, Big chances missed, Counter attacks, Counter attack shots
- Shots inside box, Shots outside box, Goalkeeper saves, Goals prevented

### Passing
- Passes, Accurate passes, Long balls, Crosses

### Duels
- Dribbles, Possession lost, Duels won, Aerials won

### Defending
- Tackles, Interceptions, Clearances

## Configuration

### Customizing Statistics

Edit the `options.py` file to customize which statistics are collected:

```python
# Select which statistic groups to include
groups = ['Expected', 'Shots', 'TVData', 'Passes']

# Select specific statistics to collect
statisticsItems = [
    'Expected goals',
    'Shots on target',
    'Corner kicks',
    # ... add more as needed
]
```

### Adding New Tournaments

Add new tournaments to `tournaments.py`:

```python
tournaments = [
    {"name": "Your Tournament", "id": tournament_id},
    # ... existing tournaments
]
```

## Output Format

Each team gets a JSON file with the following structure:

```json
[
  {
    "id": 12345,
    "tournament": "Premier League",
    "day": "2024-01-15",
    "homeTeam": "Arsenal",
    "homeScore": 2,
    "awayTeam": "Chelsea", 
    "awayScore": 1,
    "statistics": [
      {
        "name": "Expected goals",
        "home": "1.8",
        "away": "0.9"
      },
      // ... more statistics
    ]
  }
  // ... more matches
]
```

## File Structure

```
sofascore-api-stats/
├── main.py              # Main application entry point
├── controller.py        # API handling and data processing
├── tournaments.py       # Tournament definitions
├── options.py          # Configuration for statistics collection
├── menu.py             # User interface for tournament selection
├── requirements.txt    # Python dependencies
├── README.md          # This file
└── [Tournament Name]/  # Generated folders with team JSON files
    ├── Team1.json
    ├── Team2.json
    └── ...
```

## Dependencies

- **requests**: HTTP library for API calls
- **Standard libraries**: json, datetime, os, time

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Create a Pull Request

## License

This project is open source and available under the [MIT License](LICENSE).

## Disclaimer

This project is for educational and research purposes. Please respect SofaScore's terms of service and API rate limits when using this application.

## Troubleshooting

### Empty JSON Files
- Check that the tournament has completed matches
- Verify that the statistics exist for the selected matches
- Ensure your internet connection is stable

### API Errors
- The application includes error handling for failed API requests
- Check the console output for specific error messages
- Try running the script again after a few minutes

### Missing Statistics
- Some matches may not have all statistics available
- The application will collect whatever statistics are available
- Check the `options.py` file to ensure you're requesting valid statistics