from collector import Collector
from config import RIOT_API_KEY


def main():
    collector = Collector(api_key=RIOT_API_KEY, region='ru')
    # collector.start(436_605_000)
    collector.start(506_604_852)
    # collector.start(506605086)


if __name__ == '__main__':
    main()
