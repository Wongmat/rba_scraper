from datetime import datetime
import re
import requests
from bs4 import BeautifulSoup


def process_report(content):
    first_clean = re.sub(r"\n(\t)+", " ", content.get_text(strip=True))
    return re.sub(r"\r", " ", first_clean)


def fetch_reports(year):
    reports = {}

    res = requests.get(
        'https://www.rba.gov.au/monetary-policy/int-rate-decisions/'
        + str(year) + '/')

    if res:
        soup = BeautifulSoup(res.content, 'html.parser')
        content = soup.find('ul', {'class': 'list-articles'})

        if not content:
            raise Exception('No reports found for ' + str(year))
        else:
            li = content.findChildren('a', recursive=True)
            paths = list(map(lambda elem: elem.get('href'), li))
            for path in paths:
                res = requests.get('https://www.rba.gov.au' + path)
                if res:
                    soup = BeautifulSoup(res.content, 'html.parser')
                    time = soup.find(
                        'time',
                        {'itemprop': 'datePublished'}).get('datetime')

                    p_tags = soup.find(
                        'div',
                        {'itemprop': 'text'}
                    ).findChildren('p', recursive=False)

                    content = list(
                        map(process_report, p_tags))

                    reports.update(
                        {datetime.strptime(
                            time, '%Y-%m-%d'): ''.join(content)})
                else:
                    raise Exception("Couldn't access file")
        return reports
    else:
        raise Exception("Couldn't access RBA website")
