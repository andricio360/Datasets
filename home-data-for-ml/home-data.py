# Code you have previously used to load data
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
import numpy as np


iowa_file_path = "/Users/mac/Documents/Datasets/home-data-for-ml/train.csv"

home_data = pd.read_csv(iowa_file_path)
y = home_data.iloc[:, -1].values


features = ['LotArea', 'YearBuilt', '1stFlrSF', '2ndFlrSF', 'FullBath', 'BedroomAbvGr', 'TotRmsAbvGrd']
X = home_data[features].values

print(X)
#Taking Care of Missing Values
from sklearn.impute import SimpleImputer
imputer = SimpleImputer(missing_values=np.nan, strategy='mean')
#imputer.fit(X[:,:])
#X[:, 1:3] = imputer.transform(X[:, 1:3])

#Splitting dataset into Training and Test
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 1)

#Feature Scaling
from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)

#Training The Model

#LogisticRegression Model
from sklearn.linear_model import LogisticRegression

def get_mae(max_iter, train_X, val_X, train_y, val_y):
    model = LogisticRegression(max_iter=max_iter, random_state=0)
    model.fit(train_X, train_y)
    preds_val = model.predict(val_X)
    mae = mean_absolute_error(val_y, preds_val)
    return(mae)

#for i in [200,500,1000,2000]:
#    my_mae = get_mae(i,X_train,X_test,y_train,y_test)
#    print("Max iter number: %d  \t\t Mean Absolute Error:  %d" %(i, my_mae))
log_mae = get_mae ( 200,X_train,X_test,y_train,y_test)
print(log_mae)

#RandomForest Model
rf_model = RandomForestRegressor(random_state=1)
rf_model.fit(X_train, y_train)
rf_val_predictions = rf_model.predict(X_test)
rf_val_mae = mean_absolute_error(rf_val_predictions, y_test)
print(rf_val_mae)
