

# About The Project
It is an eCommerce application built with Python Django Framework. Some of the features of this project includes custom user model, categories and products, Carts, Incrementing, Decrementing and removing car items, Unlimited Product image gallery, Orders, Payments, after-order functionalities such as reduce the quantify of sold products, send the order received email, clearing the cart, Order completion page as well as generating an invoice for the order. Also we have a Review and Rating system with the interactive rating stars that even allows you to rate a half-star rating. My account functionalities for the customer who can easily edit his profile, profile pictures, change his account password, and also manage his orders and much more.

![image](https://github.com/shaweta/Ecommerce/assets/17871651/6501e57b-d3a9-4f55-9208-547a1641a382)
![image](https://github.com/shaweta/Ecommerce/assets/17871651/46475864-536d-4312-8da0-4eaf6766296f)
![image](https://github.com/shaweta/Ecommerce/assets/17871651/688f15ec-62b5-4cfe-ba53-865c0db84ce8)"


# Setup Instructions

1. Clone the repository `git clone https://github.com/shaweta/Ecommerce.git`
2. Navigate to working directory `Ekart . `
3. Open the project from the code editor `vs code .` 
4. Create virtual environment `python -m venv env`
5. Activate the virtual environment `source env/Scripts/activate`
6. Install required packages to run the project `pip install -r requirements.txt`
7. create a .env file and it should have these parameters
   ```sh
    SECRET_KEY=
    DEBUG=
    EMAIL_HOST=
    EMAIL_PORT=
    EMAIL_HOST_USER=
    EMAIL_HOST_PASSWORD=
    EMAIL_USE_TLS=
    ```
8. Fill up the environment variables:
    _Generate your own Secret key using this tool [https://djecrety.ir/](https://djecrety.ir/), copy and paste the secret key in the SECRET_KEY field._

    _Your configuration should look something like this:_
    ```sh
    SECRET_KEY=47d)n05#ei0rg4#)*@fuhc%$5+0n(t%jgxg$)!1pkegsi*l4c%
    DEBUG=True
    EMAIL_HOST=smtp.gmail.com
    EMAIL_PORT=587
    EMAIL_HOST_USER=youremailaddress@gmail.com
    EMAIL_HOST_PASSWORD=yourStrongPassword
    EMAIL_USE_TLS=True
    ```
    _Note: If you are using gmail account, make sure to [use app password](https://support.google.com/accounts/answer/185833)_
10. Create database tables
    ```sh
    python manage.py migrate
    ```
11. Create a super user
    ```sh
    python manage.py createsuperuser
    ```
12. Run server
    ```sh
    python manage.py runserver
    ```
13. Login to admin panel - (`http://127.0.0.1:8000/securelogin/`)
14. Add categories, products, add variations, register user, login, place orders and EXPLORE SO MANY FEATURES

` Thank You `


