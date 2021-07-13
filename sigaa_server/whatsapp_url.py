#import all libs above
import csv

#create a function that read csv file with col Código,Turma,Professor,Link 
#remove spaces in strings
#return a dict as {codigo: {turma: "", professor: "", link: ""}}
#return as a list of dicts
def read_csv(file_name):
    with open(file_name, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        data = {}
        for row in reader:
            row['Turma'] = row['Turma'].strip()
            row['Professor'] = row['Professor'].strip()
            data[row['Código'].strip()+row['Turma']] = row
        return data




# execute the function above
# and save the result as a list of dicts
# in the variable called 'whatsapp_group'
# and print dict key QUI072
# whatsapp_group = read_csv('src/whatsapp_url.csv')
# print(whatsapp_group['QUI072T01'])
