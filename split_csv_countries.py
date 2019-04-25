
import csv

# Receive csv file contains all tweet, country name
# return list of tweet from the specific country
def create_list_by_counry(csv_fileName, counrty_name, counrty_short):
    list_toRet = []
    with open(csv_fileName, newline='') as f:
        reader = list(csv.reader(f))
    for val in reader:
        if counrty_name in val[2].lower() or counrty_short in val[2].lower():
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



