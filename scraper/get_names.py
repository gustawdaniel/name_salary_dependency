import requests
from vars import popular_names, name_genders

for index in range(len(popular_names)):
    url = "https://rhiever.github.io/name-age-calculator/names/{}/{}/{}.txt".format(
        name_genders[index],
        popular_names[index][0],
        popular_names[index]
    )

    print(url)

    response = requests.get(url)

    with open("raw/{}.csv".format(popular_names[index]), 'w') as f:
        f.write(response.text)
        f.close()

