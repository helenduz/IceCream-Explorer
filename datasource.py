import psycopg2
import os

class DataSource:
    '''
    DataSource executes all of the queries on the database.
    It also formats the data to send back to the frontend, typically in a list
    or some other collection or object.
    '''

    def __init__(self):
        '''
        Establishes a connection to the database
        '''
        self.connection = self.connect()


    def connect(self):
        '''
        Establishes a connection to the database with the following credentials:
            user - username, which is also the name of the database
            password - the password for this database on perlman

        Returns: a database connection.

        Note: exits if a connection cannot be established.
        '''
        DATABASE_URL = os.environ['DATABASE_URL']
        try:
            connection = psycopg2.connect(DATABASE_URL, sslmode='require')
        except Exception as e:
            print("Connection error: ", e)
            exit()
        return connection
     
        
    def match_product(self, keyword, match_column):
        '''
        Retrieve the image keys of all products that contain the input keyword in the specified column of that product
        
        Parameters: 
            keyword - string of user input
            match_column - the name of the column in which keyword should be searched, a string. Three options: "brand", "name", "ingredients"
        
        Returns:
            a list of image keys of all products whose match_column contains keyword. Empty list if there is no match.
        '''
        if (match_column == "ingredients"):
            keyword = keyword.upper()
        try:
            cursor = self.connection.cursor();
            if (match_column != "name"):
                query = "SELECT image_key FROM products WHERE " + str(match_column) + " LIKE '%" + str(keyword) + "%'"
                cursor.execute(query)
                return list(sum(cursor.fetchall(), ()))
            elif (match_column == "name"):
                return self.match_name(keyword)
            else:
                print("Invalid match_column")
                return []
        
        except Exception as e:
            print ("Something went wrong when executing the query: ", e)
            return []
    
    
    def match_name(self, keyword):
        '''
        Retrieve the image keys of all products that contain the input keyword in the name or subhead of that product

        Parameters:
            keyword - string of user input

        Returns:
            a list of image keys of all products whose product name or subhead contains keyword. Empty list if there is no match.
        '''
        try:
            cursor = self.connection.cursor();
            query  = "SELECT image_key FROM products WHERE product_name "+ " LIKE '%"+str(keyword).title() +"%'" + "OR subhead " + "LIKE '%"+str(keyword).title() + "%'"
            cursor.execute(query)
            out = list(sum(cursor.fetchall(), ()))
            return out
        
        except Exception as e:
            print ("Something went wrong when executing the query: ", e)
            return []
   
   
    def advance_match(self, brand, product_name, upper_rating, lower_rating, ingredients, review_text):
        '''
        Call the two helper function advance_products_match and advance_reviews_match and merge the two lists into one without dulipcate image_key
        
        Parameters: 
            brand - user input brand name string
            product_name - user input product name string
            upper_rating - upper bound on the user's input range of rating, integer
            lower_rating - lower bound on the user's input range of rating, integer
            ingredients - user input ingredient names string
            review_text - user input review segment string 
                
        Returns:
            a list of image keys of all products that match the input condition. Empty list if there is no match.
        '''
        if upper_rating == "":
            upper_rating = "5"
        elif not self.isNumber(upper_rating):
            upper_rating = "999"
        if lower_rating == "":
            lower_rating = "0"
        elif not self.isNumber(lower_rating):
            lower_rating = "999"
        products_match = self.advance_products_match(brand, product_name, upper_rating, lower_rating, ingredients)
        reviews_match = self.advance_reviews_match(review_text)

        advance_match = [value for value in products_match if value in reviews_match]
        return advance_match


    def advance_products_match(self, brand, product_name, upper_rating, lower_rating, ingredients):
        '''
        Retrieve the image keys of all products that match the input conditions specified by the parameters(excluding the condition on reviews)
        
        Parameters: 
            brand - user input brand name string
            product_name - user input product name string
            upper_rating - upper bound on the user's input range of rating, integer
            lower_rating - lower bound on the user's input range of rating, integer
            ingredients - user input ingredient names string
        
        Returns:
            a list of image keys of all products that match the input condition. Empty list if there is no match.            
        '''
        try:
            cursor = self.connection.cursor();
            query_products  = "SELECT image_key FROM products WHERE (brand " + " LIKE '%" + str(brand) + "%') AND (rating BETWEEN " + str(lower_rating) + " AND " + str(upper_rating) + ") AND (ingredients " + "LIKE '%" + str(ingredients).upper() + "%')"
            cursor.execute(query_products)
            query_without_name = list(sum(cursor.fetchall(), ()))
            return [value for value in query_without_name if value in self.match_name(product_name)]
        
        except Exception as e:
            print ("Something went wrong when executing the query: ", e)
            return []


    def advance_reviews_match(self, review_text):
        '''
        Retrieve the image keys of all products whose review contains review_text

        Parameters:
            brand - user input brand name string
            review_text - user input review segment string 
                
        Returns: 
            a list of image keys of all products whose review contains review_text. Empty list if there is no match.
        '''
        try:
            cursor = self.connection.cursor();
            query_reviews = "SELECT image_key FROM reviews WHERE review_text " + "LIKE '%" + str(review_text) + "%'"
            cursor.execute(query_reviews)
            return list(sum(cursor.fetchall(), ()))
        
        except Exception as e:
            print ("Something went wrong when executing the query: ", e)
            return []

    # This is the method we implemented using TDD
    def rank_product(self, product_list, rank_column):
        '''
        Rank the input products with respect to the input column

        Parameters:
            prodcut_list - list of all product image_key given by the search page
            rank_column - name of the column used to rank the product_list
        
        Returns:
            a list of ranked products image_key with respect to the input column
        '''
        # if product_list is empty, no need to rank
        if product_list == []:
            return product_list
        try:
            cursor = self.connection.cursor();
            if rank_column == "product_name":
                query = 'SELECT image_key FROM products WHERE image_key IN ({}) ORDER BY {}'.format(','.join(['%s'] * len(product_list)), str(rank_column))
            else:
                query = 'SELECT image_key FROM products WHERE image_key IN ({}) ORDER BY {} DESC'.format(','.join(['%s'] * len(product_list)), str(rank_column))
            # we only rank in decending order
            cursor.execute(query, product_list)
            return list(sum(cursor.fetchall(), ()))
        
        except Exception as e:
            print ("Something went wrong when executing the query: ", e)
            return []



    def getProductSummary(self, image_key):
        '''
        Retrieve the product's name, brand name, image key, and rating as a dictionary, for display on the list of results page
        
        Parameters:
            image_key - the image key (got from the user's click) that serves as a unique ID for the product, a string

        Returns:
            a dictionary (column name : value pairs) for the product with the specified image key. Column names contain the product's name, brand name, image, and rating
        '''
        try:
            cursor = self.connection.cursor();
            query = 'SELECT image_key, product_name, brand, rating FROM products WHERE image_key = '+ " \'"+str(image_key) + "\' "
            cursor.execute(query)
            productValue = list(sum(cursor.fetchall(), ()))
            productKey = ["image_key", "product_name", "brand", "rating"]
            return self.makeProductDictionary(productValue, productKey)
        
        except Exception as e:
            print ("Something went wrong when executing the query: ", e)
            return []
            

    def getProductInfo(self, image_key):
        '''
        Retrieve the product's name, image key, brand, subhead, description, ingredients, rating, rating count for display on the product section of the product detail page 
        
        Parameters: 
            image_key - the image key (got from the user's click) that serves as the unique ID for the product, a string
            
        Returns: 
            a dictionary (column name : value) that contains all the info about the product for the product section on the product detail page
        '''
        try:
            cursor = self.connection.cursor();
            query = 'SELECT * FROM products WHERE image_key = '+ " \'"+ str(image_key)+ "\'"
            cursor.execute(query)
            productValue = list(sum(cursor.fetchall(), ()))
            productKey = ['brand', 'image_key', 'product_name', 'subhead' , 'product_description', 'rating' , 'rating_count', 'ingredients']
            return self.makeProductDictionary(productValue, productKey)
        
        except Exception as e:
            print ("Something went wrong when executing the query: ", e)
            return []


    def getProductReviewInfo(self, image_key):
        '''
        Retrieve the star, text and author infomation from the product's reviews for display on the review section of the product detail page

        Parameters:
            image_key - the image key (got from the user's click) that serves as the unique ID for the product, a string
        
        Returns: 
            a dictionary (column name : value) that contains all the review related info we need to make the review section of the product detail html page
        '''
        try:
            cursor = self.connection.cursor();
            query = 'SELECT stars, review_text, author, title FROM reviews WHERE image_key = \'' + str(image_key) + "\'"
            cursor.execute(query)
            key_tuple = ("stars", "review_text", "author", "title")
            return self.makeReviewDictionary(key_tuple, list(map(list, cursor.fetchall())))
            
        except Exception as e:
            print ("Something went wrong when executing the query: ", e)
            return []
    
        
    def makeProductDictionary(self, value_list, key_list):
        '''
        Get the dictionary (value_list element : key_list element) from two lists
        
        Parameters:
            value_list - the list containing all the value name
            key_list - the list containing all the key value

        Returns:
            dictionary (value_list element : key_list element). If the two lists are of different size, return none
        '''
        productDictionary= {}
        brandName = {"bj":"Ben & Jerry's", "breyers": "Breyers", "talenti":"Talenti", "hd": "Häagen-Dazs"}
        if len(value_list) != len(key_list):
            print("Incorrect size. Unable to form a dictionary.")
            return None
        # convert the brand names from acronyms to full name
        for i in range(len(key_list)):
            if value_list[i] in brandName.keys():
                value_list[i] = brandName.get(value_list[i])
            productDictionary[key_list[i]] = value_list[i]
        return productDictionary
    
    def makeReviewDictionary(self, key_tuple, value_list):
        '''
        Get the list of dictionary (value_list element : key_list element) from two parameters
        
        Parameters:
            value_list - the list of tuples containing all review, each tuple contains each review's stars, review_text and author
            key_tuple - the tuple containing all the key value

        Returns:
            list of dictionary where each dictionary contains one review (value_list tuple element : key_tuple element)
        '''
        list_of_dict = [dict(zip(key_tuple, values)) for values in value_list]
        return list_of_dict
    
    def isNumber(self, s):
        '''
        Helper funtion to determine whether a given string is a number

        Parameter:
            s - the string to check whether it is a number
        
        Returns:
            A boolean indiacte whether the string is a number 
        '''
        try:
            float(s)
            return True
        except ValueError:
            return False
    

