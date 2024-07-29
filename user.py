import pandas as pd
import regex
import random
import logging
from utilities import LibraryMangUntilities

# Configure logging to show INFO and above
logging.basicConfig(level=logging.error)


class UsersManager(LibraryMangUntilities):
    """
    Does the following:
    1. validate_id := check validity of user's unique id number
    2. search_among_user_attributes:= searches based on attributes
    2.1. search_id := searches by id number
    2.2. search_name := search by name
    3. generate_unique_id := generates unique id for user
    4. update_an_existing_user_detail := update a cell in existing dataset
    5. list_all_user := print to screen all the users
    6. add_a_user := adds a new row with details of a new user
    7. delete_a_user_based_on_id := delete a user data based on id number
    """
    def __init__(self):
        pass

    # check validity of user's unique id number
    def validate_id(self,id):
        """
        Used to validate the id
        Rules 
        1. max length should be 17 including the prefix id
        2. type is string
        3. characters after prefix "id" must be digits

        Input:
        id, a string 17chars long

        Return:
        False, type=bool ;if validation fails
        id, type=string ; if validation success
        """
        #removing trailing spaces
        id=id.strip()

        #format string
        if not self.format_string(id):
            return False
        id=self.format_string(id)

        #check if empty or spaces
        if id=="":
            error_message="\nError: id cannot be whitespaces or simply empty, try again....\n"
            logging.error(error_message)
            return False
        #check "id" as prefix
        if id[:2]!="id":
            # print(id[:4])
            logging.error("prefix is not id")
            return False
        #check that its only numbers
        if not id[2:].isdigit():
            error_message="\nError: Ensure only numbers are entered, try again....\n"
            logging.error(error_message)
            # if input failed, we ask for input again
            return False

        # check if max length exceed 13
        if len(id)!=17:
            error_message="\nError: The required length is 17, try again\n"
            logging.error(error_message)
            return False

        return id
   
    # searches based on attributes
    def search_among_user_attributes(self):
        """
        searches for user based on input query. this query can be any attribute amoing
        1. id
        2. name

        Rules:
        1. You can enter a part of the id, name as a substring and all the rows that has it as a substring will be outputed
        
        Input: 
        one among 1.id, 2.Name as user input
            Input: enter whole string or substring as input
        
        Output:
        Rows that qualify the seach is printed on to the terminal
        """
        # choose the attributes you want to search by, input the values, validate it according to the type
        # 

        print("\n Choose among the attributes to search from:")
        print("1. id")
        print("2. Name")
        # storing option number with attribute for easy access
        attribute_dict={1:"id",2:"Name"}
        # getting the input from user, converting from string to int
        selected_attribute= input("Enter corresponding number: ")
        # validate the input to be one among [1,2]
        try:
            # converting from string to int
            selected_attribute=int(selected_attribute)
            if selected_attribute not in [1,2]:
                logging.error("\nIncorrect input, choose among 1,2 only. Try again...")
            print(f"You have chosen {selected_attribute}. {attribute_dict.get(selected_attribute, 'Incorrect input, choose among 1, 2 only. Try again...')}")
        except ValueError:
            logging.error("\nIncorrect input, choose among 1,2 only. Try again...")
            self.search_among_user_attributes()

        if selected_attribute==1:
            #search by id value
            logging.info("id search selected")
            self.search_id()
        elif selected_attribute==2:
            #search by author's name
            logging.info("author search selected")
            self.search_name()

    #  searches by id number
    def search_id(self):
        """
        Used to search the library based on id number
        Rules:
        1. only numbers are inputed, prefix of "id" NOT to be inputed
        2. since max length for  id is 13 digits, the input should not exceed that

        Returns:
        It does not return anything, it prints all rows that contain the entered string or substring to the terminal
        """
        #Get id value as input from user
        sub_string=input("enter the whole or partial id number to search for, (DO NOT include id as prefix): ")
        
        # Validate the input
        #removing trailing spaces
        sub_string=sub_string.strip()

        #check if empty or spaces
        if sub_string=="":
            logging.error("\nError: input cannot be whitespaces or simpy empty, try again....\n")
            #if input fails, we asks for input again
            self.search_id()

        #check that its only numbers
        if not sub_string.isdigit():
            logging.error("\nError: Ensure only numbers are entered, try again....\n")
            # if input failed, we ask for input again
            self.search_id()

        # check if max length exceed 13
        if len(sub_string)>15:
            logging.error("\nError: The max possible input length is 13, try again\n")
            self.search_id()
        
        #search for said substring in the id col of the dataframe
        # print(self.users_df[self.users_df["id"].str.contains(sub_string,case=False,na=False)])
        
        output=self.users_df[self.users_df["id"].str.contains(sub_string,case=False,na=False)]
        
        # if no match found
        if (output.empty):
            error_message="Tried searching, no match found"
            logging.error(error_message)
            return self.search_id()
        logging.info("sub_string match found under id")
        print(output)
   
    #  search by name   
    def search_name(self):
        """
        Used to search for a string or substring within the column "Name"
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
            self.search_name()

        sub_str=self.validate_name(sub_str)
        # print("sub_str=",sub_str)
        # search for substring in column Name
        output=self.users_df[self.users_df["Name"].str.contains(sub_str)]
        
        # if no match found
        if (output.empty):
            print("="*50)
            error_message="Tried searching, no match found"
            print(error_message)
            print("="*50)
            logging.error(error_message)
            return self.search_name()
        logging.info("sub_string match found under Names name")
        print(output)
    
    #  generates unique id for user
    def generate_unique_id(self):
        """
        id is an system generated unique id given to each user to identify it in the library

        The function generates an unique 17char id value for every new user entered into library
        Rules:
        1. we have to check id in the dataset before assigning to prevent duplicates 

        Output:
        id
        type: string
        
        """
        def unique_id():
            """
            generates the unique 17char id with the prefix "id", Totalling a 17 char long string

            This is used in generate_unique_id function. Its nested to follow DRY principles

            Output:
            id
            type: string

            """
            id="id"+"".join([str(random.randint(0,9)) for i in range(15)])
            return id
            
    
        #generated number with the prefix id
        id=unique_id()

        #check for duplicates
        while id in self.users_df["id"]:
            id=unique_id()
        
        return id
    
    #  update a cell in existing dataset
    def update_an_existing_user_detail(self):
        """
        Used to update an existing user record, using the user inputed id values
        from CLI

        Input:
        No inputs args, but input take running run time from CLI
        Return:
        Does not return anything, but prints to screen
        """

        input_id=input("Enter id number: ")
        if not self.validate_id(input_id):
            logging.error("entered id value does not exist")
            print("-"*20)
            print("1. Enter id number again")
            print("2. Exit")
            print("-"*20)
            choice=input("Enter Choice number: ")
            if not self.validate_choice_and_available_choices(choice,['1','2']):
                logging.info("validation failed")
                print("Ensure entered choice is among the available choices")
            if choice.strip()=="1":
                # we try again
                self.update_an_existing_user_detail()
                #id valdiated
            if choice.strip()=="2":
                logging.info("Exiting")
                return

        input_id=self.validate_id(input_id)
        print("id value inputed exists in library, proceed to update details")


        # the updated user name
        def get_new_name_and_validate_it():
            """
            Gets name as input from the user via CLI and provices option to try again

            Input:
            No Args, inputs are taken dynamically via CLI

            Output:
            name, type=string
            """
            new_name=input("Enter new  name: ")
            if not self.validate_name(new_name):
                logging.error("failedn to validate new user name")
                print("The entered name is not valid")
                print("-"*20)
                print("1. Enter name again")
                print("2. Exit")
                print("-"*20)
                choice=input("Enter Choice number: ")
                if not self.validate_choice_and_available_choices(choice,['1','2']):
                    logging.info("validation failed")
                    print("Ensure entered choice is among the available choices")
                if choice.strip()=="1":
                    # we try again
                    get_new_name_and_validate_it()
                    #id valdiated
                if choice.strip()=="2":
                    logging.info("Exiting")
                    return
            return new_name
        logging.info("getting the new name from user via CLI")
        udpated_name=get_new_name_and_validate_it()
        logging.info("received the new name from user via CLI")

        # temparily storing the user's list of borrowed book
        borrowed_books=(self.users_df.loc[self.users_df['id'] == input_id, 'Borrowed'].values)
        # print("BORROWING values=",str(borrowed_books))
        # print("BORROWING type=",type(str(borrowed_books)))
        logging.info("removing entire row")
        self.users_df=self.users_df[self.users_df['id']!=input_id]

        
        # logging.info("savinng data to .csv file")
        new_book=pd.DataFrame({'id':input_id,'Name':udpated_name,'Borrowed':borrowed_books})
        self.users_df=pd.concat([self.users_df,new_book],ignore_index=True)


        #save the updates to the .csv file
        logging.info("savinng data to .csv file")
        self.save_user_df_to_csv()
        logging.info("saved to file")

    # show all users in file
    def list_all_user(self,rows=10):
        """
        Method prints all the users in the dataset to the terminal. By default prints 10 rows.
        Args:
        rows, defaults=10, type=int
        
        """
        # if number of rows not mentioned, print first 10 rows
        # even if 10 rows are not available, pandas will still print what is available and wont give an error
        # if not rows:
        #     print(self.users_df.head(10))
        if type(rows)!=int:
            return "Only integer values allowed for rows argument"
        
        if self.users_df.empty:
            error_message="the .csv file is empty, try populating it"
            logging.error(error_message)
            return error_message

        if rows>len(self.users_df):
            print(f"The max number of rows is{len(self.users_df)}, you have requested for {rows} rows, printing available rows")
        #printing according to the user inputed number of rows
        print(self.users_df.head(rows))

    #adds a users
    def add_a_user(self):
        # validate id, Title and Name
        logging.info("validating id...")
        id=self.generate_unique_id()
        id=self.validate_id(id)

        # check if another row has the same id
        if not self.users_df[self.users_df['id']==id].empty:
            error_message="\nError: duplicate id exits in library"
            logging.error(error_message)
            return False
        logging.info("id validation complete")
        
    

        # the updated user name
        def get_new_name_and_validate_it():
            """
            Gets name as input from the user via CLI and provices option to try again

            Input:
            No Args, inputs are taken dynamically via CLI

            Output:
            name, type=string
            """
            new_name=input("Enter new name: ")
            if not self.validate_name(new_name):
                logging.error("failedn to validate new user name")
                print("The entered name is not valid")
                print("-"*20)
                print("1. Enter name again")
                print("2. Exit")
                print("-"*20)
                choice=input("Enter Choice number: ")
                if not self.validate_choice_and_available_choices(choice,['1','2']):
                    logging.info("validation failed")
                    print("Ensure entered choice is among the available choices")
                if choice.strip()=="1":
                    # we try again
                    get_new_name_and_validate_it()
                    #id valdiated
                if choice.strip()=="2":
                    logging.info("Exiting")
                    return
            return new_name
        logging.info("getting the new name from user via CLI")
        name=get_new_name_and_validate_it()
        logging.info("received the new name from user via CLI")
        logging.info("savinng data to .csv file")
        new_user=pd.DataFrame({'id':[id],'Name':[name],'Borrowed':[" "]})
        self.users_df=pd.concat([self.users_df,new_user],ignore_index=True)
        print(self.users_df[self.users_df['id']==id])
        self.save_user_df_to_csv()
        logging.info("saved to file")
    
    # delete a row according to id or title, but not according to Name, since author could have written multiple users
    def delete_a_user_based_on_id(self):
        """
        Used to delete a record of a user based on id values

        The id is 17 char long unique identifier for a user. It takes the id string as input, checks if its valid,
        checks if it exists, deletes that record from the .csv file

        Input:
        id, type=String

        Return:
        It does not Return anything, but saves the output to the .csv file
        """
        input_id=input("Enter id number: ")
        if not self.validate_id(input_id):
            logging.error("entered id value does not exist")
            print("-"*20)
            print("1. Enter id number again")
            print("2. Exit")
            print("-"*20)
            choice=input("Enter Choice number: ")
            if not self.validate_choice_and_available_choices(choice,['1','2']):
                logging.info("validation failed")
                print("Ensure entered choice is among the available choices")
            if choice.strip()=="1":
                # we try again
                self.update_an_existing_user_detail()
                #id valdiated
            if choice.strip()=="2":
                logging.info("Exiting")
                return

        input_id=self.validate_id(input_id)
        # check if another row has the same id
        if self.users_df[self.users_df['id']==input_id].empty:
            error_message="\nError: id entered Not found in database"
            logging.error(error_message)
            # return self.delete_a_user_based_on_id()
            print("-"*20)
            print("1. Enter id number again")
            print("2. Exit")
            print("-"*20)
            choice=input("Enter Choice number: ")
            if not self.validate_choice_and_available_choices(choice,['1','2']):
                logging.info("validation failed")
                print("Ensure entered choice is among the available choices")
            if choice.strip()=="1":
                # we try again
                self.delete_a_user_based_on_id()
                #id valdiated
            if choice.strip()=="2":
                logging.info("Exiting")
                return
        
        
        logging.info("inputted id validated, proceeding to delete row")
        print("id value inputed exists in library")
        print("checking if the person has any Borrowed books")
        

        # print("OUTPUT=",self.users_df.loc[self.users_df['id']==input_id,"Borrowed"].str.strip()=="")
        # print("OUTTT",self.users_df.loc[self.users_df['id']==input_id,"Borrowed"].str.strip())
        # output=self.users_df.loc[self.users_df['id']==input_id,"Borrowed"].str.strip()

        logging.info("checking if the person has any Borrowed books")
        #finding the exact row and returning the cotents of "Borrorwed"
        logging.info('finding the exact row and returning the cotents of "Borrorwed"')
        output=self.users_df.loc[self.users_df['id']==input_id,"Borrowed"].str.strip()
        #the output is in Serries, converting it to string
        if str(output)!="":
            self.users_df=self.users_df[self.users_df['id']!=input_id]
            logging.info("Record removed")
            self.save_user_df_to_csv()
            logging.info("saved to file")
        else:
            msg='User has Borrowed book, removing user after he/she has returned all the books'
            logging.info(msg)
            print(msg)

    # saves dataset to .csv file
    def save_user_df_to_csv(self):
        """
        saves dataset to .csv file
        """
        # to do: thsi replaces the entire contnets of the csv file, how to only reflect the changes that occured?
        self.users_df.to_csv(self.user_df_file_path,index=False)

if __name__=="__main__":
    pass


