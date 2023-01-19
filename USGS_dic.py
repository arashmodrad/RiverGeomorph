
import pandas as pd
  
# Read text file into Json
df = pd.read_csv("HUC_names.csv", sep=",",
on_bad_lines='skip')
df.to_json("HUC8_names.json", orient="split")
print(df.head(20))
print("\n------------------------\n")
print(df.tail(20))