# Retrieve all broken links from Cohere's blog posts

## The problem

As I was reading through the [Multilingual Semantic Search with Cohere and Langchain](https://txt.cohere.com/search-cohere-langchain/) article in Cohere's blog, I stumbled into 2 broken links pointing to Langchain’s Chains ([broken link](https://api.python.langchain.com/en/latest/modules/chains.html?ref=txt.cohere.com)) and Indexes ([broken link](https://api.python.langchain.com/en/latest/modules/indexes/getting_started.html?ref=txt.cohere.com)) modules.

Since there is no way to add edit suggestions for blog posts, I shared the feedback with the article's author.

It turns out that the world of AI is moving fast, and links to API documentations or Github pages can quickly break. Also, internal links break regularly as the site gets reorganized.

It would be impossible for a documentation team to regularly check all such links. And we can't expect blog post writers to regularly check the validity of the links in their past articles.

So how can we solve that programatically?

## A proposed solution

We can simply scrape all blog posts and check whether links contained in them return a 404 or not.

Then, we can export a CSV containing the list of all broken links and their associated posts.

Using various Python libraries, this is rather trivial.

## The approach

The main blog page is the following: https://txt.cohere.com.

A challenge is that it is using infinite scrolling, so the scraper doesn't have access to the articles not initially loaded.
By checking the network devtools tab and scrolling, we see that as we scroll, we are calling subsequent pages like this: https://txt.cohere.com/page/2/ until we get to the initial blog post.

There are currently 7 pages, but we can use an infinite loop that increments the page number and breaks once we reach a 404. So this script will keep working as more pages are added.

Then, for each page we extract all the blog posts (we take all relative links starting with `/` and exclude links starting with `/tag` and `/author` since these are not blog posts).

Then, for each blog post, we call each link and if we get a 404, we append it to a list of tuples storing the calling article and the broken link.

Then we export all tuples in the `broken_links.csv` file.

## Performance considerations

Since each HTTP call takes time, we are using 20 parallel worker threads to parallelize the calls. Otherwise it would take way too long.

## How to run the script

Install the dependencies (`pip install…`) and run the main script in your terminal (for my Python version, it is: `python3.10 main.py`).
