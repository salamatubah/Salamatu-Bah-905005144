"""
Library Management System - Core Operations
==========================================

This module contains the core classes for the Library Management System:
- Book: Represents individual books with ISBN, title, author, genre, and copy information
- Member: Represents library members with ID, name, email, and borrowed books
- Library: Main class managing books, members, and all CRUD operations

"""

import re
from typing import Dict, List, Optional, Tuple


class Book:
    def __init__(self, isbn: str, title: str, author: str, genre: str, total_copies: int):
        if total_copies <= 0:
            raise ValueError("Total copies must be a positive integer")
            
        self.isbn = isbn
        self.title = title
        self.author = author
        self.genre = genre
        self.total_copies = total_copies
        self.available_copies = total_copies
    
    def __str__(self) -> str:
        """Return string representation of the book."""
        return f"Book(ISBN: {self.isbn}, Title: {self.title}, Author: {self.author}, Genre: {self.genre}, Available: {self.available_copies}/{self.total_copies})"
    
    def __repr__(self) -> str:
        """Return detailed string representation of the book."""
        return self.__str__()


class Member:
    """
    Represents a library member.

    Attributes:
        member_id (str): Unique identifier for the member
        name (str): Full name of the member
        email (str): Email address of the member
        borrowed_books (List[str]): List of ISBNs of currently borrowed books
    """

    def __init__(self, member_id: str, name: str, email: str):
        """
        Initialize a new Member instance.
        
        Args:
            member_id (str): Unique identifier for the member
            name (str): Full name of the member
            email (str): Email address of the member
            
        Raises:
            ValueError: If email format is invalid
        """
        if not self._is_valid_email(email):
            raise ValueError("Invalid email format")
            
        self.member_id = member_id
        self.name = name
        self.email = email
        self.borrowed_books = []
    
    def _is_valid_email(self, email: str) -> bool:
        """
        Validate email format using regex.
        
        Args:
            email (str): Email address to validate
            
        Returns:
            bool: True if email format is valid, False otherwise
        """
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def __str__(self) -> str:
        """Return string representation of the member."""
        return f"Member(ID: {self.member_id}, Name: {self.name}, Email: {self.email}, Borrowed: {len(self.borrowed_books)} books)"
    
    def __repr__(self) -> str:
        """Return detailed string representation of the member."""
        return self.__str__()


class Library:
    """
    Main library management class handling all operations.
    
    Attributes:
        books (Dict[str, Book]): Dictionary mapping ISBN to Book objects
        members (List[Member]): List of Member objects
        genres (Tuple[str, ...]): Tuple of valid genres
    """
    
    def __init__(self):
        """Initialize an empty library."""
        self.books: Dict[str, Book] = {}
        self.members: List[Member] = []
        self.genres = ("Fiction", "Non-Fiction", "Sci-Fi", "Mystery", "Biography", "Romance", "Thriller", "History")
    
    def add_book(self, isbn: str, title: str, author: str, genre: str, total_copies: int) -> bool:
        """
        Add a new book to the library.
        
        Args:
            isbn (str): Unique identifier for the book
            title (str): Title of the book
            author (str): Author of the book
            genre (str): Genre of the book
            total_copies (int): Total number of copies available
            
        Returns:
            bool: True if book was added successfully, False otherwise
            
        Raises:
            ValueError: If ISBN already exists or genre is invalid
        """
        if isbn in self.books:
            raise ValueError(f"Book with ISBN {isbn} already exists")
        
        if genre not in self.genres:
            raise ValueError(f"Invalid genre. Valid genres are: {', '.join(self.genres)}")
        
        try:
            book = Book(isbn, title, author, genre, total_copies)
            self.books[isbn] = book
            return True
        except ValueError as e:
            raise ValueError(f"Failed to add book: {str(e)}")
    
    def add_member(self, member_id: str, name: str, email: str) -> bool:
        """
        Add a new member to the library.
        
        Args:
            member_id (str): Unique identifier for the member
            name (str): Full name of the member
            email (str): Email address of the member
            
        Returns:
            bool: True if member was added successfully, False otherwise
            
        Raises:
            ValueError: If member ID already exists or email is invalid
        """
        if any(member.member_id == member_id for member in self.members):
            raise ValueError(f"Member with ID {member_id} already exists")
        
        try:
            member = Member(member_id, name, email)
            self.members.append(member)
            return True
        except ValueError as e:
            raise ValueError(f"Failed to add member: {str(e)}")
    
    def search_books(self, query: str) -> List[Book]:
        """
        Search for books by title or author (case-insensitive).
        
        Args:
            query (str): Search query for title or author
            
        Returns:
            List[Book]: List of matching books
        """
        query_lower = query.lower()
        results = []
        
        for book in self.books.values():
            if (query_lower in book.title.lower() or 
                query_lower in book.author.lower()):
                results.append(book)
        
        return results
    
    def update_book(self, isbn: str, **kwargs) -> bool:
        """
        Update book details.
        
        Args:
            isbn (str): ISBN of the book to update
            **kwargs: Keyword arguments for fields to update (title, author, genre, total_copies)
            
        Returns:
            bool: True if book was updated successfully, False otherwise
            
        Raises:
            ValueError: If book not found or invalid update data
        """
        if isbn not in self.books:
            raise ValueError(f"Book with ISBN {isbn} not found")
        
        book = self.books[isbn]
        
        # Update allowed fields
        if 'title' in kwargs:
            book.title = kwargs['title']
        
        if 'author' in kwargs:
            book.author = kwargs['author']
        
        if 'genre' in kwargs:
            if kwargs['genre'] not in self.genres:
                raise ValueError(f"Invalid genre. Valid genres are: {', '.join(self.genres)}")
            book.genre = kwargs['genre']
        
        if 'total_copies' in kwargs:
            new_total = kwargs['total_copies']
            if new_total <= 0:
                raise ValueError("Total copies must be a positive integer")
            
            # Adjust available copies if needed
            borrowed_count = book.total_copies - book.available_copies
            if new_total < borrowed_count:
                raise ValueError(f"Cannot reduce total copies below currently borrowed count ({borrowed_count})")
            
            book.total_copies = new_total
            book.available_copies = new_total - borrowed_count
        
        return True
    
    def update_member(self, member_id: str, **kwargs) -> bool:
        """
        Update member information.
        
        Args:
            member_id (str): ID of the member to update
            **kwargs: Keyword arguments for fields to update (name, email)
            
        Returns:
            bool: True if member was updated successfully, False otherwise
            
        Raises:
            ValueError: If member not found or invalid update data
        """
        member = self._find_member_by_id(member_id)
        if not member:
            raise ValueError(f"Member with ID {member_id} not found")
        
        if 'name' in kwargs:
            member.name = kwargs['name']
        
        if 'email' in kwargs:
            if not member._is_valid_email(kwargs['email']):
                raise ValueError("Invalid email format")
            member.email = kwargs['email']
        
        return True
    
    def delete_book(self, isbn: str) -> bool:
        """
        Delete a book from the library.
        
        Args:
            isbn (str): ISBN of the book to delete
            
        Returns:
            bool: True if book was deleted successfully, False otherwise
            
        Raises:
            ValueError: If book not found or currently borrowed
        """
        if isbn not in self.books:
            raise ValueError(f"Book with ISBN {isbn} not found")
        
        book = self.books[isbn]
        
        # Check if all copies are available (not borrowed)
        if book.available_copies != book.total_copies:
            raise ValueError(f"Cannot delete book {isbn} - some copies are currently borrowed")
        
        del self.books[isbn]
        return True
    
    def delete_member(self, member_id: str) -> bool:
        """
        Delete a member from the library.
        
        Args:
            member_id (str): ID of the member to delete
            
        Returns:
            bool: True if member was deleted successfully, False otherwise
            
        Raises:
            ValueError: If member not found or has borrowed books
        """
        member = self._find_member_by_id(member_id)
        if not member:
            raise ValueError(f"Member with ID {member_id} not found")
        
        if member.borrowed_books:
            raise ValueError(f"Cannot delete member {member_id} - they have {len(member.borrowed_books)} borrowed books")
        
        self.members.remove(member)
        return True
    
    def borrow_book(self, member_id: str, isbn: str) -> bool:
        """
        Borrow a book for a member.
        
        Args:
            member_id (str): ID of the member borrowing the book
            isbn (str): ISBN of the book to borrow
            
        Returns:
            bool: True if book was borrowed successfully, False otherwise
            
        Raises:
            ValueError: If member/book not found, member has max books, or book unavailable
        """
        member = self._find_member_by_id(member_id)
        if not member:
            raise ValueError(f"Member with ID {member_id} not found")
        
        if isbn not in self.books:
            raise ValueError(f"Book with ISBN {isbn} not found")
        
        book = self.books[isbn]
        
        # Check if member has reached borrowing limit
        if len(member.borrowed_books) >= 3:
            raise ValueError(f"Member {member_id} has reached the maximum borrowing limit of 3 books")
        
        # Check if book is available
        if book.available_copies <= 0:
            raise ValueError(f"Book {isbn} is not available for borrowing")
        
        # Check if member already has this book
        if isbn in member.borrowed_books:
            raise ValueError(f"Member {member_id} already has book {isbn}")
        
        # Borrow the book
        member.borrowed_books.append(isbn)
        book.available_copies -= 1
        
        return True
    
    def return_book(self, member_id: str, isbn: str) -> bool:
        """
        Return a borrowed book.
        
        Args:
            member_id (str): ID of the member returning the book
            isbn (str): ISBN of the book to return
            
        Returns:
            bool: True if book was returned successfully, False otherwise
            
        Raises:
            ValueError: If member/book not found or member doesn't have the book
        """
        member = self._find_member_by_id(member_id)
        if not member:
            raise ValueError(f"Member with ID {member_id} not found")
        
        if isbn not in self.books:
            raise ValueError(f"Book with ISBN {isbn} not found")
        
        if isbn not in member.borrowed_books:
            raise ValueError(f"Member {member_id} does not have book {isbn}")
        
        # Return the book
        member.borrowed_books.remove(isbn)
        self.books[isbn].available_copies += 1
        
        return True
    
    def _find_member_by_id(self, member_id: str) -> Optional[Member]:
        """
        Find a member by their ID.
        
        Args:
            member_id (str): ID of the member to find
            
        Returns:
            Optional[Member]: Member object if found, None otherwise
        """
        for member in self.members:
            if member.member_id == member_id:
                return member
        return None
    
    def get_library_status(self) -> Dict:
        """
        Get current library status.
        
        Returns:
            Dict: Dictionary containing library statistics
        """
        total_books = len(self.books)
        total_members = len(self.members)
        total_copies = sum(book.total_copies for book in self.books.values())
        available_copies = sum(book.available_copies for book in self.books.values())
        borrowed_copies = total_copies - available_copies
        
        return {
            'total_books': total_books,
            'total_members': total_members,
            'total_copies': total_copies,
            'available_copies': available_copies,
            'borrowed_copies': borrowed_copies
        }
    
    def list_all_books(self) -> List[Book]:
        """
        Get a list of all books in the library.
        
        Returns:
            List[Book]: List of all Book objects
        """
        return list(self.books.values())
    
    def list_all_members(self) -> List[Member]:
        """
        Get a list of all members in the library.
        
        Returns:
            List[Member]: List of all Member objects
        """
        return self.members.copy()

