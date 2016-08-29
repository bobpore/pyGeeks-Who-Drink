import requests
import re
from bs4 import BeautifulSoup


##get_quiz_results returns a list of lists of the scoring results of a geeks who drink venue on a specific quiz
def get_quiz_results(quiz_id,venue_id):

    page = requests.get('http://www.geekswhodrink.com/blogpost?qid='+str(quiz_id)+'&venueId='+str(venue_id))

    soup = BeautifulSoup(page.content,'html.parser')

    team_names = soup.findAll("span", { "class" : "team_name" })

    team_list = []
    for team in team_names:
        team_list.append(team.text)

    score_list = []
    scores = soup.findAll("span", { "class" : "score" })

    for score in scores:
        score_list.append(int(score.text))

    date = re.search('day, ([A-z].*[0-9]{4})',soup.find("div", { "class" : "dashedTop" }).text).group(1)

    venue_full = soup.find("div", { "id" : "venueInfo" })
    venue = venue_full.find('a')

    venue_name = venue.text
    venue_address_full = (venue_full.text).split('\n')
    venue_street_address = re.search('(\S.*)',venue_address_full[2]).group(1)
    venue_city = re.search('(\S.*)[0-9]{5}',venue_address_full[3]).group(1)
    venue_zip = re.search('([0-9]{5})',venue_address_full[3]).group(1)
    venue_day= (re.search('\[([A-z]*)',venue_address_full[4]).group(1))
    venue_start_time= (re.search('([0-9].*m)',venue_address_full[4]).group(1))
    number_of_teams_index = len(team_list)
    
    team_results = []
    for x in range(0,number_of_teams_index):
        team_results.append({
                            "Team Name":team_list[x],
                             "Score":score_list[x],
                             "Venue Name":venue_name,
                             "Quiz Date":date,
                             "Rank":x+1,
                             "Venue Address":venue_street_address,
                            "Venue City":venue_city,
                            "Venue Zipcode":venue_zip,
                            "Venue Start Time":venue_start_time,
                            "Venue Day":venue_day,
                            "Quiz Id":int(quiz_id),
                            "Venue Id":int(venue_id)
                             }
                            )

    return team_results


#Returns a list of all quiz ids for a specific venue 
def get_venue_quiz_ids(venue_id):
    venue_page = requests.get('http://www.geekswhodrink.com/venue?id='+str(venue_id))

    soup = BeautifulSoup(venue_page.content,'html.parser')
    links = []

    links =soup.findAll('a')
    quiz_ids = []
    for link in links:
        if re.match('.*qid=([0-9]*).*',str(link)) != None:
            quiz_ids.append(re.match('.*qid=([0-9]*).*',str(link)).group(1))

    offset = 0
    if len(quiz_ids)>0:
        while True:
            offset = offset+16
            venue_page = requests.get('http://www.geekswhodrink.com/venue?id='+str(venue_id)+'&offset='+str(offset))

            soup = BeautifulSoup(venue_page.content,'html.parser')
            if soup.h1.text == 'There are no blog posts for this venue right now.':
                break
            links =soup.findAll('a')
            for link in links:
                if re.match('.*qid=([0-9]*).*',str(link)) != None:
                    quiz_ids.append(re.match('.*qid=([0-9]*).*',str(link)).group(1))
    quiz_ids = set(quiz_ids)
    return quiz_ids
#Get the most recent quiz id for a venue id
def get_last_venue_quiz_id(venue_id):
    venue_page = requests.get('http://www.geekswhodrink.com/venue?id='+str(venue_id))

    soup = BeautifulSoup(venue_page.content,'html.parser')
    links = []

    links =soup.findAll('a')
    quiz_ids = []
    for link in links:
        if re.match('.*qid=([0-9]*).*',str(link)) != None and len(quiz_ids)==0:
            quiz_ids.append(re.match('.*qid=([0-9]*).*',str(link)).group(1))
    quiz_id = quiz_ids[0]
    return quiz_id
#Returns a list of venue ids when a 2 digit state code is provided    
def get_venue_ids_by_state(state):
    venue_list = requests.get('http://www.geekswhodrink.com/pages/venues?action=getVenuesByState&state='+state.upper()).content

    soup = BeautifulSoup(venue_list,'html.parser')
    links =soup.findAll("a", { "class" : "left25" })
    venue_ids = []
    for link in links:
        if re.match('.*venue\?id=([0-9]*).*',str(link)) != None:
            venue_ids.append(re.match('.*venue\?id=([0-9]*).*',str(link)).group(1))
    return venue_ids
