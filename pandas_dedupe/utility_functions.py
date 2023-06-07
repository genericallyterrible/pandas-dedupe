from unidecode import unidecode
import pandas as pd
import numpy as np
from ast import literal_eval

def trim(x):
    x = x.split()
    x = ' '.join(x)
    return x


def clean_punctuation(df):
    return df.apply(
        lambda series: series.astype(str)
        .str.lower()
        .str.replace(r"[^-\\.,:/()\w\s]", "")
        .apply(lambda x: unidecode(trim(x)))
        .replace({"nan": None, "none": None, "nat": None})
    )

def select_fields(fields, field_properties):
    for i in field_properties:
        if isinstance(i, str):
            fields.append({'field': i, 'type': 'String'})
        elif len(i) == 2:
            fields.append({'field': i[0], 'type': i[1]})
        elif len(i) == 3:
            if i[1] == 'Categorical':
                fields.append({'field': i[0], 'type': i[1], 'categories': i[2]})
            elif i[1] == 'Custom':
                fields.append({'field': i[0], 'type': i[1], 'comparator': i[2]})
            elif i[2] == 'has missing':
                fields.append({'field': i[0], 'type': i[1], 'has missing': True})
            elif i[2] == 'crf':
                fields.append({'field': i[0], 'type': i[1], 'crf': True})
            else:
                raise ValueError("f{i} could not be maapped to field properties")
        else:
            raise ValueError("f{i} could not be maapped to field properties")


def latlong_datatype(x):
    if x is None:
        return None
    else:
        try:
            x = literal_eval(x)
            k,v = x
            k = float(k)
            v = float(v)
            return k, v
        except:
            raise Exception("Make sure that LatLong columns are tuples arranged like ('lat', 'lon')")


def specify_type(df, field_properties):
    for i in field_properties:
        col_name = i[0]
        if i[1] == 'LatLong':
            df[col_name] = df[col_name].apply(lambda x: latlong_datatype(x))
        elif i[1] == 'Price':
            try:
                df[col_name] = df[col_name].str.replace(",","")
                df[col_name] = df[col_name].replace({None: np.nan})
                df[col_name] = df[col_name].astype(float)
                df[col_name] = df[col_name].replace({np.nan: None})
            except:
                raise Exception('Make sure that Price columns can be converted to float.')

