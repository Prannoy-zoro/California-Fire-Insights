import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

df = pd.read_csv("California_Historic_Fire_Perimeters_3836453159319713276.csv")
df.info()
print(df.isnull().sum())
df.head()
df["Alarm Date"] = pd.to_datetime(df["Alarm Date"], errors="coerce")
df["Containment Date"] = pd.to_datetime(df["Containment Date"], errors="coerce")
df["Local Incident Number"] = pd.to_numeric(df["Local Incident Number"], errors="coerce")
df.to_csv("clean_data.csv")
