# to run 
# scrapy crawl imdb_spider -o movies.csv

import scrapy

class ImdbSpider(scrapy.Spider):
    '''
    Scrappy spider OBJ to crawl IMDB. Inherits from scrapy spider (scrapy.Spider)

    Methods
    -------
    parse: function to go from start page to full credits
    parse_full_credits: pulls paths for each actor in credits
    parse_actor page: scrapes an actor's page

    '''

    #name our spider (used to run crawl via command line)
    name = 'imdb_spider'
    
    #starting url for the crawl - show or movie page (Mad Men in this case)
    start_urls = ["https://www.imdb.com/title/tt0804503/"]

    def parse(self, response):
        '''
        Function starts at the class's set start_url and joins to it "fullcredits",
        then passes that next page to scrapy Request OBJ and invokes parse_full_credits
        as the callback.

        Parameters
        ----------
        self: the IMDB spider OBJ itself
        response: Response OBJ of this spider (inherited from scrapy.Spider)
        '''
        #join current url w/ string to create url to full credits page
        next_page = response.urljoin("fullcredits")

        if next_page: #if it exists, which it should, every IMDB listing has one...
            #Pass next_page to the Request OBJ of this spider, set the callback function to invoke the parse
            #method (since Python can't just say member function and has to remind me of Java) for full credts
            yield scrapy.Request(next_page, callback = self.parse_full_credits)
    
    def parse_full_credits(self, response):
        '''
        Function to build a list of relative paths for each actor in the full credits and
        then for each path, invoke parse_actor_page as the callback arg of a Request 
        given the url built from that path, to scrape that actor's page.

        Parameters
        ----------
        self: the IMDB spider OBJ itself
        response: Response OBJ of this spider (inherited from scrapy.Spider)
        '''
        #create list of relative paths for each actor (clicking on a headshot)
        actor_list = [a.attrib["href"] for a in response.css("td.primary_photo a")]

        #iterate through each actor path in the list
        for actor in actor_list:
            
            #join relative path to existing url
            actor_page = response.urljoin(actor)

            if actor_page: #if it is not null
                #Pass the url to this spider's request OBJ, set callback to invoke
                #the method to parse an actor's page
                yield scrapy.Request(actor_page, callback = self.parse_actor_page)

    def parse_actor_page(self, response):
        '''
        Function to scrape and actor's credits page and yield a dict of the form
        { "actor" : actor_name, "title" : title } for each credit on that page.

        Parameters
        ----------
        self: the IMDB spider OBJ itself
        response: Response OBJ of this spider (inherited from scrapy.Spider)

        '''
        #Pull actor name from header 
        actor_name = response.css("h1.header > span:nth-child(1) ::text").get()
        
        #Pull all titles in the css selector list returned by our reponse query 
        credits = response.css("div.filmo-category-section div.filmo-row b a ::text").getall()

        #iterate through the credits
        for title in credits:
            #yield an output dict 
            yield { "actor" : actor_name, "title" : title }





        
