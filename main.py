from sqlalchemy import create_engine
from fastapi import FastAPI


from ParserLog import ParserLog
from config.ConfigApp import ConfigApp
from db.fill_data_in_tables import fill_data_in_tables
from db.build_new_database import create_new_data_base
from db.db import DataBase
from db.exception import DBnotFindException
from db.queries.reports import what_they_buy_together_from_categories, which_country_most_often_looks_at_the_category, \
    what_time_of_day_the_category_is_viewed, maximum_number_of_requests_per_hour, how_many_unpaid_carts, \
    how_many_users_bought_more_than_once, which_country_most_often_visits

config = ConfigApp()

engine = create_engine(config.url)

db = DataBase(engine)

session = db.make_session()

try:
    db.check_connection()

except DBnotFindException:
    log = ParserLog(config)
    create_new_data_base(config)
    fill_data_in_tables(log, session)

app = FastAPI()


@app.get('/report_1')
async def report_one():
    try:
        answer = which_country_most_often_visits(session)
        return {"message": answer}
    except:
        return {"Error": "invalid data"}


@app.get('/report_2/{category}')
async def report_two(category: str):
    try:
        answer = which_country_most_often_looks_at_the_category(session, category)
        return {"message": answer}
    except:
        return {"Error": "invalid data"}


@app.get('/report_3/{category}')
async def report_three(category: str):
    try:
        answer = what_time_of_day_the_category_is_viewed(session, category)
        return {"answer": answer}
    except:
        return {"Error": "invalid data"}


@app.get('/report_4')
async def report_four():
    try:
        answer = maximum_number_of_requests_per_hour(session)
        return {"answer": answer}
    except:
        return {"Error": "invalid data"}


@app.get('/report_5/{category}')
async def report_five(category: str):
    try:
        answer = what_they_buy_together_from_categories(session, category)
        return {"answer": answer}
    except:
        return {"Error": "invalid data"}


@app.get('/report_6')
async def report_six():
    try:
        answer = how_many_unpaid_carts(session)
        return {"answer": answer}
    except:
        return {"Error": "invalid data"}


@app.get('/report_7')
async def report_seven():
    try:
        answer = how_many_users_bought_more_than_once(session)
        return {"answer": answer}
    except:
        return {"Error": "invalid data"}
