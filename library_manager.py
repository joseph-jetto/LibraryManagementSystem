from book import BooksManager
from user import UsersManager
from check import CheckManager
from storage import StorageManager
import pandas as pd
import logging
logging.basicConfig(level=logging.ERROR)

# inhering from BooksManager, UsersManager, CheckManager, StorageManager
class LibraryManager(BooksManager, UsersManager, CheckManager, StorageManager):
    """
    Used to combine attributes and methods of BooksManager, UsersManager, CheckManager, StorageManager
    under a single unbrella.

    This class will be the point of contact for commands from the interface / CLI.
    """
    # class variable to keep track if an instance has already been created
    _instance = None
    
    def __init__(self):
        """
        we combine the __init__ part from all the classes from which we inherit, giving access to all of its attributes
        The design is kept singleton so that only a single instance can be created. if attempt is made to create a second
        instance, an Exception would be raised.
        """
        if LibraryManager._instance is None:
            # Initialization logic
            StorageManager.__init__(self)
            # Initialize other managers if needed
            BooksManager.__init__(self)
            UsersManager.__init__(self)
            CheckManager.__init__(self, self.users_df)
            #initialising the class vairable to prevent the creation of a second instance in singleton
            LibraryManager._instance = self
            logging.info("LibraryManager initialized.")
        else:
            logging.info("An attempt to create a second instance was detected, which is not allowed in Singleton")
            raise Exception("Only single instance creation allowed for singleton usage")
            

if __name__ == "__main__":
    LibMang_obj1 = LibraryManager()


