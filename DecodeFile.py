import traceback
import csv
#get 2 list and return intersection list
def intersection(lst1, lst2):
    res = []
    lst3 = [value for value in lst1 if value in lst2]
    for i in range(len(lst3)):
        if len(lst3[i]) == 4:
            res.append(lst3[i])
            #lst3.pop(i - 1)
    return res

#First Query
def GetJoinDateByYears(begin , end, DataList):
    file = open("GetJoinDateByYears.csv" , 'w')
    file.write("From : %d , To : %d \n\n" % (begin , end) )
    res = []
    count = 0
    for value in DataList:
        if ((value[2] != "") and (value[2] != " ")):
            if (int((value[2][0:4]) >= begin) and (int(value[2][0:4]) <= end)):
                file.write(str(value[0]) + "," + str(value[2][0:10]) + '\n')
                res.append("user name = %s , join date = %s" % (value[0] , value[2]))
                count += 1
    file.write("\nTotal Count is : %d" %count)
    file.close()
    return count

#Second Query
def GetNumbersOfFollowersByInput(num ,DataList ):
    file = open("GetNumbersOfFollowersByInput.csv" , 'w')
    file.write("input followers: %d \n\n\n" % num )
    res = []
    count = 0
    for value in DataList:
        try:
            #print(len(value))
            if int(value[3]) >= num:
                file.write(str(value[0]) + "," + str(value[3]) + '\n')
                #res.append("user name = %s , number of follower = %s" % (value[0] , value[2]))
                count += 1
        except:
            #print(value)
            print(traceback.print_exc())

    file.write("\nTotal Count is : %d" %count)
    file.close()
    return count



#Third Query
def GetCountryMembers(country ,DataList ):
    file = open("GetCountryMembers.csv" , 'w')
    file.write("The number of members from this country : %s \n\n\n" % country )
    res = []
    country = country .lower()
    count = 0
    for value in DataList:
        try:
            if value[1] != None:
                if country == 'usa':
                    if country in value[1].lower() or 'united states' in value[1].lower():
                        file.write(str(value[0]) + "," + str(value[1]) + '\n')
                        count += 1
                else:
                    if country in value[1].lower():
                        file.write(str(value[0]) + "," + str(value[1]) + '\n')
                        count += 1
        except:
            continue

    file.write("\nTotal Count is : %d" %count)
    file.close()
    return count


def PrintAllIntersection():
    file = open("Intersection.csv", 'w')
    for i in IntersectionList:
        if (len(i) != 4):
            continue
        file.write(str(i[0]) + "," + str(i[1]) + "," + str(i[2]) + "," + str(i[3]) + "\n")

file1 = open("Playstation.txt" , 'r')
Playstation = file1.read().split('\n')
file2 = open("Xbox.txt" , 'r')
Xbox = file2.read().split('\n')

PlaystationList = []
XboxList = []
IntersectionList = []

for line in Playstation:
    PlaystationList.append(line.split(';'))

for line in Xbox:
    XboxList.append(line.split(';'))


IntersectionList = intersection(PlaystationList ,XboxList )
GetJoinDateByYears(2010 , 2012 ,IntersectionList)       #First Query
GetNumbersOfFollowersByInput(500 , IntersectionList)     #Second Query
GetCountryMembers('england' ,PlaystationList )              #Third Query

