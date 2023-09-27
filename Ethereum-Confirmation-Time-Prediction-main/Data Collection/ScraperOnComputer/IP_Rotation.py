from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from datetime import datetime
from bs4 import BeautifulSoup
import random
import requests
import pandas as pd

now = datetime.now().time()
print("Start Time =", now)

HashData=[]
TimeData=[]
From=[]
To=[]
Value=[]
TimeStamp=[]
TransactionFee=[]
GasPrice=[]
Block=[]


opt=webdriver.ChromeOptions()
opt.add_argument("--headless")
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36'
opt.add_argument('user-agent={0}'.format(user_agent))
s=Service("C:\Program Files (x86)\chromedriver.exe")

driver= webdriver.Chrome(service=s)



driver.get("https://free-proxy-list.net/")
proxy_elements=driver.find_elements(By.TAG_NAME, 'tr');
proxy_list =[x.text.split()[0] for x in proxy_elements]
proxy_list=proxy_list[1:-20]

PROXY = random.choice(proxy_list)
opt.add_argument('--proxy-server=%s' % PROXY)
#driver= webdriver.Chrome(service=s,options=opt)


Start_Block=input("ENTER STARTING BLOCK NUMBER ")  #Block_Number="14800000"

TotalBlocks =int(input("Total Blocks To Fetch"))

for i in range(TotalBlocks):

    Block_Number=str(i+int(Start_Block))
    
    Block_Page_url= "https://etherscan.io/block/"+ Block_Number

    Txs_Page_url="https://etherscan.io/txs?block="+ Block_Number

    driver.get(Txs_Page_url)

    Total_txs_Info = driver.find_element(By.XPATH,"/html/body/div[1]/main/div[3]/div/div/div[2]/p/span")

    Total_txs= int(Total_txs_Info.text.split()[3])

    print("Total transaction in the block" , Total_txs)

    Pages= int(Total_txs/50)+1 if Total_txs%50 else int(Total_txs/50)

    print("Total Pages" , Pages)

    Current_Page_Txs = driver.find_elements(By.CLASS_NAME,"myFnExpandBox_searchVal")
    
    AllHashes=[x.text for x in Current_Page_Txs]
        

    MissingVal=0   
    
    for x in AllHashes:
        Hash=x
        Txs_url="https://etherscan.io/tx/"+ Hash
        PROXY = random.choice ( proxy_list )
        opt.add_argument ( ' -- proxy - server = % s ' % PROXY )
        #driver= webdriver.Chrome(service=s,options=opt)
        driver.get(Txs_url)
        try:
            time_element=driver.find_element(By.XPATH,"/html/body/div[1]/main/div[3]/div[1]/div[2]/div[1]/div/div[4]/div/div[2]/span[2]").text
        except :
            MissingVal=MissingVal+1
        else:
            HashData.append(Hash)
            TimeData.append(time_element)    
                
        print(HashData[-1]+"  "+TimeData[-1]) 

        
    for i in range(Pages-1):
        driver.get(Txs_Page_url+"&p="+str(i+2))

        Current_Page_Txs = driver.find_elements(By.CLASS_NAME,"myFnExpandBox_searchVal")
        
        AllHashes=[x.text for x in Current_Page_Txs]

        for x in AllHashes:
            Hash=x  
            Txs_url="https://etherscan.io/tx/"+ Hash
            PROXY = random.choice ( proxy_list )
            opt.add_argument ( ' -- proxy - server = % s ' % PROXY )
            #driver= webdriver.Chrome(service=s,options=opt)
            driver.get(Txs_url)
            try:
                time_element=driver.find_element(By.XPATH,"/html/body/div[1]/main/div[3]/div[1]/div[2]/div[1]/div/div[4]/div/div[2]/span[2]").text
            except:
                MissingVal=MissingVal+1
            else:
                HashData.append(Hash)
                TimeData.append(time_element)
            
            print("  " + HashData[-1]+"  "+TimeData[-1]+"  ")

        
data_tuples = list(zip(HashData[1:],TimeData[1:]))
df = pd.DataFrame(data_tuples, columns=['Hash','CompletionTime'])
df.to_csv('EthDataCSV',index=False)

now = datetime.now().time()
print("End Time =", now)

driver.quit( )    
