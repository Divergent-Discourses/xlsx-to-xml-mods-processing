import pandas as pd
import xml.etree.ElementTree as ET
import xml.dom.minidom
from tqdm import tqdm
import os

def clean_data(df):
    df.fillna('', inplace=True)
    return df

def row_to_xml(row):
    record = ET.Element("Record")
    for col in row.index:
        child = ET.SubElement(record, col.replace(" ", "_"))  # Replace spaces in column names
        child.text = str(row[col])
    return record

def save_xml(data, filename):
    try:
        xml_bytes = ET.tostring(data)
        with open(filename, "wb") as file:
            file.write(xml_bytes)
    except Exception as e:
        print(f"Failed to save XML to {filename}: {e}")

def escape_special_chars(val):
    if isinstance(val, str):
        return val.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;").replace("'", "&apos;")
    return val

def sanitize_xml_element_name(name):
    return name.replace(" ", "_").replace("(", "").replace(")", "")

def sanitize_column_name(col_name):
    sanitized = col_name.replace('/', '_').replace(' ', '_')
    if sanitized[0].isdigit():
        sanitized = '_' + sanitized
    return sanitized

def process_excel(fname):
    df = pd.read_excel(fname)
    df = clean_data(df)
    df = df.applymap(escape_special_chars)
    df.columns = [sanitize_xml_element_name(col) for col in df.columns]
    df.columns = [sanitize_column_name(col) for col in df.columns]
    for index, row in tqdm(df.iterrows()):
        xml_data = row_to_xml(row)
        try:
            filename = f'xml_records/{row["DIVERGE_Code"]}.xml'
            save_xml(xml_data, filename)
        except:
            os.mkdir('xml_records')
            filename = f'xml_records/{row["DIVERGE_Code"]}.xml'
            save_xml(xml_data, filename)

if __name__ == "__main__":
    fname = input('input filepath: ')
    process_excel(fname)
    
    
