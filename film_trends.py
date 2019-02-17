# -*- coding: utf-8 -*-
# Name: Hawk Ticehurst
# CSE 160
# Final Project: Trends In Film Across Time

import matplotlib.pyplot as plt
import numpy as np

def read_movie_data(filename, movie_metadata_map):
    """Reads the text file at filename and given a dictionary, returns an
    updated nested dictionary mapping movieIDs to movie metadata.

    Parameters:
        filename: path to a text file containing data about a number of movies.
        movie_metadata_map: a dictionary that is either empty or maps movieIDs
        to movie metadata.

    Returns:
        movie_metadata_map: a nested dictionary mapping from movieIDs to
        dictionary containing movie metadata (such as character gender counts,
        IMBD rating, release year, and genre).
    """

    input_file = open(filename)

    # Reads in data as a list of rows
    for row in input_file:
        movie_row = row.split("+++$+++")

        # Determines if data is coming from "movie_characters_metadata.txt" or
        # "movie_titles_metadata.txt"
        if movie_row[0][0] == 'u':
            movie_metadata_map = character_data(movie_row, movie_metadata_map)
        else:
            movie_metadata_map = title_data(movie_row, movie_metadata_map)

    input_file.close()
    return movie_metadata_map

def test_read_movie_data():
    assert read_movie_data("movie_characters_sample.txt", {}) == {'m0': \
        {'female_count': 3, 'male_count': 5}, 'm1': \
        {'female_count': 0, 'male_count': 2}}
    assert read_movie_data("movie_titles_sample.txt", {}) == {'m0': {'genre': \
        ['comedy', 'romance'], 'release_year': 1999, 'imbd_rating': 6.90}, \
        'm1': {'genre': ['adventure', 'biography', 'drama', 'history'], \
        'release_year': 1992, 'imbd_rating': 6.20}, 'm2': {'genre': ['action', \
        'crime', 'drama', 'thriller'], 'release_year': 2001, 'imbd_rating': \
        6.10}, 'm3': {'genre': ['adventure', 'mystery', 'sci-fi'], \
        'release_year': 1968, 'imbd_rating': 8.40}, 'm4': {'genre': ['action', \
        'comedy', 'crime', 'drama', 'thriller'], 'release_year': 1982, \
        'imbd_rating': 6.90}, 'm5': {'genre': ['action', 'adventure', \
        'romance', 'sci-fi', 'thriller'], 'release_year': 1997, \
        'imbd_rating': 7.50}}


def character_data(movie_row, movie_map):
    """Given a list representing a row from a text file and a dictionary,
    returns an updated version of the input dictionary.

    Parameters:
        movie_row: a list of data points representing a row from a text file.
        movie_map: a dictionary that is either empty or maps movieIDs
        to other movie metadata.

    Returns:
        movie_map: a nested dictionary mapping movieIDs to character gender
        counts (and other movie metadata if already in input dictionary).
    """

    # Cleans movieID data points
    movie_id = movie_row[2].replace(' ', '')

    # If movieID not in dictioanry, creates new mapping from movieIDs to female
    # and male counts
    if movie_id not in movie_map:
        movie_map[movie_id] = {'female_count': 0, 'male_count': 0}

    character_gender = movie_row[4]

    # Updates dictionary with a movieID mapped to it's new corresponding
    # female or male count
    if character_gender != ' ? ':
        if character_gender == ' f ' or character_gender == ' F ':
            movie_map = update_gender_count('female_count', movie_id, movie_map)
        elif character_gender == ' m ' or character_gender == ' M ':
            movie_map = update_gender_count('male_count', movie_id, movie_map)

        return movie_map

    # Returns movie_map unchanged if character gender information is n/a
    else:
        return movie_map

def test_character_data():
    assert character_data(['u4069 ', ' BUCKY ', ' m270 ', \
        ' the black dahlia ', ' ? ', ' ?\n'], {}) == \
        {'m270': {'female_count': 0, 'male_count': 0}}
    assert character_data(['u8211 ', ' ANNA ', ' m558 ', ' the third man ', \
        ' f ', ' 2\n'], {}) == {'m558': {'female_count': 1, 'male_count': 0}}
    assert character_data(['u8682 ', ' BLIND MAN ', ' m589 ', ' u turn ', \
        ' m ', ' 5\n'], {}) == {'m589': {'female_count': 0, 'male_count': 1}}
    assert character_data(['u5856 ', ' JENNIFER ', ' m388 ', \
        ' highlander iii: the sorcerer ', ' F ', ' ?\n'], {}) == \
        {'m388': {'female_count': 1, 'male_count': 0}}
    assert character_data(['u8891 ', ' CHARLIE ', ' m605 ', \
        " who's your daddy? ", ' M ', ' ?\n'], {}) == \
        {'m605': {'female_count': 0, 'male_count': 1}}
    assert character_data(['u4325 ', ' NUKE ', ' m288 ', ' bull durham ', \
        ' m ', ' 3\n'], {'m288': {'female_count': 1, 'male_count': 2}}) == \
        {'m288': {'female_count': 1, 'male_count': 3}}


def update_gender_count(gender, movie_id, movie_map):
    """Given gender, movieID, and a dictionary, returns an updated dictionary
    reflecting an increase in the gender count for the input gender.

    Parameters:
        gender: a string that is either 'female_count' or 'male_count'.
        movie_id: a string representing the identification code for a movie in
        the dataset.
        movie_map: a dictionary mapping from genre to release year to gender
        count.

    Returns:
        movie_map: an updated version of the input dictionary reflecting an
        increase in the gender count for the input gender.
    """

    # Determines old gender count
    gender_count = movie_map[movie_id][gender]

    # Creates a new mapping for gender count where the count increases by one
    movie_map[movie_id][gender] = gender_count + 1

    return movie_map

def test_update_gender_count():
    assert update_gender_count('female_count', 'm74', {'m74': {'female_count': \
        2, 'genre': ['action', 'adventure', 'comedy', 'fantasy', 'sci-fi', \
        'action', 'adventure', 'comedy', 'sci-fi'], 'imbd_rating': 6.1, \
        'male_count': 5, 'release_year': 1989}, 'm79': {'female_count': 2, \
        'genre': ['crime', 'drama', 'thriller'], 'imbd_rating': 7.0, \
        'male_count': 3, 'release_year': 1990}}) == {'m74': {'female_count': \
        3, 'genre': ['action', 'adventure', 'comedy', 'fantasy', 'sci-fi', \
        'action', 'adventure', 'comedy', 'sci-fi'], 'imbd_rating': 6.1, \
        'male_count': 5, 'release_year': 1989}, 'm79': {'female_count': 2, \
        'genre': ['crime', 'drama', 'thriller'], 'imbd_rating': 7.0, \
        'male_count': 3, 'release_year': 1990}}
    assert update_gender_count('male_count', 'm528', {'m239': {'female_count': \
        1, 'genre': ['drama', 'history', 'thriller'], 'imbd_rating': 8.0, \
        'male_count': 5, 'release_year': 1976}, 'm528': {'female_count': 1, \
        'genre': ['drama', 'horror', 'mystery', 'sci-fi', 'thriller'], \
        'imbd_rating': 5.6, 'male_count': 4, 'release_year': 1998}, 'm399': \
        {'female_count': 1, 'genre': ['drama', 'fantasy'], 'imbd_rating': 7.4, \
        'male_count': 4, 'release_year': 1994}}) == {'m239': {'female_count': \
        1, 'genre': ['drama', 'history', 'thriller'], 'imbd_rating': 8.0, \
        'male_count': 5, 'release_year': 1976}, 'm528': {'female_count': 1, \
        'genre': ['drama', 'horror', 'mystery', 'sci-fi', 'thriller'], \
        'imbd_rating': 5.6, 'male_count': 5, 'release_year': 1998}, 'm399': \
        {'female_count': 1, 'genre': ['drama', 'fantasy'], 'imbd_rating': 7.4, \
        'male_count': 4, 'release_year': 1994}}


def title_data(movie_row, movie_map):
    """Given a list representing a row from a text file and a dictionary,
    returns an updated version of input dictionary.

    Parameters:
        movie_data: a list representing a row from a text file.
        movie_map: a dictionary that is either empty or maps movieIDs
        to other movie metadata.

    Returns:
        movie_map: a nested dictionary mapping movieIDs to IMBD rating,
        release year, and genre(s) (and other movie metadata if already in
        input dictionary).
    """

    # Cleans movieID data points
    movie_id = movie_row[0].replace(' ', '')

    # If movieID not in dictionary, creates new mapping from movieID to empty
    # dictionary
    if movie_id not in movie_map:
        movie_map[movie_id] = {}

    # Cleans data, converts release year to an interger, then maps movieID to
    # release year
    release_year = movie_row[2].replace('/I', '')
    release_year = release_year.replace(' ', '')
    release_year_int = int(release_year)
    movie_map[movie_id]['release_year'] = release_year_int

    # Cleans data, converts IMBD rating to a floar, then maps movieID to IMBD
    # rating
    imbd_rating = movie_row[3].replace(' ', '')
    imbd_rating_float = float(imbd_rating)
    movie_map[movie_id]['imbd_rating'] = imbd_rating_float

    # Cleans data, converts genre(s) to a list of strings, then maps movieID to
    # genre(s)
    genre = movie_row[5].replace('\n', ' ')
    replace_list = ['[', ']', '\'', ' ']
    for item in replace_list:
        genre = genre.replace(item, '')
    genre_list = genre.split(',')
    movie_map[movie_id]['genre'] = genre_list

    return movie_map

def test_title_data():
    assert title_data(['m476 ', " the ploughman's lunch ", ' 1983 ', \
        ' 6.80 ', ' 154 ', " ['drama']\n"], {}) == \
        {'m476': {'genre': ['drama'], 'release_year': 1983, \
        'imbd_rating': 6.80}}
    assert title_data(['m112 ', ' knight moves ', ' 1992 ', ' 5.80 ', \
        ' 3272 ', " ['mystery', 'thriller']\n"], {}) == {'m112': {'genre': \
        ['mystery', 'thriller'], 'release_year': 1992, 'imbd_rating': 5.80}}
    assert title_data(['m53 ', ' the elephant man ', ' 1980 ', ' 8.40 ', \
        ' 59625 ', " ['biography', 'drama', 'history']\n"], {}) == {'m53': \
        {'genre': ['biography', 'drama', 'history'], 'release_year': 1980, \
        'imbd_rating': 8.40}}
    assert title_data(['m603 ', ' the witching hour ', ' 1996 ', ' 6.50 ', \
        ' 69 ', " ['documentary', 'short']\n"], {}) == {'m603': {'genre': \
        ['documentary', 'short'], 'release_year': 1996, 'imbd_rating': 6.50}}
    assert title_data(['m112 ', ' knight moves ', ' 1992 ', ' 5.80 ', \
        ' 3272 ', " ['mystery', 'thriller']\n"], {'m476': {'genre': ['drama'], \
        'release_year': 1983, 'imbd_rating': 6.80}}) == {'m476': {'genre': \
        ['drama'], 'release_year': 1983, 'imbd_rating': 6.80}, 'm112': \
        {'genre': ['mystery', 'thriller'], 'release_year': 1992, \
        'imbd_rating': 5.80}}
    assert title_data(['m45 ', ' confidence ', ' 2003 ', ' 6.80 ', ' 17235 ', \
        " ['crime', 'thriller']\n"], {'m364': {'genre': \
        ['biography', 'drama', 'history'], 'release_year': 1982, \
        'imbd_rating': 8.20}, 'm0': {'genre': ['comedy', 'romance'], \
        'release_year': 1999, 'imbd_rating': 6.90}, 'm493': {'genre': \
        ['drama', 'romance'], 'release_year': 1968, 'imbd_rating': 7.80}}) == \
        {'m364': {'genre': ['biography', 'drama', 'history'], \
        'release_year': 1982, 'imbd_rating': 8.20}, 'm0': {'genre': \
        ['comedy', 'romance'], 'release_year': 1999, 'imbd_rating': 6.90}, \
        'm493': {'genre': ['drama', 'romance'], 'release_year': 1968, \
        'imbd_rating': 7.80}, 'm45': {'genre': ['crime', 'thriller'], \
        'release_year': 2003, 'imbd_rating': 6.80}}


def genre_to_gender(movie_map):
    """Given a dictionary, returns new dictionary that maps genre to release
    year to the difference of the of sum of female and male counts for each of
    those years.

    Parameter:
        movie_map: a dictionary that maps movieIDs to genre(s), release year,
        IMBD rating, female character count and male character count.

    Returns:
        genre_to_gender_map: a dictionary that maps genre to release year to
        the difference between the sum of female and male character counts for
        each of those years ("gender representation number").
    """

    genre_to_gender_map = {}
    movie_id = movie_map.keys()
    for movie in movie_id:

        # Locates release year and a list of genre(s) for a given movie
        year = movie_map[movie]['release_year']
        genre_list = movie_map[movie]['genre']

        # Calculates the difference between the number of female and male
        # characters for a given movie
        female = movie_map[movie]['female_count']
        male = movie_map[movie]['male_count']
        gender_difference = female - male

        if genre_list != ['']:
            for genre in genre_list:

                # Creates new mapping from genre to empty dictionary if genre
                # not in primary dictionary
                if genre not in genre_to_gender_map:
                    genre_to_gender_map[genre] = {}

                # Creates new mapping from genre to release year to the gender
                # representation number if release year not in nested genre dict
                if year not in genre_to_gender_map[genre]:
                    genre_to_gender_map[genre][year] = gender_difference

                # Updates gender represenation number if genre and release year
                # are already mapped in dictionary
                else:
                    old_diff = genre_to_gender_map[genre][year]
                    new_diff = old_diff + gender_difference
                    genre_to_gender_map[genre][year] = new_diff

    return genre_to_gender_map

def test_genre_to_gender():
    assert genre_to_gender({'m78': {'female_count': 3, 'genre': \
        ['drama', 'romance'], 'imbd_rating': 7.7, 'male_count': 9, \
        'release_year': 1932}, 'm238': {'female_count': 5, 'genre': ['drama'], \
        'imbd_rating': 8.5, 'male_count': 4, 'release_year': 1950}, 'm239': \
        {'female_count': 1, 'genre': ['drama', 'history', 'thriller'], \
        'imbd_rating': 8.0, 'male_count': 5, 'release_year': 1976}, 'm528': \
        {'female_count': 1, 'genre': \
        ['drama', 'horror', 'mystery', 'sci-fi', 'thriller'], 'imbd_rating': \
        5.6, 'male_count': 4, 'release_year': 1998}}) == {'drama': {1932: -6, \
        1950: 1, 1976: -4, 1998: -3}, 'romance': {1932: -6}, 'history': \
        {1976: -4}, 'thriller': {1976: -4, 1998: -3}, 'horror': {1998: -3}, \
        'mystery': {1998: -3}, 'sci-fi': {1998: -3}}
    assert genre_to_gender({'m78': {'female_count': 3, 'genre': \
        ['drama', 'romance'], 'imbd_rating': 7.7, 'male_count': 9, \
        'release_year': 1932}, 'm238': {'female_count': 5, 'genre': ['drama'], \
        'imbd_rating': 8.5, 'male_count': 4, 'release_year': 1950}, 'm239': \
        {'female_count': 1, 'genre': ['drama', 'history', 'thriller'], \
        'imbd_rating': 8.0, 'male_count': 5, 'release_year': 1976}, 'm528': \
        {'female_count': 1, 'genre': ['drama', 'horror', 'mystery', 'sci-fi', \
        'thriller'], 'imbd_rating': 5.6, 'male_count': 4, 'release_year': \
        1998}, 'm399': {'female_count': 1, 'genre': ['drama', 'fantasy'], \
        'imbd_rating': 7.4, 'male_count': 4, 'release_year': 1950}}) == \
        {'drama': {1932: -6, 1950: -2, 1976: -4, 1998: -3}, 'romance': \
        {1932: -6}, 'history': {1976: -4}, 'thriller': {1976: -4, 1998: -3}, \
        'horror': {1998: -3}, 'mystery': {1998: -3}, 'sci-fi': {1998: -3}, \
        'fantasy': {1950: -3}}


def genre_to_rating(movie_map):
    """Given a dictionary, returns new dictionary that maps genre to release
    year to a list of IMBD ratings for each of those years.

    Parameter:
        movie_map: a dictionary that maps movieIDs to genre(s), release year,
        IMBD rating, female character count and male character count.

    Returns:
        genre_to_rating_map: a dictionary that maps genre to release year to
        a list of IMBD ratings for each of those years.
    """

    genre_to_rating_map = {}
    movie_id = movie_map.keys()
    for movie in movie_id:

        # Locates release year, IMBD rating, and list of genre(s) for a given
        # movie
        year = movie_map[movie]['release_year']
        rating = movie_map[movie]['imbd_rating']
        genre_list = movie_map[movie]['genre']

        if genre_list != ['']:
            for genre in genre_list:

                # Creates new mapping from genre to empty dictionary if genre
                # not in primary dictionary
                if genre not in genre_to_rating_map:
                    genre_to_rating_map[genre] = {}

                # Creates new mapping from genre to release year to empty list
                # if release year not in nested genre dictionary
                if year not in genre_to_rating_map[genre]:
                    genre_to_rating_map[genre][year] = []

                # Locates IMBD rating list mapped to given genre and release
                # year then appends newly calculated rating to list
                rating_list = genre_to_rating_map[genre][year]
                rating_list.append(rating)

    return genre_to_rating_map

def test_genre_to_rating():
   assert genre_to_rating({'m550': {'female_count': 2, 'genre': ['drama', \
        'mystery', 'thriller'], 'imbd_rating': 7.7, 'male_count': 3, \
        'release_year': 1997}, 'm209': {'female_count': 1, 'genre': ['drama', \
        'horror', 'thriller'], 'imbd_rating': 7.4, 'male_count': 3, \
        'release_year': 1945}, 'm208': {'female_count': 5, 'genre': ['horror', \
        'romance', 'thriller'], 'imbd_rating': 7.9, 'male_count': 1, \
        'release_year': 1963}, 'm201': {'female_count': 1, 'genre': ['crime', \
        'horror', 'sci-fi', 'thriller'], 'imbd_rating': 5.8, 'male_count': 3, \
        'release_year': 2004}}) == {'drama': {1997: [7.7], 1945: [7.4]}, \
        'mystery': {1997: [7.7]}, 'thriller': {1997: [7.7], 1945: [7.4], 1963: \
        [7.9], 2004: [5.8]}, 'horror': {1945: [7.4], 1963: [7.9], 2004: \
        [5.8]}, 'romance': {1963: [7.9]}, 'crime': {2004: [5.8]}, 'sci-fi': \
        {2004: [5.8]}}
   assert genre_to_rating({'m550': {'female_count': 2, 'genre': ['drama', \
        'mystery', 'thriller'], 'imbd_rating': 7.7, 'male_count': 3, \
        'release_year': 1997}, 'm209': {'female_count': 1, 'genre': ['drama', \
        'horror', 'thriller'], 'imbd_rating': 7.4, 'male_count': 3, \
        'release_year': 1945}, 'm208': {'female_count': 5, 'genre': ['horror', \
        'romance', 'thriller'], 'imbd_rating': 7.9, 'male_count': 1, \
        'release_year': 1963}, 'm201': {'female_count': 1, 'genre': ['crime', \
        'horror', 'sci-fi', 'thriller'], 'imbd_rating': 5.8, 'male_count': 3, \
        'release_year': 2004}, 'm88': {'female_count': 1, 'genre': ['mystery', \
        'thriller'], 'imbd_rating': 8.9, 'male_count': 3, 'release_year': \
        1945}}) == {'drama': {1997: [7.7], 1945: [7.4]}, 'mystery': {1997: \
        [7.7], 1945: [8.9]}, 'thriller': {1997: [7.7], 1945: [7.4, 8.9], 1963: \
        [7.9], 2004: [5.8]}, 'horror': {1945: [7.4], 1963: [7.9], 2004: \
        [5.8]}, 'romance': {1963: [7.9]}, 'crime': {2004: [5.8]}, 'sci-fi': \
        {2004: [5.8]}}


def year_to_rating(movie_map):
    """Given a dictionary, returns new dictionary that maps release year to a
    list of IMBD ratings for each of those years.

    Parameter:
        movie_map: a dictionary that maps movieIDs to genre(s), release year,
        IMBD rating, female character count and male character count.

    Returns:
        year_to_rating_map: a dictionary that maps release year to a list of
        IMBD ratings for each of those year.
    """

    year_to_rating_map = {}
    movie_id = movie_map.keys()
    for movie in movie_id:

        # Locates release year and IMBD rating for a given movie
        year = movie_map[movie]['release_year']
        rating = movie_map[movie]['imbd_rating']

        # Creates new mapping from genre to release year to empty list
        # if release year not in dictionary
        if year not in year_to_rating_map:
            year_to_rating_map[year] = []

        # Locates IMBD rating list mapped to given release year then appends
        # newly calculated rating to list
        rating_list = year_to_rating_map[year]
        rating_list.append(rating)

    return year_to_rating_map

def test_year_to_rating():
    assert year_to_rating({'m260': {'female_count': 1, 'genre': ['action', \
        'adventure', 'crime', 'drama', 'sci-fi'], 'imbd_rating': 6.5, \
        'male_count': 5, 'release_year': 1949}, 'm359': {'female_count': 3, \
        'genre': ['horror'], 'imbd_rating': 5.1, 'male_count': 2, \
        'release_year': 1982}, 'm509': {'female_count': 1, 'genre': \
        ['adventure', 'drama', 'western'], 'imbd_rating': 8.1, 'male_count': \
        3, 'release_year': 1956}, 'm541': {'female_count': 2, 'genre': \
        ['action', 'adventure', 'comedy', 'fantasy', 'sci-fi'], 'imbd_rating': \
        4.7, 'male_count': 3, 'release_year': 1982}, 'm418': {'female_count': \
        1, 'genre': ['action', 'comedy', 'horror', 'thriller'], 'imbd_rating': \
        5.4, 'male_count': 4, 'release_year': 1999}}) == {1949: [6.5], 1982: \
        [4.7, 5.1], 1956: [8.1], 1999: [5.4]}


def sorted_years_list(genre_map, genre):
    """Given a dictionary and a genre, returns a sorted list of release years
    for that genre.

    Parameters:
        genre_map: a dictionary mapping genre to release year to either IMBD
        rating or gender representation number.
        genre: a string representing a movie genre

    Returns:
        sorted_years_list: a list of movie release years sorted chronologically
    """

    # Creates a list of release years for a given genre
    sorted_years_list = genre_map[genre].keys()

    # Sorts list of release years chronologically
    sorted_years_list.sort()

    return sorted_years_list

def test_sorted_years_list():
    assert sorted_years_list({'film-noir': {1955: -1, 1957: 0, 1950: -1, 1949: \
        -4}, 'short': {2000: -1, 2010: 0, 1996: -1, 1998: 2}, 'music': {1984: \
        -4, 1989: 0, 1990: 0, 1927: 0, 1992: 1, 1995: -1, 1964: -6, 1999: \
        -4, 2000: -3, 2001: -3, 1975: -3}}, 'film-noir') == [1949, 1950, 1955, \
        1957]
    assert sorted_years_list({'musical': {1993: [8.0], 1933: [8.1], 1934: \
        [6.9], 1997: [6.6], 1939: [8.3], 1975: [7.1], 1999: [7.8], 1981: \
        [5.4]}, 'documentary': {1996: [6.5], 2006: [6.3], 2007: [7.0]}, \
        'short': {2000: [4.8, 6.5], 2010: [8.3], 1996: [6.5], 1998: [6.7]}, \
        'film-noir': {1955: [8.2], 1957: [8.2], 1950: [8.7], 1949: [8.5]}}, \
        'short') == [1996, 1998, 2000, 2010]


def print_movie_gender_results(genre_to_gender_map):
    """Given a dictionary, prints the the gender representation number for each
    year for each genre formatted as:

        *genre*
        *space*
        *release year* : *gender representation number*

    Parameters:
        genre_to_gender_map: a dictionary mapping genres to movie release years
        to the difference between the sum of female and male character counts
        (gender represenation number) for each year.

    Returns:
        None
    """

    # Prints research question and explanation of gender representation numbers
    print "HOW HAS GENDER REPRESENTATION IN ALL GENRES CHANGED OVER TIME?"
    print
    print "A positive number represents *n* more women than men."
    print "A negative number represents *n* more men than women."
    print "A zero represents equal gender represenation."
    print

    # Creates sorted genre list
    genre_list = genre_to_gender_map.keys()
    genre_list.sort()

    for genre in genre_list:
        years_list = sorted_years_list(genre_to_gender_map, genre)

        print "Genre:", genre

        # Locates and prints gender representation number for each year for each
        # genre
        for year in years_list:
            gender_diff = genre_to_gender_map[genre][year]
            print str(year) + ":", gender_diff
        print

    return None


def print_movie_rating_results(genre_to_rating_map):
    """Given a dictionary, prints the average IMBD ratings for each year for
    each genre formatted as:

        *genre*
        *space*
        *release years* : *average IMBD rating*

    Parameters:
        genre_to_rating_map: a dictionary that maps genres to release years to
        a list of IMBD ratings for each year.

    Returns:
        None
    """

    # Prints research question and explanation of calculations on IMBD ratings
    print "HOW HAVE AVERAGE IMBD RATINGS CHANGED ACROSS GENRES OVER TIME?"
    print
    print "Each rating is an average of all the IMBD ratings for that year."
    print

    # Creates sorted genre list
    genre_list = genre_to_rating_map.keys()
    genre_list.sort()

    for genre in genre_list:
        years_list = sorted_years_list(genre_to_rating_map, genre)

        print "Genre:", genre

        # Calculates the average IMBD rating for each year for each genre
        for year in years_list:
            rating_list = genre_to_rating_map[genre][year]
            avg_rating = sum(rating_list) / float(len(rating_list))

            print str(year) + ":", avg_rating
        print

    return None


def plot_movie_gender_results(genre_to_gender_map):
    """Given a dictionary, plots the gender representation number for each year
    for each genre.

    Parameters:
        genre_to_gender_map: a dictionary mapping genres to movie release years
        to the difference between the sum of female and male character counts
        (gender representation number) for each year.

    Returns:
        None
    """

    # Creates graph
    plt.ylabel('Gender Represenation Number')
    plt.xlabel('Years')

    # Creates list of genres
    genre_list = genre_to_gender_map.keys()

    gender_num_list = []
    for genre in genre_list:

        # Creates chronologically sorted list of years for each genre
        years_list = sorted_years_list(genre_to_gender_map, genre)

        for year in years_list:

            # Creates list of gender represenation numbers for each year for
            # each genre
            gender_num = genre_to_gender_map[genre][year]
            gender_num_list.append(gender_num)

        # Plots years on x-axis and gender representation number on y-axis for
        # each genre
        plt.plot(years_list, gender_num_list, label = genre)

        years_list = []
        gender_num_list = []

    # Shows graph legend, resizes graph window, saves graph as .png and then
    # clears graph
    lgd = plt.legend(bbox_to_anchor = (1, 1.04), loc = 2, borderaxespad = 1.5, \
        prop = {'size': 10})
    plt.savefig("movie-gender-results.png", bbox_extra_artists = (lgd,), \
        bbox_inches = 'tight', dpi = 300)
    plt.clf()

    return None


def plot_movie_rating_results(genre_to_rating_map):
    """Given a dictionary, plots the average IMBD rating for each year for
    each genre.

    Parameters:
        genre_to_rating_map: a dictionary that maps genres to release years to
        a list of IMBD ratings for each year.

    Returns:
        None
    """

    # Creates graph
    plt.ylabel('IMBD Rating')
    plt.xlabel('Years')

    # Creates list of genres
    genre_list = genre_to_rating_map.keys()

    rating_list = []
    for genre in genre_list:

        # Creates chronologically sorted list of years for each genre
        years_list = sorted_years_list(genre_to_rating_map, genre)

        for year in years_list:

            # Creates list of average IMBD ratings for each year for each genre
            rating = genre_to_rating_map[genre][year]
            avg_rating = sum(rating) / float(len(rating))
            rating_list.append(avg_rating)

        # Plots years on x-axis and IMBD ratings on y-axis for each genre
        plt.plot(years_list, rating_list, label = genre)

        years_list = []
        rating_list = []

    # Shows graph legend, resizes graph window, saves graph as .png and then
    # clears graph
    lgd = plt.legend(bbox_to_anchor = (1, 1.04), loc = 2, borderaxespad = 1.5, \
        prop = {'size': 10}, scatterpoints = 1)
    plt.savefig("movie-rating-results.png", bbox_extra_artists = (lgd,), \
        bbox_inches = 'tight', dpi = 300)
    plt.clf()

    return None


def plot_rating_line_of_best_fit(year_to_rating_map):
    """Given a dictionary, plots the average IMBD rating for each year across
    all genres with a line of best fit.

    Parameters:
        year_to_rating_map: a dictionary that maps release years to a list of
        IMBD ratings for each of those years.

    Returns:
        None
    """

    # Creates graph
    plt.ylabel('IMBD Rating')
    plt.xlabel('Years')

    # Creates chronologically sorted list of years
    years_list = year_to_rating_map.keys()
    years_list.sort()

    avg_rating_list = []
    for year in years_list:

        # Creates list of average IMBD ratings for each year across all genres
        rating = year_to_rating_map[year]
        avg_rating = sum(rating) / float(len(rating))
        avg_rating_list.append(avg_rating)

    # Plots scatter points of years on x-axis and average IMBD ratings on y-axis
    # across all genres
    plt.scatter(years_list, avg_rating_list)

    # Plots the line of best fit
    plt.plot(np.unique(years_list), np.poly1d(np.polyfit( years_list, \
        avg_rating_list, 1))(np.unique(years_list)))

    # Saves graph as .png and clears graph
    plt.savefig("ratings-line-of-best-fit.png", dpi = 300)
    plt.clf()

    return None

################################################################################
# TEST FUNCTIONS
################################################################################

test_read_movie_data()
test_character_data()
test_update_gender_count()
test_title_data()
test_genre_to_gender()
test_genre_to_rating()
test_year_to_rating()
test_sorted_years_list()

################################################################################
# MAIN PROGRAM
################################################################################

def main():
    """Main function, executed when film_trends.py is run as a Python
    script.
    """

    movie_map = {}

    # Reads in data from .txt files and generate a movie metadata dictionary
    # mapping movieID to gender representation numbers, release year, IMBD
    # rating, and genre(s)
    character_map = read_movie_data("data/movie_characters_metadata.txt", movie_map)
    movie_map = read_movie_data("data/movie_titles_metadata.txt", character_map)

    # Creates dictionary mapping genre to release year to gender representation
    # numbers
    genre_to_gender_map = genre_to_gender(movie_map)

    # Creates dictionary mapping genre to release year to a list of IMBD ratings
    genre_to_rating_map = genre_to_rating(movie_map)

    # Creates dictionary mapping each release year to a list of IMBD ratings
    year_to_rating_map = year_to_rating(movie_map)

    # Prints the gender representation number for each year for each genre
    print_movie_gender_results(genre_to_gender_map)

    # Prints the average IMBD ratings for each year for each genre
    print_movie_rating_results(genre_to_rating_map)

    # Plots the gender representation number for each year for each genre
    plot_movie_gender_results(genre_to_gender_map)

    # Plots the average IMBD rating for each year for each genre
    plot_movie_rating_results(genre_to_rating_map)

    # Plots the average IMBD rating for each year across all genres with a line
    # of best fit
    plot_rating_line_of_best_fit(year_to_rating_map)


# The code in this function is executed when this file is run as a Python
# program
if __name__ == "__main__":
    main()
