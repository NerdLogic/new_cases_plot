# Created by: Era Iyer
# June 2020
#
# program purposes: determines appropriate color representation based on data 
#                   regarding daily new coronavirus cases  
#
# winning = green
# nearly there = orange
# needs action = red
#
# methods to determine color representation:
#   1. green --> current average < 10 OR current average < 20  and current avrage < 0.5*peak
#   2. orange --> current average < 1.5*20 and current average < peak*0.5 
#                 OR current average < peak*0.2
#   3. red --> all other cases 

import json
import csv
import pandas as pd

#parallel arrays to store json information 
province = []
values = []
countries = []
setColors = []
allWeekValues = []
peakCases = []
all_moving_averages = []
F0 = 0.5
F1 = 0.2
N0 = 20

colors = ["green", "orange", "red"]
daysToAverage = 7

with open('./result.json') as f:
    data = json.load(f)
    for i in data:
        #filling parallel arrays with province, values, country 
        province.append(i['state'])
        values.append(i['new_cases'])
        all_moving_averages.append(i['avg_cases'])

#another parallel array that stores each province's max number of cases 
for i in range(len(all_moving_averages)):
    
    max = 0
    for j in range(len(all_moving_averages[i])):
        if(all_moving_averages[i][j]>max):
            max = all_moving_averages[i][j]
    peakCases.append(max)

#simplifies values array to hold just values from the past week (per province/state)
for k in range(len(values)):
    #gets values from last 7 days 
    start = len(values[k])-daysToAverage
    end = len(values[k])
    stateWeekVals = []
    if(start < 0): #edge case, if data has less than 7 values
        start = 0

    for i in range(start, end):
        stateWeekVals.append(values[k][i])
    #array of array of new cases per week per state
    allWeekValues.append(stateWeekVals)


for i in range(len(allWeekValues)):
    sum = 0
    for k in range(len(allWeekValues[i])):
        sum += allWeekValues[i][k]
    average = sum/daysToAverage

    if((average < (N0 * F0)) or ((average < N0) and (average < (peakCases[i]*F0)))):
        setColors.append(colors[0])
    elif(((average < (1.5*N0)) and (average < (peakCases[i]*F0))) or (average < (peakCases[i]*F1))):
         setColors.append(colors[1])
    else: 
         setColors.append(colors[2])


with open('USStateColors.csv', 'wb') as file:
    fieldnames = ['state', 'color']
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    for i in range(len(province)):
        writer.writerow({'state': province[i], 'color': setColors[i]})
