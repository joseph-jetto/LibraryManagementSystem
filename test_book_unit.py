from book import BooksManager
import unittest
import pandas as pd

class TestBook(unittest.TestCase):
    def setUp(self):
        self.book=BooksManager()


    def test_validate_title(self):
        # check if input is empty
        result = self.book.validate_title("")
        self.assertFalse(result)
        result = self.book.validate_title(" ")
        self.assertFalse(result)
        result = self.book.validate_title("   ")
        self.assertFalse(result)
        
        #Valid author
        result = self.book.validate_title("The Great Gatsby")
        self.assertEqual(result,"the great gatsby")
        
        #Check for trailing spaces
        result = self.book.validate_title("  The Great Gatsby ")
        self.assertEqual(result,"the great gatsby")

        #remove extra spaces in between words
        result = self.book.validate_title("  the     great  gatsby")
        self.assertEqual(result, "the great gatsby")

        #Test case 9: Min length should be 2 alphabets
        result=self.book.validate_title("k")
        self.assertFalse(result)
        

        #contains non-english characters Jüne,séna
        result=self.book.validate_title("¡Cien años de soledad!")
        self.assertFalse(result)
        
        # O'Neill, check if special characters is maintained
        result=self.book.validate_title("&da*n BRo#!!@#$%^&&&&*()_+<>,./;':")
        self.assertEqual(result,"&da*n bro#!!@#$%^&&&&*()_+<>,./;':")

        #check if numbers are accepted
        result=self.book.validate_title('the firm 3')
        self.assertEqual(result,'the firm 3')
        #check if max size of 255 followed
        # when size is 255 chars
        result=self.book.validate_title("A"*255)
        self.assertEqual(result,"a"*255)
        # when size more than 255 chars
        result=self.book.validate_title("A"*256)
        self.assertFalse(result)



if __name__ == '__main__':
    unittest.main()
