from user import UsersManager
import unittest
import pandas as pd
# import logging

# logging.basicConfig(level=logging.WARNING)

class Testuser(unittest.TestCase):
    def setUp(self):
        self.user=UsersManager()


    def test_validate_title(self):
        # check if input is empty
        result = self.user.validate_title("")
        self.assertFalse(result)
        result = self.user.validate_title(" ")
        self.assertFalse(result)
        result = self.user.validate_title("   ")
        self.assertFalse(result)
        
        #Valid author
        result = self.user.validate_title("The Great Gatsby")
        self.assertEqual(result,"the great gatsby")
        
        #Check for trailing spaces
        result = self.user.validate_title("  The Great Gatsby ")
        self.assertEqual(result,"the great gatsby")

        #remove extra spaces in between words
        result = self.user.validate_title("  the     great  gatsby")
        self.assertEqual(result, "the great gatsby")

        #Test case 9: Min length should be 2 alphabets
        result=self.user.validate_title("k")
        self.assertFalse(result)
        

        #contains non-english characters Jüne,séna
        result=self.user.validate_title("¡Cien años de soledad!")
        self.assertFalse(result)
        
        # O'Neill, check if special characters is maintained
        result=self.user.validate_title("&da*n BRo#!!@#$%^&&&&*()_+<>,./;':")
        self.assertEqual(result,"&da*n bro#!!@#$%^&&&&*()_+<>,./;':")

        #check if numbers are accepted
        result=self.user.validate_title('the firm 3')
        self.assertEqual(result,'the firm 3')
        #check if max size of 255 followed
        # when size is 255 chars
        result=self.user.validate_title("A"*255)
        self.assertEqual(result,"a"*255)
        # when size more than 255 chars
        result=self.user.validate_title("A"*256)
        self.assertFalse(result)



if __name__ == '__main__':
    unittest.main()
