# pyGeeks-Who-Drink
Python module for scraping Geeks Who Drink Data from the Geeks Who Drink website. 

Py-Geeks Who Drink is a python module that contains 4 functions that can be used to quickly build a database of Geeks Who Drink information.

The main function is get_quiz_results(). get_quiz_results takes a venue id and a quiz id and returns a list of dictionaries of the quiz results. 

The information returned is:
Team Name
Score
Rank
Venue Name
Quiz Date
Rank
Venue Address
Venue City
Venue Zipcode
Venue Start Time
Venue Day
Quiz ID
Venue ID

get_venue_quiz_ids() returns a list of quiz ids for the provided venue id. As many quiz ids as can be found on the Geeks Who Drink website will be returned.

get_last_venue_quiz_id() returns the single most recent quiz id that can be found for the providied venue id. 

get_venue_ids_by_state() returns a list of active quiz venues in the state. Takes two letter state code. IE: CA, WA, NY, etc


By using these functions, you can quickly make a list of venues, find the quizs associated with those venues, and then get the individual quiz results. get_last_venue_quiz_id() can be used to keep your database up to date once an initial historical pull has been done. 




 
