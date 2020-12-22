import pandas as pd
from sklearn import tree
import graphviz
data = pd.read_csv("dt_dataset.csv")
data.describe()
clf = tree.DecisionTreeClassifier(min_samples_split=2)
del data
data = pd.read_csv("dt_dataset.csv")
data.describe()
features = ["crossing_frequency","traffic_volume"]
x_train = data[features]
x_train
y_train = data["command"]
dt = clf.fit(x_train,y_train)
dot_data = tree.export_graphviz(clf, out_file=None, 
                           feature_names=["crossing_frequency","traffic_volume"],  
                           class_names=["C1","C2"],  
                           filled=True, rounded=True,  
                           special_characters=True)
graph = graphviz.Source(dot_data)
graph.view()
command = clf.predict([[15,12]])
print("command = ",command[0])

#save model into a file
# from sklearn.externals import joblib
# joblib.dump(clf, 'command1.pkl')
# load model 
#clf = joblib.load('command1.pkl')

########################################
# data coming from previous statistics #
########################################
# get crruent hour 
# import datetime
# current_hour = datetime.datetime.now().hour
# data = pd.read_csv("traffic_volume.csv")
# data.get_value(index=current_hour,col="crossing_frequency")


