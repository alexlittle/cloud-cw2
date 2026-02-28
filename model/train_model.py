import pandas as pd

df = pd.read_csv('synth_traffic_data.csv')

print(df['action'].value_counts())

