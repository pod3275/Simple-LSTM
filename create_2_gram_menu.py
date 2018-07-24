import csv

with open('use_log.csv', mode='r', encoding='utf-8') as read_file:
    reader = csv.reader(read_file)
    next(reader)
    list = [0,0,0,0,0,0,0,0]
    i=0
    
    with open('2_gram_menu_list_ex.csv', mode='w', encoding='utf-8', newline='') as write_file:
        writer = csv.writer(write_file, delimiter=',')
        
        for row in reader:
            if row[6] != list[6] and list[6] != 0 and row[1] == list[1]:
                writer.writerow([list[6], row[6]])
                i=i+1
            list = row
        
        print(i)