import os

from dotenv import load_dotenv

load_dotenv()


class ConfigApp:
    user = os.getenv('POSTGRES_USER', 'postgres')
    db = os.getenv('POSTGRES_DB', 'all_to_the_bottom')
    password = os.getenv('POSTGRES_PASSWORD', 'mysecretpassword')
    host = os.getenv('POSTGRES_HOST', 'app-database')
    port = os.getenv('POSTGRES_PORT', '4444')
    path_file_log = os.getenv('PATH_LOG_FILE', 'input/logs.txt')
    url = rf'postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}'
