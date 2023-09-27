
# Confirmation Time Prediction in Ethereum

In Ethereum blockchain when a user makes an exchange or execute
a contract it is considered to be a Transaction.

Due to the importance of these transactions it is
very important for a user to gain some insight on how
much time it might take for the transaction to be
processed based on the network traffic.

By knowing about conformation time beforehand, a user can infer whether
right now would be the right time for them to send this
transaction to the network.

## Components Of Transaction

- Transaction value
Amount of Ether to be transferred 
- Basefees
The Base Fee is determined by the Ethereum network depends upon number of miners seeking to validate transactions
- Maxfees per gas
The Max Fee is the absolute maximum amount you are willing to pay per unit of gas to get your transaction confirmed
- Miners Tip
The part of transaction fees directly sent to miner, miner sort the transaction in order of tip
- Transaction fees
The fees user should pay to get the transaction confirmed
- Gasusage
Amount of gas that was used to execute 
a transaction.
- Gaslimit
Represents the maximum amount 
of gas that can be used to execute 
a transaction.
- Gasprice
     
Amount be paid per unit of gas for the computation cost incurred due to 
the execution of a transaction

- Etherprice	

- Burnt value

- CompletionTime
The time taken for the transaction get added into a mined block

## Data collection
The data was extracted from ethereum.io

the following selenium code was used for extraction

for each transaction one request


For each data field In our data set, that is one transaction One request was sent to etherscan, one webpage was loaded, and the data was scraped .

We were trying to create a big data set. We needed a lot of transaction data. So the extraction of one transaction should be fast.

The standard limits the number of requests sent in one minute by one user to 100.

Running the script in headless mode was the next step to doing so. That occupied all of their computational resources 




One option was to run these Selenium scripts on virtual machines for free and to make them run 24/7. We used 10 virtual machines and ran the scripts simultaneously.

Relpit provides free virtual machines for web servers.

10 servers were created on the Relpit program, which was extracting ethereum data and storing it in Google sheets. The Google Sheets API is also used for this.




These 10 servers were hosted and running 24 hours a day, which made the whole extraction process 10 times faster.


## Screenshots
- Running server on www.replit.com virtual machine
![App Screenshot](https://raw.githubusercontent.com/rishavmishra1400/Ethereum-Confirmation-Time-Prediction/1304592586a84a60d20a16c03a312c6aa4aeadbc/Screenshots/Server%20Running%20on%20Virtual%20machine.png)


- Monitoring the servers using www.uptimerobot.com and also ping in every 5 mins
![App Screenshot](https://raw.githubusercontent.com/rishavmishra1400/Ethereum-Confirmation-Time-Prediction/1304592586a84a60d20a16c03a312c6aa4aeadbc/Screenshots/Monitoring%20the%20runtime%20of%20servers.png)



- Each transaction stored as
![App Screenshot](https://raw.githubusercontent.com/rishavmishra1400/Ethereum-Confirmation-Time-Prediction/main/Screenshots/Data1.png)
![App Screenshot](https://raw.githubusercontent.com/rishavmishra1400/Ethereum-Confirmation-Time-Prediction/main/Screenshots/Data2.png)

## Proposed Model

Random forest model, in general, performs well at 
learning complex, highly non-linear relationships; like 
between time and both the gas price and the gas used 
in Ethereum blockchain dataset.

The model is known 
to outperform fundamental classification and 
regression models like naïve Bayes, polynomial and 
linear regressors. The model proposed in the 
paper employs random forest regressor to make 
confirmation time predictions. 

## Hyperparameter tuning in Random forest
RandomizedSearchCV implements a randomized search over parameters, where each setting is sampled from a distribution over possible parameter values. 

A random forest uses many parameters
- n_estimators
- max_features
- max_ depth
- min_samples_split
- min_samples_leaf

We found the best parameters by RandomizedSearchCV

![App Screenshot](https://raw.githubusercontent.com/rishavmishra1400/Ethereum-Confirmation-Time-Prediction/main/Screenshots/BestParams.png)

## Evaluation of the model
Accuracy of the model on both training and test dataset was tested


![App Screenshot](https://raw.githubusercontent.com/rishavmishra1400/Ethereum-Confirmation-Time-Prediction/main/Screenshots/Accuracy%20of%20model.png)

The model was trained with 135,712 transaction

and was tested on 33,928

Train Data Accuracy = 70.75%
Test Data Accuracy = 77.18%

Since millions of transaction are done on ethereum blockchain everyday . So the further improvement on the model can be performed by adding more data samples to the training data.

# Steps to regenerate result

## Data collection steps


1. Create a virtual machine on relp.com


2. Create running server by running [keep_alive.py](https://github.com/rishavmishra1400/Ethereum-Confirmation-Time-Prediction/blob/main/Data%20Collection/Servers%20with%20scraper/Servertemplate/keep_alive.py)


3. Mention starting block and number of blocks you want to fetch
```
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

.
.
```

4. Run the [main.py](https://github.com/rishavmishra1400/Ethereum-Confirmation-Time-Prediction/blob/main/Data%20Collection/Servers%20with%20scraper/Servertemplate/main.py)

5. Data will be downloaded and stored on the virtual machine.






Explore the [Dataset](https://drive.google.com/file/d/133Gj_O7qXpAfkVM26wgcUGEuJhZU0au6/view?usp=sharing
) used.

## EDA Steps  
[Colab Notebook](https://colab.research.google.com/drive/1Uv4y1GttltPs9CH-UDUkEdOmdoY8yK6q#scrollTo=SbDPk5OZ82ny)




1. Import numpy pandas 

2. Upload the collected [Dataset](https://drive.google.com/file/d/133Gj_O7qXpAfkVM26wgcUGEuJhZU0au6/view?usp=sharing
) to google drive and mount your drive.

Read csv file into dataframe
```
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from decimal import Decimal
from google.colab import drive
drive.mount('/content/drive')
path = "/content/drive/MyDrive/Colab Notebooks/Data.txt"

df = pd.read_csv(path)
```


3. Drop all the coloums with empty cells
```
df=df.dropna()
df=df.reset_index()
df=df.drop(['index'], axis=1)


```
4. Extracting exact ether values into floating points with slicing and type casting
also getting time data into seconds 

converting all data points to float64 , drop the coloums if not convertable

```
def isfloat(num):
    if num is None:
       return False
    try:
        float(num)
        return True
    except ValueError:
        return False

def getBurntval(value):
    list= (str(value)).split()
    return 1000000*Decimal(list[2].replace(',', ""))


def getg(value):
    list= (str(value)).split()
    return Decimal(list[-2].replace(',', ""))



def getEthval(value):
    list= (str(value)).split()
    return 1000000*Decimal(list[0].replace(',', ""))
.
.
.
```

[Colab Notebook](https://colab.research.google.com/drive/1Uv4y1GttltPs9CH-UDUkEdOmdoY8yK6q#scrollTo=SbDPk5OZ82ny)



5. Normalization Standardization using the MinMaxScalar

```
from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()

scaled = scaler.fit_transform(df)
scaled=pd.DataFrame(scaled,columns=['Burnt','TxnFees','Basefees','Maxfees/gas','Tip','Txnval','Gasusage','Gaslimit','Gasprice','Etherprice','CompletionTime'])
scaled
```

## Model training steps

1. Test Train Split

```
y = df[ 'CompletionTime']
x = df.drop(['CompletionTime'], axis = 1)

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.20, random_state=101)
print (f'x_train : {X_train.shape}')
print (f'y_train : {y_train.shape}')
print (f'x_test: {X_test.shape}')
print (f'y_test: {y_test.shape}')
```
2. Random Search CV to get best parameters for our RandomForest
```from sklearn.model_selection import RandomizedSearchCV
# Number of trees in random forest
n_estimators = [int(x) for x in np.linspace(start = 20, stop = 500, num = 50)]
# Number of features to consider at every split
max_features = ['auto', 'sqrt']
# Maximum number of levels in tree
max_depth = [int(x) for x in np.linspace(10, 1100, num = 20)]
max_depth.append(None)
# Minimum number of samples required to split a node
min_samples_split = [2, 5, 10]
# Minimum number of samples required at each leaf node
min_samples_leaf = [1, 2, 4]
# Method of selecting samples for training each tree
bootstrap = [True, False]
# Create the random grid
random_grid = {'n_estimators': n_estimators,
               'max_features': max_features,
               'max_depth': max_depth,
               'min_samples_split': min_samples_split,
               'min_samples_leaf': min_samples_leaf,
               'bootstrap': bootstrap}
print(random_grid)
```
3. Training the model 
```from sklearn.model_selection import RandomizedSearchCV
rf_random = RandomizedSearchCV(estimator= rf, param_distributions = random_grid, n_iter = 100, cv = 3, verbose=2, random_state=42, n_jobs = 40)
rf_random.fit(X_train, y_train)  
```

4. Best parameter for our model
```
rf_random.best_params_
```


## Model Evaluation
```
def evaluate(model, test_features, test_labels):
    predictions = model.predict(test_features)
    errors = absolute(predictions - test_labels)
    mape = 100 * np.mean(errors / test_labels)
    accuracy = 100 - mape
    print('Model Performance')


    print('Average Error: {:0.4f} degrees.'.format(np.mean(errors)))
    print('Accuracy = {:0.2f}%.'.format(accuracy))
    
    return accuracy





best_random = rf_random
print("On Train Data")
random_accuracy = evaluate(best_random, X_train, y_train)  
print("On Test Data")
random_accuracy = evaluate(best_random, X_test, y_test) 

```

![App Screenshot](https://raw.githubusercontent.com/rishavmishra1400/Ethereum-Confirmation-Time-Prediction/main/Screenshots/Accuracy%20of%20model.png)

The model was trained with 135,712 transaction
and was tested on 33,928

Train Data Accuracy = 70.75 %
Test Data Accuracy = 77.18 %

Since millions of transaction are done on ethereum blockchain everyday . So the further improvement on the model can be performed by adding more data samples to the training data.
