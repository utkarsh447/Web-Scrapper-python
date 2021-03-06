import urllib.request
from bs4 import BeautifulSoup
import pandas as pd

def make_soup(url):
	thepage = urllib.request.urlopen(url)
	soupdata = BeautifulSoup(thepage, "html.parser")
	return soupdata

def scrape(url):

    playerdata = playerdatasaved = ""
#    url="https://www.reuters.com/sectors/industries/rankings?industryCode=177&view=size&page=-1&sortby=mktcap&sortdir=DESC"
    soup = make_soup(url)
    #print(len(soup))

    for headline in soup.findAll('h1'):
        Headline_tag = headline.text

    try:
        print(len(Headline_tag))

    except:
        return

    print(Headline_tag) #H1 HEADING TO MATCH IN THE SHEET

    for monts in soup.findAll('div', { "class" : "column1" }):
    	for record in monts.findAll('tr'):
    		playerdata=""
    		for data in record.findAll('td'):
    			playerdata = playerdata + "@" + data.text
    		playerdatasaved = playerdatasaved + "^^" + playerdata[1:] #splitting the string after scraping based on ^^,data is being split on new line



    a = (playerdatasaved.split('^^'))
    tickers=[] #list of list or rows of ticker data  or TickerTable contains rowwise data of details correponding to TickerId
    
    for i in range(2,len(a)):
         b=str(a[i])
         c=b.split('@')
         tickers.append(c)

    tickerdata = tickerdatasaved = tickerdescription = ""
    count = 0
    for i in range (1, len(tickers)):
    	if(tickers[i][0]=='' or tickers[i][0]=='\xa0'):
     		continue

    	ticker_url = "https://www.reuters.com/finance/stocks/company-officers/" + str(tickers[i][0])
    	print(ticker_url)
    	ticker_soup = make_soup(ticker_url)
    	for monts in ticker_soup.findAll('div', { "class" : "column1" }):
    		for record in monts.findAll('tr'):
    			tickerdata = tickerdescription = ""
    			#count = 0
    			for data in record.findAll(['td','th']):
    				tickerdata = tickerdata + "@" + data.text.strip() #+ "@"+ str(tickers[i][0])
    				
    			tickerdatasaved = tickerdatasaved + "^" + tickerdata[1:] + "@" + str(tickers[i][0])

    tickerdata= (tickerdatasaved.split('^'))#list being made after splitting the tickerdatasavedlist
    tickertable=[]#list of list or rows of tickr data

    descriptiontable=[]
    stop=[]
    stop_all=[]

    ls=[]
    ds=[]
    #print (len(tickerdata))
    for i in range(len(tickers)):
        ls.append( 'Name@Description@'+tickers[i][0])
        ds.append('Name@Age@Since@Current Position@'+tickers[i][0])
    print (len(ls))  
          
    j=1
    k=1
    stop2=[]


    for i in range(len(tickerdata)):
        try:    
            if(ls[j] == tickerdata[i]):
                j = j+1
                stop.append(i)
            
            if(ds[k]== tickerdata[i]):
                k=k+1
                stop2.append(i)      
        except:
            pass
    data_all=[]
    data_desc=[]

    listfordetails3=[]
    listfordesc=[]
    for i in range(len(stop)):
        for j in range(stop2[i]+1,stop[i]-1):
            listfordetails3.append(tickerdata[j])

    tickertable=[]
    print (type(listfordetails3[0]))
    for i in range(len(listfordetails3)):
        item=listfordetails3[i]
        item2=item.split('@')
        tickertable.append(item2)


    ls1=[]
    ls2=[]
    ls3=[]
    ls4=[]
    ls5=[]
    for i in range(1,len(tickertable)):
        ls1.append(tickertable[i][0])
        ls2.append(tickertable[i][1])
        ls3.append(tickertable[i][2])
        ls4.append(tickertable[i][3])
        ls5.append(tickertable[i][4])
    d = {'Name': ls1, 'Age': ls2, 'Since':ls3,'Current Position':ls4,'Tickr':ls5}
    dataframeticker = pd.DataFrame(data=d)

    descriptiontable=[]
    listfordesc=[]
    for i in range(len(stop)):
        try:
         for j in range(stop[i]+1,stop2[i+1]-1):
            listfordesc.append(tickerdata[j])
        except:
            pass

    for i in range(len(listfordesc)):
        item=listfordesc[i]
        item2=item.split('@')
        descriptiontable.append(item2)

    ds1=[]
    ds2=[]
    ds3=[]
    for i in range(0,len(descriptiontable)):
        ds1.append(descriptiontable[i][0])
        ds2.append(descriptiontable[i][1])
        #ds3.append(descriptiontable[i][2])
    e={'Name':ds1,'Description':ds2}
    descriptionticker=pd.DataFrame(data=e)

    f=pd.merge(dataframeticker,  descriptionticker, on='Name', how='outer')
    tl1=[]
    tl2=[]
    tl3=[]
    tl4=[]
    tl5=[]
    for i in range(len(tickers)):
        tl1.append(tickers[i][0])
        tl2.append(tickers[i][1])
        tl3.append(tickers[i][2])
        tl4.append(tickers[i][3])
        tl5.append(tickers[i][4])

    fin={'Tickr':tl1,'Name':tl2,'Market Capitalization':tl3,'TTM Sales $':tl4,'Employees':tl5}
    initialframe=pd.DataFrame(data=fin)

    g=pd.merge(f,  initialframe, on='Tickr', how='outer')
    print(g)

    for headline in soup.findAll('h1'):
        Headline_tag = headline.text

    print(Headline_tag)

    headline=[]
    for i in range(g.shape[0]):
        headline.append(Headline_tag)

    h=g.assign(Industries=headline)
    writer = pd.ExcelWriter('pandas_simple.xlsx', engine='xlsxwriter')
    h.to_excel(writer, sheet_name='Sheet1')
    writer.save()

    file1 = pd.read_excel("smaller_file.xlsx")
    file2 = pd.read_excel("pandas_simple.xlsx")
    file3 = file1.merge(file2, on="Industries", how="outer")

    os.remove("smaller_file.xlsx")
    os.remove("pandas_simple.xlsx")

    file3.to_excel("smaller_file.xlsx")

import os


for i in range(1,238):
    url="https://www.reuters.com/sectors/industries/rankings?industryCode="+str(i)+"&view=size&page=-1&sortby=mktcap&sortdir=DESC"
    scrape(url)
