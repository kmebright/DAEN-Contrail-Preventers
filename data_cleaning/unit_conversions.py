import math
import os
import pandas as pd
import numpy as np

def rh_ice_conversion(temp, rh_water):
    temp = temp/10
    try:
        ln_es_ice = 21.876*(273.15/temp)**(-0.000766)
        ln_es_water = 17.2693882*(273.15/temp)**(-0.003586)
        es_ice = math.exp(ln_es_ice)
        es_water = math.exp(ln_es_water)
        rh_ice = (rh_water*(es_water/es_ice))*100
    except:
        rh_ice = np.nan
    return rh_ice

def kelvin_to_fahrenheit(kelvin):
    fahrenheit = (kelvin/10 - 273.15) * 9/5 + 32
    return fahrenheit

def press_to_altitude(pressure):
    return (1-((pressure/100)/1013.25)**0.190284)*145366.45

def main(igra_meta, igra_measure):
    vals = []
    for real, calc in zip(igra_measure['REPRH'].values, igra_measure['CALCRH'].values):
        if real != '':
            vals.append(real)
        else:
            vals.append(calc)
    igra_measure['rel_humidity'] = vals
    igra_measure['TEMP(F)'] = igra_measure['TEMP'].apply(kelvin_to_fahrenheit)
    igra_measure['ALTITUDE(FT)'] = igra_measure['PRESS'].apply(press_to_altitude)
    rh_ice = []
    for temp, rh_water in zip(igra_measure['TEMP'].values, igra_measure['rel_humidity'].values):
        rh_ice.append(rh_ice_conversion(temp, rh_water/10))
    igra_measure['RH_ICE'] = rh_ice
    igra_measure = igra_measure[['PRESS', 'TEMP(F)', 'ALTITUDE(FT)', 'RH_ICE', 'uid_fk']]
    final = pd.merge(left=igra_measure, right=igra_meta, left_on='uid_fk', right_on='uid', how='left')
    dates = []
    for y, m, d in zip(final['YEAR'], final['MONTH'], final['DAY']):
        dates.append(str(y)+'-'+str(m)+'-'+str(d))
    final['DATE'] = dates
    final = final[['uid', 'DATE', 'HOUR', 'PRESS', 'ALTITUDE(FT)', 'RH_ICE', 'TEMP(F)', 'SITEID']]
    final['SITE'] = final['SITEID'].map({'#USM00072402': 'Wallops Island', '#USM00072403': 'Sterling', '#USM00072405': 'Washington/National'})
    final.drop(columns=['SITEID'], inplace=True)
    df = final[(final['ALTITUDE(FT)']>34000) & (final['ALTITUDE(FT)']<38000)]
    df2 = final[final['ALTITUDE(FT)']<40000]
    parent_dir = os.path.join(os.getcwd(), "..")
    df.to_csv(os.path.join(parent_dir, 'data', 'igra_noaa_36000ft.csv'), index=False)
    df2.to_csv(os.path.join(parent_dir, 'data', 'igra_noaa_under_40000ft.csv'), index=False)
    return df
