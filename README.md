# FULL-STACK-PYTHON-WEB-APPLICATION
```text
PROJECT_DOCUMENTATION_A_Aa_Restaurant
====================================

Online Food Ordering System – Django 5


TABLE OF CONTENTS
-----------------
1. Project Overview
2. Tech Stack
3. Folder Structure
4. Pages & Navigation Flow
   4.1 Home Page
   4.2 Menu Page (/menu/)
   4.3 Cart Page (/cart/)
   4.4 Checkout Page (/checkout/)
   4.5 Online Payment Flow (OTP)
   4.6 Cash on Delivery (COD) Flow
5. Order System (Session Based)
6. Admin & Customer Login Flow
7. Admin Dashboard (/admin-dashboard/)
8. Models Used
9. Templates & Layout Rules
10. Context Processor (Cart Badge)
11. Database & Environment Setup
12. How to Run the Project
13. Project Features Summary
14. Conclusion


1. PROJECT OVERVIEW
-------------------
Project Name: A Aa Restaurant  
Project Type: Online Food Ordering System

Purpose:
- Users can browse the restaurant menu, view food items with images, add items to a cart, and place orders.
- The system supports both Cash on Delivery (COD) and Online Payment with OTP verification.
- Orders are tracked using Django sessions, and users can view an order list and order details.
- Admin users have a separate login. They can view all orders and update order statuses (Pending → Preparing → Delivered).

Target:
- Simple, clean, and easy-to-understand system for learning and small-scale deployments.
- Clear separation between customer-facing features and admin features.


2. TECH STACK
-------------
Backend:
- Python
- Django 5

Frontend:
- HTML
- CSS
- Bootstrap (for layout, responsive cards, buttons, and styling)
- Basic JavaScript for:
  - Handling “Add to Cart” button clicks
  - Updating the cart badge count
  - Filtering menu items by search and category
  - OTP verification and redirect logic

Database:
- Default: SQLite
  - File: `db.sqlite3` in the project root.
- Optional: MySQL
  - Controlled by an environment variable `USE_SQLITE`.
  - When `USE_SQLITE="1"` (default), the project uses SQLite.
  - When `USE_SQLITE="0"`, the project uses MySQL settings defined through environment variables.

Django Templates:
- All pages use Django’s template engine.
- `base.html` acts as the main layout with navbar and footer.
- Other templates extend `base.html` and fill the `{% block content %}` section.

Django Sessions:
- Used heavily for:
  - Shopping cart storage
  - Orders storage
  - Pending payment information (for OTP-based online payment)
- Data is kept on the server side, identified by session cookies.

Django Authentication:
- Built-in Django auth system is used for login/logout.
- Customers use the normal `/login/` page.
- Admin users use a separate `/admin-login/` page.
- Role-based access uses the `is_staff` flag on the User model to restrict admin features.

Static Files:
- Served from `/static/`
- Stored in `static/` folder inside the project.
- Includes CSS, JavaScript, and static images (for example, placeholder food images).

Media Uploads:
- Served from `/media/`
- Stored in `media/` folder.
- Food images are uploaded and stored under `media/menu_images/`
  (e.g., `media/menu_images/paneer_tikka.jpg`).


3. FOLDER STRUCTURE
-------------------
Important directories and files:

- `aa_restaurant/`
  - Django project folder containing:
    - `settings.py` – main project configuration (database, apps, templates, static/media, etc.)
    - `urls.py` – root URL routing; includes the `restaurant` app URLs and media handling.
    - `wsgi.py`, `asgi.py` – deployment entry points.

- `restaurant/`
  - Main application folder.
  - Contains:
    - `models.py` – Django models for Menu and related entities.
    - `views.py` – view functions (home, menu, cart, checkout, orders, admin dashboard, etc.).
    - `urls.py` – app-specific URL patterns.
    - `admin.py` – Django admin registration.
    - `context_processors.py` – custom context processor for cart badge.
    - `migrations/` – database migrations.

- `templates/restaurant/`
  - All HTML templates for views:
    - `base.html`
    - `home.html`
    - `menu.html`
    - `cart.html`
    - `checkout.html`
    - `otp_verification.html`
    - `payment_confirmation.html` (if present)
    - `payment_failed.html`
    - `orders.html`
    - `order_detail.html`
    - `order_not_found.html`
    - `customer_login.html`
    - `admin_login.html`
    - `admin_dashboard.html`
    - And any other supporting templates.

- `static/`
  - Static files served at `/static/`:
    - `static/css/` – stylesheets (e.g., `styles.css`).
    - `static/js/` – JavaScript (e.g., `main.js`).
    - `static/images/` – static images (e.g., a `food_placeholder.jpg` used when no product image is available).

- `media/`
  - Uploaded and local media files served at `/media/`:
    - `media/menu_images/` – local food images (e.g., `paneer_tikka.jpg`, `chicken_biryani.jpg`, etc.).
    - `.gitkeep` to keep folders in version control.

- `db.sqlite3`
  - Default SQLite database file.

- `manage.py`
  - Django’s main command-line utility file.

Example simplified tree:

- `aa_restaurant/`
  - `aa_restaurant/`
    - `settings.py`
    - `urls.py`
  - `restaurant/`
    - `models.py`
    - `views.py`
    - `urls.py`
    - `context_processors.py`
    - `migrations/`
  - `templates/`
    - `restaurant/`
      - `base.html`
      - `menu.html`
      - `cart.html`
      - `checkout.html`
      - `orders.html`
      - `order_detail.html`
      - `customer_login.html`
      - `admin_login.html`
      - `admin_dashboard.html`
  - `static/`
    - `css/`
    - `js/`
    - `images/`
  - `media/`
    - `menu_images/`
  - `db.sqlite3`
  - `manage.py`


4. PAGES & NAVIGATION FLOW
--------------------------

4.1 Home Page
-------------
URL: `/` (root)

What user sees:
- A welcoming landing page for A Aa Restaurant.
- Navigation bar, branding, and main call-to-action links.

Typical buttons / navigation:
- “Menu” or similar link that takes the user to `/menu/`.
- Links to “Cart”, “Orders”, “Login”, etc., depending on how the navbar is configured.
- Navbar includes a cart icon with a badge showing the number of items in the cart.

Flow:
- User opens home page.
- Clicks “Menu” or corresponding button to go to the Menu page (`/menu/`).

4.2 Menu Page (/menu/)
----------------------
URL: `/menu/`

Purpose:
- Show all available food items using Bootstrap cards.
- Users can browse items, filter them, and add them to the cart.

What is displayed:
- List of food items in a responsive grid layout.
- Each item is shown in a Bootstrap card.

Each card typically shows:
- Image:
  - Loaded from the local media folder: `{{ item.image.url }}` if an image is available.
  - If no image is attached, a placeholder is used, such as `/static/images/food_placeholder.jpg`.
- Name of the dish (e.g., “Paneer Tikka”).
- Price (e.g., `₹200`).
- Category badge (Starters, Main Course, Beverages, Desserts).
- Description text.
- Optional popularity badge (e.g., “Popular”).
- “Add to Cart” button.

Search and category filters:
- Search box to filter by item name or description.
- Category tabs (All, Starters, Main Course, Beverages, Desserts).
- JavaScript applies filters on the already-rendered cards (no page reload needed).

When user clicks “Add to Cart”:
- A JavaScript function sends a request to a cart endpoint (e.g., `/cart/increase/`) using fetch.
- The server updates the cart in the Django session.
- The navbar cart badge is updated (AJAX or helper function).
- A toast notification (“Added to cart ✅”) appears as visual feedback.

Cart storage:
- Cart is stored entirely inside the Django session, not in localStorage.
- Structure example (session):

  ```python
  request.session["cart"] = {
      "1": {"name": "Paneer Tikka", "price": 200, "quantity": 2, "image_url": "..."},
      "2": {"name": "Biryani", "price": 250, "quantity": 1, "image_url": "..."},
  }
  ```

4.3 Cart Page (/cart/)
----------------------
URL: `/cart/`

Purpose:
- Show current items in the session cart.
- Allow user to adjust quantities or remove items.
- Display subtotal, delivery fee, and total.

What is displayed:
- Table or list of cart items:
  - Item name
  - Image (if needed)
  - Unit price
  - Quantity
  - Line total (price × quantity)
- Quantity controls for each item:
  - “−” button (decrease quantity)
  - Quantity number
  - “+” button (increase quantity)
- Remove button to delete an item from the cart completely.
- Summary section:
  - Subtotal
  - Delivery fee (for example, ₹30 when there is at least one item)
  - Final total to pay
- “Checkout” button that takes the user to `/checkout/`.

Behavior:
- When user increases quantity:
  - Quantity is updated in the session cart.
  - Totals are recalculated.
- When user decreases quantity:
  - If quantity > 1: decreases by 1.
  - If quantity becomes 0: item is removed from the cart.
- When user removes an item:
  - Item entry is removed from the session cart.
- After any update, cart badge and totals reflect the current state.

4.4 Checkout Page (/checkout/)
------------------------------
URL: `/checkout/`

Purpose:
- Collect user details and payment method.
- Decide whether to go through COD flow or Online Payment (OTP) flow.

What is displayed:
- List of items in the cart (similar to cart page but read-only).
- Summary:
  - Subtotal
  - Delivery fee
  - Total amount
- Billing form fields:
  - Name
  - Email
  - Phone
  - Address
  - Instructions (optional)
- Payment method choice:
  - Cash on Delivery (COD)
  - Online Payment (e.g., PhonePe/GPay/Paytm-like behavior with OTP)

Behavior when form submitted:
- If cart is empty:
  - Redirect back to `/cart/`.
- If payment method is COD:
  - A session-based order is created immediately.
  - Cart is cleared.
  - User is redirected to the order detail page `/orders/<order_id>/`.
- If payment method is Online Payment:
  - Customer and payment info are stored in session as “pending order”.
  - User is redirected to the Online Payment flow (see below).


4.5 Online Payment Flow (OTP)
-----------------------------
This is the flow when the user chooses Online Payment at checkout.

High-level steps:
1. User selects Online Payment on `/checkout/` and submits the form.
2. A “pending order” object is stored in the session:

   ```python
   request.session["pending_order"] = {
       "customer": {
           "name": "...",
           "email": "...",
           "phone": "...",
           "address": "...",
           "instructions": "...",
       },
       "payment_method": "Online",
   }
   ```

3. User is redirected to a payment confirmation page (e.g. `/payment/confirm/`).
4. From payment confirmation, when user clicks “Pay Now”, they are sent to the OTP Verification page: `/otp/verify/`.
5. On `/otp/verify/`, the user enters the OTP code.

OTP Verification Page (/otp/verify/):
- Shows:
  - OTP input field.
  - Instructions and possibly a timer.
- JavaScript checks the OTP (either via AJAX or simulated logic).
- If OTP is correct:
  - Frontend redirects the browser to `/place-order/`.
- If OTP is wrong:
  - Attempt counter increases.
  - When OTP is wrong 3 times OR timer expires:
    - User is redirected to `/payment/failed/`.

Placing the order for online payment:
- URL: `/place-order/`
- Server-side logic:
  - Reads the current cart from session.
  - Reads `pending_order` details from session.
  - Creates a new order in the session orders list.
  - Generates an order ID, like `ORD` + current timestamp in milliseconds.
  - Clears the cart.
  - Removes `pending_order` from session.
  - Redirects to `/orders/<order_id>/` to show order details.

Failure:
- URL: `/payment/failed/`
- Shows a friendly page indicating payment failure.


4.6 Cash on Delivery (COD) Flow
-------------------------------
This is simpler than the online payment flow.

Steps:
1. User selects “Cash on Delivery” on the checkout page.
2. On form submit:
   - The server reads cart and customer details.
   - Creates a new order in session immediately.
   - Order is saved with payment method = COD.
   - Cart is cleared.
3. User is redirected directly to the order detail page:
   - `/orders/<order_id>/`

No OTP is required for COD.


5. ORDER SYSTEM (SESSION BASED)
-------------------------------
Orders are stored in the user’s session rather than in the database for the main customer flow.

Order ID Format:
- Each order ID is generated as:

  `ORD` + timestamp_in_milliseconds

Example:
- `ORD1768653190077`

Session Storage:
- Orders are stored in `request.session["orders"]` as a list of dictionaries.
- Example structure:

  ```python
  request.session["orders"] = [
      {
          "order_id": "ORD1768653190077",
          "items": [
              {
                  "id": 1,
                  "name": "Paneer Tikka",
                  "category": "Starters",
                  "price": 200.0,
                  "quantity": 2,
                  "image_url": "/media/menu_images/paneer_tikka.jpg",
                  "line_total": 400.0,
              },
              {
                  "id": 3,
                  "name": "Chicken Biryani",
                  "category": "Main Course",
                  "price": 260.0,
                  "quantity": 1,
                  "image_url": "/media/menu_images/chicken_biryani.jpg",
                  "line_total": 260.0,
              },
          ],
          "subtotal": 660.0,
          "delivery_fee": 30.0,
          "total": 690.0,
          "created_at": "2026-01-17 11:30",
          "status": "Pending",  # or "Preparing", "Delivered"
          "payment_method": "COD" or other method,
          "payment_status": "COD" / "Paid" / "Pending",
          "customer": {
              "name": "John",
              "email": "john@example.com",
              "phone": "9999999999",
              "address": "Hyderabad",
              "instructions": "",
          },
      },
      ...
  ]
  ```

Order Status:
- `status` field:
  - `"Pending"` – initial state after order creation.
  - `"Preparing"` – when admin marks the order as being prepared.
  - `"Delivered"` – when admin marks the order as delivered.

URLs:
- `/orders/` – Order List
  - Reads all orders from `request.session["orders"]`.
  - Displays them in reverse chronological order (latest first).
  - For each order:
    - Order ID
    - Total amount
    - Items count
    - Created date/time (if available)
    - Payment method/status
    - Status badge
    - “View” button linking to `/orders/<order_id>/`.

- `/orders/<order_id>/` – Order Detail
  - Searches the session orders list for a matching `order_id`.
  - If found:
    - Shows order header:
      - Order ID
      - Customer info (if stored)
      - Payment method & payment status
      - Status badge
    - Shows items table:
      - Item name
      - Quantity
      - Price
      - Line total
    - Shows subtotal, delivery fee, and total.
  - If not found:
    - Renders a friendly page `order_not_found.html` with a clear message instead of a default 404.


6. ADMIN & CUSTOMER LOGIN FLOW
------------------------------

Customer Login
--------------
URL: `/login/`

Behavior:
- Normal users can log in using their credentials.
- On successful login:
  - User is redirected to the menu page (`/menu/`).
- Purpose:
  - Allow customers to authenticate if needed (for a more personalized experience).

Admin Login
-----------
URL: `/admin-login/`

Behavior:
- Only staff users (with `is_staff=True`) are allowed to log in via this page.
- After the admin user logs in:
  - If `is_staff` is True, they are redirected to `/admin-dashboard/`.
  - If a normal (non-staff) user tries to login via `/admin-login/`:
    - Login will be rejected or shown with an error message indicating they are not allowed to access the admin dashboard.

Role-based access:
- Uses Django’s built-in `User` model with the `is_staff` flag.
- Admin-only views (like admin dashboard and status update endpoints) are decorated with:
  - `@login_required`
  - `@user_passes_test` with a check function to ensure `user.is_staff` or `user.is_superuser` is True.


7. ADMIN DASHBOARD (/admin-dashboard/)
--------------------------------------
URL: `/admin-dashboard/`

Access:
- Restricted to staff/admin users (`is_staff=True` or `is_superuser=True`).
- Protected via Django decorators.

What it shows:
- High-level statistics:
  - Total orders (count from session orders).
  - Pending / placed orders.
  - Total revenue (sum of `total` from each order).
  - Total menu items (count from database).
- Orders table (from session):
  - Order ID
  - Items count
  - Total amount
  - Status badge (Pending / Preparing / Delivered)
  - Payment status badge (e.g., COD / Paid)
  - Created date/time (if stored)
  - Buttons for status changes and view.

Admin actions:
- “Mark Preparing”:
  - Changes status from “Pending” to “Preparing” for the selected order.
  - Implemented by updating the order entry inside `request.session["orders"]`.
- “Mark Delivered”:
  - Changes status from “Preparing” to “Delivered”.
- “View”:
  - Opens `/orders/<order_id>/` to see full order details.

Effect:
- Status changes immediately affect what both the admin and the customer see on order detail and list pages.


8. MODELS USED
--------------
Main model: MenuItem

MenuItem (stored in database):
- Fields (simplified description):
  - `name` (CharField)
    - Name of the dish (e.g., “Paneer Tikka”).
  - `category` (CharField with choices)
    - Values like:
      - “Starters”
      - “Main Course”
      - “Beverages”
      - “Desserts”
  - `price` (DecimalField)
    - Price of the item, with decimal precision.
  - `description` (TextField)
    - Short description of the dish.
  - `rating` (DecimalField)
    - Average displayed rating (e.g., 4.5).
  - `is_popular` (BooleanField)
    - Whether the item is marked as popular.
  - `image_url` (URLField, optional)
    - Older field to store online image URLs (may still exist for compatibility).
  - `image` (ImageField, optional)
    - Actual uploaded image, stored under `media/menu_images/`.
    - Automatically linked based on item name and local image files.
  - `is_available` (BooleanField)
    - Whether the menu item is currently available for ordering.
  - `created_at` (DateTimeField)
    - Timestamp when the menu item was created.

Note on Orders:
- The core customer-facing order system described in this documentation is session-based.
- Orders are not stored in the database for the normal user flow; they are stored inside `request.session["orders"]`.
- The project also includes database models for orders and order items (for more advanced use cases), but the primary documented flow uses session-stored orders as described earlier.


9. TEMPLATES EXPLANATION
------------------------
Template rules:
- `base.html`:
  - Contains the main HTML layout, including:
    - Header / navbar
    - Footer
    - CSS and JS includes
    - Cart badge in the navbar
  - Defines a `{% block content %}` section for child templates.

- All page templates:
  - Must start with `{% extends "restaurant/base.html" %}` as the first line.
  - Should contain exactly one `{% block content %} ... {% endblock %}` block.
  - Should not duplicate navbar or footer; these come from `base.html`.

List of important templates:
- `base.html`
  - Global layout, navbar, footer, cart badge.
- `home.html`
  - Landing page for the application.
- `menu.html`
  - Display menu items as Bootstrap cards with images and “Add to Cart” buttons.
  - Uses local media images or placeholder images.
- `cart.html`
  - Shows cart items, quantity controls, and totals.
- `checkout.html`
  - Shows address form, order summary, and payment method selection.
- `payment_confirmation.html` (if present)
  - Used for online payment before OTP verification.
- `otp_verification.html`
  - Page for OTP input and validation logic (via JavaScript).
- `payment_failed.html`
  - Displayed when OTP fails 3 times or the timer ends.
- `orders.html`
  - List of all session orders with basic details.
- `order_detail.html`
  - Detailed view for a single order (items, totals, status).
- `order_not_found.html`
  - Shown when `/orders/<order_id>/` is requested with an unknown order ID.
- `customer_login.html`
  - Login form for normal customers.
- `admin_login.html`
  - Login form for admin/staff users only.
- `admin_dashboard.html`
  - Admin-only dashboard showing orders, statistics, and status update actions.


10. CONTEXT PROCESSOR
---------------------
File: `restaurant/context_processors.py`

Purpose:
- Provide global variables to all templates without manually adding them in every view.
- Specifically used for the cart item count badge in the navbar.

Logic:
- Reads the cart from the session:

  ```python
  cart = request.session.get("cart", {})
  ```

- Sums the quantities of all items to get `cart_count`:

  ```python
  cart_count = sum(item["quantity"] for item in cart.values())
  ```

- Returns this in a dictionary:

  ```python
  return {"cart_count": cart_count}
  ```

Usage:
- Registered in `settings.py` under `TEMPLATES["OPTIONS"]["context_processors"]`.
- In `base.html`, you can refer to `{{ cart_count }}` directly to display the number of items in the cart badge.
- This ensures the cart count is always up to date on every page.


11. DATABASE & ENVIRONMENT SETUP
--------------------------------
Default Database: SQLite
- Django is configured to use SQLite by default.
- Database file: `db.sqlite3` in the project root.
- No additional configuration needed for local development.

MySQL Support (Optional):
- The project supports switching to MySQL using environment variables.

Key Environment Variables:
- `USE_SQLITE`
  - `"1"` = use SQLite (default).
  - `"0"` = use MySQL.
- `DB_NAME`
  - Name of the MySQL database (e.g., `aa_restaurant`).
- `DB_USER`
  - MySQL username.
- `DB_PASSWORD`
  - MySQL password.
- `DB_HOST`
  - MySQL host (e.g., `127.0.0.1`).
- `DB_PORT`
  - MySQL port (e.g., `3306`).

Behavior:
- In `settings.py`:
  - If `USE_SQLITE == "1"`, DATABASES is configured for SQLite.
  - Otherwise, DATABASES is configured for MySQL using the values above.

Static and Media Settings:
- `STATIC_URL = "/static/"`
- `STATICFILES_DIRS = [BASE_DIR / "static"]`
- `MEDIA_URL = "/media/"`
- `MEDIA_ROOT = BASE_DIR / "media"`

Media serving in development:
- In `aa_restaurant/urls.py`, when `DEBUG` is True, it appends:

  ```python
  urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
  ```

- This tells Django to serve media files like `/media/menu_images/paneer_tikka.jpg` during development.


12. HOW TO RUN THE PROJECT
--------------------------

Step-by-step guide:

1. Open terminal in the correct folder:
   - On Windows:

     ```bash
     cd "C:\Users\hvard\Desktop\FULL\A AA\aa_restaurant"
     ```

2. Create and activate a virtual environment (optional but recommended).

3. Install dependencies:
   - Make sure `pip` is available.
   - Run:

     ```bash
     pip install -r requirements.txt
     ```

4. Apply migrations:
   - Generate migrations (if not already created):

     ```bash
     python manage.py makemigrations
     ```

   - Apply migrations to the database:

     ```bash
     python manage.py migrate
     ```

5. Run the development server:

   ```bash
   python manage.py runserver
   ```

6. Open the project in a browser:
   - Visit:

     - Home: `http://127.0.0.1:8000/`
     - Menu: `http://127.0.0.1:8000/menu/`
     - Cart: `http://127.0.0.1:8000/cart/`
     - Checkout: `http://127.0.0.1:8000/checkout/`
     - OTP Verification: `http://127.0.0.1:8000/otp/verify/`
     - Payment Failed: `http://127.0.0.1:8000/payment/failed/`
     - Orders List: `http://127.0.0.1:8000/orders/`
     - Order Detail: `http://127.0.0.1:8000/orders/ORDxxxxxxx/`
     - Customer Login: `http://127.0.0.1:8000/login/`
     - Admin Login: `http://127.0.0.1:8000/admin-login/`
     - Admin Dashboard: `http://127.0.0.1:8000/admin-dashboard/`


13. PROJECT FEATURES SUMMARY
----------------------------
Key features of “A Aa Restaurant”:

- Menu with search and category filters
  - Display all dishes using Bootstrap cards.
  - Filter by category (Starters, Main Course, Beverages, Desserts).
  - Search by name and description.

- Session-based Cart System
  - Items added from the menu are stored in the Django session.
  - Cart page shows items, quantities, and total.
  - Quantity controls (increase/decrease) and item removal.

- Checkout Flow
  - Address and contact form.
  - Payment method selection:
    - COD
    - Online payment (with OTP).

- OTP Verification for Online Payment
  - Online payment uses OTP verification at `/otp/verify/`.
  - Correct OTP leads to order placement via `/place-order/`.
  - Wrong OTP attempts (3 times) or timeout redirect to `/payment/failed/`.

- Orders List and Detail Pages
  - `/orders/` shows all session-based orders.
  - `/orders/<order_id>/` shows a detailed bill and current order status.
  - Friendly “order not found” page when the order ID is invalid.

- Separate Admin and Customer Login
  - Customer login at `/login/`, redirecting to `/menu/`.
  - Admin login at `/admin-login/`, restricted to `is_staff` users, redirecting to `/admin-dashboard/`.

- Admin Dashboard with Order Status Management
  - Admin can see all session-based orders.
  - Shows totals, pending count, and revenue.
  - Buttons to mark orders as “Preparing” or “Delivered”.
  - Links to view individual orders.

- Media Images Support for Food Items
  - Local images stored in `media/menu_images/`.
  - Automatic mapping from food names to corresponding image files.
  - Placeholder image from `/static/images/food_placeholder.jpg` when no image is available.

- Clean Template Architecture
  - All pages extend a single `base.html`.
  - Navbar and footer shared across the site.
  - Single `{% block content %}` per page to keep layout consistent.


14. CONCLUSION
--------------
The “A Aa Restaurant” project is a complete, session-based Online Food Ordering System built with Django 5. It demonstrates:

- How to build a menu-driven user interface with Bootstrap.
- How to manage carts and orders using Django sessions instead of a database.
- How to implement a two-path checkout: simple COD and an online payment flow using OTP verification.
- How to separate customer and admin roles with different login pages and access controls.
- How to design an admin dashboard for monitoring and updating order statuses.
- How to manage static and media files for serving local food images.

This documentation is intended to give you a clear, step-by-step understanding of how the system is structured, how data flows through the application, and how each page and feature works together. It can be used as a reference for learning, development, and future enhancements of the “A Aa Restaurant” project.
```