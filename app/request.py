import urllib.request,json
from .models import Quote

base_url = None

def configure_request(app):
    global base_url 
    base_url = app.config['QUOTES_API_BASE_URL']

def get_movie(category):
    get_quote_url = base_url
    
    with urllib.request.urlopen(get_quote_url) as url:
        get_quote_data = url.read()
        get_quote_response = json.loads(get_quote_data)
        
        quote_result = None
        
        if get_quote_response:
            quote_list = get_quote_response
            quote_result = process_results(quote_list)
            
    return quote_result

def process_results(quotes):
    quote_result = []
    for items in quotes:
        id = items.get('id')
        author = items.get('author')
        quote = items.get('quote')
        link = items.get('permalink')
        
        if author:
            quote_object = Quote(id, author, quote, link)
            quote_result.append(quote_object)
            
    return quote_result