import pandas as pd
import numpy as np
import random
import csv
df = pd.DataFrame.from_csv('C:/Users/luca.chech.16/Desktop/jupyter exp/all_images.csv')
#f = pd.DataFrame.from_csv('C:/Users/nilli lab/Desktop/Luca Exp/jupyter exp/all_images.csv')
df.reset_index(drop=False)

image_names = df.index.tolist()
cat1 = df['0'].tolist()
cat2 = df['1'].tolist()
cat3 = df['2'].tolist()
cat4 = df['3'].tolist()
cat5 = df['4'].tolist()
ts = df['5'].tolist()
load = df['6'].tolist()
possible_images_dict ={z[0]:list(z[1:]) for z in zip(image_names,cat1,cat2,cat3,cat4,cat5,ts,load)}

# DEFINING TARGET-PRESENT TRIALS
lista= possible_images_dict.keys()
target_present = []
intermediate = []
categories = [' bottle', ' horse', ' pottedplant', ' dog', ' cat', ' person', ' aeroplane', ' car', ' chair', ' sofa', ' bird', ' boat']
p_load = ['low','high']

for each_1 in categories:
    for load in p_load:
        i = 0
        while True:
            trial = np.random.choice(lista, 1, replace= False)
            a = str(trial)
            a =a[2:-2]
            if each_1 in possible_images_dict[a] and load in possible_images_dict[a] and a not in intermediate and a not in target_present:
                intermediate.append(a)
            if len(intermediate) == 10:
                for each in intermediate:
                    target_present.append(each)
                    possible_images_dict[each].append(each_1)
                intermediate = []
                break

print len(target_present)
#--------------------
target_present_dict = {key:possible_images_dict[key] for key in target_present}
target_absent_dict = dict(possible_images_dict)
for each in target_present:
    if each in target_absent_dict:
        del target_absent_dict[each]
exp_dict = dict(target_present_dict)
exp_dict.update(target_absent_dict)
print len(target_present_dict)
print len(target_absent_dict)
print len(exp_dict)


for each in target_present_dict:
    target_present_dict[each].append('Target Present')
for each in target_absent_dict:
    absent_question = []
    for ogni in categories:
        if ogni not in target_absent_dict[each]:
            absent_question.append(ogni)
    absent_question = np.random.choice(absent_question, 1, replace= False)
    absent_question = str(absent_question)
    absent_question = absent_question[2:-2]
    #print absent_question
    #print type(absent_question)
    target_absent_dict[each].append(absent_question)
    target_absent_dict[each].append('Target Absent')
    
# DEFINING CRITICAL TRIALS
critical_trials = []
def critical_trial(load_level, present_absent):
    intermediate = []
    for element in lista:
        if load_level in possible_images_dict[element] and present_absent in possible_images_dict[element]:
            intermediate.append(element)  
    intermediate = np.random.choice(intermediate, 20, replace= False)
    for each in intermediate:
        each = str(each)
        critical_trials.append(each)
critical_trial('low','Target Present')
critical_trial('high','Target Present')
critical_trial('low','Target Absent')
critical_trial('high','Target Absent')

for each in critical_trials:
    exp_dict[each].append('Critical')
for each in exp_dict:
    if 'Critical' not in exp_dict[each]:
        exp_dict[each].append('Normal')
#-----------------------

df = pd.DataFrame.from_dict(exp_dict)
df= df.T
#df.reset_index(inplace = 'True')
df.columns = ['Cat.1','Cat.2','Cat.3','Cat.4','Cat.5','TS','Load','question','present_absent','trial_type']
df.TS = df.TS.astype('float')
df.to_csv('randomization.csv')
