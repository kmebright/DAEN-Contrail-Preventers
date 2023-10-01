import os
import pandas as pd
from datetime import datetime
from roboflow import Roboflow

def count_object_occurrences(predictions, target_class):
    object_count = 0
    for prediction in predictions:
        if prediction['class'] in target_class:
            object_count += 1
    return object_count

def main(image_fp):
    files = os.listdir(image_fp)
    rf = Roboflow(api_key="zRb8LZg63cFvJMrp0GyO")
    project = rf.workspace().project("contrails-50-50-object-det.")
    model = project.version(2).model
    df = pd.DataFrame(files, columns=['file_name'])
    df['datetime'] = df['file_name'].apply(lambda x: datetime.strptime(x.strip('.jpg').lstrip('IMG_'), '%Y%m%d_%H%M%S'))
    df['date'] = df['datetime'].apply(lambda x: x.strftime('%Y-%m-%d'))
    df['month'] = df['datetime'].apply(lambda x: x.month)
    df['time'] = df['datetime'].apply(lambda x: x.time)
    parent_dir = os.path.join(os.getcwd(), "..")
    times = pd.read_excel(os.path.join(parent_dir, 'data', 'sunrise_sunset_times.xlsx'))
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
    df = df[df['Time of Day']=='Daytime']
    print('Number of Images to Predict:', len(df))
    data = []
    for file in df['file_name'].values:
        temp = [file]
        pred = model.predict((image_fp+file), confidence=30, overlap=30)
        if count_object_occurrences(pred, 'Cirrus') + count_object_occurrences(pred, 'LongLived') != 0:
            temp.append(1)
        else:
            temp.append(0)
        data.append(temp)
    cols = ['file_name', '30_pred']
    output = pd.DataFrame(data, columns = cols)
    parent_dir = os.path.join(os.getcwd(), "..")
    output.to_csv(os.path.join(parent_dir, 'data', 'sky_image_preds.csv'), index=False)
    return output