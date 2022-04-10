# Software Challenge

Thank you for giving me the opportunity to take this challenge as part of my application process. This is my submission to design a wool comparison portal.

Duration: It took me about 2 hours to write the initial code in the initialCode.py file.

It later took me about two days to rethink through the challenge and refactor the code to reduce compilation time, make it more readable and easier to implement with other websites. I had to learn some dynamics in other websites relating to how their URL&#39;s were generation for brands and products.

## Solution

The portal takes the URL of brand names, corresponding product names and searches for available matches from the website. It saves data in both CSV files and the sqlite database.

In the Utils directory, we have the ProductPageReader.py which reads website page information which is then used to scrap the needed data in the WebScrapper.py file.

The core code sits in the Factory directory. This Factory directory can be modified with the relevant billets, website URL and tags to be used for the scrapping. Once new factories/ websites are added, they can be created in the Factory directory.

The test cases used for this project are:

1. [https://www.woolplatz.de](https://www.woolplatz.de/)
2. [https://www.yarnplaza.com](https://www.yarnplaza.com/)
3. [https://www.woolwarehouse.co.uk/](https://www.woolwarehouse.co.uk/)
4. [https://www.lastijerasmagicas.com/en/](https://www.lastijerasmagicas.com/en/)

## Assumptions Made:

1. I could not find the Special double knit product so I assumed it was the same as the Special DK.
2. It was difficult to find delivery times on most of the websites so that information was ignored in my portal.

How to run the code:

Run the marktPilot.py file and navigate to the localhost URL in your browser. Eg. localhost:5000

This loads a comparison portal with some of the data which has been scrapped and saved in the database. NB: you can delete the markt\_pilot.sqlite.db file if you want to start a fresh database.

### Features of the Comparison Portal

Click on the **Scrapper** button to initiate the web scrapper for new results.

You can be refreshing the main page as the scrapper scraps data to see newly added data

The **Apply** button is used to apply filter changes to the website.

Hovering on the &quot;needleSize&quot; and &quot;composition&quot; buttons show their values

## Final Comments

The challenge looked very simple at first glance but was a bit tough through the thought process. I enjoyed working on it as it helped revised some of my python lessons again and learn new stuff.

Some new concepts I had never used in Python but I learnt to help me take on this task and worth sharing [https://geekyhumans.com/de/create-asynchronous-api-in-python-and-flask/](https://geekyhumans.com/de/create-asynchronous-api-in-python-and-flask/)

[https://flask.palletsprojects.com/en/2.0.x/async-await/](https://flask.palletsprojects.com/en/2.0.x/async-await/)


## Acknowledgement

HTML Template was referenced from this website: [https://bbbootstrap.com/snippets/bootstrap-4-ecommerce-products-list-range-filters-89673127](https://bbbootstrap.com/snippets/bootstrap-4-ecommerce-products-list-range-filters-89673127)
