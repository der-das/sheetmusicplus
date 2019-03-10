import argparse
from bs4 import BeautifulSoup
import os
import re
import requests
import sys

#Globals/Defaults
OUTPUT = 'htmls/'

#Other misc. things
class InvalidURLError(Exception):
    ''' Exception for invalid URLs.
    Attributes:
        expression - the URL that the message failed on
    '''
    def __init__(self, expression, message):
        print('{}'.format(message))
        print('URL: {}'.format(expression))
        self.expression = expression
        self.message = message

#Helper functions
def stash(url:str, output_dir:str):
    response = requests.get(url)
    html = response.content
    soup = BeautifulSoup(html, 'html.parser')
    urlparts = url.split('//')
    urlparts = urlparts[1].split('/')
    destpath = os.path.join(output_dir, urlparts[0]) if len(urlparts) == 1 else os.path.join(output_dir, *[urlpart for urlpart in urlparts if not re.search('.*\.html', urlpart)])
    if not os.path.exists(destpath):
        os.makedirs(destpath)
    dest = os.path.join(destpath, 'content.html') if not re.search('.*\.html', urlparts[-1]) else os.path.join(destpath, urlparts[-1])
    with open(dest, 'w+') as fh:
        fh.write(soup.prettify())
    return

#Main function
def main(arguments):
    urls = arguments.urls
    output_dir = arguments.output
    for url in urls:
        try:
            stash(url, output_dir)
        except:
            raise InvalidURLError('The following input was rejected', url)
    return
    

if __name__=="__main__":
    parser = argparse.ArgumentParser(description="Downloads a local copy of the HTML, in case you're like me and hate just using the developers console.")
    parser.add_argument('urls', metavar='u', type=str, nargs='+',
            help='The target URL(s) for download.')
    parser.add_argument('-o', '--output', type=str, default=OUTPUT,
            help='The output file/directory in which to dump the file(s), Default: {}'.format(OUTPUT))
    args = parser.parse_args()
    main(args)
