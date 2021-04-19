#!/usr/bin/python

import optparse
import os
import requests
import shutil
import sqlite3

# DEFAULT CONFIGURATION
DB_PATH = "./app/main/database"
DB_NAME = "github_users.db"

# CONSTANTS
CREATE_USERS_TABLE = "CREATE TABLE users(id integer PRIMARY KEY, username text, image_url text, type text, profile_url text)"
INSERT_USER = """INSERT INTO users(id, username, image_url, type, profile_url) VALUES(?, ?, ?, ?, ?)"""
GITHUB_USERS_ENDPOINT = "https://api.github.com/users"


def purge_database(path):
    """Purges any previous db setup; ensuring the script is idempotent"""
    # Removes previous db path
    if os.path.exists(path):
        shutil.rmtree(path)
    # Sets up db path
    if not os.path.exists(path):
        os.makedirs(path)


def initialize_database():
    """Creates the db schema, and returns a database connection"""
    db_context = sqlite3.connect(f"{DB_PATH}/{DB_NAME}")
    db_context.cursor().execute(CREATE_USERS_TABLE)
    db_context.commit()
    return db_context


def insert_user(db_context, user):
    """Inserts a user into the provided db_context"""
    db_context.cursor().execute(INSERT_USER, user)
    db_context.commit()


def parse_user(github_user):
    """Transforms a github user json into a sqlite user table tuple"""
    return (
        github_user["id"],
        github_user["login"],
        github_user["avatar_url"],
        github_user["type"],
        github_user["html_url"],
    )


def parse_users(github_users):
    """Parses a list of github users into a list of sqlite user table tuples"""
    return [parse_user(user) for user in github_users]


def fetch_github_users(total):
    """Fetches users from GitHub API"""
    # GitHub users API request limit
    API_LIMIT = 100

    n_requests = total // API_LIMIT
    rem = total % API_LIMIT
    if rem > 0:
        n_requests += 1

    users = []
    last_id = 0  # Pagination parameter for subsequent requests
    limit = API_LIMIT
    for i in range(n_requests):
        if i + 1 == n_requests and rem > 0:  # API limit or remainding
            limit = rem
        response = requests.get(
            f"{GITHUB_USERS_ENDPOINT}?since={last_id}&per_page={limit}"
        )
        data = response.json()
        last_id = data[-1]["id"]
        users.extend(data)

    return users


def parse_options():
    """Parses CLI arguments"""
    parser = optparse.OptionParser()
    parser.add_option(
        "-t",
        "--total",
        action="store",
        default=150,
        type="int",
        help="Number of users to seed",
    )
    return parser.parse_args()[0]


def main():
    options = parse_options()
    purge_database(DB_PATH)
    db_context = initialize_database()
    users = parse_users(fetch_github_users(options.total))
    for user in users:
        insert_user(db_context, user)
    db_context.close()


if __name__ == "__main__":
    main()
