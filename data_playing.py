import pandas as pd

df = pd.read_csv("ufc.csv")
mydf = (df.groupby(['event_name']).count())
print(df)
print(mydf.sort_values(by='fighter_name', ascending=False))
#print(df)
print(df['event_name'][df['event_name'=='UFC Fight Night: Henderson vs Khabilov']])