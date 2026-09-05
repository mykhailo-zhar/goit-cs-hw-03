from functools import wraps
from random import randint, sample

from faker import Faker
from pymongo.errors import PyMongoError
from pymongo.synchronous.database import Database

from .db import create_mongo_connection


def create_cats(db: Database, num=10):
    """Insert randomly generated cat documents into the cats collection.

    :param db: MongoDB database that contains the cats collection
    :param num: number of cat documents to create
    """
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


def pymongo_error_message(e: PyMongoError):
    """Build a human-readable message from a PyMongo exception.

    :param e: exception raised by a MongoDB operation
    :return: formatted error string
    """
    return f"Error with executing the query: {e}"


def error_decorator(func):
    """Wrap a MongoDB operation and print PyMongoError instead of crashing.

    :param func: function that performs a database operation
    :return: wrapped function with the same name and docstring
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        """Run the wrapped function and catch PyMongo errors."""
        try:
            func(*args, **kwargs)
        except PyMongoError as e:
            print(pymongo_error_message(e))
        finally:
            print()

    return wrapper


@error_decorator
def get_all_cats(db: Database):
    """Print every document from the cats collection.

    :param db: MongoDB database that contains the cats collection
    """
    result = db.cats.find({})
    print("All cats:")
    for el in result:
        print(el)


@error_decorator
def find_all_with_name(db, cat_name):
    """Print documents for cats that match the given name.

    :param db: MongoDB database that contains the cats collection
    :param cat_name: name entered by the user
    """
    result = db.cats.find({"name": {"$eq": cat_name}})
    print(f"Cats named {cat_name}:")
    for el in result:
        print(el)


@error_decorator
def update_cat_age(db: Database, cat_name, new_age):
    """Update the age of the first cat that matches the given name.

    :param db: MongoDB database that contains the cats collection
    :param cat_name: name of the cat to update
    :param new_age: age value to set
    """
    result = db.cats.update_one({"name": cat_name}, {"$set": {"age": new_age}})
    print(f"Updating cats with name: {cat_name} to age {new_age}")
    print(result)


@error_decorator
def add_cat_feature(db: Database, cat_name, feature):
    """Append a feature to the features list of the matching cat.

    :param db: MongoDB database that contains the cats collection
    :param cat_name: name of the cat to update
    :param feature: new characteristic to add
    """
    result = db.cats.update_one({"name": cat_name}, {"$push": {"features": feature}})
    print(f"Updating cats with name: {cat_name}. Adding feature: {feature}")
    print(result)


@error_decorator
def remove_cat_with_name(db: Database, cat_name):
    """Delete the first cat document that matches the given name.

    :param db: MongoDB database that contains the cats collection
    :param cat_name: name of the cat to delete
    """
    print(f"Deleting cat with name {cat_name}")
    db.cats.delete_one({"name": cat_name})


@error_decorator
def remove_all_cats(db: Database):
    """Delete every document from the cats collection.

    :param db: MongoDB database that contains the cats collection
    """
    print("Removing all cats")
    db.cats.delete_many({})


def main():
    """Seed cat documents and run the CRUD demo against MongoDB."""
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
