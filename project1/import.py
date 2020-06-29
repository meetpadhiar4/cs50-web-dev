import csv
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine(
    ("postgres://hhsqwqhcxruzwl:49153dee83d99d3c9b611b83dd963eebf9102a0afdb01ae453814645631bb69a@ec2-34-195-169-25.compute-1.amazonaws.com:5432/d46641l8p7qq5e"))
db = scoped_session(sessionmaker(bind=engine))


def main():
    b = open("books.csv")
    reader = csv.reader(b)
    for isbn, title, author, year in reader:
        db.execute("INSERT INTO books (isbn, title, author, year) VALUES (:isbn, :title, :author, :year)", {
                   "isbn": isbn, "title": title, "author": author, "year": year})
        print(f"Book {title} with isbn number {isbn}, author{author} and year {year} added in the database")
        db.commit()


if __name__ == "__main__":
    main()
