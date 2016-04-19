import csv

target = "iphone_sms.csv"

results = {}

knownNumbers = {"0423569238": "Ally Wilkins", "0429639273": "Noah D'Aguiar",
                "0438314319": "Sophie Arbouin",
                "0487990913": "Oliver Armstrong", "0414429172": "Oliver Armstrong",
                "0416609994": "Georgia Bell", "0457441466": "Darcy Browning",
                "0437838860": "Amii Cundy", "0424995439": "Nicole Dunn",
                "0457280399": "Alex Ebringer", "0408159191": "Alex Ebringer",
                "0488642996": "Lachlan Fairley", "0428644409": "Lachlan Fairley",
                "0459684278": "Bronte Ford", "0458240845": "Bronte Ford",
                "0458637763": "Bronte Ford", "0499859970": "Bronte Ford",
                "0437415581": "Bronte Ford", "0487708505": "Bronte Ford",
                "0401851902": "Sarah Ford", "0439151961": "Katherine Godde",
                "0450587407": "William He", "0428909684": "Sam King",
                "0488776595": "Jasmyn Bozzetto", "0468932151": "Wesley Lee",
                "0411096977": "Wesley Lee", "0403182746": "Wesley Lee",
                "0406188970": "Lucas Little", "0359750104": "Joe Macgowan",
                "0435378850": "Joe Macgowan", "0437391909": "Connor Mackay",
                "0487336381": "Connor Mackay", "0400720375": "Connor Mackay",
                "0447463195": "Brydie Mockeridge", "0438653825": "Sam O'Dempsey",
                "0412694802": "Jacob Poli", "0409174725": "Mum",
                "0487303891": "Lauren Ralph", "0413154516": "Emiel Reichinger",
                "0429177242": "Courtney Rio", "0428886168": "Maddy Rio",
                "0400205591": "Elizabeth Simons", "0407067973": "Elizabeth Simons",
                "0488250709": "Jayde Southwell", "0429231296": "Jayde Southwell",
                "0419386116": "Elsie Stoeckl", "0438733456": "Kurt Stoeckl",
                "0457944174": "Takis Tsompanellis", "0422176343": "Takis Tsompanellis",
                '0434641808': "Jess Macgowan", '0457703087': "Jenny Scott",
                "0447712220": "Ainsley Walsh", "0409899286": "Nikkita Nixon-Harding"}

with open(target) as csvfile:
    reader = csv.DictReader(csvfile)
    #reader = sorted(reader, key=lambda k: k['Number'])
    for row in reader:
        number = row['Number']
        if number[0:4] == "'+61":
            number = "0" + number[4:-1]
        else:
            number = number[1:-1]
        try:
            if results[number]:
                results[number].append([row['Date'], row['Sent'], row['Text']])
            else:
                results[row['Number']] = []
        except KeyError:
            results[number] = []
            results[number].append([row['Date'], row['Sent'], row['Text']])
        #print(row['Date'], row['Number'], row['Sent'], row['Text'])

def printTextsFormatted(textsToPerson):
    for i in textsToPerson:
        message = i[0][1:-1] + ": " + i[2][1:-1]
        if i[1] == "Y":
            print("Me - " + message)
        else:
            print("        Them - " + message)

unknown = []
for person in results:
    print
    if person in knownNumbers:
        print(knownNumbers[person] + " -"),
    else:
        unknown.append(person)
    print(person)

    printTextsFormatted(results[person])
