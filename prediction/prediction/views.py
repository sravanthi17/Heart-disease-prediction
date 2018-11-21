from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from collections import OrderedDict

import numpy as np
from sklearn import tree

from sklearn.externals.six import StringIO
from sklearn.tree import export_graphviz
from IPython.display import Image, display
import pydotplus

def index(request):
    return render(request, './userData.html')
    # return HttpResponse("Hello, world. You're at prediction app.")

@csrf_exempt
def predict(request):
    post_dict = request.POST.dict()
    del post_dict["csrfmiddlewaretoken"]
    transformedValues = OrderedDict()
    for key,value in post_dict.items():
        transformedValues[key] = getTransformedValueFromKey(key, value)
    ordered_dict = OrderedDict(sorted(transformedValues.items()))
    health = predict_health(ordered_dict.values())
    if(health == '0'):
        return render(request, './healthy.html')
    return render(request, './unhealthy.html')


def getTransformedValueFromKey(key, value):
    # values = {'male': '1', 'female': '0',
    #           'Typical type 1': '1',
    #           'Typical type angina': '2',
    #           "Non-angina type": "3",
    #           "Asymptomatic": 4,
    #           ">=120 mg/dL": "0",
    #
    #           }
    if(value == "male"):
        return '1'
    elif(value == "female"):
        return '0'
    elif(value == "Typical type 1"):
           return '1'
    elif(value == "Typical type angina"):
        return '2'
    elif (value == "Non-angina type"):
        return '3'
    elif(value == "Asymptomatic"):
        return '4'
    elif(value == ">=120 mg/dL"):
        return '1'
    elif(value == "<120 mg/dL"):
        return '0'
    elif (value == "Normal" and key == "07restecg"):
        return '0'
    elif (value == "ST-T wave abnormal"):
        return '1'
    elif(value == "Left ventricular hypertrophy"):
        return '2'
    elif (value == "yes"):
        return '1'
    elif (value == "no"):
        return '0'
    elif (value == "flat"):
        return '2'
    elif (value == "Unslopping"):
        return '1'
    elif (value == "Downslopping"):
        return '3'
    elif (value == "Normal" and key == "13thal"):
        return '3'
    elif (value == "Fixed"):
        return '6'
    elif (value == "Reversible"):
        return '7'
    else:
        return str(value)

def predict_health(input):
    data = np.loadtxt('/Users/sravanthi/Downloads/cleveland.data copy.txt', dtype=object)
    cleanedInputData = []
    targetValues = []
    for eachRow in data:
        cleanedRow =[]
        for eachIndex in [2,3,8,9,11,15,18,31,37,39,40,43,50]:
            cleanedRow.append(eachRow[eachIndex])
        cleanedInputData.append(cleanedRow)
        targetValues.append(eachRow[57])
    clf = tree.DecisionTreeClassifier()
    clf = clf.fit(cleanedInputData, targetValues)
    # uncomment the below line to generateTree
    # generateTree(clf)
    return clf.predict([input])[0]

def generateTree(clf):
    dot_data = StringIO()
    export_graphviz(clf, out_file=dot_data,
                    class_names=["age", "gender", "restecg", "cp", "chol", "fbs", "std", "exang", "mhr", "slope", "rbp", "thal", "ca"],
                    filled=True, rounded=True,
                    special_characters=True)

    graph = pydotplus.graph_from_dot_data(dot_data.getvalue())
    plt = Image(graph.create_png())
    display(plt)
    graph.write_png("tree.png")



def viewTree(request):
    return render(request, './viewTree.html')
