
import logging
import sys
logging.basicConfig(level=logging.ERROR)

class LibraryMangUntilities:
    """
    Contains methods used to format and validate the following:
    1. For users dataset: userid, name, Borrowed
    2. For books dataset: isbn,titles, authors

    Funtionalities:
    1. format_string := removes trailing spaces, special chars etc
    2. validate_name := validates the name according to preset rules
    3. validate_choice_and_available_choices := used to check inputs from CLI and validate it
    4. Exit := exits the program gracefully
    """
    def __init__(self):
        pass


    def format_string(self,input_str):
        """
        formats the input by:
        1. removing trailing spaces
        2. converting string to lowercase


        Return:
        False, type=bool if formating failes
        string type=string if formating success 
        """
        #removing trailing spaces
        input_str=input_str.strip()

        #check if empty or spaces
        if input_str=="":
            logging.error("\nError: input cannot be whitespaces or simply empty, try again....\n")
            return False

        # convert string to lower case
        input_str=input_str.lower()

        # remove extra spaces in between words "dan     Brown  " ="dan brown"
        input_str=" ".join(input_str.split())

        #output
        return input_str

    def validate_name(self,name):
        """
        validates whether Authors name follows the following rules.
        
        # Rule:
        1. only Alphabets (A-Z) (a-z) are allowed,
        2. ambersand and dot are allowed as special characters
        3. The name should have atleast 2 characters, and both should be alphabets
        4. Numbers are not allowed
        5. dorts not allowed within words, example da.n     Brown 
        6. trailing dots from end like MRS. DR. 'Dr. .Ram. will be automatically removed
        7. only ASCII inputs
        8. max 255 chars


        # Input:
        # Arg: input, type=string
        """
        # check if formating is possible
        if not self.format_string(name):
            logging.error("formating of string not possible")
            return False
        name=self.format_string(name)
        logging.info("formatting of authors name successfull")
        
        #set max length limit for a name, should not exceed 255 chars
        if len(name)>255:
            error_message="Name should have max 255 characters"
            logging.error(error_message)
            return False
        
        # check if input is in ascii
        if not name.isascii():
            error_message="Use only basic English letters and symbols."
            logging.error(error_message)
            return False

        # checks if any specials chars other than apostrophe or a dot are used
        allowed_special_chars=["'",'.',]
        detected_special_chars=[char for char in set(name) if char not in allowed_special_chars if not char.isalnum() if not char.isspace()]
        if detected_special_chars:
            error_message="Author's name cannot contain Special characters ~!@#$%^&*()_+-=, except for apostrophe or a dot"
            logging.error(error_message)
            return False
        
        logging.info("remove trailing dots from end like MRS. DR. 'Dr. .Ram.'")
        #remove trailing dots from end like MRS. DR. "Dr. .Ram."
        name=" ".join([word.strip(".") for word in name.split(" ")])
        logging.info("removal of trailing dots successfull")

        if "." in list(name):
            error_message="Please not do use dot to separate words, use a space instead"
            logging.error(error_message)
            return False

        #check if any numbers are present in the name
        if any([char.isdigit() for char in list(name)]):
            error_message="Name cannot have a number, please try again"
            logging.error(error_message)
            return False
        
        #the name needs to have length of alteast 2 and these should alphabets
        if len([elem for elem in list(name) if elem.isalpha()])<=1:
            error_message="Name should have atleast 2 alphabets"
            logging.error(error_message)
            return False
        
        #We should be left with the processed string
        logging.info("author's name validated,returning name as output")
        return name

    def validate_choice_and_available_choices(self,choice,all_choices):
        """
        We often have input choices that the user has to enter to proceed.
        1. This method will check if the input is of int data type
        2. If the entered choice is one of the options available. We validate these too
        
        Example of when this is used:
        1. Try enternig value again
        2. Exit to main menu

        we enter :1
        In the program it looks like:
        validate_choice_and_available_choices('1',['1','2'])

        Input:
        choice, type=int
        all_choices, type=list

        Return:
        False, type=bool if validation fails
        choice, type=int if the validation success
        """
        #check if type is str
        if not (type(choice)==str):
            logging.error("choice type should be a string")
            return False
        
        #removes the trailing spaces
        choice=choice.strip()
        logging.info("trailing spaces removed from choice")

        #check if empty
        if choice=="":
            logging.error("choice cannot be empty")
            return False
        

        #checking if type is str for each of choices in all_choices
        if [elem for elem in all_choices if type(elem)!=str]:
            logging.error("all_choices should be of type str")
            return False
        
        #removes the trailing spaces for each elem in all_choices
        all_choices=[elem.strip() for elem in all_choices]
        logging.info("trailing spaces removed from each otion in all_choices")
        #checling if any elem in empty
        if [elem for elem in all_choices  if elem==""]:
            logging.error("all_choices should be  non-empty")
            return False
        
        #check if choices is one among all_choices
        if not (choice in all_choices):
            logging.error("choice entered is not part of all_choices")
            return False

        return choice,all_choices
    
    def Exit(self):
        """
        Exits the program. No params or returns
        """
        logging.info("Exiting the program gracefully")
        sys.exit(0)


if __name__=="__main__":
    obj=LibraryMangUntilities()
    # print(obj.validate_choice_and_available_choices('1',['',' 2','3 ']))
    print(obj.main_menu())
