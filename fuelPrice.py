from tabulate import tabulate
import requests
from bs4 import BeautifulSoup


ZIP_CODE = 58453
RANGE = 2
FUEL = 2
# 1 -> SUPER (E10)
# 2 -> SUPER (E5)
# 4 -> DIESEL

ORDER = "date"
# distance, price, zip, date


def get_price(item):
    item_split= str(item.select(".PriceList__itemPrice")).split(">")[1]
    return item_split.split("\n")[1].lstrip()


def get_company(item):
    item_split = str(item.select(".PriceList__itemTitle")).split("\n")[1]
    return item_split.lstrip()


def get_address(item):
    item_split = str(item.select(".PriceList__itemSubtitle")).split("\n")[1]
    return item_split.lstrip()


def get_datetime(item):
    item_split = str(item.select(".PriceList__itemUpdated")).split("\n")
    last_updated = item_split[1].lstrip()
    last_datetime = item_split[2].lstrip()
    return {"last": last_updated.split("<")[0], "datetime": last_datetime}


def get_open_time(item):
    item_split = str(item.select(".PriceList__itemBody")).split(">")[2]
    return item_split.split("<")[0]


def get_distance(item):
    item_split = str(item.select(".PriceList__itemBody")).split(">")[4]
    return item_split.split("<")[0].lstrip()


def main():
    html_doc = requests.get(f'https://mehr-tanken.de/tankstellen?searchText={ZIP_CODE}&brand=0&fuel={FUEL}&range={RANGE}&order={ORDER}').text
    soup = BeautifulSoup(html_doc, 'html.parser')
    item_soup_list = soup.select(".PriceList__fuelList > .PriceList__item")
    item_list = []
    for item in item_soup_list:
        try:
            item = [get_price(item), get_company(item), get_address(item),
                    get_datetime(item)["last"], get_datetime(item)["datetime"],
                    get_open_time(item), get_distance(item)]
            item_list.append(item)
        except IndexError:
            pass
    print(soup.h2.text)
    print(tabulate(item_list, headers=["Preis", "Firma", "Adresse", "letze Abfrage", "letztes Update", "geöffnete Zeit", "Distanz"], tablefmt="pretty"))
        
    
if __name__ == '__main__':
    main()