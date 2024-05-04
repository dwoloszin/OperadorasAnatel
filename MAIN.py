import pandas as pd
import os
import sys
import time
import zipfile
import time

import AnatelFiles
import ImportDF
import Csv_zip
import CleanData
import distCalc
import distanceT
import GOOGLE_CREATOR
import timeit
inicioTotal = timeit.default_timer()

#timeexport = time.strftime("%Y%m%d_")
script_dir = os.path.abspath(os.path.dirname(sys.argv[0]) or '.')


csv_path = os.path.join(script_dir, 'export/'+'AnatelBase'+'.csv')
zip_path = os.path.join(script_dir, 'export/'+'AnatelBase'+'.zip')

#Download All files
AnatelFiles.download('SP',['GSM'])
#AnatelFiles.download('SP',['GSM', 'WCDMA', 'LTE', 'NR'])




# Example usage:
#zip_directory = 'E:\GoogleDriveOnline\PYTHON\OperadorasAnatel\import\BaseAnatel'
zip_directory = os.path.join(script_dir, 'import/'+'Baseanatel')
df = ImportDF.ImportDFFromZip(zip_directory)
 

df.drop_duplicates(inplace=True, ignore_index=True)

df = CleanData.process(df)

'''
#==========================================
#run once a month
opList = ['TIM','CLARO','VIVO','ALGAR']
for i in opList:
    distCalc.process(i)
#=======================================
'''


df = distanceT.process(df)


df.to_csv(csv_path, sep=',',encoding='ANSI', index=False)  # Save DataFrame as CSV
time.sleep(10)
Csv_zip.process(csv_path)



GOOGLE_CREATOR.process()



fimtotal = timeit.default_timer()
print ('duracao: %f' % round(((fimtotal - inicioTotal)/60),2) + ' min') 
print ('\nALL_DONE!!!')

