#!/usr/bin/python
import csv
from datetime import datetime
import feedparser

from feeds import FEED_URLS


def get_posts():
    posts = {}
    for url in FEED_URLS:
        feed = feedparser.parse(url)
        for entry in feed.entries:
            key = (entry.id, entry.title)
            text = entry.title.lower() + ' ' + entry.description.lower()
            has_trump = 'trump' in text or 'president' in text
            post_data = {
                'title': entry.title,
                'link': entry.link,
                'description': entry.description,
                'published': entry.published,
                'id': entry.id,
                'title_description': text,
                'trump': str(has_trump)
            }
            posts[key] = post_data

    today = datetime.today().date()
    fieldnames = ['key', 'title', 'link', 'description', 'published',
                  'id', 'title_description', 'trump']
    with open('raw_posts_{}.csv'.format(today), 'w') as raw_outfile:
        with open('filtered_posts_{}.csv'.format(today), 'w') as filtered_outfile:
            raw_writer = csv.DictWriter(raw_outfile, fieldnames=fieldnames)
            filtered_writer = csv.DictWriter(filtered_outfile, fieldnames=fieldnames)
            raw_writer.writeheader()
            filtered_writer.writeheader()
            for row in posts.values():
                formatted_row = {field: value.encode('utf-8') for field, value in row.items()}
                raw_writer.writerow(formatted_row)
                if formatted_row['trump'] == 'True':
                    filtered_writer.writerow(formatted_row)

              
if __name__ == '__main__':
    get_posts()

