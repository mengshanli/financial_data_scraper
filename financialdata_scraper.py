# -*- coding: utf-8 -*-

import requests 
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

'''
==============================================================================
爬蟲
'''
def value(url, n1):          
        resp = requests.get(url)
        soup = BeautifulSoup(resp.text, 'html.parser')         
                      
        n=1
        tem=[] 
        for i in soup.select('.cr_dataTable'):
            if n == n1: # block 1 or 2
                for ii in i.find_all('td'):
                    answer=ii.text 
                    tem.append(answer)
            n += 1
                
        close=tem[4]
        
        return close
    
'''
# currency
https://quotes.wsj.com/index/XX/BUXX
https://quotes.wsj.com/fx/EURUSD
https://quotes.wsj.com/fx/USDJPY
https://quotes.wsj.com/fx/USDCNY
https://quotes.wsj.com/fx/USDTWD?mod=mdc_curr_dtabnk

'''
def currency():   
         
    WSJ_Dollar_Index=value("https://quotes.wsj.com/index/XX/BUXX",2)
    Euro_EURUSD=value('https://quotes.wsj.com/fx/EURUSD', 1)
    Yen_USDJPY=value('https://quotes.wsj.com/fx/USDJPY',1)
    ChineseYuan_USDCNY=value('https://quotes.wsj.com/fx/USDCNY',1)
    USDTWD=value('https://quotes.wsj.com/fx/USDTWD?mod=mdc_curr_dtabnk',1)
    
    return  WSJ_Dollar_Index, Euro_EURUSD, Yen_USDJPY, ChineseYuan_USDCNY, USDTWD  
        
   
'''
# stock
https://quotes.wsj.com/index/XX/CALCULATED/BUXX?mod=mdc_uss_dtabnk
'''

def stock():
    url = 'https://quotes.wsj.com/index/XX/CALCULATED/BUXX?mod=mdc_uss_dtabnk' 
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, 'html.parser')
    
    # today               
    time1=soup.select("#timestamp")  # adjust 
    time=[]               
    for i in time1:
        text=i.get_text()
        time.append(text)
        
    # stock value    
    country=[] 
    last=[] 
    for ii in soup.select('#stockindexes'): # adjust 
        country1=ii.select(".label")  # country   # adjust                
        for i in country1:
            text=i.get_text()
            country.append(text)                     
        last1=ii.select("#currency_value")     # currency last value     # adjust             
        for i in last1:
            text=i.get_text()
            last.append(text)
                                 
    country=pd.DataFrame(country,columns=['Country'])
    last=pd.DataFrame(last,columns=['Last'])
    stock_table=pd.concat([country,last], axis=1) # 各國股市表格                         
                             
    
    # final output
    #today=time[0]
    DJIA=stock_table[stock_table['Country'] == 'DJIA'].iloc[0,1]
    SP_500=stock_table[stock_table['Country'] == 'S&P 500'].iloc[0,1]
    Nasdaq_Composite=stock_table[stock_table['Country'] == 'Nasdaq Composite'].iloc[0,1]
    Stoxx_Europe600=stock_table[stock_table['Country'] == 'Stoxx Europe 600'].iloc[0,1]
    Germany_DAX=stock_table[stock_table['Country'] == 'Germany: DAX'].iloc[0,1]
    France_CAC40=stock_table[stock_table['Country'] == 'France: CAC 40'].iloc[0,1]
    UK_FTSE100=stock_table[stock_table['Country'] == 'UK: FTSE 100'].iloc[0,1]
    China_Shanghai_Composite=stock_table[stock_table['Country'] == 'China: Shanghai Composite'].iloc[0,1]

    return DJIA, SP_500, Nasdaq_Composite, Stoxx_Europe600, Germany_DAX, France_CAC40, UK_FTSE100, China_Shanghai_Composite 

'''
# bond
https://quotes.wsj.com/bond/BX/TMUBMUSD10Y?mod=mdc_bnd_dtabnk
'''
def bond():
    url = 'https://quotes.wsj.com/bond/BX/TMUBMUSD10Y?mod=mdc_bnd_dtabnk' 
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, 'html.parser')
    
    bond=[]
    for ultag in soup.select('.cr_dataTable'): # adjust 
        for litag in ultag.find_all('td'): # adjust 
            answer=litag.text 
            bond.append(answer)
    
    #bond_date=bond[0]
    bond_close=bond[4] # adjust 
    
    return bond_close

'''
# gold
https://www.cnyes.com/futures/heavymetal.aspx
'''
def gold():
    url = 'https://www.cnyes.com/futures/heavymetal.aspx' 
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, 'html.parser')
    
    value=[]
    for ultag in soup.select('.tab'): # adjust
        for litag in ultag.find_all('tr')[3]: # 近月黃金 # adjust
            answer=litag.text 
            value.append(answer)
    
    gold_value=strtofloat(value[len(value)-1]) # 近月黃金 昨收 # adjust

    return gold_value

'''
metal
https://www.cnyes.com/futures/basicmetal.aspx?ga=nav
'''
import ast

#nums=0
def strtofloat(number):
    global nums
    number=ast.literal_eval(number)
    num=len(str(int(number[1])))
    if num == 3:
        nums=1000
    elif num == 6:
        nums=1000000
               
    result=number[0]*nums + number[1]
    
    return result

def metal():
    url = 'https://www.cnyes.com/futures/basicmetal.aspx?ga=nav' 
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, 'html.parser')
    
    value=[]
    for i in soup.find_all('table'): # adjust
        for j in i.find_all('tr'): # adjust
            value1=[]
            for jj in j.find_all('td'): # adjust
                answer=jj.text 
                value1.append(answer)
            value.append(value1)
    
    # adjust (以下)
    Lme=strtofloat(value[1][4]) # LME基本金屬指數
    Copper=strtofloat(value[4][4]) #銅
    Aluminum=strtofloat(value[15][4]) #鋁
    Lead=strtofloat(value[23][4]) #鉛
    Nickel=strtofloat(value[39][4] )#鎳
    Tin=strtofloat(value[46][4]) #錫
    Zinc=strtofloat(value[31][4])  #鋅
    # adjust (以上)
    
    return Lme, Copper, Aluminum, Lead, Nickel, Tin, Zinc

'''
# oil
https://quotes.wsj.com/futures/US/CRUDE%20OIL%20-%20ELECTRONIC
https://quotes.wsj.com/bond/BX/TMUBMUSD10Y?mod=mdc_bnd_dtabnk
'''
def oil():
    
    BrentCrude=value('https://quotes.wsj.com/futures/UK/BRENT%20CRUDE' ,2)
    CrudeOil=value('https://quotes.wsj.com/futures/US/CRUDE%20OIL%20-%20ELECTRONIC',2)
    
    return CrudeOil, BrentCrude

'''
final output
'''
WSJ_Dollar_Index, Euro_EURUSD, Yen_USDJPY, ChineseYuan_USDCNY, USDTWD=currency()
DJIA, SP_500, Nasdaq_Composite, Stoxx_Europe600, Germany_DAX, France_CAC40, UK_FTSE100, China_Shanghai_Composite= stock()
bond_close=bond()
gold=gold()
Lme,Copper, Aluminum, Lead, Nickel, Tin, Zinc=metal()
CrudeOil, BrentCrude=oil()

table={
       "USD Index":WSJ_Dollar_Index,
       "EURUSD":Euro_EURUSD,
       "USDJPY":Yen_USDJPY,
       "USDCNY":ChineseYuan_USDCNY,
       "USDTWD":USDTWD,
       "US DJIA":DJIA,
       "US SPX":SP_500,
       "NASDAQ":Nasdaq_Composite,
       "STOXX Europe 600":Stoxx_Europe600,
       "DAX Germany":Germany_DAX,
       "CAC40 France":France_CAC40,
       "FTSE100 UK":UK_FTSE100,
       "Shanghai Composite Index":China_Shanghai_Composite,
       "US Bonds":bond_close,
       "US Crude Oil":CrudeOil,
       "Brent Crude":BrentCrude,
       "Gold":gold,
       "LME Metal Index":Lme,
       "Copper":Copper,
       "Aluminum":Aluminum,
       "Lead":Lead,
       "Nickel":Nickel,
       "Tin":Tin,
       "Zinc":Zinc
       }


table_df = pd.DataFrame(list(table.items()))

print(table_df)

'''
爬蟲結束
==============================================================================
寫入excel & 儲存折線圖
'''
# date
import datetime
def today_date_def():
    weekday=datetime.datetime.today().isoweekday() # 今天星期幾
    
    if weekday == 1: # 表示日期是要抓上週五(三天前)的
        date=datetime.date.today() - datetime.timedelta(days=3)
    else: #抓前一天的
        date=datetime.date.today() - datetime.timedelta(days=1)
    
    today_date=date.strftime("%m-%d") 
    #today_date=date.strftime("%Y-%m-%d") # 有"年"

    return today_date


# 找出 initial_row (尚無數值的列)
def initial_row_def(book1, sheet_name):
    sheet1 = book1.sheet_by_name(sheet_name)  #AAAAA
    for n in range(60000): # 上限6萬列
        tem=sheet1.col_values(0,n)
        if tem == []:
            initial_row=n
            break
    return initial_row

# 將最新資料寫進excel        
def update_value(book1, book2, sheet_name, obj, initial_row, todaydata_start, today_date):

    sheet1 = book1.sheet_by_name(sheet_name)  
    sheet2 = book2.get_sheet(sheet_name)  
    
    # 前一日的數字
    previous_data=sheet1.row_values(initial_row-1)    
    previous_data=emptyvalue(previous_data, sheet1, initial_row)  # 若前一日資料為空白，抓取最近日的值           
    previous_data=np.array_split(previous_data,obj)
    
    previous_value=[]
    for i in range(len(previous_data)):
        tem=previous_data[i][1]
        previous_value.append(float(tem))
    
    # 今日抓取的數字
    #todaydata_start=>table_df 第幾個開始
    today_data=table_df.iloc[todaydata_start:todaydata_start+obj][1]
    today_data=today_data.tolist()
    today_value=[]
    for t in today_data:        
        today_value.append(float(t))
    
    table_change=pd.DataFrame(today_value, columns=['today'])
    table_change['previous']=previous_value
    
    # 變化率為幾% 
    change=(table_change['today']-table_change['previous'])/table_change['previous'] 
    changes=[]
    for i in range(len(change)):
        tem='{:,.2%}'.format(change[i])
        changes.append(tem)    
    table_change['change']=changes
    
    table_change.insert(0, 'date', today_date) # 插入當天日期
    table_change=table_change.drop(['previous'], axis=1) #剔除 previous value
    
    results=[]
    for i in range(len(table_change)):
        tem=table_change.iloc[i,:]
        for t in tem:
            results.append(t)
    
    for index, value in enumerate(results):
        sheet2.write(initial_row, index, value)
    
    book2.save('Daily Market Recap.xls')

# 若前一日資料為空白，抓取最近日的值                   
def emptyvalue(previous_data, sheet1, initial_row): 
    index_empty=[]
    for i in range(len(previous_data)):        
        if previous_data[i] == '':
            index_empty.append(i)  # 空白值的index
            
            rowdatas=[]
            for r in range(1, 5):
                rowdata=sheet1.row_values(initial_row-r)
                rowdatas.append(rowdata)
            
            results=[]
            for r in range(len(rowdatas)):
                for em in index_empty:
                
                    tem=rowdatas[r][em]
                    result=r,em,tem
                    results.append(result)
            results=pd.DataFrame(results)    
            results=results[results[2] != ''].reset_index(drop=True)
            results=results[:len(index_empty)]
            
            for i in index_empty:                    
                previous_data[i]=float(results[results[1] == i][2])  
    
    return previous_data
        

'''
# 折線圖
https://matplotlib.org/api/_as_gen/matplotlib.figure.Figure.html
https://matplotlib.org/api/_as_gen/matplotlib.axes.Axes.set_ylim.html
https://chartio.com/resources/tutorials/how-to-save-a-plot-to-a-file-using-matplotlib/
https://medium.com/@yehjames/%E8%B3%87%E6%96%99%E5%88%86%E6%9E%90-%E6%A9%9F%E5%99%A8%E5%AD%B8%E7%BF%92-%E7%AC%AC2-5%E8%AC%9B-%E8%B3%87%E6%96%99%E8%A6%96%E8%A6%BA%E5%8C%96-matplotlib-seaborn-plotly-75cd353d6d3f

'''
import matplotlib.pyplot as plt
plt.style.use('seaborn-whitegrid')
import pylab as pl

# oil 的折線圖
def oilplot(sheet1, initial_row, plot_data):
    value2=(sheet1.cell(i-1,4).value for i in range(initial_row-28,initial_row+2)) # value
    
    values=[]
    for i in value2:
        values.append(i)
        
    values=pd.DataFrame(values, columns=['value2'])
    plot_data1=pd.concat([plot_data, values], axis=1)
   
    empty_index=[]
    for i in range(len(plot_data1)): 
        for j in range(3):
            if plot_data1.iloc[i][j]== '':
                tem=i, j
                empty_index.append(tem)  # 空白值的index
    empty_index1=pd.DataFrame(empty_index)
    try:        
        df=empty_index1.drop_duplicates(0, keep = False) # 只有一個 oil 是空值
        plot_data1.iloc[int(df[0])][int(df[1])]=plot_data1.iloc[int(df[0]-1)][int(df[1])] # 若非兩項指數皆為空值，空值補上前一日的值
    except:                
        plot_data_oil= plot_data1[plot_data1['value'] !=''] # 直接剔除空白值
        
    plt.plot(plot_data_oil['date'],plot_data_oil['value'],  label='US Crude Oil')
    plt.plot(plot_data_oil['date'],plot_data_oil['value2'],  label='Brent Crude')
    plt.legend()
    
# 折線圖        
def linechart(sheet_name, initial_row, title_name, col):
    book = xlrd.open_workbook('Daily Market Recap.xls')
    sheet1 = book.sheet_by_name(sheet_name)  
    
    date=(sheet1.cell(i-1,0).value for i in range(initial_row-28,initial_row+2)) # 過去30天的資料
    value1=(sheet1.cell(i-1,col).value for i in range(initial_row-28,initial_row+2)) # value
    
    dates=[]
    try:
        for i in date:          
            dates.append(i)
    except:
            pass
        
    values=[]
    try:
        for i in value1:          
            values.append(i)
    except:
            pass    
                
    date1=pd.DataFrame(dates, columns=['date'])       
    value1=pd.DataFrame(values, columns=['value'])
    plot_data=pd.concat([date1, value1], axis=1)
    
    if sheet_name == 'Oil':
        oilplot(sheet1, initial_row, plot_data)          
    else:        
        for i in range(len(plot_data)):
            if plot_data['value'][i] == '':
                plot_data=plot_data.drop([i]) # 剔除空白值

        plt.plot(plot_data['date'],plot_data['value'])
    
    plt.gca().set_ylim(auto=True) #自動調整y軸最大與最小值    
    pl.xticks(rotation=90) # 旋轉x軸文字
    plt.title(title_name)  
    plt.savefig('%s.png' % title_name, bbox_inches='tight', dpi=300, transparent=True) #AAAAA
    plt.show()

# 處理每一個工作表
# obj=> 該工作表中有幾項指數
# todaydata_start=> 當日資料(table_df)從哪裡開始是該指數的資料
def each(book1,book2, sheet_name, obj, todaydata_start): 
    today_date=today_date_def()
    initial_row=initial_row_def(book1, sheet_name)    
    update_value(book1, book2, sheet_name, obj, initial_row, todaydata_start, today_date)    
    

def chart(book1, sheet_name, obj, todaydata_start):    
    initial_row=initial_row_def(book1, sheet_name)    
    end=todaydata_start+obj 
        
    if sheet_name == 'Oil':
        title_name='Oil'
        linechart(sheet_name, initial_row, title_name, 1)
        
    else:
        c=1
        for i in range(todaydata_start,end):
            title_name=table_df[0][i]  
            linechart(sheet_name, initial_row, title_name, c)
            c += 3 #每一指數占3格(日期、數值、變化率)

'''
===============================================================================
# 主程式
'''
from xlutils.copy import copy
import xlrd
book1 = xlrd.open_workbook('Daily Market Recap.xls')
book2 = copy(book1)  #拷貝一份原來的excel
#book1.sheet_names()

each(book1, book2, 'Currency', 5, 0) # 5種指數、在tabel_df是從index=0開始
chart(book1, 'Currency', 5, 0)

each(book1,book2, 'Stocks (US)', 3, 5) # 將最新數據匯入excel
chart(book1, 'Stocks (US)', 3, 5) # 讀取excel數據匯出折線圖

each(book1,book2, 'Stocks (EU)', 4, 8)
chart(book1, 'Stocks (EU)', 4, 8)

each(book1,book2, 'Stocks (China)', 1, 12)
chart(book1, 'Stocks (China)', 1, 12)

each(book1,book2,  'Bonds', 1, 13)
chart(book1, 'Bonds', 1, 13)

each(book1,book2, 'Oil', 2, 14)
chart(book1, 'Oil', 2, 14)

each(book1,book2, 'Gold', 1, 16)
chart(book1, 'Gold', 1, 16)

each(book1,book2, 'Metal', 7, 17)
chart(book1, 'Metal', 7, 17)
