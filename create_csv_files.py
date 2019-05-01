
import csv
import html
import re
import glob, os

# clean tweets

class CsvCountries():
    def __init__(self):
        self.getFilesList()
        self.readCsvPerDay()

    def naturalLanguage(self, sentence):
        emoji_pattern = re.compile("["
                u"\U0001F600-\U0001F64F"  # emoticons
                u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                u"\U0001F680-\U0001F6FF"  # transport & map symbols
                u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                   "]+", flags=re.UNICODE)
        ch = "\\x"  #replace \xfdsda to @
        sentence = str(sentence.encode('utf-8'))
        sentence = sentence.replace(ch, "@")
        sentence = html.unescape(sentence)  # unescape HTML
        sentence = re.sub(r"http\S+", "", sentence)  # remove normal URLS
        sentence = re.sub(r"pic\.twitter\.com/\S+", "", sentence)  # remove pic.twitter.com URLS
        sentence = re.sub(r"@\S+", "", sentence)  # remove User Tags
        sentence = re.sub(emoji_pattern, '', sentence) #remove emojis
        return sentence[4:]


    # Receive csv file contains all tweet, country name
    # return list of tweet from the specific country
    def create_list_by_counry(self, csv_fileName, counrty_name, counrty_short):
        list_toRet = []
        with open(csv_fileName, newline='') as f:
            reader = list(csv.reader(f))
        for val in reader:
            if counrty_name in val[2].lower() or counrty_short in val[2].lower():
                val[1] = self.naturalLanguage(val[1])
                if not val[1].isspace():
                    if val[1].startswith('. ') or val[1].startswith('\ ') or val[1] == '\\':
                        pass
                    else:
                        list_toRet.append(val)
        f.close()
        return list_toRet

    # Receive list of tweet from specific country
    # create csv file for that country
    def create_csv_by_country(self, country_name, country_list):
        csvData = ['Date', 'Tweet', 'Country']
        with open(country_name, 'w', newline='') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(csvData)
            for val in country_list:
                writer.writerow(val)
            csvFile.close()

    def createCsvByDate(self, date):
        self.create_csv_by_country('Csv By Days/California/'+date, self.California_list)
        self.create_csv_by_country('Csv By Days/NewYork/'+date, self.NewYork_list)
        self.create_csv_by_country('Csv By Days/Texas/'+date, self.Texas_list)
        self.create_csv_by_country('Csv By Days/Florida/'+date, self.Florida_list)

    def getFilesList(self):
        self.file_list = glob.glob("Tweets By Days/*.csv")

    def readCsvPerDay(self):
        self.folder_list = ['California','NewYork','Texas', 'Florida']
        self.createFolders()
        for file in self.file_list:
            print(file)
            self.California_list = self.create_list_by_counry(file, "california", ", ca")
            self.NewYork_list = self.create_list_by_counry(file, "new york", ", ny")
            self.Texas_list = self.create_list_by_counry(file, "texas", ", tx")
            self.Florida_list = self.create_list_by_counry(file, "florida", ", fl")
            current_date = file[file.find('\\')+1:]
            self.createCsvByDate(current_date)

    def createFolders(self):
        path = os.getcwd()
        if self.folderValidation(path + '/Csv By Days') == 0:
            os.mkdir(path + '/Csv By Days')
        for name in self.folder_list:
            if self.folderValidation(path + '/Csv By Days'+'/'+name) == 0:  # Folder doesnt exists
                os.mkdir(path + '/Csv By Days'+'/'+name)

    def folderValidation(self, path_name):
        if not os.path.isdir(path_name):
            print('Create dir : ' +path_name)
            return 0
        return -1


if __name__ == "__main__":
    window = CsvCountries()



