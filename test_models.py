from utilities import LibraryMangUntilities
import unittest
import pandas as pd
# import logging

# logging.basicConfig(level=logging.WARNING)

class TestBook(unittest.TestCase):
    def setUp(self):
        self.utiles_obj=LibraryMangUntilities()

    def test_format_string(self):
        # check if input is empty
        result = self.utiles_obj.format_string("")
        self.assertFalse(result)

        result = self.utiles_obj.format_string(" Dan    brown ")
        self.assertEqual(result,"dan brown")

        
    def test_validate_name(self):
        # Test case : when there are dots at the end of a word
        result = self.utiles_obj.validate_name("dan. Brown.")
        self.assertEqual(result,"dan brown")

        # Test case : check for dot in between words
        result = self.utiles_obj.validate_name("  da.n     Brown ")
        self.assertFalse(result)

        #Test case : if any numbers are present
        result=self.utiles_obj.validate_name("jaco7n gate8")
        self.assertFalse(result)

        result=self.utiles_obj.validate_name("k")
        self.assertFalse(result)
        #Test case : Min length should be 2 alphabets

        #contains non-english characters Jüne,séna
        result=self.utiles_obj.validate_name("Jüne")
        self.assertFalse(result)
        
        # O'Neill, check if ambersand is maintained
        result=self.utiles_obj.validate_name("O'Neil")
        self.assertEqual(result,"o'neil")
        #check if max size of 255 followed
        # when size is 255 chars
        result=self.utiles_obj.validate_name("A"*255)
        self.assertEqual(result,"a"*255)

        # when size more than 255 chars
        result=self.utiles_obj.validate_name("A"*256)
        self.assertFalse(result)

    
    def test_validate_choice_and_available_choices(self):
        # result=self.utiles_obj.validate_choice_and_available_choices('1',['1 ','2 ','3'])
        # self.assertEqual(result,('1',['1','2','3']))
        result=self.utiles_obj.validate_choice_and_available_choices('1',['','2 ','3'])
        self.assertFalse(result)
        result=self.utiles_obj.validate_choice_and_available_choices('1',[1,'2 ','3'])
        self.assertFalse(result)
        result=self.utiles_obj.validate_choice_and_available_choices('4',['1','2 ','3'])
        self.assertFalse(result)
if __name__ == '__main__':
    unittest.main()
