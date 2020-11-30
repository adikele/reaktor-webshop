# reaktor-webshop
A web app programmed for Reaktor’s selection test for developer positions. App provides a simple listing page for three product categories: jackets, shirts, and accessories. 

App is written in Python 3.7 and Flask. App uses two different legacy APIs to fetch information about the products.

Stage 1 coding (completed on 29.11.2020):
Currently, page loading is slow due to the numerous calls to the availability API (six calls in all, corresponding to each of the manufacturer). 

Stage 2 coding (starting from 30.11.2020):
1. Goal will be to speed up page loading by using asynchronous procedures while calling the availability API.
2. Better exception handling in the code.
3. Fix known bugs and document new ones.

Known bugs:
During some runs, the application’s product page fails to load with a 500 response error message. The cause of this failure is not yet clear (there is some provision in code already to handle API retries).
