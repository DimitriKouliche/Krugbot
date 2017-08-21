# -*- coding: utf-8 -*-
# !/usr/bin/env python3
"""This module handles news feed"""

import logging
import os
import requests
from textblob import TextBlob

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)


class NewsParser:
    """NewsParser retrieves news to parse.
     Attributes:
         self.NEWS_API_KEY (str): An API to consume news API, stored in an environment variable"""
    NEWS_API_KEY = os.environ["NEWS_API_KEY"]
    THRESHOLD = 0.15

    def get_sources(self, category, language):
        """Retrieves sources from news API
        Args:
            category (str): A category to target certain types of news
            language (str): A language in which we want the news to be written in
        Returns:
            list: A list of source IDs"""
        sources = []
        payload = {'category': category, 'language': language, 'apiKey': self.NEWS_API_KEY}
        request = requests.get('https://newsapi.org/v1/sources', params=payload)
        for source in request.json()['sources']:
            sources.append(source['id'])
        return sources

    def get_news(self, source_id):
        """Retrieves news from news API using a source
        Args:
            source_id (str): A source id
        Returns:
            list: A list of news"""
        payload = {'source': source_id, 'sortBy': 'latest', 'apiKey': self.NEWS_API_KEY}
        request = requests.get('https://newsapi.org/v1/articles', params=payload)
        response = request.json()
        if 'articles' in response:
            return response['articles']
        return []

    def feel_news(self, articles):
        """Returns a list of couples with article title and sentiment felt when reading it
        Args:
            articles (list): A list of articles
        Returns:
            list: A list of couples article / sentiment"""
        news_pieces = []
        for article in articles:
            news_piece = {}
            if 'title' in article:
                blob = TextBlob(article['title'])
                sentiment = blob.sentiment.polarity / (blob.sentiment.subjectivity + 2)
                if abs(sentiment) > self.THRESHOLD:
                    news_piece['title'] = article['title']
                    news_piece['sentiment'] = sentiment
            if news_piece:
                news_pieces.append(news_piece)
        return news_pieces
