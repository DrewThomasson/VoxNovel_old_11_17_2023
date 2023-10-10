import csv
import os

def process_csv(quotes_file_path, non_quotes_file_path):
    # Step 1: Read the contents of quotes.csv and non_quotes.csv into two lists.
    quotes = []
    with open(quotes_file_path, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader)  # skip the header
        for row in csvreader:
            text = row[0]
            start_location = int(row[1])
            end_location = int(row[2])
            speaker = row[4]  # Assuming "Speaker" is in the 4th column
            quotes.append((text, start_location, end_location, speaker, 'True'))

    results = []
    with open(non_quotes_file_path, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader)  # skip the header
        for row in csvreader:
            text = row[0]
            start_location = int(row[1])
            end_location = int(row[2])
            speaker = row[4]  # Assuming "Speaker" is in the 4th column
            results.append((text, start_location, end_location, speaker, 'False'))

    # Step 2: Merge and sort the two lists by start location.
    combined = quotes + results
    combined.sort(key=lambda x: x[1])  # sort based on start location

    # Step 3: Write the sorted list to book.csv.
    with open('Working_files/Book/book.csv', 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['Text', 'Start Location', 'End Location', 'Speaker', 'Is Quote'])
        for row in combined:
            csvwriter.writerow(row)

    print("Processing complete! book.csv has been created.")


def find_files(directory, filename):
    matches = []

    # Walk through directory
    for root, dirnames, filenames in os.walk(directory):
        for fname in filenames:
            if fname == filename:
                matches.append(os.path.join(root, fname))

    return matches


if __name__ == "__main__":
    quotes_file_path = find_files("Working_files", "quotes.csv")
    non_quotes_file_path = find_files("Working_files", "non_quotes.csv")

    if quotes_file_path and non_quotes_file_path:
        process_csv(quotes_file_path[0], non_quotes_file_path[0])
    else:
        print("Error: Required CSV files not found in the specified directory!")

