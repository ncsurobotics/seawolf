import csv
save_directory = ''

new_rows = []

with open(save_directory + 'labels.csv', 'rb') as csvfile:
    reader = csv.reader(csvfile , delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    new_rows.append(reader.next())
    for row in reader:
      print row
      file_name = row[0]
      new_file_name = 'frame-' + file_name[5:]
      row[0] = new_file_name
      new_rows.append(row)

with open(save_directory + 'labels.csv', 'wb') as csvfile:
    writer = csv.writer(csvfile , delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for row in new_rows:
      print row
      writer.writerow(row)