import sys
import pandas as pd
import requests
from bs4 import BeautifulSoup as bs

def Airbnb_webscrape(city_name, state_name, number_of_runs=3, max_pages = 14):
    '''Defines css class identifiers to be used in spider and webscraper'''
    airbnb_url = 'https://airbnb.com'
    next_page_class = '_za9j7e',
    #features to be scraped
    title_class = '_bzh5lkq',
    type_location_class = '_167qordg',
    price_class = '_l2ulkt8',
    rooms_class = '_kqh46o'
    listing_links_class = '_gjfol0'
    forbidden_characters = [',', '.', '✪', '|', '/', '"', '*', '-', '+',
                          '✤', '♥', '~', '☆', '🎓','🌟','🚑','⚡', '🌈'
                          '★','☀','❤','✔', '🏳️', '★']



    def city_url(city_name, state_name, country='United-States'):
        '''build url for city and check in and out dates'''
        base = 'https://www.airbnb.com/s/'
        post = '/homes?tab_id=home_tab&refinement_paths'
        url = base + city_name + '--' + state_name + '--' + country + post
        return str(url)

    def get_page_links(url):
        '''get links for pages of listings, max number is 15 pages'''

        # add first page to list
        page_links = []
        page_links.append(url)
        link = url

        # add pages 2-15 to list
        for i in range(max_pages):
            try:
            # make soup and extraxt next page link
                page = requests.get(link)
                soup = bs(page.content, 'html.parser')
                link = soup.find(class_=next_page_class).get('href')
                link = airbnb_url + link
                page_links.append(link)
            except:
                print('page limit reached')
                break
        print(len(page_links))
        return page_links

    def scrape_listings_from_page(url):
        '''scrapes multi listing page, only extracts basic info'''
        # make soup
        page = requests.get(url)
        soup = bs(page.content, 'html.parser')

        # scrape titles and remove special characters
        titles = []
        for i in soup.find_all(class_=title_class):
            t = i.get_text()
            for character in forbidden_characters:
                t = t.replace(character, ' ')
            titles.append(t)

        # scrape dwelling type and location, split text and append into 2 separate lists
        dwelling_types = []
        locations = []
        for i in soup.find_all(class_=type_location_class):
            t = i.get_text()
            if 'reviews' not in t:
                split = t.find(' in ')
                dwelling_type = t[:split]
                dwelling_types.append(dwelling_type)
                location = t[split:].replace('in ', '')
                locations.append(location)

        # scrape prices, leave only numbers
        prices = []
        for i in soup.find_all(class_=price_class):
            t = i.get_text()
            t = t.replace('From', '')
            t = t.replace('Price:$', '')
            t = t.replace(' / night', '')
            prices.append(t)

        # scrape room description and featured amentities
        rooms_amenities = []
        for i in soup.find_all(class_=rooms_class):
            rooms_amenities.append(i.get_text())

        rooms = []
        n = 0
        for i in range(len(titles)):
            rooms.append(rooms_amenities[n])
            n += 2

        # split rooms
        guests = []
        bedrooms = []
        beds = []
        bathrooms = []
        for i in rooms:
            words = ['guests', 'guest', 'bedrooms', 'bedroom', 'beds', 'bed', 'bath' 'baths']
            for word in words:
                i = i.replace(word, '')
            t = i.split('·')
            if len(t) == 4:
                guests.append(t[0])
                bedrooms.append(t[1])
                beds.append(t[2])
                bathrooms.append(t[3])
            else:
                guests.append('1')
                bedrooms.append('1')
                beds.append('1')
                bathrooms.append('1')

        # split amenities
        amenities = []
        n = 1

        for i in range(len(titles)):
            amenities.append(rooms_amenities[n])
            n += 2

        amenity_1 = []
        amenity_2 = []
        amenity_3 = []
        amenity_4 = []

        for i in amenities:
            t = i.split('·')
            if len(t) == 4:
                amenity_1.append(t[0])
                amenity_2.append(t[1])
                amenity_3.append(t[2])
                amenity_4.append(t[3])
            elif len(t) == 3:
                amenity_1.append(t[0])
                amenity_2.append(t[1])
                amenity_3.append(t[2])
                amenity_4.append('None')
            elif len(t) == 2:
                amenity_1.append(t[0])
                amenity_2.append(t[1])
                amenity_3.append('None')
                amenity_4.append('None')
            elif len(t) == 1:
                amenity_1.append(t[0])
                amenity_2.append('None')
                amenity_3.append('None')
                amenity_4.append('None')
            elif len(t) == 0:
                amenity_1.append('None')
                amenity_2.append('None')
                amenity_3.append('None')
                amenity_4.append('None')



        # scrape individual listing urls
        listing_links = []
        for link in soup.find_all(class_=listing_links_class):
            link = link.get('href')
            link = airbnb_url + link
            listing_links.append(link)

        # print(len(titles))
        # print(len(dwelling_types))
        # print(len(locations))
        # print(len(prices))
        # print(len(guests))
        # print(len(bedrooms))
        # print(len(beds))
        # print(len(bathrooms))
        # print(len(amenity_1))
        # print(len(amenity_2))
        # print(len(amenity_3))
        # print(len(amenity_4))
        # print(len(listing_links))

        print(len(titles) == len(locations) == len(prices) == len(guests) == len(bedrooms) == len(bathrooms) == len(
            amenity_1) == len(amenity_2) == len(amenity_3) == len(amenity_4) )

        # Build listing list objects
        listings = []
        column_headers = ['title', 'type', 'location', 'price',
                          'guests', 'bedrooms', 'beds',
                          'bathrooms', 'amenity_1', 'amenity_2',
                          'amenity_3', 'amenity_4', 'link']
        # listings.append(column_headers)
        for t, type, loc, p, g, bdr, bed, bath, a1, a2, a3, a4, li in zip(titles, dwelling_types,locations,
                                                                          prices, guests, bedrooms,
                                                                          beds, bathrooms, amenity_1,
                                                                          amenity_2,amenity_3, amenity_4,
                                                                          listing_links):
            listing = []
            f = [t, type, loc, p, g, bdr, bed, bath, a1, a2, a3, a4, li]
            for i in f:
                listing.append(i)

            listings.append(listing)
        ldf = pd.DataFrame(listings)
        return ldf

    def scrape_city(city_name, state_name, write_csv = False, csv_output = r'/home/kfrech/project/airbnb_webscrape/csv/'):
        '''returns a maximum of 300 results per run and outputs to csv'''
        try:
            url = city_url(city_name, state_name)
            page_links = get_page_links(url)
            headers = []
            column_headers = ['title', 'type', 'location', 'price',
                              'guests', 'bedrooms', 'beds',
                              'bathrooms', 'amenity_1', 'amenity_2',
                              'amenity_3', 'amenity_4', 'link']
            headers.append(column_headers)
            city_df = pd.DataFrame(headers)

            for url in page_links:
                listing_df = scrape_listings_from_page(url)
                city_df = city_df.append(listing_df)
            if write_csv:
                csv_name = f"{city_name}_{state_name}_airbnb.csv"
                city_df.to_csv(csv_output + csv_name)

        finally:
            print('run complete')
            return city_df

    def multi_run_scrape(city_name, state_name, number_of_runs, write_csv = True, csv_output = r'/home/kfrech/project/airbnb_webscrape/csv/'):
        '''runs the city scraper for given number of runs and removes duplicates
        writes to csv'''
        headers = []
        column_headers = ['title', 'type', 'location', 'price',
                          'guests', 'bedrooms', 'beds',
                          'bathrooms', 'amenity_1', 'amenity_2',
                          'amenity_3', 'amenity_4', 'link']
        headers.append(column_headers)
        city_df = pd.DataFrame(headers)
        for i in range(number_of_runs):
            run_df = scrape_city(city_name, state_name)
            city_df = city_df.append(run_df)
        city_df = city_df.drop_duplicates()
        print('duplicates:')
        print(number_of_runs * 300  - len(city_df.index))
        if write_csv:
            csv_name = f"{city_name}_{state_name}_airbnb.csv"
            city_df.to_csv(csv_output + csv_name)
        print('webscrape complete')
        return city_df
    multi_run_scrape(city_name, state_name, number_of_runs)

if __name__ == "__main__":
    Airbnb_webscrape(sys.argv[1], sys.argv[2])
