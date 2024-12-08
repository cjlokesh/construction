import re
from time import sleep 
import csv
from datetime import date
import os

def clear_unmatched(file_name=""):
    unmatched_file = open(file_name, 'w')
    unmatched_file.write("")
    unmatched_file.close()

def get_construction_amout(data_file="", unmatched_file="", filter=""):
    count = 0
    filter_count = 0
    amounts = []
    total_amounts  = []
    with open(data_file) as my_file:
        clear_unmatched(unmatched_file)
        for line in my_file:
            # if filter and filter in line:
            #     filter_count +=1 
            #     print(f"filter: {line} and filter_count: {filter_count}")
            if "/" not in line:
                number = re.sub("[^0-9]", "", line)
                if number.isdigit() and int(number) > 200000:
                    unm_file = open(unmatched_file, 'a')
                    unm_file.writelines(line)
                else:
                    amounts.append(number)
                    count += 1
    filter_only_amounts(amounts, total_amounts)
    final_amount = calculate_final_amounts(total_amounts)
    update_csv(today_date=get_todays_date(), calculated_amount=final_amount, remarks='Till date all types spending amount are included')

def filter_only_amounts(amounts=[], total_amounts=[]):
    if amounts:                
        for amount in amounts:
            if amount != "":
                total_amounts.append(amount)

def calculate_final_amounts(total_amounts=[]):
    total = 0
    if total_amounts:
        total_amount = []
        for amount in total_amounts:
            total_amount.append(int(amount))
        total = sum(total_amount)
    return total

def create_csv(csv_file="House_construction_total_amount.csv"):
    with open(csv_file, 'a+', newline='') as file:
        writer = csv.writer(file)
        field = ["Date","Calculated Amount","Manual Amount", "Final Amount","Remarks"]
        writer.writerow(field)

def get_todays_date():
    today = date.today()
    # dd/mm/YY
    today_date = today.strftime("%b-%d-%Y")
    return today_date

def update_csv(csv_file="House_construction_total_amount.csv", today_date="", calculated_amount=0, remarks="Add umatched amounts manually", manual_amount=65579):
    with open(csv_file, 'a+', newline='') as file:
        final_amounts = calculated_amount + manual_amount
        writer = csv.writer(file)
        writer.writerow([today_date,calculated_amount,manual_amount,final_amounts, remarks])
        print(f"Calculated amount: {calculated_amount}\nManual amount: {manual_amount}\nFinal House Construction amount:{final_amounts}")    

if not os.path.exists("House_construction_total_amount.csv"):
    create_csv()

# get_construction_amout("House construction _2024-06-24_10-48_PM.txt", "unmatched_data.txt")
# get_construction_amout("House construction _2024-08-08_9-48_PM.txt", "unmatched_data.txt")
# get_construction_amout("./construction-details/House construction _2024-09-01_12-33_PM.txt", "unmatched_data.txt")
get_construction_amout("./construction-details/House construction _2024-12-08_2-45_PM.txt", "unmatched_data.txt")
