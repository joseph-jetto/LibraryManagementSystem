import pandas as pd
import regex
import random
import logging
from utilities import LibraryMangUntilities


# Configure logging to show INFO and above
logging.basicConfig(level=logging.ERROR)



class BooksManager(LibraryMangUntilities):
    """
    used to manage the following data about book:
    1. ISBN: unique 17char string assigned to each book
    2. Title: Title of the book
    3. Author's name: Name of the author

    Functionalities:
    1. validate_isbn := checks validity of entered isbn
    2. validate_title := checks validity of validate_title
    3. search_among_book_attributes := searches for rows with matching string
    3.1 search_isbn := search by isbn value
    3.2 search_author := search by authors name
    3.3 searc_title := searches by title
    4. generate_unique_isbn := generate unique_isbn value
    5. update_an_existing_book_detail := update value in a row
    6. list_all_book := list all contents to CLI
    7. check_if_book_exists_using_isbn :=validity of isbn
    8. check_if_book_exists_using_title_author := validity using title/author
    9. check_if_book_exists_using_isbn_title_author  := validity using isbn/title/author
    10. add_a_book := add a new row
    11. delete_a_book_based_on_isbn := deletes a record
    12. save_book_df_to_csv := save to .csv file
    """
    # initialise
    def __init__(self):
        pass
    
    # checks validity of entered isbn
    def validate_isbn(self,isbn):
        """
        Used to validate the isbn
        Rules 
        1. max length should be 17 including the prefix isbn
        2. type is string
        3. characters after prefix "isbn" must be digits

        Input:
        isbn, a string 17chars long

        Return:
        False, type=bool ;if validation fails
        isbn, type=string ; if validation success
        """
        #removing trailing spaces
        isbn=isbn.strip()

        #format string
        if not self.format_string(isbn):
            return False
        isbn=self.format_string(isbn)

        #check if empty or spaces
        if isbn=="":
            error_message="\nError: isbn cannot be whitespaces or simply empty, try again....\n"
            logging.error(error_message)
            return False
        #check "ISBN" as prefix
        if isbn[:4]!="isbn":
            # print(isbn[:4])
            logging.error("prefix is not isbn")
            return False
        #check that its only numbers
        if not isbn[4:].isdigit():
            error_message="\nError: Ensure only numbers are entered, try again....\n"
            logging.error(error_message)
            # if input failed, we ask for input again
            return False

        # check if max length exceed 13
        if len(isbn)!=17:
            error_message="\nError: The required length is 13, try again\n"
            logging.error(error_message)
            return False
        # # check if another row has the same isbn
        # if not self.books_df[self.books_df['isbn']==isbn].empty:
        #     error_message="\nError: duplicate isbn exits in library"
        #     logging.error(error_message)
        #     return False
        return isbn

    # checks validity of validate_title
    def validate_title(self,title):
        # check if formating is possible
        logging.info("check if formating is possible")
        if not self.format_string(title):
            logging.error("formating of string not possible")
            return False
        logging.info("formatting successful")
        title=self.format_string(title)


        #set max length limit for a name, should not exceed 255 chars
        if len(title)>255:
            error_message="title should have max 255 characters"
            logging.error(error_message)
            return False
        
        logging.info("Title length under 255")
        
        # check if input is in ascii
        if not title.isascii():
            error_message="Use only basic English letters and symbols."
            logging.info(error_message)
            return False

        # remove extra spaces in between words "The Great   Gatsby"
        title=" ".join(title.split())
        logging.info("removed spaces in between")

        #the title needs to have length of alteast 2 and these should alphabets
        if len(title)<=1:
            error_message="Title should have atleast 2 alphabets"
            logging.info(error_message)
            return False
        
        logging.info("Title valdiation successfull")
        #We should be left with the processed string
        return title

    # searches for rows with matching string
    def search_among_book_attributes(self):
        """
        searches for books based on input query. this query can be any attribute amoing
        1. isbn
        2. Title
        3. Author

        Rules:
        1. You can enter a part of the isbn, Title or Author as a substring and all the rows that has it as a substring will be outputed
        
        Input: 
        one among 1.isbn, 2.Title, 3. Author as user input
            Input: enter whole string or substring as input
        
        Output:
        Rows that qualify the seach is printed on to the terminal
        """
        # choose the attributes you want to search by, input the values, validate it according to the type
        # 

        print("\n Choose among the attributes to search from:")
        print("1. isbn")
        print("2. Title")
        print("3. Author")
        # storing option number with attribute for easy access
        attribute_dict={1:"isbn",2:"Title",3:"Author"}
        # getting the input from user, converting from string to int
        selected_attribute= input("Enter corresponding number: ")
        # validate the input to be one among [1,2,3]
        try:
            # converting from string to int
            selected_attribute=int(selected_attribute)
            if selected_attribute not in [1,2,3]:
                logging.error("\nIncorrect input, choose among 1,2,3 only. Try again...")
            print(f"You have chosen {selected_attribute}. {attribute_dict.get(selected_attribute, 'Incorrect input, choose among 1, 2, 3 only. Try again...')}")
        except ValueError:
            logging.error("\nIncorrect input, choose among 1,2,3 only. Try again...")
            self.search_among_book_attributes()

        if selected_attribute==1:
            #search by isbn value
            logging.info("isbn search selected")
            self.search_isbn()
        elif selected_attribute==2:
            #search by titles
            logging.info("Title search selected")
            self.search_title()
        elif selected_attribute==3:
            #search by author's name
            logging.info("author search selected")
            self.search_author()

    # search by isbn value
    def search_isbn(self):
        """
        Used to search the library based on isbn number
        Rules:
        1. only numbers are inputed, prefix of "isbn" NOT to be inputed
        2. since max length for  isbn is 13 digits, the input should not exceed that

        Returns:
        It does not return anything, it prints all rows that contain the entered string or substring to the terminal
        """
        #Get isbn value as input from user
        sub_string=input("enter the whole or partial isbn number to search for, (DO NOT include isbn as prefix): ")
        
        # Validate the input
        #removing trailing spaces
        sub_string=sub_string.strip()

        #check if empty or spaces
        if sub_string=="":
            logging.error("\nError: input cannot be whitespaces or simpy empty, try again....\n")
            #if input fails, we asks for input again
            self.search_isbn()

        #check that its only numbers
        if not sub_string.isdigit():
            logging.error("\nError: Ensure only numbers are entered, try again....\n")
            # if input failed, we ask for input again
            self.search_isbn()

        # check if max length exceed 13
        if len(sub_string)>13:
            logging.error("\nError: The max possible input length is 13, try again\n")
            self.search_isbn()
        
        #search for said substring in the isbn col of the dataframe
        # print(self.books_df[self.books_df["isbn"].str.contains(sub_string,case=False,na=False)])
        
        output=self.books_df[self.books_df["isbn"].str.contains(sub_string,case=False,na=False)]
        
        # if no match found
        if (output.empty):
            error_message="Tried searching, no match found"
            logging.error(error_message)
            return self.search_isbn()
        logging.info("sub_string match found under isbn")
        print(output)
   
    # search by authors name    
    def search_author(self):
        """
        Used to search for a string or substring within the column "Author"
        Rules:
        1. same validation rules from validate_name() function applies here, refer to validate_name's docstring

        Input:
        input is taken from user

        Return:
        Nothing is returned, rows that satisfies condition printed to screen
        """ 
        print("""
    Rule:
        1. only Alphabets (A-Z) (a-z) are allowed,
        2. ambersand and dot are allowed as special characters
        3. The name should have atleast 2 characters, and both should be alphabets
        4. Numbers are not allowed
        5. dorts not allowed within words, example da.n     Brown 
        6. trailing dots from end like MRS. DR. 'Dr. .Ram. will be automatically removed
        7. only ASCII inputs
        8. max 255 chars""")
        #take authors name as input from user
        sub_str=input("Enter partial or full name: ")
        # validate the name
        if not self.validate_name(sub_str):
            print("="*50)
            print("Invalid input, please follow naming rules")
            print("="*50)
            self.search_author()

        sub_str=self.validate_name(sub_str)

        output=self.users_df[self.users_df["Author"].str.contains(sub_str)]
        
        # if no match found
        if (output.empty):
            error_message="Tried searching, no match found"
            print(error_message)
            print("="*50)
            logging.error(error_message)
            return self.search_name()
        logging.info("sub_string match found under Names name")
        print(output)

# searches by title
    def search_title(self):
        """
        Used to search for a string or substring within the column "Title"
        Rules:
        1. same validation rules from validate_title() function applies here, refer to validate_title's docstring

        Input:
        input is taken from user

        Return:
        Nothing is returned, rows that satisfies condition printed to screen
        """ 
        #take authors name as input from user
        sub_str=input("Enter partial or full Title: ")
        # validate the name
        # sub_str=self.validate_title(sub_str)

        if not self.validate_title(sub_str):
            print("="*50)
            print("Invalid input, please follow Title rules")
            print("="*50)
            self.search_title()

        sub_str=self.validate_title(sub_str)



        # search for substring in column Author
        output=self.books_df[self.books_df["Title"].str.contains(sub_str)]
        
        # if no match found
        if output.empty:
            error_message="Tried searching, no match found\n"
            logging.error(error_message)
            return self.search_title()
        logging.info("sub_string match found under Title name")
        #printing matches
        print(output)

# generate unique_isbn value 
    def generate_unique_isbn(self):
        """
        isbn is an system generated unique id given to each book to identify it in the library

        The function generates an unique unique 17char isbn value for every new book entered into library
        Rules:
        1. we have to check isbn in the dataset before assigning to prevent duplicates 

        Output:
        isbn
        type: string
        
        """
        def unique_isbn():
            """
            generates the 13 digit isbn with the prefix "isbn", Totalling a 17 char long string

            This is used in generate_unique_isbn function. Its nested to follow DRY principles

            Output:
            isbn
            type: string

            """
            isbn="isbn"+"".join([str(random.randint(0,9)) for i in range(13)])
            return isbn
            
    
        #generated number with the prefix isbn
        isbn=unique_isbn()

        #check for duplicates
        while isbn in self.books_df["isbn"]:
            isbn=unique_isbn()
        
        return isbn

# update value in a row    
    def update_an_existing_book_detail(self):
        """
        Used to update an existing book record, using the user inputed ISBN values
        from CLI

        Input:
        No inputs args, but input take running run time from CLI
        Return:
        Does not return anything, but prints to screen
        """

        input_isbn=input("Enter ISBN number: ")
        if not self.validate_isbn(input_isbn):
            logging.error("entered ISBN value does not exist")
            print("-"*20)
            print("1. Enter ISBN number again")
            print("2. Exit")
            print("-"*20)
            choice=input("Enter Choice number: ")
            if not self.validate_choice_and_available_choices(choice,['1','2']):
                logging.info("validation failed")
                print("Ensure entered choice is among the available choices")
            if choice.strip()=="1":
                # we try again
                self.update_an_existing_book_detail()
                #isbn valdiated
            if choice.strip()=="2":
                logging.info("Exiting")
                return

        input_isbn=self.validate_isbn(input_isbn)
        print("ISBN value inputed exists in library, proceed to update details")

        # the updated book name
        def get_new_title_and_validate_it():
            """
            Gets name as input from the user via CLI and provices option to try again

            Input:
            No Args, inputs are taken dynamically via CLI

            Output:
            name, type=string
            """
            new_book_name=input("Enter new title: ")
            if not self.validate_title(new_book_name):
                logging.error("failed to validate new title")
                print("The entered title is not valid")
                print("-"*20)
                print("1. Enter title again")
                print("2. Exit")
                print("-"*20)
                choice=input("Enter Choice number: ")
                if not self.validate_choice_and_available_choices(choice,['1','2']):
                    logging.info("validation failed")
                    print("Ensure entered choice is among the available choices")
                if choice.strip()=="1":
                    # we try again
                    get_new_title_and_validate_it()
                    #isbn valdiated
                if choice.strip()=="2":
                    logging.info("Exiting")
                    return
            return new_book_name
        logging.info("getting the new title from user via CLI")
        updated_title=get_new_title_and_validate_it()
        logging.info("getting the new title from user via CLI")

        # the updated book name
        def get_new_author_name_and_validate_it():
            """
            Gets name as input from the user via CLI and provices option to try again

            Input:
            No Args, inputs are taken dynamically via CLI

            Output:
            name, type=string
            """
            new_name=input("Enter new Author's name: ")
            if not self.validate_name(new_name):
                logging.error("failedn to validate new book name")
                print("The entered Author's name is not valid")
                print("-"*20)
                print("1. Enter Author's name again")
                print("2. Exit")
                print("-"*20)
                choice=input("Enter Choice number: ")
                if not self.validate_choice_and_available_choices(choice,['1','2']):
                    logging.info("validation failed")
                    print("Ensure entered choice is among the available choices")
                if choice.strip()=="1":
                    # we try again
                    get_new_author_name_and_validate_it()
                    #isbn valdiated
                if choice.strip()=="2":
                    logging.info("Exiting")
                    return
            return new_name
        logging.info("getting the new name from user via CLI")
        udpated_name=get_new_author_name_and_validate_it()
        logging.info("received the new name from user via CLI")
        #remove the existing row
        logging.info("Removing row based on isbn")
        self.books_df=self.books_df[self.books_df['isbn']!=input_isbn]
        logging.info("Record removed")
        # Define the new values
        # print(self.books_df)
        logging.info("savinng data to .csv file")
        new_book=pd.DataFrame({'isbn':[input_isbn],'Title':[updated_title],'Author':[udpated_name]})
        self.books_df=pd.concat([self.books_df,new_book],ignore_index=True)

        #save the updates to the .csv file

        self.save_book_df_to_csv()
        logging.info("saved to file")

    #  list all contents to CLI
    def list_all_book(self,rows=10):
        """
        Method prints all the books in the dataset to the terminal. By default prints 10 rows.
        Args:
        rows, defaults=10, type=int
        
        """
        # if number of rows not mentioned, print first 10 rows
        # even if 10 rows are not available, pandas will still print what is available and wont give an error
        # if not rows:
        #     print(self.books_df.head(10))
        if type(rows)!=int:
            return "Only integer values allowed for rows argument"
        
        if self.books_df.empty:
            error_message="the .csv file is empty, try populating it"
            logging.error(error_message)
            return error_message

        if rows>len(self.books_df):
            print(f"The max number of rows is{len(self.books_df)}, you have requested for {rows} rows, printing available rows")
        #printing according to the user inputed number of rows
        print(self.books_df.head(rows))

    # validity of isbn
    def check_if_book_exists_using_isbn(self,isbn):
        """
        We are checking if a book or book details we want to add to the book dataset already exists or not.
        used to check before we add a book, delete a book or update a book.

        Note: inputedisbn should have already undergone validation

        Input

        Title, type="string"
        Author, type="string"

        Return
        Bool, True for book exists, False for book does not exists
        """
        # check if book already exists
        logging.info("checking if book already exists in the library")
        output=self.books_df[(self.books_df['isbn']==isbn)]
        #if book already exists
        if not output.empty:
            error_message="book exists"
            logging.info(error_message)
            return True
        else:
            logging.info("book does not exist")
            return False

    # validity using title/author    
    def check_if_book_exists_using_title_author(self,Title,Author):
        """
        We are checking if a book or book details we want to add to the book dataset already exists or not.
        used to check before we add a book, delete a book or update a book.

        Note: inputed Title and Author should have already undergone validation

        Input

        Title, type="string"
        Author, type="string"

        Return
        Bool, True for book exists, False for book does not exists
        """
        # check if book already exists
        logging.info("checking if book already exists in the library")
        output=self.books_df[(self.books_df['Title']==Title)&(self.books_df["Author"]==Author)]
        #if book already exists
        if not output.empty:
            error_message="book exists"
            logging.info(error_message)
            return True
        else:
            logging.info("book does not exist")
            return False
    
    # validity using isbn/title/author
    def check_if_book_exists_using_isbn_title_author(self,isbn,Title,Author):
        """
        We are checking if a book or book details we want to add to the book dataset already exists or not.
        used to check before we add a book, delete a book or update a book.

        Note: inputed Title and Author should have already undergone validation

        Input
        isbn, type="string"
        Title, type="string"
        Author, type="string"

        Return
        Bool, True for book exists, False for book does not exists
        """
        # check if book already exists
        logging.info("checking if book already exists in the library")
        output=self.books_df[(self.books_df['isbn']==isbn)&(self.books_df['Title']==Title)&(self.books_df["Author"]==Author)]
        #if book already exists
        if not output.empty:
            error_message="book exists"
            logging.info(error_message)
            return True
        else:
            logging.info("book does not exist")
            return False

    # add a new row
    def add_a_book(self):
        # validate isbn, Title and Author
        logging.info("validating isbn...")
        isbn=self.generate_unique_isbn()
        isbn=self.validate_isbn(isbn)

        # check if another row has the same isbn
        if not self.books_df[self.books_df['isbn']==isbn].empty:
            error_message="\nError: duplicate isbn exits in library"
            logging.error(error_message)
            return False
        logging.info("isbn validation complete")
        
            # the updated book name
        def get_new_title_and_validate_it():
            """
            Gets name as input from the user via CLI and provices option to try again

            Input:
            No Args, inputs are taken dynamically via CLI

            Output:
            name, type=string
            """
            new_book_name=input("Enter new title: ")
            if not self.validate_title(new_book_name):
                logging.error("failed to validate new title")
                print("The entered title is not valid")
                print("-"*20)
                print("1. Enter title again")
                print("2. Exit")
                print("-"*20)
                choice=input("Enter Choice number: ")
                if not self.validate_choice_and_available_choices(choice,['1','2']):
                    logging.info("validation failed")
                    print("Ensure entered choice is among the available choices")
                if choice.strip()=="1":
                    # we try again
                    get_new_title_and_validate_it()
                    #isbn valdiated
                if choice.strip()=="2":
                    logging.info("Exiting")
                    return
            return new_book_name
        logging.info("getting the new title from user via CLI")
        title=get_new_title_and_validate_it()
        logging.info("getting the new title from user via CLI")

        # the updated book name
        def get_new_author_name_and_validate_it():
            """
            Gets name as input from the user via CLI and provices option to try again

            Input:
            No Args, inputs are taken dynamically via CLI

            Output:
            name, type=string
            """
            new_name=input("Enter new Author's name: ")
            if not self.validate_name(new_name):
                logging.error("failedn to validate new book name")
                print("The entered Author's name is not valid")
                print("-"*20)
                print("1. Enter Author's name again")
                print("2. Exit")
                print("-"*20)
                choice=input("Enter Choice number: ")
                if not self.validate_choice_and_available_choices(choice,['1','2']):
                    logging.info("validation failed")
                    print("Ensure entered choice is among the available choices")
                if choice.strip()=="1":
                    # we try again
                    get_new_author_name_and_validate_it()
                    #isbn valdiated
                if choice.strip()=="2":
                    logging.info("Exiting")
                    return
            return new_name
        logging.info("getting the new name from user via CLI")
        name=get_new_author_name_and_validate_it()
        logging.info("received the new name from user via CLI")
        logging.info('creating and adding new row')
        new_book=pd.DataFrame({'isbn':[isbn],'Title':[title],'Author':[name]})
        self.books_df=pd.concat([self.books_df,new_book],ignore_index=True)
        print(self.books_df[self.books_df['isbn']==isbn])
        self.save_book_df_to_csv()
        logging.info("saved to file")
    
    # delete a row according to isbn or title, but not according to Author, since author could have written multiple books
    def delete_a_book_based_on_isbn(self):
        """
        Used to delete a record of a book based on isbn values

        The isbn is 17 char long unique identifier for a book. It takes the isbn string as input, checks if its valid,
        checks if it exists, deletes that record from the .csv file

        Input:
        isbn, type=String

        Return:
        It does not Return anything, but saves the output to the .csv file
        """
        input_isbn=input("Enter ISBN number: ")
        if not self.validate_isbn(input_isbn):
            logging.error("entered ISBN value does not exist")
            print("-"*20)
            print("1. Enter ISBN number again")
            print("2. Exit")
            print("-"*20)
            choice=input("Enter Choice number: ")
            if not self.validate_choice_and_available_choices(choice,['1','2']):
                logging.info("validation failed")
                print("Ensure entered choice is among the available choices")
            if choice.strip()=="1":
                # we try again
                self.update_an_existing_book_detail()
                #isbn valdiated
            if choice.strip()=="2":
                logging.info("Exiting")
                return

        input_isbn=self.validate_isbn(input_isbn)
        # check if another row has the same isbn
        if self.books_df[self.books_df['isbn']==input_isbn].empty:
            error_message="\nError: isbn entered Not found in database"
            logging.error(error_message)
            # return self.delete_a_book_based_on_isbn()
            print("-"*20)
            print("1. Enter ISBN number again")
            print("2. Exit")
            print("-"*20)
            choice=input("Enter Choice number: ")
            if not self.validate_choice_and_available_choices(choice,['1','2']):
                logging.info("validation failed")
                print("Ensure entered choice is among the available choices")
            if choice.strip()=="1":
                # we try again
                self.delete_a_book_based_on_isbn()
                #isbn valdiated
            if choice.strip()=="2":
                logging.info("Exiting")
                return
        





        logging.info("inputted ISBN validated, proceeding to delete row")
        print("ISBN value inputed exists in library, proceeding to delete")
        logging.info("Removing row based on isbn")
        self.books_df=self.books_df[self.books_df['isbn']!=input_isbn]
        logging.info("Record removed")
        self.save_book_df_to_csv()
        logging.info("saved to file")

    # modular so that 
    def save_book_df_to_csv(self):
        # to do: thsi replaces the entire contnets of the csv file, how to only reflect the changes that occured?
        self.books_df.to_csv(self.book_df_file_path,index=False)

if __name__=="__main__":
    pass
    # bookObj=BooksManager(r'D:\LibraryManagementSystem\Redesigning Poor Code\csv_files\Books.csv')

    # bookObj.delete_a_book_based_on_isbn()
    # print(bookObj.books_df["isbn"])
