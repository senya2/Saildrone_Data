#!/usr/bin/env python
# coding: utf-8

# In[5]:


import numpy as np
import pandas as pn
import xarray as xr
import matplotlib.pyplot as plt
import datetime as dt
import netCDF4


# In[6]:


url = 'https://podaac-opendap.jpl.nasa.gov/opendap/hyrax/allData/insitu/L2/saildrone/Baja/saildrone-gen_4-baja_2018-sd1002-20180411T180000-20180611T055959-1_minutes-v1.nc'
ds = xr.open_dataset(url, drop_variables = {'WING_ANGLE','BARO_PRES_STDDEV', 'ROLL', 'PITCH', 'TEMP_AIR_STDDEV', 'RH_STDDEV', 'UWND_STDDEV', 'VWND_STDDEV', 'GUST_WND_STDDEV', 'TEMP_CTD_STDDEV', 'COND_STDDEV', 'SAL_STDDEV', 'O2_CONC_UNCOR_MEAN', 'O2_CONC_UNCOR_STDDEV', 'O2_SAT_MEAN', 'O2_SAT_STDDEV', 'TEMP_O2_MEAN', 'TEMP_O2_STDDEV', 'CHLOR_MEAN', 'CHLOR_STDDEV', 'BKSCT_RED_MEAN', 'BKSCT_RED_STDDEV', 'CDOM_STDDEV', ' WWND_STDDEV', 'TEMP_IR_UNCOR_STDDEV' })
ds


# In[ ]:


# swap obs for time
ds=ds.isel(trajectory=0)
ds = ds.swap_dims({'obs':'time'})
print(ds)

#pd_ds = ds.to_dataframe()
#dshr = pd_ds.set_index('time').groupby(pd.Grouper(freq='1H')).mean()
#dshr = ds
dshr=ds.resample(time='1h', skipna=True, label='left').mean()
dshr

dshr = ds
size = int(len(ds['time']))


# In[ ]:


#define variables 
time_shift = dshr.time + np.timedelta64(30,'m')
lat_shift = ds.latitude
lon_shift = ds.longitude
DS_var = ds.COG
DV_var = ds.SOG
IM = '01'
ATTC = ' '
TI_var = '2'
LI_var = '5'
#NID-2 
NID = '  '
II = '  '#2
ID = '         '#9
C1 = '02'
### C1 is The country that recruited a ship, which may differ from the country of immediate receipt, see page 21, # 16 in IMMA documentation for full list of codes
#VI-1 VV-2 WW-2 W1- 1
VItoW1 = '      '
AtoIT = '    '
WBTItoDPT = '          '

SI_var = '04'
NtoCH = '       '
ALL_var = ''
for i in range(617):
       ALL_var += ' '
        
for i in range(size):
    #format string output and put hours in correct units (.01hr)
    HR = '{time_shift.dt.hour[i]+time_shift.dt.minute[i]/60:.2f}'
    HR = str(HR)
           
    time_str = str(time_shift.dt.year[i])+str(time_shift.dt.month[i])+str(time_shift.dt.day[i])+HR
    #time_str is YR + MO + DY + HR
    LAT = '{lat_shift[i]:.2f}'
    LON = '{lon_shift[i]:.2f}'
    pos_str = str(LAT)+str(LON)

    DSDV = str(DS_var[i])+str(DV_var[i])
    
    DI_var = '6'
    D_var = str(np.arctan2(ds.VWND_MEAN[i], ds.UWND_MEAN[i])*180/np.pi) #this is wind TO direction, is imma wind FROM?
    WI_var = '4'
    W_var = np.sqrt(ds.UWND_MEAN[i]**2 + ds.VWND_MEAN[i]**2) #convert vectors to speed
    W_var = W_var/1.9444  #unit conversion (kn to .1 m/s)
    W_var = '{W_var:.1f}'
    W_var = str(W_var)
    
    #reformat the SLP and put in correcnt units
    SLP_var = ds.BARO_PRES_MEAN[i]*.1
    SLP_var = '{SLP_var:.1f}'
    SLP_var = str(SLP_var)
    IT_var = '8'

    AT_var = ds.TEMP_AIR_MEAN[i]
    AT_var = AT_var*.1
    AT_var = '{AT_var:.1f}'
    AT_var = str(AT_var)
    
    ##IF DS HAS WAVE PERIOD AND HEIGHT DATA, THIS WILL NEED CHANGING
    #some sets have wave data, some don't:
  #  WD_var = '  '
  #  WP_var = WAVE_DOMINANT_PERIOD
  #  WH_var = WAVE_SIGNIFICANT_HEIGHT

        #WD-2 WP-2 WH-2
    WD_var = '  '
    WP_var = '  '
    WH_var = '  '
        
    Final_IMMA1_str = time_str + pos_str + IM + ATTC #+ TI_var + LI_var + DSDV + NID + II + ID + C1 + DI_var + D_var + WI_var + W_var + VItoW1 + SLP_var + AtoIT + IT_var + AT_var + WBTItoDPT + SI_var + SST_var + NtoCH + WD_var + WP_var + WH_var + ALL_var 
    
    f = open("IMMA_saildrone_test.imma", 'a+')
    f.write(Final_IMMA1_str)
    f.close


# In[ ]:




