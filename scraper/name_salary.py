import pandas as pd
import os.path as osp  # relative paths
import datetime

from vars import popular_names


def salary(age):
    return max(
        -51424.8
        + 336.148 * age ** 2
        - 11.3976 * age ** 3
        + 0.155952 * age ** 4
        - 0.00079979 * age ** 5,
        0
    )


now = datetime.datetime.now()
res = {"name": [], "salary": [], "count": [], "age": []}

# drop duplicates
for name in list(dict.fromkeys(popular_names)):

    nameData = pd.read_csv(osp.join("raw", "{}.csv".format(name)))

    totalSalary = 0
    totalAge = 0
    totalCount = 0

    for i in range(len(nameData.YOB)):
        age = now.year - nameData.YOB[i]

        totalSalary = totalSalary + salary(age) * nameData.Alive[i]
        totalAge = totalAge + age * nameData.Alive[i]
        totalCount = totalCount + nameData.Alive[i]

    res["name"].append(name)
    res["salary"].append(totalSalary / totalCount)
    res["age"].append(totalAge / totalCount)
    res["count"].append(totalCount)

nameSalaryFrame = pd.DataFrame(data=res)

print(nameSalaryFrame)

nameSalaryFrame.to_csv('name_salary.csv')
