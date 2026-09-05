from src.mongo import main as mongo_main
from src.queries import main as postgres_main


def main():
    print("Queries to postgres: ")
    postgres_main()
    print("-" * 40)
    print("Queries to Mongo:")
    mongo_main()


if __name__ == "__main__":
    main()
