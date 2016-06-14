# -*- coding: utf-8 -*-
import pandas as pd
import requests
import collections
import matplotlib.pyplot as plt
import numpy as np

class Wiki_views(object):

    def __init__(self, title):
        if not title:
            print 'String is empty'
        if not isinstance(title, basestring):
            print 'No string type found'
        title = title.lower()
        for ch in [':', '.', '/', '\'', '-', '|', '?', '<', '>', '+', '=', '#']:
            if ch in title:
                title = title.replace(ch, ' ')        # Replace above characters with white space
        title = ' '.join(title.split())                 # Remove all multiple spaces with just one
        self.title = title

    def list_of_movies(self):
        self.movie_titles = [x.strip() for x in self.title.split(',')]
        # Creating list using inputed string seperated by ',' and removing front and back spaces (List comprehension)
    def getting_data_creating_files(self):
        # Function responsible for getting data from website to files with correct format
        for movie in self.movie_titles:
            url = 'http://stats.grok.se/json/en/201501/%s' % movie
            mon = requests.get(url).json()
            mon.get(True)
            views = {}
            views.update(mon)        # Creating base dictionary to use later for all months from specific movie
            for month in range(2,13):    # looping through every month and adding views to dict created above
                if month < 10:
                    m = '20150' + str(month)
                else:
                    m = '2015' + str(month)
                url = 'http://stats.grok.se/json/en/%s/%s' %(m, movie)
                mon2 = requests.get(url).json()
                views['daily_views'].update(mon2.get('daily_views'))
            views = collections.OrderedDict(sorted(views.items()))    # Adding new data to dictionary in order
            xx = pd.DataFrame(views)                                                  # Creating collumns using pandas library
            xx.to_json('%s.json' % movie)                                            # Exporting created Data Frame to file with name of the movie

    def graphs(self):                                   # Function responsible for ploting general graphs using viewership
        for item in self.movie_titles:
            df = pd.read_json('%s.json' %item)    # Read data from files
            aa = pd.DataFrame(df)
            a_array = np.array(aa['daily_views'])   # Using numpy to creat an array from column
            a_sum = np.sum(a_array)                    # Sum from all numbers in array
            aa = aa['daily_views']
            aa.plot(label = '\"%s\" total views: %s' % (item, a_sum))    # Using matplotlib for ploting graphs
        plt.xlabel('Date')
        plt.ylabel('Views')
        plt.title('Wiki views of different movies')
        plt.grid(True)
        plt.legend(loc='best')
        plt.show()

    def changes(self):                  # Function used to calculate changes in views from last 2 weeks
        for item in self.movie_titles:
            stats = []
            df = pd.read_json('%s.json' % item)
            aa = pd.DataFrame(df)
            a_array = np.array(aa['daily_views'])
            x = len(a_array)
            changes = []
            for i in range(x - 15, x):
                changes.append(a_array[i])
            for index in range(1, len(changes)):
                stats.append(changes[index] - changes[index - 1])
            average = sum(stats)
            N = len(stats)
            x_days = range(N)     # Number of elements in stats list
            width = 1/1                # Set width of bars as well as interval between them
            plt.figure()                 # Assuring that function will loop through all movie titles and open every graph as new window
            plt.bar(x_days, stats, width, label = '\"%s\" (average views trend: %s)' % (item, average))
            plt.legend(loc = 'best')            # Setting up a legend for graphs
            plt.grid(True)                           # Show grid on graphs
            plt.xlabel('Days')
            plt.ylabel('Changes')
            plt.title('Changes in views per day in last 2 weeks')
        plt.show()                                    # Display the graphs