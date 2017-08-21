# -*- coding: utf-8 -*-
# !/usr/bin/env python3
"""Run this to listen to the news and analyze economics"""

import news


def news_check():
    """Searches the web for shockingly good or bad news articles
    Returns:
        list: A list of couples article / sentiment"""
    parser = news.NewsParser()
    sources = parser.get_sources(category='business', language='en')
    articles = []
    for source_id in sources:
        articles += parser.get_news(source_id)
    articles = [dict(t) for t in set([tuple(d.items()) for d in articles])]
    print("Here is a list of articles you way be interested in:")
    for article in parser.feel_news(articles):
        if article['sentiment'] > 0:
            print("Good news! ")
        else:
            print("Bad news! ")
        print(article['title'])


def main():
    """
    Runs the program
    :return:
    """
    news_check()

if __name__ == '__main__':
    main()
