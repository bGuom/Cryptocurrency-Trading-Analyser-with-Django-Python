# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from django.http import HttpResponse

import requests
import json


def index(request):
    return HttpResponse(getTradeData())


def getTradeData():
    tick_interval = '1d'
    LEVEL = 30
    limit = '300'

    tradepairs = ['ETHUSDT', 'ETHBTC', 'BNBETH', 'HOTETH', 'EOSETH', 'XRPETH', 'TUSDETH', 'KNCETH', 'BATETH', 'ENJETH', 'TRXETH', 'LTCETH', 'ETHUSDC', 'FUELETH', 'THETAETH', 'ICXETH', 'YOYOETH', 'ADAETH', 'NEOETH', 'PAXETH', 'XLMETH', 'VETETH', 'ONTETH', 'LOOMETH', 'ETCETH', 'ARNETH', 'APPCETH', 'MANAETH', 'OMGETH', 'POWRETH', 'INSETH', 'DENTETH', 'MFTETH', 'ELFETH', 'IOTAETH', 'MDAETH', 'AEETH', 'DATAETH', 'SKYETH', 'STORJETH', 'ZRXETH', 'ZILETH', 'QKCETH', 'LUNETH', 'WABIETH', 'LINKETH', 'XMRETH', 'DGDETH', 'KMDETH', 'EVXETH', 'WAVESETH', 'GXSETH', 'QLCETH', 'NANOETH', 'STEEMETH', 'WANETH', 'AIONETH', 'PHXETH', 'RDNETH', 'VIBETH', 'DASHETH', 'STRATETH', 'CMTETH', 'ASTETH', 'GNTETH', 'IOSTETH', 'GVTETH', 'RCNETH', 'REPETH', 'TNBETH', 'XVGETH', 'BQXETH', 'LRCETH', 'DOCKETH', 'ZECETH', 'ARKETH', 'BLZETH', 'WPRETH', 'WTCETH', 'OAXETH', 'SCETH', 'BNTETH', 'QTUMETH', 'CNDETH', 'MCOETH', 'GTOETH', 'DLTETH', 'MTLETH', 'XEMETH', 'AGIETH', 'NCASHETH', 'ADXETH', 'IOTXETH', 'CVCETH', 'RLCETH', 'POEETH', 'ENGETH', 'STORMETH', 'GRSETH', 'NULSETH', 'OSTETH', 'BCDETH', 'TNTETH', 'SNTETH', 'REQETH', 'HCETH', 'BCPTETH', 'DNTETH', 'NASETH', 'AMBETH', 'SNGLSETH', 'BRDETH', 'ZENETH', 'PPTETH', 'ARDRETH', 'BTSETH', 'SNMETH', 'FUNETH', 'XZCETH', 'NEBLETH', 'QSPETH', 'CDTETH', 'KEYETH', 'BTGETH', 'POAETH', 'PIVXETH', 'SYSETH', 'LSKETH', 'VIBEETH', 'LENDETH', 'VIAETH', 'MTHETH', 'NXSETH', 'NAVETH', 'EDOETH']
    StochRSIArr = []
    TradePairName = []

    for pair in tradepairs: 
        
        url = 'https://api.binance.com/api/v1/klines?symbol='+pair+'&interval='+tick_interval + "&limit="+limit
        data = requests.get(url).json()


        #print(data[0][0])

        # RSI = 100-100/1+RS
        #RS = Average Gain / Average Loss

        #First Average Gain = Sum of Gains over the past 14 periods / 14.
        #First Average Loss = Sum of Losses over the past 14 periods / 14

        #Average Gain = [(previous Average Gain) x 13 + current Gain] / 14.
        #Average Loss = [(previous Average Loss) x 13 + current Loss] / 14.


        # close -> print(data[0][4])

        RSI =0
        RS=0

        SOG =0
        SOL =0


        for k in range(1,15):
            dif = (float(data[0:15][k][4])-float(data[0:15][k-1][4]))
            
            if(dif>0):
                SOG+=dif
            if(dif<0):
                SOL+=(dif*-1)



        AG = (SOG/14)
        AL = (SOL/14)


        RSIARRAY= []

        for i in xrange(15,len(data)):

            dif = (float(data[i][4])-float(data[i-1][4]))
                  
            if(dif>0):
                AG = ((AG*13)+dif)/14
                AL = ((AL*13))/14
            if(dif<0):
                AG = ((AG*13))/14
                AL = ((AL*13)+(dif*-1))/14
            if(AL!=0):
                RS = AG/AL
                RSI = round((100-(100/(1+RS))),2)
            else:
                RSI =100

            RSIARRAY.append(RSI)
           



        #StochRSI = (RSI - Lowest Low RSI) / (Highest High RSI - Lowest Low RSI)


        
        if(len(RSIARRAY)>13):
            StochRSI=100
            
            LLR = min(RSIARRAY[len(RSIARRAY)-13:len(RSIARRAY)])
            HHR = max(RSIARRAY[len(RSIARRAY)-13:len(RSIARRAY)])


            StochRSI = ((RSIARRAY[-1]-LLR)/(HHR-LLR))*100
            
            if(StochRSI<LEVEL):
                StochRSIArr.append(StochRSI)
                TradePairName.append(pair)
                
                


    return json.dumps(TradePairName)