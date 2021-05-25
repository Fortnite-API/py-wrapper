## How To Get Data Using Raw Data

#### Example 1: Stats

```
  # Import API
  import fortnite_api
  api = fortnite_api.FortniteAPI()
  
  # Get Stats For A User
  stats = api.stats.fetch_by_name('Ship').stats
  
  # Getting Raw Data
  data = stats.raw_data
  
  # Filter Data
  data = data['all']
  data = data['overall']
  wins = data['wins'] # This Be Wins, Kills, Top5 etc..

```
#### Example 2: Battle Pass

```
  # Import API
  import fortnite_api
  api = fortnite_api.FortniteAPI()
  
  # Get Stats For A User
  stats = api.stats.fetch_by_name('Ship').battle_pass
  
  # Get Raw Data
  data = stats.raw_data
  level = data['level']
  progress = data['progress']
```
