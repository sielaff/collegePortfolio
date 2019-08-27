import pandas as pd
import sys

df = pd.read_csv('mtcars.csv', header = 0) # starts at line 0
df.drop('hp', axis = 1, inplace = True)    # drop the hp column

df_train = df.loc[df['carb']=='train']
df_test = df.loc[df['carb']=='test']

df_test = df_test.drop('carb', axis=1)
df_train = df_train.drop('carb', axis=1)

y_train = df_train.loc[:, 'vs']
y_test = df_test.loc[:, 'vs']

x_train = df_train.drop('vs', axis=1)
x_test = df_test.drop('vs', axis=1)

from sklearn.linear_model import LogisticRegression
clf = LogisticRegression()

clf.fit(x_train, y_train)
y_predict = clf.predict(x_test)
from sklearn.metrics import confusion_matrix
confusion_matrix = confusion_matrix(y_test, y_predict)


print ("Confusion Matrix:")
print confusion_matrix
print y_test
