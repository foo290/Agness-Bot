"""
This module contains two web crawlers: One for scraping the results kof organic search of google and second is for
wikipedia.

This is used in search system for given query in bot.
"""

from bs4 import BeautifulSoup as bs
import requests
import json
import os
from .decorators import export

cwd = os.getcwd()

if not os.path.exists(f'{cwd}/web_crawler_cache'):
    os.mkdir(f'{cwd}/web_crawler_cache')

default_cache_loc = f'{cwd}/web_crawler_cache'


class CacheManager:
    """
    A cache system that stores previously fetched files and shows directly from stored files
    if query matches in future rather than searching again on internet.
    """

    def __init__(self):
        pass

    def read_cache(self, query, directory):
        """ Returns a saved file if found in saved files """

        file_names = []

        if query.lower() not in file_names:
            for files in os.listdir(directory):
                if files:
                    f_name = files.split('.json')[0]
                    file_names.append(f_name.lower()) if f_name.lower() not in file_names else print()

                    if query.lower() == f_name.lower():
                        with open(f'{directory}/{f_name}.json') as file:
                            cache = json.load(file)
                        return cache
                    else:
                        pass
                else:
                    return 0
        else:
            temp_ind = file_names.index(query)
            with open(f'{file_names[temp_ind]}.json') as f:
                cache = json.load(f)
            return cache

    def write_cache(self, file_name, data, directory):
        """
        Writes the search results into the memory
        file name will be automatically set as query name.
        """

        try:
            with open(f'{directory}/{file_name}.json', 'w') as file:
                json.dump(data, file, indent=4)
            return 1
        except Exception as error:
            print(error)
            return 0


@export
class GoogleWebCrawler:
    """
    A web crawler for extracting the search results from google organic search results
    :param query, cache_location: Name of the query and location to store json file
    cache_location must be a directory not file
    """

    def __init__(self, query, cache_location=default_cache_loc, command='start'):
        if command == 'start':
            self.query = query
            self.cache_dir = cache_location

            self.query_shortsummary = {}

            self.cache_object = CacheManager()
            self.cached_data = ''
            self.cache_found = self.cache_object.read_cache(self.query, self.cache_dir)
            self.connection_status = 1

            if not self.cache_found:
                try:
                    self.source = requests.get(f'https://www.google.com/search?q={self.query}').text
                    self.soup = bs(self.source, 'lxml')
                    self.level1 = self.soup.find('div', id='Main')
                    print(self.level1)
                except Exception as error:
                    if str(error).split(':')[-2].strip() == 'Failed to establish a new connection':
                        self.connection_status = 0
            else:
                self.cached_data = self.cache_found

    def fetch_webpage(self, results=5, manage_cache=True):
        """
        :param results:
            Take "results" as argument which is number of results you want.

        :returns dictionaries:
            A dict containing headings and its content {Heading : Content},
            A dict containing headings and its links {Heading : Link}
            An additional variable containing short summary of query
        """

        headings_content_dic = {}
        heading_link_dic = {}

        if not self.cached_data:
            if self.connection_status:

                # shortsum = self.level1.find('div', class_='BNeawe s3v9rd AP7Wnd').text
                # self.query_shortsummary[self.query] = shortsum
                r = results
                for parsed_content in self.soup.find_all('div', class_='ZINbbc xpd O9g5cc uUPGi'):
                    try:
                        title = parsed_content.h3.text
                        details = parsed_content.find('div', class_='BNeawe s3v9rd AP7Wnd').text

                        webpage_link = parsed_content.find('div', class_='BNeawe UPmit AP7Wnd').text
                        webpage_link = "/".join(str(webpage_link).split(' › '))

                        headings_content_dic[title] = details
                        heading_link_dic[title] = webpage_link
                        # r -= 1
                        # if not r:
                        break
                    except:
                        r -= 1
                        pass
                if manage_cache:
                    if not self.cache_object.write_cache(self.query,
                                                         (headings_content_dic, heading_link_dic,
                                                          self.query_shortsummary),
                                                         self.cache_dir):
                        print('Can not save cache file due to an error.')
                return headings_content_dic, heading_link_dic
            else:
                return 0
        else:
            return self.cached_data


@export
class WikipediaCrawler:
    """ A Fast web crawler that fetches a topic on wikipedia """

    def __init__(self, query, cache_location_wiki=default_cache_loc, command='start'):
        self.cache_dir = cache_location_wiki
        self.cache_object = CacheManager()
        self.cached_data = ''
        self.connection_status = 1

        if command == 'start':
            self.cache_found = self.cache_object.read_cache(query, self.cache_dir)
            if not self.cache_found:
                try:
                    print('beep_')
                    self.topic = query
                    self.source = requests.get(f'https://en.wikipedia.org/wiki/{self.topic}').text
                    self.soup = bs(self.source, 'lxml')
                    self.summary = self.soup.find('div', class_='mw-body')
                    self.level2 = self.summary.find('div', class_='mw-content-ltr')
                    self.level3 = self.level2.find('div', class_='mw-parser-output')
                except Exception as error:
                    if str(error).split(':')[-2].strip() == 'Failed to establish a new connection':
                        self.connection_status = 0
            else:
                self.cached_data = self.cache_found

    def fetch_wiki(self):
        """
        :return dictionary: A dic "headings_content" containing heading and its content
        """
        headings_content = {}
        try:
            if not self.cached_data:
                if self.connection_status:
                    heading = [self.summary.h1.text]
                    content = []
                    for para in self.level3.find_all('p'):
                        content.append(para.text)
                    content = [i.strip() for i in content if i != '\n']
                    headings_content[heading[0]] = content
                    if not self.cache_object.write_cache(heading[0], headings_content, self.cache_dir):
                        print('can not save cache file due to an internal error')
                    return headings_content
                else:
                    return 0
            else:
                return self.cached_data
        except Exception as error:
            return error
