import datetime
from pathlib import Path
from docxtpl import DocxTemplate
import pandas as pd
import sys
import os
import jinja2

base_dir = Path(__file__).parent
word_template_path = base_dir / "Dummy.docx"
print(word_template_path)
doc = DocxTemplate(word_template_path)
print("Testing Doc : ", doc)
context_dictionary = {}
data = pd.read_excel("Source File.xlsx")
for i in range(len(data.index)):
    values, keys = data.values.tolist()[i], data.columns.tolist()
    for key, value in zip(keys, values):
        context_dictionary[key] = value
        print(key) # , "-> ", value
#print(context_dictionary)

    doc.render(context_dictionary)
    doc_name = "generated_dummy_" + str(i) + ".docx" 
    doc.save(base_dir / doc_name)
    print(doc_name, "-> Rendered!!")