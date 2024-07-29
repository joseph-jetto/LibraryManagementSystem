import pandas as pd
import logging

logging.basicConfig(level=logging.ERROR)


class StorageManager:
    """
    Class deals with:
    1. checks if the user required .csv files are present in the same directory as one we are running hte program from
    2. if not found, a file is creted, initialised and loaded into a dataframe to be used.
    
    functionalities:
    1. __init__ := loads the dataframe from .csv
    2. storage_operation := checks file existance, creates one if one doesn't exitst, and intialises it
    3. return_complete_file_path := used to get the directory path we are opeating from. 
    """

    #loads the dataframes
    def __init__(self):
        """
        Runs automatically when we create an object
        used to validate file exitance and column name existances

        Loads the dataframe from the valdiated file paths
        Uses the instances variables to load into pandas dataframe
        """
        self.users_df_file_path,self.book_df_file_path=self.storage_operation()
        logging.info("loading from files into dataframe")
        # self.book_df_file_path=book_df_file_path
        self.books_df=pd.read_csv(self.book_df_file_path)
        self.users_df=pd.read_csv(self.users_df_file_path)
        logging.info("successfully created dataframe")

    #checks file existance, creates one if one doesn't exitst, and intialises it
    def storage_operation(self):
        """
        # check if file path exits for Users_csv.csv
            # if it doesn't,create the file and initialise the colums name ['id','Name','Borrowed']
        # if does exits, check if the columsn are intilised with ['id','Name','Borrowed']

        # check if file path exits for Books_csv.csv
            # if it doesn't,create the file and initialise the colums name ['isbn','Title','Author']
        # if does exits, check if the columsn are intilised with ['isbn','Title','Author']
        
        Params:
        complete_file_path to the .csv file
        column_names is the names of the attributes ex:['isbn','Title','Author']
        
        Return:
        Does not return anything, but creates the column names in the .csv files
        """
        csv_files={'Users_csv.csv': ['id','Name','Borrowed'],'Books_csv.csv':['isbn','Title','Author']}
        validated_filepaths=[]
        for csv_name,column_names in csv_files.items():
            #check if csv file exitst already in the operating directory
            file_path=self.return_complete_file_path(csv_name)
            try:
                df=pd.read_csv(file_path)
                logging.info(".csv file exitst at the mentioned file_path")
                # .csv file exitst at the mentioned file_path
                if not all(df.columns.values==column_names):
                    logging.info("column names are not a match")
                    #if they are not a match,set the attributes
                    df.columns=column_names
                    # save to file, making the changes
                    logging.info('column names matched to predetermined column names')
                    df.to_csv(file_path,index=False)
            except (FileNotFoundError,pd.errors.EmptyDataError):
                logging.error('file not found at file_path or columns not initialised')
                # print(f"File not found at file_path or columns not initialised")
                logging.info("creating a dataframe, initialise the column names to fix error")
                df = pd.DataFrame(columns=column_names)
                logging.info("Saving to file")
                df.to_csv(file_path,index=False)
            validated_filepaths.append(file_path)
        return validated_filepaths

    # used to get the directory path we are opeating from
    def return_complete_file_path(self,csv_file_name):
        """
        Checks to see if a .csv files has already been created
        
        Params:
        the file name of the .csv file
        Returns:
        Path
        """
        dir_path=os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(dir_path,csv_file_name)
        # return os.path.exists(file_path)
        return file_path
    
import os
if __name__=="__main__":
    obj=StorageManager()
