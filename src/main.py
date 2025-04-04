import datetime
import re
import psycopg2


df ="file.txt"#path of the file
with open("file.txt",'r') as file:
    a =[line.rstrip().lower() for line in file]


expense =[]
personal =[]
savings=[]
bakery=[]
def category(file):
    items =["food","expense","personal","savings","bakery"]
    a = file
    a_food =[]
    a_expense=[]
    a_personal=[]
    a_savings=[]
    a_bakery=[]
    for i in range(len(a)):
        if 'food' in a[i]:
            a_food.append(a[i])
        elif 'expense' in a[i]:
            a_expense.append(a[i])
        elif 'personal' in a[i]:
            a_personal.append(a[i])
        elif 'bakery' in a[i]:
            a_bakery.append(a[i])
                
    money_values_food = [re.search(r'\$\d+\.\d{2}', item).group() for item in a_food]
    money_values_expense = [re.search(r'\$\d+\.\d{2}', item).group() for item in a_expense]
    money_values_personal = [re.search(r'\$\d+\.\d{2}', item).group() for item in a_personal]
    money_values_bakery = [re.search(r'\$\d+\.\d{2}', item).group() for item in a_bakery]

    # Remove the dollar sign if needed
    money_values_food = [amount.replace('$', '') for amount in money_values_food]
    money_values_expense = [amount.replace('$', '') for amount in money_values_expense]
    money_values_personal = [amount.replace('$', '') for amount in money_values_personal]
    money_values_bakery = [amount.replace('$', '') for amount in money_values_bakery]

    food  = list(map(float,money_values_food))
    expense  = list(map(float,money_values_expense))
    personal  = list(map(float,money_values_personal))
    bakery  = list(map(float,money_values_bakery))

    print(money_values_food)
    q = sum(food)
    print(food)
    print(q)
arr = category(a)
