
import argparse
import json
import requests

BASE_URL = "http://localhost:8000"


# Display server response
def print_response(response):
    print(f"Status Code: {response.status_code}")

    try:
        print(json.dumps(response.json(), indent=2))
    except ValueError:
        print(response.text)


# Convert ratings into a list
def parse_ratings(ratings):
    if not ratings:
        return []

    values = [
        int(r.strip())
        for r in ratings.split(",")
        if r.strip()
    ]

    if any(r < 1 or r > 5 for r in values):
        raise ValueError("Ratings must be between 1 and 5")

    return values


# Search books by genre
def search_books_by_genre(genre):
    response = requests.get(
        f"{BASE_URL}/books/genre/{genre}"
    )
    print_response(response)


# Count all books
def count_books():
    response = requests.get(f"{BASE_URL}/books/count")
    print_response(response)


# Calculate average book rating
def average_rating(book_id):
    response = requests.get(f"{BASE_URL}/books/{book_id}")
    response.raise_for_status()

    book = response.json()
    ratings = book.get("ratings", [])

    if ratings:
        average = sum(ratings) / len(ratings)
        print(f"Average Rating: {average:.2f}")
    else:
        print("No ratings available")


# Get all books
def get_all_books():
    response = requests.get(f"{BASE_URL}/books")
    print_response(response)


# Get a book by ID
def get_book(book_id):
    response = requests.get(f"{BASE_URL}/books/{book_id}")
    print_response(response)


# Create a new book
def create_book(title, author_name, author_email, year, genre, ratings=None):
    response = requests.get(f"{BASE_URL}/books")
    response.raise_for_status()
    existing_books = response.json()

    new_id = max(
        (book["id"] for book in existing_books),
        default=0
    ) + 1

    book = {
        "id": new_id,
        "title": title,
        "author": {
            "name": author_name,
            "email": author_email
        },
        "year": year,
        "genre": genre,
        "ratings": ratings if ratings is not None else []
    }

    response = requests.post(
        f"{BASE_URL}/books",
        json=book
    )
    print_response(response)


# Update an existing book
def update_book(
    book_id, title, author_name, author_email,
    year, genre, ratings=None
):
    book = {
        "id": book_id,
        "title": title,
        "author": {
            "name": author_name,
            "email": author_email
        },
        "year": year,
        "genre": genre,
        "ratings": ratings if ratings is not None else []
    }

    response = requests.put(
        f"{BASE_URL}/books/{book_id}",
        json=book
    )
    print_response(response)


# Update selected book fields
def patch_book(book_id, title=None, year=None, genre=None):
    updates = {}

    if title is not None:
        updates["title"] = title

    if year is not None:
        updates["year"] = year

    if genre is not None:
        updates["genre"] = genre

    if not updates:
        print("Provide at least one field to update.")
        return

    response = requests.patch(
        f"{BASE_URL}/books/{book_id}",
        json=updates
    )
    print_response(response)


# Delete a book
def delete_book(book_id):
    response = requests.delete(f"{BASE_URL}/books/{book_id}")
    print_response(response)


def main():
    parser = argparse.ArgumentParser(
        description="Book API Client"
    )

    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser(
        "list", help="List all books"
    )

    get_parser = subparsers.add_parser(
        "get", help="Get a book"
    )
    get_parser.add_argument("id", type=int)

    create_parser = subparsers.add_parser(
        "create", help="Create a book"
    )
    create_parser.add_argument("title")
    create_parser.add_argument("author_name")
    create_parser.add_argument("author_email")
    create_parser.add_argument("year", type=int)
    create_parser.add_argument("genre")
    create_parser.add_argument(
        "--ratings",
        default="",
        help="Comma-separated ratings"
    )

    update_parser = subparsers.add_parser(
        "update", help="Update a book"
    )
    update_parser.add_argument("id", type=int)
    update_parser.add_argument("title")
    update_parser.add_argument("author_name")
    update_parser.add_argument("author_email")
    update_parser.add_argument("year", type=int)
    update_parser.add_argument("genre")
    update_parser.add_argument(
        "--ratings",
        default="",
        help="Comma-separated ratings"
    )

    # Exercise 3
    patch_parser = subparsers.add_parser(
        "patch", help="Partially update a book"
    )
    patch_parser.add_argument("id", type=int)
    patch_parser.add_argument("--title")
    patch_parser.add_argument("--year", type=int)
    patch_parser.add_argument("--genre")

    delete_parser = subparsers.add_parser(
        "delete", help="Delete a book"
    )
    delete_parser.add_argument("id", type=int)

    # Exercise 1
    genre_parser = subparsers.add_parser(
        "search-genre",
        help="Search books by genre"
    )
    genre_parser.add_argument("genre")

    # Exercise 5
    subparsers.add_parser(
        "count", help="Count all books"
    )

    # Calculate average rating
    rating_parser = subparsers.add_parser(
        "average-rating",
        help="Calculate average book rating"
    )
    rating_parser.add_argument("id", type=int)

    args = parser.parse_args()

    try:
        if args.command == "list":
            get_all_books()

        elif args.command == "get":
            get_book(args.id)

        elif args.command == "create":
            create_book(
                args.title,
                args.author_name,
                args.author_email,
                args.year,
                args.genre,
                parse_ratings(args.ratings)
            )

        elif args.command == "update":
            update_book(
                args.id,
                args.title,
                args.author_name,
                args.author_email,
                args.year,
                args.genre,
                parse_ratings(args.ratings)
            )

        elif args.command == "patch":
            patch_book(
                args.id,
                args.title,
                args.year,
                args.genre
            )

        elif args.command == "delete":
            delete_book(args.id)

        elif args.command == "search-genre":
            search_books_by_genre(args.genre)

        elif args.command == "count":
            count_books()

        elif args.command == "average-rating":
            average_rating(args.id)

        else:
            parser.print_help()

    except ValueError as error:
        print(f"Invalid input: {error}")

    except requests.exceptions.RequestException as error:
        print(f"Request failed: {error}")


if __name__ == "__main__":
    main()
