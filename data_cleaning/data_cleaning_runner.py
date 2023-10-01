import pandas as pd
import igra_clean
import pred_features
import predict_sky_images
import unit_conversions

def main(image_fp, txt_file_fp):
    print('Predicting Sky Images...')
    sky_image = predict_sky_images.main(image_fp)
    print('Done Predicting Sky Images')
    print('Starting IGRA Cleaning...')
    meta_df, data_df = igra_clean.main(txt_file_fp)
    print('IGRA Cleaning Done')
    print('Starting Unit Conversions...')
    output_df = unit_conversions.main(meta_df, data_df)
    print('Done Converting Units')
    del meta_df
    del data_df
    print('Mapping Datasets...')
    pred_features.main(output_df, sky_image, ['RH_ICE', 'TEMP(F)', 'PRESS'])
    print('Done Mapping Data')

main(r'C:\Users\kmebr\Documents\data_analytics_project_fall_2023\images/',
     r'C:\Users\kmebr\Documents\data_analytics_project_fall_2023\DAEN-Contrail-Preventers\data/')