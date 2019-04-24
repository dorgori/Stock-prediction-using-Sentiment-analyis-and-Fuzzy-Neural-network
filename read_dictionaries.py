
calm_file = open("Classification\calm.txt","r")
happy_file = open("Classification\happy.txt","r")
kind_file = open("Classification\kind.txt","r")
alert_file = open("Classification\\alert.txt","r")


calm_dictionary = (calm_file.read()).split()
happy_dictionary = (happy_file.read()).split(',')
kind_dictionary = (kind_file.read()).split(',')
alert_dictionary = (alert_file.read()).split(',')

print (calm_dictionary[0])
print (happy_dictionary[0])
print (kind_dictionary[0])
print (alert_dictionary[0])