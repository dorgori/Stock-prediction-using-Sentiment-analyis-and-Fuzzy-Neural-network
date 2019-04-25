
import csv
import html
import re

# clean tweets
def naturalLanguage(sentence):
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
def create_list_by_counry(csv_fileName, counrty_name, counrty_short):
    list_toRet = []
    with open(csv_fileName, newline='') as f:
        reader = list(csv.reader(f))
    for val in reader:
        if counrty_name in val[2].lower() or counrty_short in val[2].lower():
            val[1] = naturalLanguage(val[1])
            if not val[1].isspace():
                if val[1].startswith('. ') or val[1].startswith('\ ') or val[1] == '\\':
                    pass
                else:
                    list_toRet.append(val)
    f.close()
    return list_toRet

# Receive list of tweet from specific country
# create csv file for that country
def create_csv_by_country(country_name, country_list):
    csvData = ['Date', 'Tweet', 'Country']
    with open(country_name, 'w', newline='') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(csvData)
        for val in country_list:
            writer.writerow(val)
        csvFile.close()

def main():
    California_list = create_list_by_counry('tweets.csv', "california", ", ca")
    NewYork_list = create_list_by_counry('tweets.csv', "new york", ", ny")
    Texas_list = create_list_by_counry('tweets.csv', "texas", ", tx")
    Florida_list = create_list_by_counry('tweets.csv', "florida", ", fl")

    create_csv_by_country('Csv_countries/California.csv', California_list)
    create_csv_by_country('Csv_countries/NewYork.csv', NewYork_list)
    create_csv_by_country('Csv_countries/Texas.csv', Texas_list)
    create_csv_by_country('Csv_countries/Florida.csv', Florida_list)


if __name__ == "__main__":
    main()



