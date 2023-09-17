import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from datetime import datetime

def make_preds(df, features, dates):
    data = []
    for date in dates:
        temp = [date]
        date_use = datetime.strptime(date, '%Y%m%d_%H%M%S') #waiting on final datetime format
        df_filt = df[(df['YEAR']==date_use.year)&(df['MONTH']==date_use.month)&(df['DAY']==date_use.day)]
        x = np.array(df_filt['HOUR'].values).reshape((-1, 1))
        for feature in features:
            y = np.array(df_filt[feature].values)
            model = LinearRegression()
            model.fit(x, y)
            temp.append(model.predict(date_use.hour))
        data.append(temp)
    return pd.DataFrame(data, columns=['datetime']+features)

def main(fp, features, dates):
    '''
    df = file path to dataframe or actual dataframe (FIGURE OUT HOW TO ADD IN PROCESS)
    features = the features to be predicted
    dates = the dates and times from the images (FORMAT PENDING)
    '''
    df = make_preds(pd.read_csv(fp), features, dates)
    df.to_csv(r'C:\Users\kmebr\Documents\data_analytics_project_fall_2023\DAEN-Contrail-Preventers\data/output.xlsx', index=False)

if __name__ == "__main__":
    main('FILE_PATH', ['feature1', 'feature2', 'feature3'], ['date1', 'date2'])