import re

from config.ConfigApp import ConfigApp
from helper.helper import get_unique_elements, clear_list, cut_web_id, check_one_ip_on_goods, split_content_carts

""" class ParserLog needed to read the log file and find data in it for transfer to the database"""


class ParserLog:

    def __init__(self, config: ConfigApp):
        self.file = config.path_file_log
        self.userIPadres = self.get_ip_from_log()
        self.Category = self.get_category_log()
        self.visits = self.get_visits_log()
        self.webUserId = self.get_web_user_id()
        self.webCartId = self.get_web_cart_id()
        self.SuccessfulTransactions = self.GetSuccessfulTransactions()
        self.Goods = self.get_goods()
        self.ContentCarts = self.get_content_carts()

    def get_ip_from_log(self) -> list:
        mass = []
        log = open(self.file)
        for line in log:
            ip = re.search(
                r'\b(?:(?:2(?:[0-4][0-9]|5[0-5])|[0-1]?[0-9]?[0-9])\.){3}(?:(?:2([0-4][0-9]|5[0-5])|[0-1]?[0-9]?['
                r'0-9]))\b',
                line)
            mass.append(ip.group(0))
        log.close()
        return get_unique_elements(mass)

    def get_category_log(self) -> list:
        log = open(self.file)
        mass = []
        for line in log:
            endpoint = re.search(
                r'\b\/[a-z_]{2,20}(\.[a-z]{2})?((/[a-zA-Z0-9_%]*)+)?(\.[a-z]*)?', line)
            if endpoint is not None:
                mass.append(endpoint.group(0))
        log.close()
        mass = get_unique_elements(mass)
        return clear_list(mass, True)

    def get_visits_log(self) -> dict:
        result = {"ip": [], "category": [], "date": [], "time": []}
        file = open(self.file)
        for i in file:

            ip = re.search(
                r'\b(?:(?:2(?:[0-4][0-9]|5[0-5])|[0-1]?[0-9]?[0-9])\.){3}(?:(?:2([0-4][0-9]|5[0-5])|[0-1]?[0-9]?['
                r'0-9]))\b',
                i)
            endpoint = re.search(
                r'\b\/[a-z_]{2,20}(\.[a-z]{2})?((/[a-zA-Z0-9_%]*)+)?(\.[a-z]*)?', i)

            if endpoint is not None and endpoint.group(0) != "/pay" and endpoint.group(0) != "/cart" and endpoint.group(
                    0) != "/success_pay_":
                pass
            else:
                endpoint = None

            time = re.search(
                r'([01]?[0-9]|2[0-3]):[0-5][0-9](:[0-5][0-9])?', i)
            date = re.search(r'(20)([01]?[0-9]|2[0-3])-[0-5][0-9](-[0-5][0-9])?', i)
            if ip is not None and endpoint is not None and time is not None and date is not None:
                result["ip"].append(ip.group(0))
                result["category"].append(endpoint.group(0))
                result["time"].append(time.group(0))
                result["date"].append(date.group(0))

        file.close()
        result["category"] = clear_list(result["category"], False)
        return result

    def get_web_user_id(self) -> dict:
        log = open(self.file)
        result = {"ip": [], "web_id": []}
        for line in log:
            userId = re.search(r'user_id=[0-9]{1,}', line)
            if userId is not None:
                ip = re.search(
                    r'\b(?:(?:2(?:[0-4][0-9]|5[0-5])|[0-1]?[0-9]?[0-9])\.){3}(?:(?:2([0-4][0-9]|5[0-5])|[0-1]?[0-9]?['
                    r'0-9]))\b',
                    line)
                result["ip"].append(ip.group(0))
                result["web_id"].append(userId.group(0))
        log.close()
        result["web_id"] = get_unique_elements(cut_web_id(result["web_id"]))
        result["ip"] = get_unique_elements(result["ip"])
        return result

    def get_web_cart_id(self) -> list:
        log = open(self.file)
        result = []
        for line in log:
            cartWebId = re.search(r'cart_id=[0-9]{1,}', line)
            if cartWebId is not None:
                result.append(cartWebId.group(0))

        return get_unique_elements(cut_web_id(result))

    def GetSuccessfulTransactions(self) -> dict:
        log = open(self.file)
        result = {"cart_web_id": [], "user_web_id": []}
        for line in log:
            successfulPay = re.search(r'pay\?', line)
            if successfulPay is not None:
                cartWebId = re.search(r'cart_id=[0-9]{1,}', line)
                userId = re.search(r'user_id=[0-9]{1,}', line)
                result["cart_web_id"].append(cartWebId.group(0))
                result["user_web_id"].append(userId.group(0))
        result["cart_web_id"] = cut_web_id(result["cart_web_id"])
        result["user_web_id"] = cut_web_id(result["user_web_id"])
        return result

    def get_goods(self) -> dict:
        massIp = self.userIPadres
        log = self.file
        result = {"id": [], "category_and_name": []}
        for i in massIp:
            oneIp = check_one_ip_on_goods(log, i)
            for j in oneIp["id"]:
                result["id"].append(j)

            for j in oneIp["category_and_name"]:
                result["category_and_name"].append(j)

        result["id"] = get_unique_elements(result["id"])
        result["category_and_name"] = get_unique_elements(result["category_and_name"])
        return result

    def get_content_carts(self) -> dict:
        log = open(self.file)
        result = []
        for line in log:
            cart_content = re.search(r'\bgoods_id([-a-zA-Z0-9@:%_\+.~#?&//=]*)?', line)
            if cart_content is not None:
                result.append(cart_content.group(0))

        return split_content_carts(result)
