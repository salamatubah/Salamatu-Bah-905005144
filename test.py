"""
Library Management System - Unit Tests
=====================================

This module contains comprehensive unit tests for the Library Management System
using assert statements to verify all functionality and edge cases.

Author: Library Management System
Date: 2024
"""

from operations import Library, Book, Member


def test_add_book_valid_genre():
    """Test 1: Add book with valid genre."""
    print("Running Test 1: Add book with valid genre...")
    library = Library()
    
    # Add a book with valid genre
    result = library.add_book("978-1234567890", "Test Book", "Test Author", "Fiction", 2)
    assert result == True, "Book should be added successfully"
    assert "978-1234567890" in library.books, "Book should be in library"
    assert library.books["978-1234567890"].title == "Test Book", "Book title should match"
    assert library.books["978-1234567890"].available_copies == 2, "Available copies should match total"
    
    print("✅ Test 1 PASSED: Book with valid genre added successfully")


def test_add_book_invalid_genre():
    """Test 2: Add book with invalid genre (should fail)."""
    print("Running Test 2: Add book with invalid genre...")
    library = Library()
    
    # Try to add book with invalid genre
    try:
        library.add_book("978-1234567890", "Test Book", "Test Author", "InvalidGenre", 2)
        assert False, "Should have raised ValueError for invalid genre"
    except ValueError as e:
        assert "Invalid genre" in str(e), "Error message should mention invalid genre"
        assert "978-1234567890" not in library.books, "Book should not be added to library"
    
    print("✅ Test 2 PASSED: Invalid genre correctly rejected")


def test_borrow_book_successfully():
    """Test 3: Borrow book successfully."""
    print("Running Test 3: Borrow book successfully...")
    library = Library()
    
    # Add book and member
    library.add_book("978-1234567890", "Test Book", "Test Author", "Fiction", 2)
    library.add_member("M001", "Test Member", "test@email.com")
    
    # Borrow book
    result = library.borrow_book("M001", "978-1234567890")
    assert result == True, "Book should be borrowed successfully"
    
    # Check book availability
    book = library.books["978-1234567890"]
    assert book.available_copies == 1, "Available copies should decrease by 1"
    assert book.total_copies == 2, "Total copies should remain unchanged"
    
    # Check member's borrowed books
    member = library.members[0]
    assert "978-1234567890" in member.borrowed_books, "Book should be in member's borrowed list"
    assert len(member.borrowed_books) == 1, "Member should have 1 borrowed book"
    
    print("✅ Test 3 PASSED: Book borrowed successfully")


def test_borrow_more_than_3_books():
    """Test 4: Borrow more than 3 books (should fail)."""
    print("Running Test 4: Borrow more than 3 books...")
    library = Library()
    
    # Add member and 4 books
    library.add_member("M001", "Test Member", "test@email.com")
    library.add_book("978-0000000001", "Book 1", "Author 1", "Fiction", 1)
    library.add_book("978-0000000002", "Book 2", "Author 2", "Fiction", 1)
    library.add_book("978-0000000003", "Book 3", "Author 3", "Fiction", 1)
    library.add_book("978-0000000004", "Book 4", "Author 4", "Fiction", 1)
    
    # Borrow first 3 books successfully
    library.borrow_book("M001", "978-0000000001")
    library.borrow_book("M001", "978-0000000002")
    library.borrow_book("M001", "978-0000000003")
    
    # Try to borrow 4th book (should fail)
    try:
        library.borrow_book("M001", "978-0000000004")
        assert False, "Should have raised ValueError for exceeding borrowing limit"
    except ValueError as e:
        assert "maximum borrowing limit" in str(e), "Error message should mention borrowing limit"
        assert "978-0000000004" not in library.members[0].borrowed_books, "4th book should not be borrowed"
        assert len(library.members[0].borrowed_books) == 3, "Member should have exactly 3 borrowed books"
    
    print("✅ Test 4 PASSED: Borrowing limit correctly enforced")


def test_delete_book_that_is_borrowed():
    """Test 5: Delete book that's borrowed (should fail)."""
    print("Running Test 5: Delete book that's borrowed...")
    library = Library()
    
    # Add book and member, then borrow book
    library.add_book("978-1234567890", "Test Book", "Test Author", "Fiction", 2)
    library.add_member("M001", "Test Member", "test@email.com")
    library.borrow_book("M001", "978-1234567890")
    
    # Try to delete borrowed book (should fail)
    try:
        library.delete_book("978-1234567890")
        assert False, "Should have raised ValueError for deleting borrowed book"
    except ValueError as e:
        assert "currently borrowed" in str(e), "Error message should mention book is borrowed"
        assert "978-1234567890" in library.books, "Book should still be in library"
    
    print("✅ Test 5 PASSED: Cannot delete borrowed book")


def test_return_book_and_verify_availability():
    """Test 6: Return book and verify availability update."""
    print("Running Test 6: Return book and verify availability...")
    library = Library()
    
    # Add book and member, then borrow book
    library.add_book("978-1234567890", "Test Book", "Test Author", "Fiction", 3)
    library.add_member("M001", "Test Member", "test@email.com")
    library.borrow_book("M001", "978-1234567890")
    
    # Verify book is borrowed
    book = library.books["978-1234567890"]
    member = library.members[0]
    assert book.available_copies == 2, "Available copies should be 2 after borrowing 1"
    assert "978-1234567890" in member.borrowed_books, "Book should be in borrowed list"
    
    # Return book
    result = library.return_book("M001", "978-1234567890")
    assert result == True, "Book should be returned successfully"
    
    # Verify availability updated
    assert book.available_copies == 3, "Available copies should be back to 3"
    assert "978-1234567890" not in member.borrowed_books, "Book should not be in borrowed list"
    assert len(member.borrowed_books) == 0, "Member should have no borrowed books"
    
    print("✅ Test 6 PASSED: Book returned and availability updated")


def test_add_member_duplicate_id():
    """Test 7: Add member with duplicate ID (should fail)."""
    print("Running Test 7: Add member with duplicate ID...")
    library = Library()
    
    # Add first member
    library.add_member("M001", "First Member", "first@email.com")
    assert len(library.members) == 1, "Should have 1 member"
    
    # Try to add member with same ID (should fail)
    try:
        library.add_member("M001", "Second Member", "second@email.com")
        assert False, "Should have raised ValueError for duplicate member ID"
    except ValueError as e:
        assert "already exists" in str(e), "Error message should mention member already exists"
        assert len(library.members) == 1, "Should still have only 1 member"
        assert library.members[0].name == "First Member", "Original member should be unchanged"
    
    print("✅ Test 7 PASSED: Duplicate member ID correctly rejected")


def test_search_books():
    """Test 8: Search books by title and author."""
    print("Running Test 8: Search books...")
    library = Library()
    
    # Add multiple books
    library.add_book("978-1111111111", "Python Programming", "John Doe", "Non-Fiction", 1)
    library.add_book("978-2222222222", "Java Guide", "Jane Smith", "Non-Fiction", 1)
    library.add_book("978-3333333333", "Advanced Python", "John Doe", "Non-Fiction", 1)
    library.add_book("978-4444444444", "Fiction Novel", "Alice Johnson", "Fiction", 1)
    
    # Search by title
    python_books = library.search_books("Python")
    assert len(python_books) == 2, "Should find 2 Python books"
    assert any(book.title == "Python Programming" for book in python_books), "Should find Python Programming"
    assert any(book.title == "Advanced Python" for book in python_books), "Should find Advanced Python"
    
    # Search by author
    john_books = library.search_books("John Doe")
    assert len(john_books) == 2, "Should find 2 books by John Doe"
    
    # Search by partial match
    guide_books = library.search_books("Guide")
    assert len(guide_books) == 1, "Should find 1 book with 'Guide' in title"
    assert guide_books[0].title == "Java Guide", "Should find Java Guide"
    
    # Search with no results
    no_results = library.search_books("NonExistent")
    assert len(no_results) == 0, "Should find no books for non-existent search"
    
    print("✅ Test 8 PASSED: Book search functionality works correctly")


def test_update_operations():
    """Test 9: Update book and member information."""
    print("Running Test 9: Update operations...")
    library = Library()
    
    # Add book and member
    library.add_book("978-1234567890", "Original Title", "Original Author", "Fiction", 2)
    library.add_member("M001", "Original Name", "original@email.com")
    
    # Update book
    library.update_book("978-1234567890", title="Updated Title", author="Updated Author")
    book = library.books["978-1234567890"]
    assert book.title == "Updated Title", "Book title should be updated"
    assert book.author == "Updated Author", "Book author should be updated"
    assert book.genre == "Fiction", "Book genre should remain unchanged"
    
    # Update member
    library.update_member("M001", name="Updated Name", email="updated@email.com")
    member = library.members[0]
    assert member.name == "Updated Name", "Member name should be updated"
    assert member.email == "updated@email.com", "Member email should be updated"
    
    print("✅ Test 9 PASSED: Update operations work correctly")


def test_delete_member_with_borrowed_books():
    """Test 10: Delete member with borrowed books (should fail)."""
    print("Running Test 10: Delete member with borrowed books...")
    library = Library()
    
    # Add book and member, then borrow book
    library.add_book("978-1234567890", "Test Book", "Test Author", "Fiction", 1)
    library.add_member("M001", "Test Member", "test@email.com")
    library.borrow_book("M001", "978-1234567890")
    
    # Try to delete member with borrowed books (should fail)
    try:
        library.delete_member("M001")
        assert False, "Should have raised ValueError for deleting member with borrowed books"
    except ValueError as e:
        assert "borrowed books" in str(e), "Error message should mention borrowed books"
        assert len(library.members) == 1, "Member should still be in library"
    
    # Return book and then delete member (should succeed)
    library.return_book("M001", "978-1234567890")
    library.delete_member("M001")
    assert len(library.members) == 0, "Member should be deleted after returning books"
    
    print("✅ Test 10 PASSED: Member deletion constraints work correctly")


def run_all_tests():
    """Run all unit tests."""
    print("🧪 Starting Library Management System Unit Tests")
    print("=" * 60)
    
    tests = [
        test_add_book_valid_genre,
        test_add_book_invalid_genre,
        test_borrow_book_successfully,
        test_borrow_more_than_3_books,
        test_delete_book_that_is_borrowed,
        test_return_book_and_verify_availability,
        test_add_member_duplicate_id,
        test_search_books,
        test_update_operations,
        test_delete_member_with_borrowed_books
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"❌ {test.__name__} FAILED: {e}")
            failed += 1
        except Exception as e:
            print(f"❌ {test.__name__} ERROR: {e}")
            failed += 1
    
    print("\n" + "=" * 60)
    print(f"📊 Test Results: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("🎉 All tests passed! The Library Management System is working correctly.")
    else:
        print("⚠️  Some tests failed. Please check the implementation.")
    
    return failed == 0


if __name__ == "__main__":
    run_all_tests()

