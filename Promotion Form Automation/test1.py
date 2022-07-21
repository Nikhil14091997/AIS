import datetime
from pathlib import Path
from docxtpl import DocxTemplate
import pandas as pd
import sys
import os
import jinja2

base_dir = Path(__file__).parent
print(base_dir)
word_template_path = base_dir / "dummy.docx"
print(word_template_path)
context_dictionary = {}

data = pd.read_excel("Test_Source.xlsx")
for i in range(len(data.index)):
    values, keys = data.values.tolist()[i], data.columns.tolist()
    for key, value in zip(keys, values):
        context_dictionary[key] = value
        print(key, "-> ", value)
print("\n ------------------------------------------------")

# doc1.render(context_dictionary)
# doc1.save(base_dir / "generated_test2.docx")