def readData(teams, games):
    with open(teams) as teams_file, open(games) as games_file:
        # Each row read from the csv file is returned as a list of strings
        teams_dataset = list(csv.reader(teams_file,delimiter=','))
        games_dataset = list(csv.reader(games_file, delimiter=','))
        print 'outputinng'
        for team in teams_dataset:
            print team
        for game in games dataset:
            print games 