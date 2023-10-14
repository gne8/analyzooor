import csv

def write_csv_filter_mnt_as_it_is(response, filename=''):
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        for i in response:
            if i['chain'] == 'mnt':
                writer.writerow([i])

