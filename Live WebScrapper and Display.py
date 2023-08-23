# Web Scraper Project
# Name: Sudarshan Sowndiah
# Dec/2022


# This program consists of two types of data scraped from two different websites.
# The first of the two is data extracted from the movie review website the IMDB which displays the user with top 100 movies of all time.
# The second is the website related to sports which shows the user with the points table of the current year's(2022-2023) Laliga football tournament.
# The user can choose to view either of them from the main menu he is displayed at the start of the program.
# Everytime the user wants to view the data the code will scrape the live data from the website and data is stored separately in the system.
# All the data displayed is real and live from the website, be it the IMDb rating or the Laliga points table.
# The visualization of these data follows the same method, whatever data is displayed in a graph is real and live from the website.
# The user has multiple graphs to view from from both the websites, the user is given the option to choose from the menu where he/she is explained what each graph visualizes.
# Thus making it simple for the user to better understand the data.  


# Required Imports/libs/modules/.....
import requests
import pandas as pd
import openpyxl
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt

# a class containing all the functions performing the web scraping and visualization processes
class WebScraping:
  
    # function carrying the main menu where the user first interacts with the menu asking for what does he want to view.
    def mainMenu(self):
        # user enters their name here with a greeting.
        username = input("\nHello User!\nPlease enter your name: ")
        print(f"\nWelcome to the program {username}")
        # Explaining the user with what is to expect and see in this program.
        print("\nThis is a program where you can get the Web Scraped data on either Movie Ratings or Football teams points table")
        
        while(True):
            # predefined data for initializing the userchoice variable
            userchoice = 0
            # if loop for exception handling in case the user provides invalid entry.
            if userchoice not in range(1,4):
                try:
                    # user is asked to choose either of the three options in the main menu.
                    userchoice = int(input(f"\nPress 1 - To check for IMDB Movie Ratings \nPress 2 - To check for Laliga Points Table \nPress 3 - Exit\nEnter your Choice here: "))
                except ValueError:
                    print("\nInvalid entry \nPlease enter a Valid number")
            
            # if user chooses number 1 then they are redirected to the function for IMDB movie rating data scraped live from the website.
            if userchoice == 1:
                print("\nThese are the IMDB Top 100 Movies")
                # calling the imdb website scraping function
                self.scrapeImdbRatings()
            # if user chooses number 2 then they are redirected to the function for football points table data scraped live from the website.
            elif userchoice == 2:
                print("\nThis is Laliga 2022-2023 Points Table")
                ## calling the football website scraping function
                self.scrapeFootballPoints()
            # incase the user wants to quit the program.
            elif userchoice == 3:
                print(f"\nThanks you {username}!")
                break
            # if the user provides a wrong input value.
            else:
                print("\nWrong Input!!!")


    # function to scrape the IMDB top rated movies website.
    def scrapeImdbRatings(self):
        
        # initializing an excel file
        self.excel = openpyxl.Workbook()
        self.sheets = self.excel.active
        # renaming the first sheet in the excel file
        self.sheets.title = 'Top Movie Ratings'
        # appending the column headings into the excel file
        self.sheets.append(['Movie Rank', 'Movie Name', 'Release Year', 'Certificate', 'IMDB Rating', 'Genre', 'MetaScore'])
        
        # handling exception incase there is any issue with calling the website. 
        try:
            # IMDB website link.
            URL = "https://www.imdb.com/search/title/?count=100&groups=top_1000&sort=user_rating"
            # calling requests module 
            websiteSource = requests.get(URL)  
            # checking if the status of the website is alright
            websiteSource.raise_for_status()
            # calling beautifulsoup module
            soup = BeautifulSoup(websiteSource.text,'html.parser') 
            # finding all the required tags within the div tag we need.
            moviesList = soup.findAll('div', attrs={'class':'lister-item mode-advanced'})
            
            # initializing empty arrays to hold the data scraped from the IMDB website
            self.movie_rank = []
            self.movie_name = []
            self.year_of_release = []
            self.movie_certificate = []
            self.movie_rating = []
            self.movie_genre = []
            self.movie_metascore = []

            for movie in moviesList:
                # scraping the movie rank data
                movieRank = movie.find('span', class_="lister-item-index unbold text-primary").text.strip('.') if movie.find('span', class_='lister-item-index unbold text-primary') else '0'
                # appending the data into the array
                self.movie_rank.append(movieRank)
                # scraping the movie name data
                movieName = movie.find('h3', class_="lister-item-header").a.text if movie.find('h3', class_="lister-item-header") else '0'
                self.movie_name.append(movieName)
                # scraping the movie release year data
                movieReleaseYear = movie.find('span', class_="lister-item-year text-muted unbold").text.replace('(', '').replace(')', '').replace('I', '').strip() if movie.find('span', class_="lister-item-year text-muted unbold") else '0'
                self.year_of_release.append(movieReleaseYear)
                # scraping the movie certificate data
                movieCertificate = movie.find('span', class_="certificate").text if movie.find('span', class_="certificate") else '0'
                self.movie_certificate.append(movieCertificate)
                # scraping the movie rating data
                movieRating = movie.find('div', class_="inline-block ratings-imdb-rating").strong.text if movie.find('div', class_="inline-block ratings-imdb-rating") else '0'
                self.movie_rating.append(movieRating)
                # scraping the movie genre data
                movieGenre = movie.find('span', class_="genre").text.strip() if movie.find('span', class_="genre") else '0'
                self.movie_genre.append(movieGenre)
                # scraping the movie metascore data
                movieMetaScore = movie.find('span', class_="metascore").text.strip() if movie.find('span', class_="metascore") else '0'
                self.movie_metascore.append(movieMetaScore)
                # appending the scraped data into the excel file
                self.sheets.append([movieRank, movieName, movieReleaseYear, movieCertificate, movieRating, movieGenre, movieMetaScore])
                self.excel.save('IMDB Top Movie Ratings Data.xlsx')
                # reading the data from the excel file using pandas
                df = pd.read_excel('IMDB Top Movie Ratings Data.xlsx')
                for ind in df.index:
                    # printing the data from the excel file
                    print(df['Movie Rank'][ind], df['Movie Name'][ind], df['Release Year'][ind], df['Certificate'][ind], df['Genre'][ind], df['MetaScore'][ind])
            
            # looping the second menu for the user to view the data in a visualized format using the graphs
            while(True):
                # predefined data for initializing the userinput variable
                userInput = 0
                # if loop for exception handling in case the user provides invalid entry.
                if(userInput not in range(1,4)):
                    try:
                        # user is asked to choose either of the three options in the second menu.
                        print(f"\nWhich Graph would you like to see? \nPress 1 - Graph with the Movie Rank and Year of Release \nPress 2 - Graph comparing Movie Rating and Meta Score \nPress 3 - Exit to main menu")
                        userInput = int(input("\nEnter your choice here: "))
                    except ValueError:
                        print("\nInvalid entry!!!\nPlease enter a Valid number ")

                # if the user enters 1 then they are displayed the graph of Top ranked movies.
                if userInput == 1:
                    # graph's title
                    plt.title("Top Movie Rankings")
                    # number of data to be displayed
                    plt.locator_params(axis='x', nbins = 25)
                    # graph's xaxis with the movie rank data
                    xaxis = sorted(self.movie_rank)
                    plt.xlabel("Movie Rank")
                    # graph's yaxis with the release year data
                    yaxis = (self.year_of_release)
                    plt.ylabel("Year Of Release")
                    # ploting both axis into a graph
                    plt.plot(xaxis, yaxis)
                    # displaying the graph
                    plt.show()
                # if the user enters 2 then they are displayed the graph of Top rated movies.
                elif userInput == 2:
                    plt.title("Top Movie Ratings")
                    # graph's xaxis with the movie metascore data
                    xaxis = (self.movie_metascore)
                    plt.xlabel("Movie MetaScore")
                    # graph's yaxis with the movie rating data
                    yaxis = (self.movie_rating)
                    plt.ylabel("Movie Rating")
                    plt.bar(xaxis, yaxis)
                    plt.show()
                # if the user enters 3 then they exit this menu and go back to the main menu.
                elif userInput == 3:
                    print("\nReturning to Main Menu!")
                    break
                else:
                    print("\nWrong Input!!!")

                # the pause menu is used to provide a break to the user between the graphs.
                self.pauseMenu()      
        # handling the exception
        except Exception as notfound:
            print(f"This website is not available!!!{notfound}")

    
    # function to scrape the football points table website.
    def scrapeFootballPoints(self):
        
        # initializing an excel file
        self.excelSheet = openpyxl.Workbook()
        self.sheet = self.excelSheet.active
        self.sheet.title = 'Points Table'
        # appending the column headings into the excel file
        self.sheet.append(['Team Standings', 'Team Name', 'Games Played', 'Games Won', 'Games Drawn', 'Games Lost', 'Goals Scored', 'Goals Conceded', 'Goal Difference', 'Team Points'])
    
        # handling exception incase there is any issue with calling the website.
        try:
            # points table website link.
            url = "https://www.soccertimes.com/leagues/spanish-la-liga"
            source = requests.get(url)
            source.raise_for_status()
            soup = BeautifulSoup(source.text,'html.parser')
            # finding all the required tags within the tr tag we need.
            teams = soup.findAll('tr', attrs={'class':'standings-row'})

            # initializing empty arrays to hold the data scraped from the football website
            team_standings = []
            team_name = []
            games_played = []
            games_won = []
            games_drawn = []
            games_lost = []
            goal_scored = []
            goal_conceded = []
            goal_difference = []
            team_points = []
            
            for team in teams:
                # scraping team current standings data
                teamStandings = team.find('span', class_='number').text.strip()
                # appending the data into the array
                team_standings.append(teamStandings)
                # scraping the team name data
                teamName = team.find('span', class_='team-names').text
                team_name.append(teamName)
                # scraping the games played data
                gamesPlayed = team.find_all('td')
                games_played.append(gamesPlayed[1].text)
                # scraping the games won data
                gamesWon = team.find_all('td')
                games_won.append(gamesWon[2].text)
                # scraping the games drawn data
                gamesDrawn = team.find_all('td')
                games_drawn.append(gamesDrawn[3].text)
                # scraping the games lost data
                gamesLost = team.find_all('td')
                games_lost.append(gamesLost[4].text)
                # scraping the total goals scored data
                goalScored = team.find_all('td')
                goal_scored.append(goalScored[5].text)
                # scraping the total goals conceded data
                goalConceded = team.find_all('td')
                goal_conceded.append(goalConceded[6].text)
                # scraping the goal difference data
                goalDifference = team.find_all('td')
                goal_difference.append(goalDifference[7].text)
                # scraping the points data
                teamPoints = team.find_all('td')
                team_points.append(teamPoints[8].text)
                # appending the scraped data into the excel file
                self.sheet.append([teamStandings, teamName, gamesPlayed[1].text, gamesWon[2].text, gamesDrawn[3].text, gamesLost[4].text, goalScored[5].text, goalConceded[6].text, goalDifference[7].text, teamPoints[8].text])        
                self.excelSheet.save('Laliga Points Table.xlsx')
                # reading the data from the excel file using pandas
                df = pd.read_excel('Laliga Points Table.xlsx')
                for ind in df.index:
                    # printing the data from the excel file
                    print(df['Team Standings'][ind], df['Team Name'][ind], df['Games Played'][ind], df['Games Won'][ind], df['Games Drawn'][ind], df['Games Lost'][ind], df['Goals Scored'][ind], df['Goals Conceded'][ind], df['Goal Difference'][ind], df['Team Points'][ind])
                      
            # looping the second menu for the user to view the data in a visualized format using the graphs
            while(True):
                # predefined data for initializing the userinput variable
                userInput = 0
                # if loop for exception handling in case the user provides invalid entry.
                if(userInput not in range(1,5)):
                    try:
                        # user is asked to choose either of the four options in the second menu.
                        print(f"\nWhich Graph would you like to see? \nPress 1 - Graph comparing the Number of Games Won and Lost by a Team \nPress 2 - Graph comparing the Number of Goals Scored and Conceded by a Team \nPress 3 - Graph comparing the Number of Games Won and the Points Scored by a Team \nPress 4 - Exit to main menu")
                        userInput = int(input("\nEnter your choice here: "))
                    except ValueError:
                        print("\nInvalid entry!!!\nPlease enter a Valid number ")

                # if the user enters 1 then they are displayed the graph of Win-Loss comparison
                if userInput == 1:
                    # graph's title
                    plt.title("Games Win-Loss Comparison")
                    # graph's xaxis with games won data
                    xaxis = (games_won)
                    plt.xlabel("Games Won")
                    # graph's yaxis with games lost data
                    yaxis = sorted(games_lost)
                    plt.ylabel("Games Lost")
                    plt.plot(xaxis, yaxis)
                    plt.show()
                # if the user enters 2 then they are displayed the graph of teams goal scoring data
                elif userInput == 2:
                    plt.title("Goals Scoring-Conceding Comparison")
                    # graph's xaxis with goals conceded data
                    xaxis = (goal_conceded)
                    plt.xlabel("Goals Conceded")
                    # graph's yaxis with goals scored data
                    yaxis = sorted(goal_scored)
                    plt.ylabel("Goals Scored")
                    plt.bar(xaxis, yaxis)
                    plt.show()
                # if the user enters 3 then they are displayed the graph of teams points table
                elif userInput == 3:
                    plt.title("Teams Points based on matches Won")
                    # graph's xaxis with team points data
                    xaxis = sorted(team_points)
                    plt.xlabel("Team Points")
                    # graph's yaxis with games won data
                    yaxis = (games_won)
                    plt.ylabel("Games Won")
                    plt.plot(xaxis, yaxis)
                    plt.show()
                # if the user enters 4 then they exit this menu and go back to the main menu.
                elif userInput == 4:
                    print("\nReturning to Main Menu!")
                    break
                else:
                    print("\nWrong Input!!!")
                # the pause menu is used to provide a break to the user between the graphs.
                self.pauseMenu()      
        # handling the exception
        except Exception as notfound:
            print(f"This website is not available!!!{notfound}")
        
    
    # function for the pause menu
    def pauseMenu(self):
        print(input("\nPress Enter to Continue"))


# main function
def main():
    # calling the class inside the main function
    scrape = WebScraping()
    # calling the mainmenu function
    scrape.mainMenu()

if __name__ == "__main__":
    main() 