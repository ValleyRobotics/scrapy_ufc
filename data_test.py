#import pandas as pd


#df = pd.read_csv('ufc.csv')
f = open('ufc.csv','r')
#f.readlines()
for i, line in enumerate(f):
    if len(line) < 500:
        print(line)
        print(i, len(line))
print(f)

#df.head()