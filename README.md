# Web Scraping with Python: Jumia Nigeria

The project is carried out to fulfill the following requirements:

* Create a PostgreSQL database on Heroku.
* Create a python script to scrape data from an online mall (www.jumia.com.ng).
* Insert the data into the created database.
* Perform join using sql query and export to a `csv`

Data scraped are:

* `post_title` : The title of the product
* `post_url` : The url of the product
* `post_price` : The actual price of the product less the discount
* `post_thumb_url`: The url of the image

### Code Snippets:

#### To scrape data for disposable diapers:

The function `getLastPageNumber` gets the last page on the category. The function `getData` uses the page number and the url to scrape the number of data required.

```
url = "https://www.jumia.com.ng/baby-disposable-diapers/"

last_page = getLastPageNumber(url)

data = getData(last_page, url)
```

#### To commit data to the PostgreSQL database:

The function `load_csv_to_db` takes in th csv directory and the table name.

```
load_csv_to_db("/data/data_bikes.csv", "bikes")
```
 



