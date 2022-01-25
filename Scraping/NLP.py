# from transformers import pipeline
import pandas as pd
from MainScript import dataHuggingFace
df = pd.DataFrame.from_dict(dataHuggingFace)
print(df)
