import graphlab as gl
import csv
import csvParser

trainDataPath = r"data\trainingData.csv"
testDataPath = r"data\testData.csv"

trainDataSplittedCompanyPath = r"data\TrainingWithCompaniesSplitted.csv"
testDataSplittedCompanyPath = r"data\TestWithCompaniesSplitted.csv"

outputFilePath = r"result.csv"
splittedTrainData = r"data\splittedTrainData.csv"
splittedTestData = r"data\splittedTestData.csv"

def saveOutput(data):
    data.remove_column('probability')
    data.export_csv(outputFilePath,delimiter=';', header=False)

def getHintColumns(columnsCount, isTestData):
    if isTestData:
        hint = [str]
    else:
        hint = [str,str] # jak dane train to dodatkowo jest kolumna Decision

    for i in range(0,columnsCount/4):
        hint.append(long)
        hint.append(str)
        hint.append(float)
        hint.append(long)
    return hint

def getColumnsCount(file):
    with open(file, 'rb') as f:
        reader = csv.reader(f, delimiter=';')
        data = list(reader)
        return data[0].__len__()


# po rozdzieleniu na wiele kolumn potrzebne jest podanie mu jakiego typu jest dana kolumna bo inaczej sie wydupi.
# Po to jest ta metoda getHintColumns, jak uzywacie pliku trainDataPath to on te 3 kolumny sam sobie ogarnie
def loadData(path):
    columnsCount = getColumnsCount(path)
    return gl.SFrame.read_csv(path,
                                header=True,
                                delimiter=';',
                                #column_type_hints = getHintColumns(columnsCount)
                              )

def compute():
    usage_data = loadData(trainDataPath)

    model = gl.random_forest_classifier.create(usage_data, target=  'Decision',
                                                       max_iterations= 15,
                                                       max_depth= 41,
                                                       validation_set=None,
                                                       #class_weights= {'Buy': 50, 'Hold': 7, 'Sell': 7},
                                               )
    usage_data = loadData(testDataPath)

    r = model.classify(usage_data)
    saveOutput(r)

def computeWithPerformanceTest():
    usage_data = loadData(trainDataPath)
    train_data, test_data = usage_data.random_split(0.8)

    model = gl.random_forest_classifier.create(train_data, target=  'Decision',
                                                       max_iterations= 15,
                                                       max_depth= 41,
                                                       validation_set=None,
                                                       #class_weights= {'Buy': 50, 'Hold': 7, 'Sell': 7},
                                               )

    predictions = model.classify(test_data)
    results = model.evaluate(test_data)
    print results

    usage_data = loadData(testDataPath)
    r = model.classify(usage_data)
    saveOutput(r)

# zeby rozbic dane na kolumny
# csvParser.parseToFile(trainDataPath,splittedTrainData,False)
# csvParser.parseToFile(testDataPath,splittedTestData,True)

# uczenie na penym zbiorze danach
compute()
# uczenie na 80% + 20% jako dane testowe i wyrzuca w konsoli wyniki
# computeWithPerformanceTest()