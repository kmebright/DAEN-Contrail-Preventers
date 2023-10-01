import os
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from datetime import datetime

def make_preds(igra, skyimage, features):
    rh = []
    temp = []
    press = []
    igra['datetime'] = igra['DATE'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d'))
    igra['YEAR'] = igra['datetime'].apply(lambda x: x.year)
    igra['MONTH'] = igra['datetime'].apply(lambda x: x.month)
    igra['DAY'] = igra['datetime'].apply(lambda x: x.day)
    for date in skyimage['file_name'].values:
        date_use = datetime.strptime(date.strip('.jpg').lstrip('IMG_'), '%Y%m%d_%H%M%S')
        df_filt = igra[(igra['YEAR']==date_use.year)&(igra['MONTH']==date_use.month)&(igra['DAY']==date_use.day)]
        df_rh = df_filt.dropna(subset=['RH_ICE'])
        preds = []
        for feature in features:
            if feature == 'RH_ICE':
                x = np.array(df_rh['HOUR'].values).reshape((-1, 1))
                y = np.array(df_rh[feature].values)
            else:
                x = np.array(df_filt['HOUR'].values).reshape((-1, 1))
                y = np.array(df_filt[feature].values)
            model = LinearRegression()
            model.fit(x, y)
            preds.append(model.predict(np.array(date_use.hour).reshape(1, -1)))
        rh.append(preds[0][0])
        temp.append(preds[1][0])
        press.append(preds[2][0])
    skyimage['RH_ICE'] = rh
    skyimage['TEMP(F)'] = temp
    skyimage['PRESS'] = press

    return skyimage

def main(igra, skyimage, features):
    parent_dir = os.path.join(os.getcwd(), "..")
    df = make_preds(igra, skyimage, features)
    keep_cols = [col for col in df.columns if '_output' not in col]
    df = df[keep_cols]
    df['datetime'] = df['file_name'].apply(lambda x: datetime.strptime(x.strip('.jpg').lstrip('IMG_'), '%Y%m%d_%H%M%S'))
    df['date'] = df['datetime'].apply(lambda x: x.strftime('%Y-%m-%d'))
    df.to_csv(os.path.join(parent_dir, 'data', 'output.csv'), index=False)
