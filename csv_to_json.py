#state 
#dates
#new_cases


import csv
import json

import pandas as pd
us_states = ["Alaska", "Alabama", "Arkansas", "American Samoa", "Arizona", "California", "Colorado", "Connecticut", 
            "District of Columbia", "Delaware", "Florida", "Georgia", "Guam", "Hawaii", "Iowa", "Idaho", "Illinois", 
            "Indiana", "Kansas", "Kentucky", "Louisiana", "Massachusetts", "Maryland", "Maine", "Michigan", "Minnesota",
            "Missouri", "Mississippi", "Montana", "North Carolina", "North Dakota", "Nebraska", "New Hampshire", 
            "New Jersey", "New Mexico", "Nevada", "New York", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Puerto Rico", 
            "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Virginia", "Virgin Islands", 
            "Vermont", "Washington", "Wisconsin", "West Virginia", "Wyoming"]
dates = []
states = []
total_cases = []

url = "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv"
data = pd.read_csv(url)

for index, row in data.iterrows():
    dates.append(row['date'])
    states.append(row['state'])
    total_cases.append(row['cases'])

arr = []
for idx, val in enumerate(us_states):
    state_dict = {"state":val, "dates": [], "total_cases": [], "new_cases": []}
    for i, states_name in enumerate(states):
        if states[i] == val: 
            state_dict["dates"].append(dates[i])
            state_dict["total_cases"].append(total_cases[i])
    for i, case_val in enumerate(state_dict["total_cases"]):
        new_cases = 0
        if i > 0:
            new_cases = state_dict["total_cases"][i] - state_dict["total_cases"][i-1]
        if new_cases < 0:
                new_cases = 0
        state_dict["new_cases"].append(new_cases)

    arr.append(state_dict)


with open('result.json', 'w') as fp:
    json.dump(arr, fp)