import math
import os.path as osp  # relative paths

import matplotlib.pyplot as plt
import pandas as pd  # data processing, CSV file I/O (e.g. pd.read_csv)

conversion_rates = pd.read_csv(
    osp.join("..", "input", "conversionRates.csv")
)
conversion_rates = dict(zip(
    list(conversion_rates.originCountry),
    list(conversion_rates.exchangeRate)
))
multiple_choice = pd.read_csv(
    osp.join("..", "input", "multipleChoiceResponses.csv"),
    low_memory=False,
    encoding="ISO-8859-1"
)

age_salary = multiple_choice[['Age', 'CompensationAmount', "CompensationCurrency"]]
age_salary = age_salary.dropna()
age_salary["CompensationAmount"] = age_salary["CompensationAmount"].str.replace(",", "")
age_salary["CompensationAmount"] = pd.to_numeric(age_salary["CompensationAmount"], errors="coerce")

WANTED = "EUR"
total = []
for index, row in age_salary.iterrows():
    Age = row["Age"]
    if row["CompensationCurrency"] in conversion_rates:
        USD = row["CompensationAmount"] * conversion_rates[row["CompensationCurrency"]]
        WANTED_CURR = USD / conversion_rates[WANTED]
        total.append((Age, USD, WANTED_CURR))

dictionary_count = {}
dictionary_amount = {}
for row in total:
    amount = row[2]
    age = row[0]
    if amount > 1e6:
        continue
    if age not in dictionary_count:
        dictionary_count[age] = 0
    if age not in dictionary_amount:
        dictionary_amount[age] = 0
    dictionary_amount[age] += amount
    dictionary_count[age] += 1

average_salary = {}
for country, amount in dictionary_amount.items():
    if math.isnan(amount):
        continue
    average_salary[country] = amount / dictionary_count[country]

del average_salary[0.0]
del average_salary[1.0]
del average_salary[99.0]

del dictionary_count[0.0]
del dictionary_count[1.0]
del dictionary_count[99.0]

plt.scatter(average_salary.keys(), average_salary.values(), s=list(dictionary_count.values()))
plt.title('Salary in EUR vs age YEARS')
plt.savefig('salary_age.png')

my_dict = {'1': 'aaa', '2': 'bbb', '3': 'ccc'}
with open('salary_age.csv', 'w') as f:
    f.write("Age,Salary EUR,Count\n")
    for key in average_salary.keys():
        f.write("%s,%s,%s\n" % (key, average_salary[key], dictionary_count[key]))

print('Results saved in salary_age.png and salary_age.csv')

