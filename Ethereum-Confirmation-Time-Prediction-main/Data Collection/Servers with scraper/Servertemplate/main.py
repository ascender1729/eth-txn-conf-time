from keep_alive import keep_alive
keep_alive()
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd


HashData=[]
TimeData=[]
TxnFees=[]
Burnt=[]
Glimit=[]
Gdata=[]
Gprice=[]
Eprice=[]
TxnVal=[]
Base=[]
MaxperG=[]
Maxpriority=[]

while True:

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--no-sandbox')
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36'
    chrome_options.add_argument('user-agent={0}'.format(user_agent))
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(options=chrome_options)
    
    Start_Block = 14800000

    TotalBlocks = 500

    for i in range(TotalBlocks):

        Block_Number = str(i + int(Start_Block))

        Block_Page_url = "https://etherscan.io/block/" + Block_Number

        Txs_Page_url = "https://etherscan.io/txs?block=" + Block_Number

        driver.get(Txs_Page_url)

        Total_txs_Info = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[3]/div/div/div[2]/p/span")

        Total_txs = int(Total_txs_Info.text.split()[3])

        Pages = int(Total_txs / 50) + 1 if Total_txs % 50 else int(Total_txs / 50)

        Current_Page_Txs = driver.find_elements(By.CLASS_NAME, "myFnExpandBox_searchVal")

        MissingVal = 0
        for x in Current_Page_Txs:
            Hash = x.text
            Txs_url = "https://etherscan.io/tx/" + Hash
            driver.execute_script("window.open()")
            driver.switch_to.window(driver.window_handles[1])
            driver.get(Txs_url)
            try:
                time_element = driver.find_element(By.XPATH,
                                                   "//span[@class='text-secondary ml-2 d-none d-sm-inline-block']").text
                TotalFee=driver.find_element(By.ID, "ContentPlaceHolder1_spanTxFee").text
                value=driver.find_element(By.XPATH, "//span[@class='u-label u-label--value u-label--secondary text-dark rounded mr-1']").text 
                gasprice=driver.find_element(By.ID, "ContentPlaceHolder1_spanGasPrice").text
                ethprice=driver.find_element(By.ID, "ContentPlaceHolder1_spanClosingPrice").text

                
                button=driver.find_element(By.ID, "collapsedLink")
                driver.execute_script("arguments[0].click();", button)

                tempvar=driver.find_element(By.ID, "ContentPlaceHolder1_spanGasLimit").text
                gaslimit=driver.find_element(By.ID, "ContentPlaceHolder1_spanGasLimit").text
                gasusage=driver.find_element(By.ID, "ContentPlaceHolder1_spanGasUsedByTxn").text
                burnt= driver.find_element(By.XPATH, "//span[@class='u-label u-label--value u-label--warning text-dark rounded mr-1 mb-1']").text  
                Feesarr= driver.find_elements(By.XPATH, "//span[@class='mr-1 mb-1']")
          

            except:
                MissingVal = MissingVal + 1
            else:
                TimeData.append(time_element) 
                HashData.append(Hash)
                Burnt.append(burnt)
                Base.append(Feesarr[0].text)
                MaxperG.append(Feesarr[1].text)
                Maxpriority.append(Feesarr[2].text)
                TxnFees.append(TotalFee)
                TxnVal.append(value)
                Gdata.append(gasusage)
                Glimit.append(gaslimit)
                Gprice.append(gasprice)
                Eprice.append(ethprice)
            print(len(HashData))
            #if len(HashData):
              #print(HashData[-1], Burnt[-1],TimeData[-1],TxnVal[-1],TxnFees[-1],Eprice[-1],Gprice[-1],Glimit[-1],Gdata[-1],Base[-1],MaxperG[-1],Maxpriority[-1],sep="\n")
            driver.close()
            driver.switch_to.window(driver.window_handles[0])

        for i in range(Pages - 1):
            driver.get(Txs_Page_url + "&p=" + str(i + 2))

            Current_Page_Txs = driver.find_elements(By.CLASS_NAME, "myFnExpandBox_searchVal")

            for x in Current_Page_Txs:
                Hash = x.text
                Txs_url = "https://etherscan.io/tx/" + Hash
                driver.execute_script("window.open()")
                driver.switch_to.window(driver.window_handles[1])
                driver.get(Txs_url)
                try:
                    time_element = driver.find_element(By.XPATH,
                                                   "//span[@class='text-secondary ml-2 d-none d-sm-inline-block']").text
                    TotalFee=driver.find_element(By.ID, "ContentPlaceHolder1_spanTxFee").text
                    value=driver.find_element(By.XPATH, "//span[@class='u-label u-label--value u-label--secondary text-dark rounded mr-1']").text 
                    gasprice=driver.find_element(By.ID, "ContentPlaceHolder1_spanGasPrice").text
                    ethprice=driver.find_element(By.ID, "ContentPlaceHolder1_spanClosingPrice").text

                
                    button=driver.find_element(By.ID, "collapsedLink")
                    driver.execute_script("arguments[0].click();", button)

                    tempvar=driver.find_element(By.ID, "ContentPlaceHolder1_spanGasLimit").text
                    gaslimit=driver.find_element(By.ID, "ContentPlaceHolder1_spanGasLimit").text
                    gasusage=driver.find_element(By.ID, "ContentPlaceHolder1_spanGasUsedByTxn").text
                    burnt= driver.find_element(By.XPATH, "//span[@class='u-label u-label--value u-label--warning text-dark rounded mr-1 mb-1']").text  
                    Feesarr= driver.find_elements(By.XPATH, "//span[@class='mr-1 mb-1']")
          

                except:
                    MissingVal = MissingVal + 1
                else:
                    TimeData.append(time_element) 
                    HashData.append(Hash)
                    Burnt.append(burnt)
                    Base.append(Feesarr[0].text)
                    MaxperG.append(Feesarr[1].text)
                    Maxpriority.append(Feesarr[2].text)
                    TxnFees.append(TotalFee)
                    TxnVal.append(value)
                    Gdata.append(gasusage)
                    Glimit.append(gaslimit)
                    Gprice.append(gasprice)
                    Eprice.append(ethprice)
                print(len(HashData))
                #if len(HashData):
                  #print(HashData[-1], Burnt[-1],TimeData[-1],TxnVal[-1],TxnFees[-1],Eprice[-1],Gprice[-1],Glimit[-1],Gdata[-1],Base[-1],MaxperG[-1],Maxpriority[-1],sep="\n")
                driver.close()
                driver.switch_to.window(driver.window_handles[0])

        data_tuples = list(zip(HashData[1:],Burnt[1:],TxnFees[1:],Base[1:],MaxperG[1:], Maxpriority[1:], TxnVal[1:],Gdata[1:],Glimit[1:],Gprice[1:],Eprice[1:],TimeData[1:]))
        df = pd.DataFrame(data_tuples, columns=['Hash','Burnt','TxnFees','Basefees','Maxfees/gas','Tip','Txnval','Gasusage','Gaslimit','Gasprice','Etherprice','CompletionTime'])
        df.to_csv(Block_Number,index=False)

  
