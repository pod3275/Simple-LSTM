import csv

with open('use_log_no_duplicate_user_sort.csv', mode='r', encoding='utf-8') as read_file:
    reader = csv.reader(read_file)
    next(reader)
    list = [0,0,0,0,0,0,0,0]
    list2 = [0,0,0,0,0,0,0,0]
    i=0
    
    with open('3_gram_menu_list.csv', mode='w', encoding='utf-8', newline='') as write_file:
        writer = csv.writer(write_file, delimiter=',')
        
        for row in reader:
            if list[6] != 0 and list2[6] != 0 and row[1] == list[1] and row[1] == list2[1]:
                writer.writerow([list2[6] + ' + ' + list[6], row[6]])
                i=i+1
            list2 = list
            list = row
        
        print(i)