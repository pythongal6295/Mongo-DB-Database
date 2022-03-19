from os import path
import csv
from loguru import logger
import pymongo
import users
import user_status as us
import time
import functools
#import pysnooper


# logger.remove()
# logger.add("log_{time}.log")

#timing decorator
def timer(func):
    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        start_time = time.perf_counter()  # also time.process_time()
        value = func(*args, **kwargs)
        end_time = time.perf_counter()
        run_time = end_time - start_time
        print(f"Ran {func.__name__!r} in {run_time:.4f} secs")
        return value

    return wrapper_timer

def init_user_collection(db):
    '''
    Creates and returns a new instance
    of UserCollection
    '''
    usercollection_obj = users.UserCollection(db)
    logger.info('new UserCollection object initialized.')

    return usercollection_obj

def init_status_collection(db):
    '''
    Creates and returns a new instance
    of UserStatusCollection
    '''
    userstatuscol_obj = us.UserStatusCollection(db)

    return userstatuscol_obj

#@pysnooper.snoop()
def load_users(filename, user_collection):
    '''
    Opens a CSV file with user data and
    adds it to an existing instance of
    UserCollection

    Requirements:
    - If a user_id already exists, it
    will ignore it and continue to the
    next.
    - Returns False if there are any errors
    (such as empty fields in the source CSV file)
    - Otherwise, it returns True.
    '''
    if path.isfile(filename):
        print('File exists')
    else:
        print('File does not exist.')
        return False
    t = time.time()
    try:
        with open(filename, 'r') as file:
            #reads the header
            file.readline()
            reader = csv.reader(file)
            for row in reader:
                user_collection.add_user(user_id=row[0], user_name=row[1], user_last_name=row[2], email=row[3])
    except pymongo.errors.DuplicateKeyError:
        logger.warning("This user already exists.")
        return False
    print(time.time() - t)
    return True


def load_status_updates(filename, status_collection, user_collection):
    '''
    Opens a CSV file with status data and
    adds it to an existing instance of
    UserStatusCollection

    Requirements:
    - If a status_id already exists, it
    will ignore it and continue to the
    next.
    - Returns False if there are any errors
    (such as empty fields in the source CSV file)
    - Otherwise, it returns True.
    '''
    if path.isfile(filename):
        print('File exists')
    else:
        print('File does not exist.')
        return False
    t = time.time()
    try:
        with open(filename, 'r') as file:
            #reads the header
            file.readline()
            reader = csv.reader(file)
            for row in reader:
                status_collection.add_status(status_id=row[0], user_id=row[1], status_text=row[2], user_collection = user_collection)
    except pymongo.errors.DuplicateKeyError:
        logger.warning("This user already exists.")
        return False
    
    print(time.time() - t)
    return True


#@timer()
def add_user(user_id, email, user_name, user_last_name, user_collection):
    '''
    Creates a new instance of User and stores it in user_collection
    (which is an instance of UserCollection)

    Requirements:
    - user_id cannot already exist in user_collection.
    - Returns False if there are any errors (for example, if
    user_collection.add_user() returns False).
    - Otherwise, it returns True.
    '''
    t = time.time()
    add_user_return = user_collection.add_user(user_id, email, user_name, user_last_name)
    print(time.time() - t)
    return add_user_return


def update_user(user_id, email, user_name, user_last_name, user_collection):
    '''
    Updates the values of an existing user

    Requirements:
    - Returns False if there any errors.
    - Otherwise, it returns True.
    '''
    update_user_return = user_collection.modify_user(user_id, email, user_name, user_last_name)
    return update_user_return


def delete_user(user_id, user_collection):
    '''
    Deletes a user from user_collection.

    Requirements:
    - Returns False if there are any errors (such as user_id not found)
    - Otherwise, it returns True.
    '''
    delete_user_return = user_collection.delete_user(user_id)
    return delete_user_return


def search_user(user_id, user_collection):
    '''
    Searches for a user in user_collection
    (which is an instance of UserCollection).

    Requirements:
    - If the user is found, returns the corresponding
    User instance.
    - Otherwise, it returns None.
    '''
    search_user_return = user_collection.search_user(user_id)
    logger.info(f'main.py: {search_user_return}')
    return search_user_return


def add_status(user_id, status_id, status_text, status_collection, user_collection):
    '''
    Creates a new instance of UserStatus and stores it in user_collection
    (which is an instance of UserStatusCollection)

    Requirements:
    - status_id cannot already exist in user_collection.
    - Returns False if there are any errors (for example, if
    user_collection.add_status() returns False).
    - Otherwise, it returns True.
    '''
    add_status_return = status_collection.add_status(status_id, user_id, status_text, user_collection)
    return add_status_return


def update_status(status_id, user_id, status_text, status_collection):
    '''
    Updates the values of an existing status_id

    Requirements:
    - Returns False if there any errors.
    - Otherwise, it returns True.
    '''
    update_status_return = status_collection.modify_status(status_id, user_id, status_text)
    return update_status_return


def delete_status(status_id, status_collection):
    '''
    Deletes a status_id from user_collection.

    Requirements:
    - Returns False if there are any errors (such as status_id not found)
    - Otherwise, it returns True.
    '''
    delete_status_return = status_collection.delete_status(status_id)
    return delete_status_return


def search_status(status_id, status_collection):
    '''
    Searches for a status in status_collection

    Requirements:
    - If the status is found, returns the corresponding
    UserStatus instance.
    - Otherwise, it returns None.
    '''
    search_status_return = status_collection.search_status(status_id)
    return search_status_return
