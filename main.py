from library_manager import LibraryManager

# validate_choice_and_available_choices
import logging
# Configure logging to show INFO and above
logging.basicConfig(level=logging.ERROR)


class Run:
    """
    Used to create the interface. This handles only the interactions, but all operations
    are performed by the Library manager class. Following is the primary interface.
    
        "Library Management System"
        ----------------------------
        "Main Menu"
        "1. List Books"
        "2. List users"
        "3. Add a Books"
        "4. Add a User"
        "5. update a book's detail"
        "6. update a user's detail"
        "7. search for a book"
        "8. Search for a user"
        "9. Borrow a book"
        "10. Return a book"
        "11. Exit"

    """
    def __init__(self):
        #initialise the Library manager which run on singleton design pattern

        self.library_obj=LibraryManager()
        logging.info("Created an a single instance of LibraryManager")
        # self.library_obj.main_menu()
        self.menu_dict={'1':'List Books','2':'List users','3':'Add a Books','4':'Add a User',
                    '5':"update a book's detail",'6':"update a user's detail",
                    '7':"search for a book",'8':"Search for a user",
                    '9': "Borrow a book",'10':'Return a book','11': 'Exit'}
    
    def main_menu(self):
        """
        This are all the options available to user. This will be commonly used as an exit
        method by all the classes in case user want to come out
        """
        print("="*50)
        print("\nLibrary Management System")
        print("1. List Books")
        print("2. List users")
        print("3. Add a Books")
        print("4. Add a User")
        print("5. update a book's detail")
        print("6. update a user's detail")
        print("7. search for a book")
        print("8. Search for a user")
        print("9. Borrow a book")
        print("10. Return a book")
        print("11. Exit")
        print("="*50)
        #list of all the options
        menu_options=['1','2','3','4','5','6','7','8','9','10','11']
        #entering input
        user_input=input("Enter the corresponding number: ")
        # validating user_input
        logging.info("validating user_input")
        if not self.library_obj.validate_choice_and_available_choices(user_input,menu_options):
            print("Choose one among 1,2,3,4,5,6,7,8,9 only")
            logging.error("wrong user_input from user, valdiation failed")
            self.main_menu()
        user_input,menu_options= self.library_obj.validate_choice_and_available_choices(user_input,menu_options)
        print("users entered=",user_input)
        # data validated
        if user_input=='1':
            # List Books
            msg=f"{user_input}. {self.menu_dict[user_input]} chosen"
            logging.info(msg)
            print(msg)
            self.library_obj.list_all_book()
        elif user_input=='2':
            # List Books
            msg=f"{user_input}. {self.menu_dict[user_input]} chosen"
            logging.info(msg)
            print(msg)
            self.library_obj.list_all_user()
        elif user_input=='3':
            # List Books
            msg=f"{user_input}. {self.menu_dict[user_input]} chosen"
            logging.info(msg)
            print(msg)
            self.library_obj.add_a_book()
        elif user_input=='4':
            # List Books
            msg=f"{user_input}. {self.menu_dict[user_input]} chosen"
            logging.info(msg)
            print(msg)
            self.library_obj.add_a_user()
        elif user_input=='5':
            # List Books
            msg=f"{user_input}. {self.menu_dict[user_input]} chosen"
            logging.info(msg)
            print(msg)
            self.library_obj.update_an_existing_book_detail()
        elif user_input=='6':
            # List Books
            msg=f"{user_input}. {self.menu_dict[user_input]} chosen"
            logging.info(msg)
            print(msg)
            self.library_obj.update_an_existing_user_detail()
        elif user_input=='7':
            # List Books
            msg=f"{user_input}. {self.menu_dict[user_input]} chosen"
            logging.info(msg)
            print(msg)
            self.library_obj.search_among_book_attributes()
        elif user_input=='8':
            # List Books
            msg=f"{user_input}. {self.menu_dict[user_input]} chosen"
            logging.info(msg)
            print(msg)
            self.library_obj.search_among_user_attributes()
        elif user_input=='9':
            # List Books
            msg=f"{user_input}. {self.menu_dict[user_input]} chosen"
            logging.info(msg)
            print(msg)
            self.library_obj.borrow_a_book()
        elif user_input=='10':
            # List Books
            msg=f"{user_input}. {self.menu_dict[user_input]} chosen"
            logging.info(msg)
            print(msg)
            self.library_obj.return_a_book()
        elif user_input=='11':
            # List Books
            msg=f"{user_input}. {self.menu_dict[user_input]} chosen"
            logging.info(msg)
            print(msg)
            self.library_obj.Exit()
        


    def run(self):
        """
        Shows options Number along with the corresponding program to run 
        """

        try:
            while(True):
                self.main_menu()
        except KeyboardInterrupt:
            logging.info("Exiting program Gracefully via Keyboard Interrupt")
            print("\n")
            print("="*50)
            print("Exiting program Gracefully via Keyboard Interrupt")
            print("="*50)
            self.library_obj.Exit()
        



if __name__ == "__main__":
    run_obj=Run()
    run_obj.run()
