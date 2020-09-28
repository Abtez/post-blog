import unittest
from app.models import Quote

class QuoteTest(unittest.TestCase):  
   
    def setUp(self):
        self.new_quote = Quote(1,'pass','Marketing','http//:www.abzed.com')
        
    def test_check_instance_variables(self):
        self.assertEquals(self.new_quote.id,1)
        self.assertEquals(self.new_quote.author,'pass')
        self.assertEquals(self.new_quote.quote,"Marketing")
        self.assertEquals(self.new_quote.link,'http//:www.abzed.com')
        
    def test_save_quote(self):
        self.new_quote.save_quote()
        self.assertTrue(len(Quote.quote_list),0)
        
    def test_get_blog_by_id(self):

        self.new_quote.save_quote()
        got_quote = Quote.get_quote(1)
