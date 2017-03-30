# Import necessary
import pandas as pd
from bs4 import BeautifulSoup
from urllib.error import URLError, HTTPError
from urllib.request import urlopen
from get_headings import get_headings

# List of DIV Classes to extract from
Classes = ["page--gallery-async"    #mom.me - gallery
          ,"publishable__content"   #mom.me - article
          ,"post-body"              #wonderwall - gallery
          ,"standard-article"       #redbookmag
          ,"title-header"           #yourtango - header
          ,"content-article"        #yourtango - article
          ,"ui-article"]            #sheknows - seems to double scan but not sure what can be done

# Load article addresses csv file with URLs to be scraped
df = pd.read_csv("data/article_addresses.csv")
URLs = list(df.values.flatten())

# Create empty list
data = []

# Loop through all the URLs in the list, scraping each one as we go
for (i,url) in enumerate(URLs):
    # Checks that the URL can be opened and connected too, also skips webpages that throws unicode error
    try:
         html = urlopen(url)
    except(URLError, HTTPError,UnicodeEncodeError):
         print("Something bad happened")
    else:
        # Using the URL we begin to parse
        soup = BeautifulSoup(html, "html.parser")
        # Loop through class list
        for css_class in Classes:
            # Loops through, selecting only the divs that have one of these classes
            for row in soup.find_all('div',attrs={"class" : css_class}):
                # Extract all h1 headings
                h1 = get_headings(heading = "h1",row = row,add_bracket_end = " <br> ")
                # Extract all h2 headings
                h2 = get_headings(heading = "h2",row = row,add_bracket_end = " <br> ")
                # Extract all h3 headings
                h3 = get_headings(heading = "h3",row = row,add_bracket_end = " <br> ")
                # Extract all h4 headings
                h4 = get_headings(heading = "h4",row = row,add_bracket_end = " <br> ")
                # Extract all p headings, limiting to the first 100 words
                p = get_headings("p",row,100,"..."," <br><br> ")
                # Create link to be put at end of post to original article
                a = " <a href = '" + url + "' > Read the rest of the article here </a>"

                # Unify all these into one html post
                WP_Post = h1 + h2 + h3 + h4 + p + a

                # Insert tuple of URL & post data into list of tuples
                data.append((url,WP_Post))
                # print progress to screen
                print("url scraped: " + url)

# Create dataframe from list of tuples and export to csv
df = pd.DataFrame(data)
df.to_csv('wp_content.csv', index=False, header=False)
