"""
    clent-server app
"""
from django.shortcuts import render

import csv
import re

                
class CsvReader:
    """
        Csv reader class, open static file when init, have "write to csv" classmethod
    """
    def __init__(self) -> None:
        with open('Test_Python.csv', newline='') as file:
            textreader = csv.reader(file, delimiter=';')
            lst = []

            for row in textreader:
                user_info_list = ', '.join(row).split(', ')

                if user_info_list[4]:
                    fio_split = user_info_list[4].split(' ')
                    
                    try:
                        name = fio_split[0]
                    except:
                        name = ''

                    try:
                        surname = fio_split[1]
                    except:
                        surname = ''

                    try:
                        middle_name = fio_split[2]
                    except:
                        middle_name = ''
                
                user_info_dict = {
                    "ip": user_info_list[0],
                    "mask": user_info_list[1],
                    "subnet": user_info_list[2],
                    "pc_num": user_info_list[3],
                    "fio": {
                        "name": name,
                        "surname": surname,
                        "middle_name": middle_name
                    }
                }
                lst.append(user_info_dict)

            self.lst = lst


    def write_csv(self) -> None:
        with open('new_csv.csv', 'w', newline='') as file:
            fieldnames = ['ip', 'mask', 'subnet', 'pc_num', 'fio', 'error']
            writer = csv.DictWriter(file, fieldnames=fieldnames)

            writer.writeheader()

            for i in range(len(self.lst)):
                writer.writerow({
                    'ip': self.lst[i]["ip"],
                    'mask': self.lst[i]["mask"],
                    'subnet': self.lst[i]["subnet"],
                    'pc_num': self.lst[i]["pc_num"],
                    'fio': (self.lst[i]["fio"]),
                })


def ip_mask_validator(string) -> bool:
    """ 
        validate with re for 0.0.0.0 mask
    """
    if re.match(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', string):
        return True
    else:
        return False


def computer_num_validator(string) -> bool:
    """
        check ps_number
    """
    if string.isnumeric() and string.isnumeric() > 0:
        return True
    else:
        return False


def main(request):
    """
        main view
    """
    if request.method == 'GET' and 'doit' in request.GET:

        obj = CsvReader()

        for i in range(len(obj.lst)):
            if not ip_mask_validator(obj.lst[i]["ip"]):
                obj.lst[i]["error"] = 'IP err,'
            if not ip_mask_validator(obj.lst[i]["mask"]):
                obj.lst[i]["error"] = 'Mask err'               
            if obj.lst[i]["subnet"] != '' and not ip_mask_validator(obj.lst[i]["subnet"]) != '':
                obj.lst[i]["error"] = 'Subnet err'

            if obj.lst[i]["pc_num"] == '':
                obj.lst[i]["pc_num"] == str(i+1)
            try:
                if int(obj.lst[i]["pc_num"]) <= i+1:
                    obj.lst[i]["pc_num"] == str(i+1)
            except:
                pass

            if not computer_num_validator(obj.lst[i]["pc_num"]):
                obj.lst[i]["error"] = 'Num err,'

        obj.write_csv()

    return render(request, 'testapp/index.html')
