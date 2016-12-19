import re
import csv

trainDataPath = r"F:\[SSIED] DataMiner\data\trainingData.csv"
testDataPath = r"F:\[SSIED] DataMiner\data\testData.csv"
expertCompanyPath = r"F:\[SSIED] DataMiner\data\company_expert.csv"

tempParsedDataPath = r"file.csv"

regexPattern = r"{([0-9]+),([a-zA-Z]*),([-+]?[.0-9]+|NA),([0-9]+)}"

def swapExpertWithCompany(expertId):
    with open(expertCompanyPath, 'rb') as f:
        reader = csv.reader(f, delimiter=';')
        data = list(reader)

    for row in data:
        if row[1] == expertId:
            return row[0]

def parseByRegex(pattern, text):
    dict = []
    for m in re.finditer(pattern, text):
        dict.append(m.group(1))
        dict.append(m.group(2))
        dict.append(m.group(3) if m.group(3) != 'NA' else None)
        dict.append(m.group(4))

    return dict

def getMaxNumberOfRecommendations(data):
    tempMax = 0
    maxIndex = 0
    for id in range(0,data.__len__()):
        if data[id][1].__len__() > tempMax:
            tempMax = data[id][1].__len__()
            maxIndex = id

    return data[maxIndex][1].count('{')

def parseToFile(fromFile,toFileName,isTestData):
    colmunsCount = 2 if isTestData else 3
    recommendationsValuesCount = 4
    with open(fromFile, 'rb') as f:
        reader = csv.reader(f, delimiter=';')
        data = list(reader)
        maxRecommendation = getMaxNumberOfRecommendations(data)
        convertedData = []
        for i in range(0,data.__len__()):
            convertedData.append([None] * (colmunsCount-1 + maxRecommendation * recommendationsValuesCount))


        for i in range(0,data.__len__()):
            convertedData[i][0] = data[i][0]
            convertedData[i][1] = data[i][2] if not isTestData else None
            values = parseByRegex(regexPattern,data[i][1])
            for j in range(colmunsCount-1,values.__len__()+colmunsCount-1):
                convertedData[i][j] = values.pop(0)

    with open(toFileName, 'w') as f:
        writer = csv.writer(f, delimiter=';', lineterminator='\n')
        convertedData[0] = ['SymbolId']
        convertedData[0].append('Decision') if not isTestData else None

        for id in range(colmunsCount-1,colmunsCount-1 + maxRecommendation * recommendationsValuesCount, recommendationsValuesCount):
            convertedData[0].append('Days')
            convertedData[0].append('rating')
            convertedData[0].append('opinion')
            convertedData[0].append('officerId')

        for row in convertedData:
            writer.writerow(row)

    return convertedData[0].__len__()