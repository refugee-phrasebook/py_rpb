# -*- coding: utf-8 -*-

"""
Scrape rpb

Examples
--------

>>> sheet_uri = 'https://docs.google.com/spreadsheets/u/1/d/1D21SK15oYTRrCWMEi8J6txiCWCYkuhEbkSqSCqGAQx4/pubhtml?gid=0&single=true'
    s = SheetScraper(sheet_uri, to_row=106)
    s.fetch()
    s.all_languages()
    s.select_columns(0, 7, 9, 11, 13, 19, 33)
    s.selected_languages()
    o = s.output_sections()
    print('\n'.join(o))

    with open('example-output-mediawiki.txt', 'wt') as ft:
        ft.write('\n'.join(o))
        ft.write('\n')

    with open('example-output-html.html', 'wt') as ft:
        h = s.output_sections(fmt='html')
        ft.write('\n'.join(h))
        ft.write('\n')

[('German', 0),
 ('Arabic / Syrian Phonetic', 1),
 ('English', 2),
 ('French', 3),
 ('Slovenian', 5),
 ('Dutch', 6),
 ('Urdu', 7),
 ('Urdu Phonetic', 8),
 ('Bangla / বাংলা ', 9),
  .
  .
  .
 ('mandarin  / (chinese)', 40)]


"""
import re
import logging
from itertools import tee

import requests
from bs4 import BeautifulSoup

from py_rpb.tabulate import tabulate

logger = logging.getLogger(__name__)


def pairwise(iterable):
    """s -> (s0,s1), (s1,s2), (s2, s3), ..."""
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


def human_range_to_slice(from_val=None, to_val=None):
    """
    Prepare a human from - to range (including from, including to) for a python slice
    """
    if from_val:
        from_val -= 1
    if to_val:
        to_val += 1
    return dict(slice_i=from_val,
                slice_j=to_val)


def fetch_sheet(sheet_uri):
    try:
        return requests.get(sheet_uri)
    except requests.exceptions.RequestException as e:
        logger.error('Could not fetch %s: %s', sheet_uri, e)


def scrape_google_sheet(html, slice_i=None, slice_j=None):
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.findAll('table')[0]

    # Find all rowheaders in sheet having id 0Rx
    pattern = re.compile('^0R(\d+)')
    rh = table.find_all('th', {'id': pattern})

    records = []
    section_rows = {1}  # The first section is directly below language title row
    row = 0
    for th in rh[slice_i:slice_j]:
        m = re.match(pattern, th.attrs.get('id'))
        sheet_row_id = m.group(1)
        sheet_row = th.parent
        first_td = sheet_row.td

        # first cell in row contains text
        if first_td.string:
            logger.debug('Row %s, Sheet Row: %s. %s', row, sheet_row_id, first_td.get_text())
            cells = [first_td.get_text()]

            for td in first_td.find_next_siblings('td'):
                cells.append(td.get_text())

            records.append(cells)
            row += 1
        # empty row. next row is a section
        else:
            section_rows.add(row)
            logger.debug('next section: row %s', row)

    languages = [dict(column=i, language=l) for i, l in enumerate(records[0]) if l]
    sections = [dict(row=r, cells=records[r]) for r in sorted(list(section_rows)) if
                r < len(records)]
    result = dict(records=records, languages=languages, sections=sections)

    return result


class SheetScraper:
    def __init__(self, uri, output_fmt='mediawiki', from_row=None, to_row=None):
        self.sheet_uri = uri
        self.output_fmt = output_fmt
        self.from_row = from_row
        self.to_row = to_row
        self.selected_cols = [0]
        self.languages = []
        self.sections = []
        self.records = []

    def fetch(self):
        response = fetch_sheet(self.sheet_uri)
        rowrange = human_range_to_slice(self.from_row, self.to_row)
        result = scrape_google_sheet(response.text, **rowrange)
        self.records = result.get('records')
        self.languages = result.get('languages')
        self.sections = result.get('sections')

    def all_languages(self):
        return [(l.get('language'), l.get('column')) for l in self.languages]

    def select_columns(self, *col_nums):
        self.selected_cols = list(col_nums)

    def selected_languages(self):
        return [l.get('language') for l in self.languages if l.get('column') in self.selected_cols]

    def list_of_lists(self, rows):
        data = [[self.records[row][col] for col in self.selected_cols]
                for row in [0] + rows]
        return data

    def output_sections(self, fmt=None):
        tablefmt = fmt or self.output_fmt
        section_rows = [s.get('row') for s in self.sections] + [len(self.records)]
        outputs = []
        for x, y in pairwise(section_rows):
            rows = [i for i in range(x, y)]
            data = self.list_of_lists(rows)
            t = tabulate(data, headers='firstrow', tablefmt=tablefmt)
            outputs.append(t)
        return outputs
