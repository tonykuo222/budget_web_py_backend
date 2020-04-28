from loader import *
from constants import ColumnSets
import json
import pandas as pd

def getLineData():
    df = load_excel_file(ColumnSets.BUDGET_ALL)
    datasets = []
    series = df.columns
    series = series.delete(series.get_loc("Date"))
    for i in range(0, len(series)):
        datasets.append([])
    for index, row in df.iterrows():
        count = 0
        for header in series:
            datasets[count].append({
                'x': row["Date"],
                'y': row[header]
            })
            count += 1

    return json.dumps(datasets, default=dateConverter)

def dateConverter(date):
    if isinstance(date, pd.Timestamp):
        return date.strftime('%Y-%m-%d')