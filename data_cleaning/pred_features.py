import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from datetime import datetime

def make_preds(igra, skyimage, features):
    rh = []
    temp = []
    igra['datetime'] = igra['DATE'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d'))
    igra['YEAR'] = igra['datetime'].apply(lambda x: x.year)
    igra['MONTH'] = igra['datetime'].apply(lambda x: x.month)
    igra['DAY'] = igra['datetime'].apply(lambda x: x.day)
    for date in skyimage['file_name'].values:
        date_use = datetime.strptime(date.strip('.jpg').lstrip('IMG_'), '%Y%m%d_%H%M%S')
        df_filt = igra[(igra['YEAR']==date_use.year)&(igra['MONTH']==date_use.month)&(igra['DAY']==date_use.day)]
        x = np.array(df_filt['HOUR'].values).reshape((-1, 1))
        preds = []
        for feature in features:
            y = np.array(df_filt[feature].values)
            model = LinearRegression()
            model.fit(x, y)
            preds.append(model.predict(np.array(date_use.hour).reshape(1, -1)))
        rh.append(preds[0][0])
        temp.append(preds[1][0])
    skyimage['RH_ICE'] = rh
    skyimage['TEMP(F)'] = temp

    return skyimage #pd.DataFrame(data, columns=['datetime']+features)

def main(fp, fp2, features):
    df = make_preds(pd.read_csv(fp), pd.read_pickle(fp2), features)
    keep_cols = [col for col in df.columns if '_output' not in col]
    df = df[keep_cols]
    df['datetime'] = df['file_name'].apply(lambda x: datetime.strptime(x.strip('.jpg').lstrip('IMG_'), '%Y%m%d_%H%M%S'))
    df['date'] = df['datetime'].apply(lambda x: x.strftime('%Y-%m-%d'))
    df['month'] = df['datetime'].apply(lambda x: x.month)
    df['time'] = df['datetime'].apply(lambda x: x.time)
    times = pd.read_excel(r'C:\Users\kmebr\Documents\data_analytics_project_fall_2023\DAEN-Contrail-Preventers\data\sunrise_sunset_times.xlsx')
    times['MONTH'] = times['Month'].apply(lambda x: datetime.strptime(str(x), '%m').month)
    tod = []
    for date in df['datetime'].values:
        date = pd.to_datetime(date)
        temp = times[times['MONTH']==date.month]
        if date.time() >= temp['Sunrise'].values[0] and date.time() < temp['Sunset'].values[0]:
            tod.append('Daytime')
        else:
            tod.append('Nighttime')
    df['Time of Day'] = tod
    df.drop(columns=['month', 'time'], inplace=True)
    df.to_csv(r'C:\Users\kmebr\Documents\data_analytics_project_fall_2023\DAEN-Contrail-Preventers\data/output.csv', index=False)

if __name__ == "__main__":
    main(r'C:\Users\kmebr\Documents\data_analytics_project_fall_2023\DAEN-Contrail-Preventers\data\igra_noaa_for_pred_map.csv',
         r'C:\Users\kmebr\Documents\data_analytics_project_fall_2023\DAEN-Contrail-Preventers\data\pred_output.pkl', ['RH_ICE', 'TEMP(F)'])