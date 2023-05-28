# all to the bottom
### Exercise
https://docs.google.com/document/d/1OtmRJFGZXVgQm4QJKAyUrxjiEfUK_WPGrqwEYaEoSBw/edit



### Settings

Перед началом использования приложения, необходимо созадть ".env" файл в корневом каталоге и указать в нём настроки для базы данных как в файле ".template.env" 
### Installing dependencies
```
pip install -r requirements.txt
```

### Run application
```
hypercorn main:app
```
### Endpoints
- /report_1 - Посетители из какой страны чаще всего посещают сайт
- /report_2/{category} - Посетители из какой страны чаще всего интересуются товарами из определенной категории {category}
- /report_3/{category} - В какое время суток чаще всего просматривают категорию {category}
- /report_4 - Какое максимальное число запросов на сайт за астрономический час (c 00 минут 00 секунд до 59 минут 59 секунд)?
 
- /report_5/{category} - Товары из какой категории чаще всего покупают совместно с товаром из категории {category}
- /report_6 - Сколько не оплаченных корзин имеется
- /report_7 - Какое количество пользователей совершали повторные покупки

### Tech
- Python 3 - language 
- PostgresSQL - database
- Sqlalchemy - ORM
- FastAPI - web framework for building API
