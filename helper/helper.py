import re

import requests


def get_country_by_ip(ip: str) -> str:
    """Args:
        :param (str)
    Returns:
        str: returns the name of the country.
        If the site returns "(Unknown Country?)" Or "(Private Address)" then the function returns " " """

    url = rf"https://api.hostip.info/get_html.php?ip={ip}"
    try:
        response = requests.get(url)
        res = str(response.content)
        res = res[11:len(res) - 1]
        country = ''
        if "(Unknown Country?)" in res or "(Private Address)" in res:
            return " "
        for i in res:
            if i == "(" or i == ",":
                break
            else:
                country += i

        if country[-1] == " ":
            country = country[0:len(country) - 1]
        return country
    except:
        return " "


def get_unique_elements(numbers: list) -> list:
    """Args:
        :param (list)

    Returns:
         list: unique list.
        the function takes a list and returns a list with all unique values
      """
    unique = []
    for number in numbers:
        if number not in unique:
            unique.append(number)
    return unique


def find_most_popular_element(mass: list):
    """Args:
            :param (list)

        Returns:
            returns the most common element
            the function takes a list and returns the most frequent item

           """

    a_set = set(mass)
    most_common = None
    qty_most_common = 0
    for item in a_set:
        qty = mass.count(item)
        if qty > qty_most_common:
            qty_most_common = qty
            most_common = item
    return most_common


def from_data_time_to_part_of_the_day(mass: list) -> list:
    """Args:
               :param (list)
    Example:
                ['00:28:02','06:40:40','06:05:15']

           Returns:
               str: returns 'night','morning','day','evening'
               the function creates a list based on the resulting list and returns the most frequently encountered element
              """

    result = []
    for i in mass:
        hour = int(i[0:2])
        if 0 <= hour <= 6:
            result.append("night")
        elif 7 <= hour <= 12:
            result.append("morning")
        elif 13 <= hour <= 18:
            result.append("day")
        elif 19 <= hour <= 24:
            result.append("evening")
    return find_most_popular_element(result)


def count_request_in_hour(mass: list) -> int:
    """Args:
                  :param (list)
       Example:
                   ['00:28:02','06:40:40','06:05:15']

              Returns:
                  int: returns count most non-breaking elements
                  the function counts the non-breaking elements in the array and returns the largest of them
                 """
    lastSym = mass[0][0:2]
    lastPos = 0
    count = 0
    for i in range(len(mass)):
        if mass[i][0:2] != lastSym:
            if count < (i - lastPos):
                count = i - lastPos
            lastPos = i
            lastSym = mass[i][0:2]
    if count < (len(mass) - lastPos):
        count = (len(mass) - lastPos)
    return count


def clear_list(mass:list, needUnique: bool) -> list:
    """Args:
                          :param1 (list)
                          :param2 (bool)


                      Returns:
                          list: cleaned urls list without garbage data
                          the function accepts a list of urls and clears unnecessary data
                         """
    def deleteSlash(s):
        res = ''
        for i in range(1, len(s)):
            if s[i] == "/":
                break
            else:
                res += s[i]
        return res

    result = []
    for i in mass:
        result.append(deleteSlash(i))

    if needUnique is True:
        result = get_unique_elements(result)
    clearRes = []
    for i in result:
        if i == "pay" or i == "cart" or i == "success_pay_":
            continue
        else:
            clearRes.append(i)
    return clearRes


def cut_web_id(mass) -> list:
    """Args:
                      :param (list)
           Example:
                       ['web_id=12456','cart_id=53421','user_id=31242']

                  Returns:
                      list: returns list id numbers
                      the function takes a list and returns a list with id numbers
                     """

    result = []
    for i in mass:
        s = ''
        for j in i:
            if j.isdigit():
                s += j
        result.append(s)
    return result


def check_one_ip_on_goods(file, _ip) -> dict:
    """Args:
                          :param1 (path_file)
                          :param2: (ip address)


                      Returns:
                          dict: returns a dictionary with data for the database
                         the function reads the log file returns a dictionary with the product ID and its category name
                         """
    res = []
    log = open(file)

    for i in log:
        ip = re.search(
            rf'{_ip}',
            i)
        if ip is not None:
            url = re.search(
                r'\.[a-z]{2,4}\b(\/[-a-zA-Z0-9@:%_\+.~#?&//=]*)?',
                i)

            if url is not None:
                res.append(url.group(0))
    log.close()
    return share_goods_and_category(clear_mass_for_goods(res))


def clear_mass_for_goods(mass) -> dict:
    """Args:
                             :param (list)

                         Returns:
                             dict: returns a dictionary with id_goods and category/name
                            takes a list of url addresses and separates them into goods id and category/name
                            """
    result = {"id": [], "category_and_name": []}

    se = []

    for i in range(len(mass)):
        if "goods_id" in mass[i]:
            result["id"].append(mass[i])
            result["category_and_name"].append(mass[i - 1])

    for i in result["id"]:
        str_id = ""
        for j in i:
            if j == "&":
                break
            else:
                str_id += j
        se.append(str_id)
    se = cut_web_id(se)

    result["id"] = se

    return result


def share_goods_and_category(mass: dict) -> dict:
    """Args:
                               :param (dict)

                           Returns:
                               dict: dictionary with separated urls

                              the function takes a dictionary and iterates over it. Converting endpoint to string
                              """
    result = []
    for i in mass["category_and_name"]:
        x = i.split("/")
        str_ = x[1] + " " + x[2]
        result.append(str_)
    mass["category_and_name"] = result
    return mass


def split_content_carts(mass: list) -> dict:
    """Args:
                                  :param (list)

                              Returns:
                                  dict: dictionary with goods_id, amount, cart_id for db

                                 the function takes a list of urls and splits it into a dictionary with the
                                  necessary data for the database
                                 """

    result = {"goods_id": [], "amount": [], "cart_id": []}
    for i in mass:
        spl = i.split("&")
        result["goods_id"].append(spl[0])
        result["amount"].append(spl[1])
        result["cart_id"].append(spl[2])

    result["goods_id"] = cut_web_id(result["goods_id"])
    result["amount"] = cut_web_id(result["amount"])
    result["cart_id"] = cut_web_id(result["cart_id"])
    return result


def duplicate_elements(mass: list) -> list:
    """Args:
        :param (list)

    Returns:
            list: returns list of all elements that have occurred more than 1 time
            the function takes a list and returns a list of all elements that have occurred more than 1 time
                   """
    result = []
    for i in mass:
        if mass.count(i) > 1:
            result.append(i)
    result = get_unique_elements(result)
    return result


def most_popular_country(mass: list) -> str:
    """Args:
           :param (list) ip address

       Returns:
               str: the most frequent country
               the function takes a list of ip, determines the country and returns the most frequent one
                      """
    result = []
    for i in mass:

        country = get_country_by_ip(i)
        if country == " ":
            continue
        else:
            result.append(country)

    return find_most_popular_element(result)
