import pandas as pd
import logging
logging.basicConfig(level=logging.ERROR)
from user import UsersManager
from book import BooksManager

class CheckManager():
    """
    Used to show borrowing and returning of books in a library. This is based on the "Users.csv" dataframe

    Functionalities:
    1. __init__ := loads the users_df dataframe, making it available for rest of code
    2. all_borrowed_book := outputs list of all borrowed books
    3. borrow_a_book := handles everything related to borrowing of a book
    4.     borrow_book_internal :=  the internal code that is run when we borrow a book
    5. return_a_book := handles everything related to returning of a book
    6.     return_book_internal :=  the internal code that is run when we return a book
    """
    #intialises users_df
    def __init__(self,user_df):
        """
        all operations are performed on the user_df dataset, which is first read from "Users.csv".
        Inputs:
        pandas_data_frame, is the dataframe read from Users.csv file
        """
        self.users_df=user_df
        self.user_obj=UsersManager()
        self.book_obj=BooksManager()
    
    # outputs list of all borrowed books
    def all_borrowed_book(self,id):
        """
        Given user id number, it will return a list of all teh books borrowed
        Note: id send here would have to be already validated

        Input:
        id, string

        Output:
        list_of_all_borrowed_books, type=list
        """
        borrowed_books_string=(self.users_df.loc[self.users_df['id'] == id, 'Borrowed'].fillna("").astype(str).values[0])
        list_of_all_borrowed_books=borrowed_books_string.split("-")
        #remove "" from list_of_all_borrowed
        list_of_all_borrowed_books=[book for book in list_of_all_borrowed_books if book.strip()!=""]
        return (list_of_all_borrowed_books)
        # print(type(borrowed_books))
        
    #the internal code that is run when we borrow a book.
    def borrow_book_internal(self,borrower_id,book_id):
        """
        method to add a book under borrowed corresponding to user
        Rules:
        1. a person can add a maximim of 10 books. 
        2. You are only allowed one copy of a book
        Note: borrower_id and book_id inputed would have to be already validated
        
        Args: 
        borrower_id=string
        book_id=string

        Return:
        False if any of the above rules fail.
        
        if rules are satisfied, adds bool_id to the users.csv file under
        "Borrow" column if existing books borrowed is less than 10
        """
        #enter the id of the person that wants to borrow a book, validate
        #check if he has crossed max borrowing cap of 10 books
        #if not, get the ISBN from user, validate it, presence in the isbn 
        # check if ISBN
        # Let the valdiatoisn be taken care of by the library manager

        #check if max borrowing of 10 reached
        already_borrowed_books=self.all_borrowed_book(borrower_id)
        # check if the person has already borrowed the same book, only one per person
        if book_id in already_borrowed_books:
            logging.error("only one copy of a book per person")
            return False

        if len(already_borrowed_books)<10:
            
            already_borrowed_books.append(book_id)
            #conver from list to string to store in .csv file
            output="-".join(already_borrowed_books)
            self.users_df.loc[self.users_df['id']==borrower_id,'Borrowed']=output
            print(self.users_df)

            logging.info("saving to users.csv file")
            # Saving to .csv file
            self.save_user_df_to_csv()   
            logging.info("saved")
        else:
            print("You have reached max borrowig capacity of 10 books")
            return False
    
    # the internal code that is run when we return a book
    def return_book_internal(self,borrower_id,book_id):
        """
        returns a book that was already borrowed
        Rules:
        1. the bookid needs to be present in the already borrowed book list
        
        Args: 
        borrower_id=string
        book_id=string

        Return:
        False if any of the above rules fail.
        
        if rules are satisfied, removes bool_id from users.csv
        """
        already_borrowed_books=self.all_borrowed_book(borrower_id)
        # check if the person has borrowed this book
        if not (book_id in already_borrowed_books):
            logging.error("the person has not borrowed this book, recheck inputs")
            return False
        logging.info("borrowed book is present in the borrowed_list")
        already_borrowed_books.remove(book_id)
        output="-".join(already_borrowed_books)
        self.users_df.loc[self.users_df['id']==borrower_id,'Borrowed']=output
        print(self.users_df)

        logging.info("saving to users.csv file")
        # Saving to .csv file
        self.save_user_df_to_csv()   
        logging.info("saved")

    # handles everything related to borrowing of a book
    def borrow_a_book(self):
        """
        Handles complete process of borrowing a book

        Takes input from user to get borrower_id and book_id via CLI
        
        Input:
        borrow_id, book_id := both are string type inputed dynamically via CLI

        Return:
        Nothing is returned, content saved to Users.csv file
        """
        def input_borrower_id():
            borrower_id=input("enter Borrower's complete userID")
            # validate inputs
            if not(self.user_obj.validate_id(borrower_id)):
                logging.error("invalid input, try again")
                print("invalid input, try again")
                return input_borrower_id()
            borrower_id=self.user_obj.validate_id(borrower_id)
            return borrower_id
        
            # apply to borrow_book_internal
        def input_book_id():
            book_id=input("enter complete bookID")
            # validate inputs
            if not(self.book_obj.validate_isbn(book_id)):
                logging.error("invalid input, try again")
                print("invalid input, try again")
                return input_book_id()
            book_id=self.book_obj.validate_isbn(book_id)
            return book_id
        
        borrower_id=input_borrower_id()
        book_id=input_book_id()
        self.borrow_book_internal(borrower_id,book_id)
    
    # handles everything related to returning of a book
    def return_a_book(self):
        """
        Handles complete process of retuning a book

        Takes input from user to get borrower_id and book_id via CLI
        
        Input:
        borrow_id, book_id := both are string type inputed dynamically via CLI

        Return:
        Nothing is returned, content saved to Users.csv file
        """

        def input_borrower_id():
            borrower_id=input("enter Borrower's complete userID")
            # validate inputs
            if not(self.user_obj.validate_id(borrower_id)):
                logging.error("invalid input, try again")
                print("invalid input, try again")
                return input_borrower_id()
            borrower_id=self.user_obj.validate_id(borrower_id)
            return borrower_id
        
            # apply to borrow_book_internal
        def input_book_id():
            book_id=input("enter complete bookID")
            # validate inputs
            if not(self.book_obj.validate_isbn(book_id)):
                logging.error("invalid input, try again")
                print("invalid input, try again")
                return input_book_id()
            book_id=self.book_obj.validate_isbn(book_id)
            return book_id
        
        borrower_id=input_borrower_id()
        book_id=input_book_id()
        self.return_book_internal(borrower_id,book_id)

