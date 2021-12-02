from helper.helper import get_country_by_ip, get_unique_elements, find_most_popular_element, from_data_time_to_part_of_the_day, \
    count_request_in_hour, cut_web_id, duplicate_elements, most_popular_country


def test_get_country_by_ip():
    assert get_country_by_ip("81.169.181.179") == "GERMANY"


def test_get_unique_elements():
    test_list = [4, 4, 4, 2, 3, 1, 2, 6, 7, 8]
    assert get_unique_elements(test_list) == [4, 2, 1, 6, 7, 8]


def test_find_most_popular_element():
    test_list = [5, 5, 1, 6, 77, 78, 3, 2, 5]
    assert find_most_popular_element(test_list) == 5


def test_from_data_time_to_part_of_the_day():
    test_list = ["14:01:47", "16:12:57", "12:56:32", "13:56:32", "01:56:32", "02:56:32"]
    assert from_data_time_to_part_of_the_day(test_list) == "day"


def test_count_request_in_hour():
    test_list = ["01:01:47", "01:12:57", "01:16:57" "03:56:32", "13:56:32", "01:56:32", "02:56:32"]
    assert count_request_in_hour(test_list) == 3


def test_cut_web_id():
    test_list = ["web_id=1", "user_id=231", "cart_id=123123123141"]
    assert cut_web_id(test_list) == ['1', '231', '123123123141']


def test_duplicate_elements():
    test_list = [2, 2, 1, 6, 8, 99, 99, 1, 3]
    assert duplicate_elements(test_list) == [2, 1, 99]


def test_most_popular_country():
    test_list = ['148.127.59.52', '241.235.170.130', '154.168.8.45','183.201.18.244']
    assert most_popular_country(test_list) == "UNITED STATES"
