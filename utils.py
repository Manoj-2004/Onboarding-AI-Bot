import csv

# Load the questions from the CSV file

def read_csv_file() -> list:
    questions = []
    with open('sample1.csv', 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            questions.append(row['question'])
    return questions