import tournaments as t
import controller as c
import menu as m
import options as o
import time

start = time.time()

tournament = m.choose_option(t.tournaments)
season = c.get_last_season(tournament)
teams = c.get_standings(tournament, season)

for team in teams:
  print(f"\nProcessing team: {team['name']}")
  events = c.get_events(tournament, season, team)
  print(f"Events found: {len(events) if events else 0}")
  
  if events:
    statistics = c.get_statistics(events)
    print(f"Statistics processed for {len(statistics)} events")
    file = c.create_file(tournament, team, statistics)
  else:
    print(f"No events found for {team['name']}, skipping...")
    # Create empty file to indicate the team was processed
    c.create_file(tournament, team, [])

end = time.time()
duration = (end - start) / 60
print(f'Total execution time: {duration:.2f} m')
time.sleep(3)