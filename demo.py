"""
Library Management System - Demo Script
======================================

This script demonstrates all the functionality of the Library Management System
including adding books and members, borrowing/returning books, searching,
updating, and deleting operations.

Author: Library Management System
Date: 2024
"""

from operations import Library


def print_separator(title: str):
    """Print a formatted separator with title."""
    print(f"\n{'='*60}")
    print(f" {title}")
    print(f"{'='*60}")


def print_library_status(library: Library):
    """Print current library status."""
    status = library.get_library_status()
    print(f"\nLibrary Status:")
    print(f"   Total Books: {status['total_books']}")
    print(f"   Total Members: {status['total_members']}")
    print(f"   Total Copies: {status['total_copies']}")
    print(f"   Available Copies: {status['available_copies']}")
    print(f"   Borrowed Copies: {status['borrowed_copies']}")


def print_books(library: Library, title: str = "Books"):
    """Print all books in the library."""
    books = library.list_all_books()
    print(f"\n{title}:")
    if not books:
        print("   No books in library")
    else:
        for i, book in enumerate(books, 1):
            print(f"   {i}. {book}")


def print_members(library: Library, title: str = "Members"):
    """Print all members in the library."""
    members = library.list_all_members()
    print(f"\n {title}:")
    if not members:
        print("   No members in library")
    else:
        for i, member in enumerate(members, 1):
            print(f"   {i}. {member}")


def main():
    """Main demo function."""
    print("Welcome to the Library Management System Demo!")
    print("This demo will showcase all the features of the system.")

    # Create a new library
    library = Library()
    print_separator("1. CREATING LIBRARY")
    print("New library created successfully!")
    print_library_status(library)

    # Add books
    print_separator("2. ADDING BOOKS")
    books_to_add = [
        ("978-0134685991", "Effective Python", "Brett Slatkin", "Non-Fiction", 3),
        ("978-0132350884", "Clean Code", "Robert Martin", "Non-Fiction", 2),
        ("978-0553418026", "The Martian", "Andy Weir", "Sci-Fi", 4),
        ("978-0061120084", "To Kill a Mockingbird", "Harper Lee", "Fiction", 2),
        ("978-0307277679", "The Da Vinci Code", "Dan Brown", "Mystery", 3),
        ("978-0743273565", "The Great Gatsby", "F. Scott Fitzgerald", "Fiction", 2),
        ("978-0553382563", "Dune", "Frank Herbert", "Sci-Fi", 3)
    ]

    for isbn, title, author, genre, copies in books_to_add:
        try:
            library.add_book(isbn, title, author, genre, copies)
            print(f"Added: {title} by {author} ({copies} copies)")
        except ValueError as e:
            print(f"Failed to add {title}: {e}")

    print_books(library)
    print_library_status(library)

    # Add members
    print_separator("3. ADDING MEMBERS")
    members_to_add = [
        ("M001", "Alice Johnson", "alice.johnson@email.com"),
        ("M002", "Bob Smith", "bob.smith@email.com"),
        ("M003", "Carol Davis", "carol.davis@email.com"),
        ("M004", "David Wilson", "david.wilson@email.com")
    ]

    for member_id, name, email in members_to_add:
        try:
            library.add_member(member_id, name, email)
            print(f"Added member: {name} ({member_id})")
        except ValueError as e:
            print(f"Failed to add {name}: {e}")

    print_members(library)
    print_library_status(library)

    # Demonstrate borrowing books
    print_separator("4. BORROWING BOOKS")
    borrow_operations = [
        ("M001", "978-0134685991"),  # Alice borrows Effective Python
        ("M001", "978-0132350884"),  # Alice borrows Clean Code
        ("M002", "978-0553418026"),  # Bob borrows The Martian
        ("M003", "978-0061120084"),  # Carol borrows To Kill a Mockingbird
        ("M001", "978-0307277679"),  # Alice borrows The Da Vinci Code (3rd book)
    ]

    for member_id, isbn in borrow_operations:
        try:
            library.borrow_book(member_id, isbn)
            book = library.books[isbn]
            member = next(m for m in library.members if m.member_id == member_id)
            print(f"{member.name} borrowed '{book.title}'")
        except ValueError as e:
            print(f"Failed to borrow: {e}")

    print_books(library, "Books After Borrowing")
    print_members(library, "Members After Borrowing")
    print_library_status(library)

    # Demonstrate borrowing limit
    print_separator("5. TESTING BORROWING LIMIT")
    try:
        library.borrow_book("M001", "978-0743273565")  # Alice tries to borrow 4th book
        print("Alice borrowed 4th book")
    except ValueError as e:
        print(f"Expected error: {e}")

    # Demonstrate book unavailability
    print_separator("6. TESTING BOOK UNAVAILABILITY")
    try:
        library.borrow_book("M002", "978-0134685991")  # Bob tries to borrow already borrowed book
        print("Bob borrowed already borrowed book")
    except ValueError as e:
        print(f"Expected error: {e}")

    # Demonstrate returning books
    print_separator("7. RETURNING BOOKS")
    return_operations = [
        ("M001", "978-0134685991"),  # Alice returns Effective Python
        ("M002", "978-0553418026"),  # Bob returns The Martian
    ]

    for member_id, isbn in return_operations:
        try:
            library.return_book(member_id, isbn)
            book = library.books[isbn]
            member = next(m for m in library.members if m.member_id == member_id)
            print(f"{member.name} returned '{book.title}'")
        except ValueError as e:
            print(f"Failed to return: {e}")

    print_books(library, "Books After Returning")
    print_members(library, "Members After Returning")
    print_library_status(library)

    # Demonstrate searching
    print_separator("8. SEARCHING BOOKS")
    search_queries = ["Python", "Fiction", "Dan Brown", "Sci-Fi"]

    for query in search_queries:
        results = library.search_books(query)
        print(f"\n Search for '{query}':")
        if results:
            for book in results:
                print(f"   - {book.title} by {book.author} ({book.genre})")
        else:
            print("   No books found")

    # Demonstrate updating
    print_separator("9. UPDATING BOOKS AND MEMBERS")

    # Update book
    try:
        library.update_book("978-0134685991", title="Effective Python: 90 Specific Ways to Write Better Python")
        print("Updated book title")
    except ValueError as e:
        print(f"Failed to update book: {e}")

    # Update member
    try:
        library.update_member("M001", email="alice.johnson.new@email.com")
        print("Updated member email")
    except ValueError as e:
        print(f"Failed to update member: {e}")

    print_books(library, "Books After Update")
    print_members(library, "Members After Update")

    # Demonstrate deletion constraints
    print_separator("10. TESTING DELETION CONSTRAINTS")

    # Try to delete borrowed book
    try:
        library.delete_book("978-0132350884")  # Clean Code (still borrowed by Alice)
        print("Deleted borrowed book")
    except ValueError as e:
        print(f"Expected error: {e}")

    # Try to delete member with borrowed books
    try:
        library.delete_member("M001")  # Alice still has borrowed books
        print("Deleted member with borrowed books")
    except ValueError as e:
        print(f"Expected error: {e}")

    # Return remaining books and delete successfully
    print_separator("11. SUCCESSFUL DELETIONS")

    # Return Alice's remaining books
    try:
        library.return_book("M001", "978-0132350884")  # Clean Code
        library.return_book("M001", "978-0307277679")  # The Da Vinci Code
        print("Alice returned all books")
    except ValueError as e:
        print(f"Failed to return books: {e}")

    # Now delete Alice
    try:
        library.delete_member("M001")
        print("Deleted Alice (no borrowed books)")
    except ValueError as e:
        print(f"Failed to delete Alice: {e}")

    # Delete a book with all copies available
    try:
        library.delete_book("978-0743273565")  # The Great Gatsby (not borrowed)
        print("Deleted The Great Gatsby (all copies available)")
    except ValueError as e:
        print(f"Failed to delete book: {e}")

    print_books(library, "Final Books")
    print_members(library, "Final Members")
    print_library_status(library)

    # Demonstrate error handling
    print_separator("12. ERROR HANDLING DEMONSTRATION")

    # Try to add duplicate ISBN
    try:
        library.add_book("978-0134685991", "Duplicate Book", "Author", "Fiction", 1)
        print("Added duplicate ISBN")
    except ValueError as e:
        print(f"Expected error: {e}")

    # Try to add invalid genre
    try:
        library.add_book("978-9999999999", "Invalid Genre Book", "Author", "InvalidGenre", 1)
        print("Added invalid genre book")
    except ValueError as e:
        print(f"Expected error: {e}")

    # Try to add duplicate member ID
    try:
        library.add_member("M002", "Duplicate Member", "duplicate@email.com")
        print("Added duplicate member ID")
    except ValueError as e:
        print(f"Expected error: {e}")

    # Try to add invalid email
    try:
        library.add_member("M999", "Invalid Email", "invalid-email")
        print("Added invalid email")
    except ValueError as e:
        print(f"Expected error: {e}")

    print_separator("DEMO COMPLETED")
    print("The Library Management System demo has been completed successfully!")
    print("All core features have been demonstrated:")
    print("   Adding books and members")
    print("   Borrowing and returning books")
    print("   Searching books")
    print("   Updating books and members")
    print("   Deleting with proper constraints")
    print("   Error handling and validation")
    print("\nThank you for using the Library Management System!")


if __name__ == "__main__":
    main()

