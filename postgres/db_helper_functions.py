import csv

def readSQLCommands(fileName):
    fd = open(fileName, 'r')
    sqlFile = fd.read()
    fd.close()
    sqlCommands = sqlFile.strip().split(';')
    return sqlCommands

def convert_csv_to_tuple_list(csv_file):
    data = []
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        data = [tuple(row) for row in reader]
    return data