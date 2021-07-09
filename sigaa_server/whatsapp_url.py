#import all libs above
import csv

#create a function that read csv file with col Código,Turma,Professor,Link 
#return as a list of dicts
def read_csv(file_name):
        with open(file_name, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            return [row for row in reader]


# execute read_csv_turma('src/whatsapp_url.csv')

print(read_csv("src/whatsapp_url.csv"))




