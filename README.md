# Ecommerce Project

A Django-based ecommerce demo application built for product browsing, cart
management, checkout, shipping addresses, order history, and user
authentication.

This repository is structured for a portfolio/GitHub presentation. The Django
project configuration is at the repository root, the ecommerce business logic is
inside the `store` app, and demo product data is provided through a fixture
instead of committing the local SQLite database.

## Features

- Product listing on the home page by category.
- Category pages for mobiles, laptops, top wear, and bottom wear.
- Product detail page with add-to-cart and buy-now actions.
- User registration, login, logout, password reset, and password change.
- Customer profile and shipping address creation.
- Authenticated cart page with AJAX quantity increase, decrease, and remove.
- Checkout page with address selection.
- Order placement from cart items.
- Order history page with order status progress display.
- Django admin configuration for managing customers, products, carts, and orders.
- Product fixture for loading demo catalog data.
- Focused tests for cart, checkout, profile ownership, and order behavior.

## Tech Stack

- Python 3.12
- Django 6.0.7
- SQLite for local development
- Bootstrap 5
- jQuery
- Owl Carousel
- Font Awesome
- Pillow for image handling

## Project Structure

```text
Ecommerce_Project/
  config/
    settings.py       Project settings
    urls.py           Root URL routing
    asgi.py           ASGI entrypoint
    wsgi.py           WSGI entrypoint

  store/
    admin.py          Django admin setup
    apps.py           Store app configuration
    context_processors.py
    forms.py          Registration and profile forms
    models.py         Customer, Product, Cart, OrderPlaced models
    urls.py           Store URL routes
    views.py          Store views and ecommerce workflows
    tests.py          Automated tests

    fixtures/
      products.json   Demo product catalog data

    migrations/
      0001_initial.py
      0002_alter_customer_address_alter_customer_phone.py
      0003_alter_product_discounted_price_and_more.py

    static/store/
      css/
      js/
      images/

    templates/store/
      base.html
      home.html
      product_detail.html
      cart.html
      checkout.html
      profile.html
      orders.html
      ...

  media/
    productimg/       Demo product images used by fixture data

  manage.py
  requirements.txt
  README.md
```

## Main Application Flow

1. A visitor opens the home page and browses products by category.
2. A visitor can open any product detail page.
3. To add a product to cart or buy now, the user must be logged in.
4. The cart page lets the user increase, decrease, or remove products.
5. The checkout page shows cart items and the logged-in user's saved addresses.
6. The user selects an address and places the order.
7. Cart items are converted into order records and the cart is cleared.
8. The user can view placed orders from the orders page.

## Data Models

- `Customer`: stores user shipping/profile information.
- `Product`: stores catalog data, pricing, category, brand, and product image.
- `Cart`: stores a user's cart item and quantity.
- `OrderPlaced`: stores completed order items and delivery status.

Important model behavior:

- Product prices use `DecimalField` for accurate money values.
- A user can only have one cart row per product.
- Cart item cost is calculated from quantity and discounted product price.
- Order item cost is calculated from quantity and discounted product price.

## Security And Behavior Notes

- Cart, profile, address, checkout, payment, and orders require login.
- Checkout order submission uses `POST` and CSRF protection.
- Users can only place orders using their own saved addresses.
- Profile submission always assigns the logged-in user server-side.
- Cart totals are calculated only from the logged-in user's cart.
- The local `db.sqlite3` database is ignored and should not be committed.
- Environment variables can override sensitive deployment settings.

## Setup

Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Apply database migrations:

```bash
python manage.py migrate
```

Load demo product data:

```bash
python manage.py loaddata products
```

Run the development server:

```bash
python manage.py runserver
```

Open the app:

```text
http://127.0.0.1:8000/
```

## Admin User

Create a superuser to access Django admin:

```bash
python manage.py createsuperuser
```

Open the admin panel:

```text
http://127.0.0.1:8000/admin/
```

From the admin panel you can manage:

- Products
- Customers
- Cart records
- Orders
- Order statuses

## Useful URLs

```text
/                         Home page
/mobile/                  Mobile products
/laptop/                  Laptop products
/topwear/                 Top wear products
/bottomwear/              Bottom wear products
/product-detail/<id>      Product detail
/showcart/                Shopping cart
/checkout/                Checkout
/profile/                 Customer profile/address form
/address/                 Saved addresses
/orders/                  Order history
/accounts/login/          Login
/signup/                  Registration
/admin/                   Django admin
```

## Tests

Run Django system checks:

```bash
python manage.py check
```

Run the test suite:

```bash
python manage.py test store
```

Current test coverage focuses on:

- Login protection for cart pages.
- Cart duplicate prevention and quantity incrementing.
- Cart quantity lower bound.
- Buy-now redirect behavior.
- Checkout rendering for the logged-in user's address.
- Profile ownership assignment.
- Preventing checkout with another user's address.
- Order creation and cart cleanup.

## Environment Variables

The app works locally without environment variables, but these can be set for
deployment or staging:

```bash
DJANGO_SECRET_KEY=change-me
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=example.com,www.example.com
```

Meaning:

- `DJANGO_SECRET_KEY`: overrides the development secret key.
- `DJANGO_DEBUG`: set to `False` outside local development.
- `DJANGO_ALLOWED_HOSTS`: comma-separated list of allowed hostnames.

## GitHub And Portfolio Notes

This repository intentionally excludes generated and local-only files:

- `.venv/`
- `__pycache__/`
- `*.pyc`
- `.idea/`
- `.env`
- `db.sqlite3`

The product catalog is stored in `store/fixtures/products.json`, so a fresh clone
can recreate the demo catalog with:

```bash
python manage.py loaddata products
```

The demo images are stored in `media/productimg/` because the fixture references
those image paths.

## Development Notes

- Keep reusable app code inside `store/`.
- Keep project-level configuration inside `config/`.
- Add new templates under `store/templates/store/`.
- Add new static files under `store/static/store/`.
- Add model changes through Django migrations.
- Add tests when changing cart, checkout, profile, or order behavior.