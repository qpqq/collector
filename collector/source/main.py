from collector import Collector, Region
from config import RIOT_API_KEY, POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_HOST, POSTGRES_DB
from db import DB


def main():
    db = DB(POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_HOST, POSTGRES_DB)
    db.create_tables()
    collector = Collector(db, api_key=RIOT_API_KEY, region=Region.RU)

    # collector.start(436_605_000)
    collector.start(506_604_852)


if __name__ == '__main__':
    main()
