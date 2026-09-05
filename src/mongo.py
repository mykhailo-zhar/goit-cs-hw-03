from random import randint, sample

from faker import Faker
from pymongo.synchronous.database import Database

from db import create_mongo_connection


def create_cats(db: Database, num=10):
    toilet = ["ходить в лоток", "не ходить в лоток"]
    handling = ["не дає себе гладити", "дає себе гладити"]
    color = [
        "чорний",
        "білий",
        "сірий",
    ]
    fake = Faker()
    db.cats.insert_many(
        [
            {
                "name": fake.first_name(),
                "age": randint(1, 30),
                "features": sample(toilet, 1) + sample(handling, 1) + sample(color, 1),
            }
            for _ in range(num)
        ]
    )


def get_all_cats(db: Database):
    result = db.cats.find({})
    print("All cats:")
    for el in result:
        print(el)
    print()


def find_all_with_name(db, cat_name):
    result = db.cats.find({"name": {"$eq": cat_name}})
    print(f"Cats named {cat_name}:")
    for el in result:
        print(el)
    print()


def update_cat_age(db: Database, cat_name, new_age):
    result = db.cats.update_one({"name": cat_name}, {"$set": {"age": new_age}})
    print(f"Updating cats with name: {cat_name} to age {new_age}")
    print(result)
    print()


def add_cat_feature(db: Database, cat_name, feature):
    result = db.cats.update_one({"name": cat_name}, {"$push": {"features": feature}})
    print(f"Updating cats with name: {cat_name}. Adding feature: {feature}")
    print(result)
    print()


def remove_cat_with_name(db: Database, cat_name):
    print(f"Deleting cat with name {cat_name}")
    db.cats.delete_one({"name": cat_name})


def remove_all_cats(db: Database):
    print("Removing all cats")
    db.cats.delete_many({})


def main():
    db = create_mongo_connection()

    create_cats(db)

    get_all_cats(db)
    cat_name = input("Введіть ім'я кота: ")
    find_all_with_name(db, cat_name)
    update_cat_age(db, cat_name, randint(1, 20))
    add_cat_feature(db, cat_name, "сфінкс")
    get_all_cats(db)
    remove_cat_with_name(db, cat_name)
    get_all_cats(db)
    remove_all_cats(db)
    get_all_cats(db)


if __name__ == "__main__":
    main()
