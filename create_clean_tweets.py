
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
    def create_clean_file_daily(self, csv_fileName):
        list_toRet = []
        diction_set = set()
        with open(csv_fileName, 'r',newline='',encoding="ISO-8859-1") as f:
            reader = list(csv.reader(f))
        for val in reader:
            if len(val) == 2 or len(val) == 3:
                val[1] = self.naturalLanguage(val[1])
                val[1] = val[1].replace('\n',"")
                if not val[1].isspace():
                    if val[1].startswith('. ') or val[1].startswith('\ ') or val[1] == '\\':
                        pass
                    else:
                        if val[1] not in diction_set:
                            list_toRet.append(val)
                            diction_set.add(val[1])
        f.close()
        return list_toRet

    # Receive list of tweet from specific country
    # create csv file for that country
    def create_csv_by_day(self,filename):
        csvData = ['Date', 'Tweet']
        with open(filename, 'w', newline='') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(csvData)
            for i, val in enumerate(self.clean_tweets):
                writer.writerow(val)
                if i == 800:
                    break
            csvFile.close()

    def getFilesList(self):
        self.file_list = glob.glob("Tweets By Days/*.csv")

    def readCsvPerDay(self):
        self.createFolders()
        for file in self.file_list:
            print(file)
            self.clean_tweets = self.create_clean_file_daily(file)
            current_date = file[file.find('\\')+1:]
            self.create_csv_by_day('Csv By Days/' + current_date)

    def createFolders(self):
        path = os.getcwd()
        if self.folderValidation(path + '/Csv By Days') == 0:
            os.mkdir(path + '/Csv By Days')
        # for name in self.folder_list:
        #     if self.folderValidation(path + '/Csv By Days'+'/'+name) == 0:  # Folder doesnt exists
        #         os.mkdir(path + '/Csv By Days'+'/'+name)

    def folderValidation(self, path_name):
        if not os.path.isdir(path_name):
            print('Create dir : ' +path_name)
            return 0
        return -1


if __name__ == "__main__":
    window = CsvCountries()



