from collector import Collector, Region
from config import RIOT_API_KEY


def main():
    collector = Collector(api_key=RIOT_API_KEY, region=Region.RU)
    collector.start(436_605_000)
    # collector.start(506_604_852)


if __name__ == '__main__':
    main()
