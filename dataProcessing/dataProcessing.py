# -*- coding: utf-8 -*-
"""
data process
"""
import pandas as pd

#define function to output processed file
def outputFile(data,source):
    data.to_excel(source+'.xlsx',encoding='utf-8')

name=['000002','600690','002001','600009','000001','002008','002236','002384','002304','600885','000046','000858']
suffix='_price'

returnData=pd.DataFrame()
turnoverData=pd.DataFrame()
for i in range(len(name)):
    data=pd.read_excel('../rowData/'+name[i]+suffix+'.xlsx')
    data.index=pd.to_datetime(data['时间'])
    returnData[name[i]]=data['涨幅']
    turnoverData[name[i]]=data['换手%']

returnData=returnData.fillna(0)
turnoverData=turnoverData.fillna(0)
outputFile(returnData,'../processedData/returns')
outputFile(turnoverData,'../processedData/turnovers')


