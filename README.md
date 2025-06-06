### FinCompare
## Abstract
FinCompare is an investment return comparator microservice that lets users compare historical returns of Mexico’s public retirement funds (Afores) with those of various stock market assets. Designed as a Minimum Viable Product (MVP) for a Cloud Computing course, this Django-based service provides real-time comparisons through a simple API endpoint. Users can simulate the growth of a fixed principal amount invested in a traditional retirement vehicle (Afore) versus investing in major indices or individual stocks (for example, FAANG companies).

## Introduction
In Mexico, options for retirement savings can be limited, fragmented, and confusing for the average person. FinCompare was created to centralize information on Afores and overlay it with historical performance data of global markets, empowering users to make data-driven decisions about where to allocate their retirement assets. By visualizing and comparing returns side by side—ranging from low-risk, government-backed Afore accounts to higher-risk equity investments—FinCompare helps users identify which strategy best aligns with their risk tolerance and financial goals.

## Importance
Promoting an investment culture in Mexico is critical for improving financial literacy and long-term wealth building. FinCompare’s mission is to inspire users to consider alternatives beyond traditional savings accounts and make informed decisions that foster financial independence. By offering transparent, side-by-side comparisons of retirement fund options, this project aims to close the information gap and encourage users to take charge of their financial future.

## Features
Investment Growth Calculator
Computes and compares growth of a user-defined principal in:

Afore (using a fixed annual return rate).

Stock market indices and select equities via the Yahoo Finance API.

Data Sources

Afore: Assumes a net annual rate of return (default: 5% compounded annually).

Stock Markets: Retrieves historical price data for major indices and popular stocks (S&P 500, NASDAQ, Dow Jones, Apple, Amazon, Google [Alphabet], Meta [Facebook], Netflix) using the yfinance library.

Output
Returns a clean JSON response summarizing final portfolio values, cumulative returns, and percentage differences between the Afore and equity investments.

Dockerized Deployment
Packaged into Docker and orchestrated via Docker Compose for rapid, reproducible deployment on cloud platforms (for example, AWS EC2).

Backend-Only MVP
Focuses on core API functionality; exposes a simple web interface for entering parameters and triggering comparisons.

## How It Works
User Input
The user visits the service’s web interface at http://78.13.85.189/ (replace with the active Elastic IP if different).

Parameter Entry
On the homepage, the user enters:

Principal Amount (for example, 10000 MXN).

Investment Horizon in years (for example, 10).

API Request
When the user clicks “Compare Returns”, the frontend issues a GET request to the /api/comparar_inversion/ endpoint, passing amount and years as query parameters.

Afore Calculation
The backend computes the future value of the principal in an Afore using a fixed annual net rate (for example, 5% per year, compounded annually).

Plain text formula:

ini
Copiar
Editar
Value_in_Afore = principal * (1 + annual_afore_rate) ^ years
where annual_afore_rate is the net annual return rate (default: 0.05).

Equity Calculation
Using the yfinance Python package, the service fetches historical daily closing prices for one or more selected tickers (for example, ^GSPC for S&P 500) over the same horizon. It calculates the compounded return of investing the principal at the date exactly years ago compared to today.

Plain text formula:

ini
Copiar
Editar
Value_IndexOrStock = principal * (Price_today / Price_years_ago)
where Price_today is the closing price today and Price_years_ago is the closing price exactly years ago.

JSON Response
The API returns a JSON object of the form:

json
Copiar
Editar
{
  "principal": 10000,
  "years": 10,
  "afore_return": 16288.95,
  "sp500_return": 23145.62,
  "nasdaq_return": 28517.09,
  "dowjones_return": 19875.12,
  "apple_return": 42023.74,
  "comparison": {
    "diff_sp500_vs_afore": 686.02,
    "pct_sp500_vs_afore": 42.00
    // …etc.
  }
}
Frontend Display
Although this MVP focuses on returning JSON, the template comparador.html (found under app/templates/app/) can be extended to display results in charts or tables. For now, users see a minimal page with input fields; developers can modify it later to render results dynamically.

## Regulatory Context: Afore Laws
Afores (Administradoras de Fondos para el Retiro) in Mexico are regulated under the Ley de los Sistemas de Ahorro para el Retiro (LSAR). This federal law governs how retirement funds are collected, managed, and invested. For more information, see the official publication of the law on the Mexican government’s website:

Ley de los Sistemas de Ahorro para el Retiro (Current Text)

Technologies Used
Python 3.9 (backend logic and calculations)

Django 5.x (web framework and API views)

Docker & Docker Compose (containerization and deployment)

yfinance (Yahoo Finance API wrapper for retrieving historical market data)

Git & GitHub (version control and repository management)

AWS EC2 (Ubuntu Server) (target deployment environment with Elastic IP)

## Installation & Deployment
1. Clone the Repository
bash
Copiar
Editar
git clone https://github.com/Alejandro-CrzB/fincompare.git
cd fincompare
2. Configure Environment Variables
Create a .env file in the project root (next to docker-compose.yml) with contents similar to:

env
Copiar
Editar
DJANGO_SECRET_KEY=<your-secret-key>
ALLOWED_HOSTS=78.13.85.189       # Replace with your Elastic IP or domain
DEBUG=False
3. Docker Compose Setup
Ensure you have Docker Engine and Docker Compose installed. Then run:

bash
Copiar
Editar
docker-compose build
docker-compose up -d
This will:

Build the Django application into a Docker image.

Launch two containers:

web (running Django’s development server or Gunicorn if configured).

db (if you have a PostgreSQL or other database service defined; otherwise, skip or remove the DB service).

Note: For production, replace Django’s development server with Gunicorn or uWSGI and configure a reverse proxy like Nginx. This README focuses on the MVP deployment for demonstration.

4. Database Migrations (if applicable)
If you’re using Django’s ORM with a database (for example, SQLite by default), run:

bash
Copiar
Editar
docker-compose exec web python manage.py migrate
If you prefer a persistent database (PostgreSQL or MySQL), configure the DATABASES setting in settings.py or via environment variables, then apply migrations.

5. Collect Static Files
bash
Copiar
Editar
docker-compose exec web python manage.py collectstatic --noinput
This step gathers static assets (CSS, JavaScript) into the STATIC_ROOT directory for serving.

6. Access the Service
Open your browser and navigate to:

cpp
Copiar
Editar
http://78.13.85.189/ 
Replace 78.13.85.189 with your EC2 Elastic IP or custom domain. You should see the minimal landing page with fields for Amount and Years. Enter a principal amount (for example, 10000) and a horizon (for example, 10), then click “Compare Returns”.

Usage
1. Web Interface
URL: http://<Elastic_IP>/

Fields:

Amount: Initial investment amount (for example, 5000 MXN).

Years: Number of years to project returns (for example, 15).

After submitting, the page makes an AJAX call to:

php-template
Copiar
Editar
http://<Elastic_IP>/api/comparar_inversion/?amount=<amount>&years=<years>
2. API Endpoint
Endpoint: /api/comparar_inversion/

Method: GET

Query Parameters:

amount (required): A positive integer or float representing the principal in MXN.

years (required): A positive integer representing the investment horizon in years.

Example Request
http
Copiar
Editar
GET /api/comparar_inversion/?amount=10000&years=10 HTTP/1.1
Host: 78.13.85.189
Example JSON Response
json
Copiar
Editar
{
  "principal": 10000,
  "years": 10,
  "afore_return": 16288.95,
  "sp500_return": 23145.62,
  "nasdaq_return": 28517.09,
  "dowjones_return": 19875.12,
  "apple_return": 42023.74,
  "amazon_return": 38655.88,
  "google_return": 25512.30,
  "meta_return": 17455.67,
  "netflix_return": 13212.45,
  "comparison": {
    "diff_sp500_vs_afore": 686.02,
    "pct_sp500_vs_afore": 42.00,
    "diff_nasdaq_vs_afore": 12228.14,
    "pct_nasdaq_vs_afore": 75.05
    // …etc.
  }
}
3. Customizing Return Rates
Afore Rate: In app/views.py, adjust the constant:

python
Copiar
Editar
RENDIMIENTO_PROMEDIO_AFORE = 0.05  # 5% net annual by default
Yahoo Finance Tickers: In app/utils.py or the equivalent utility file, update the list of tickers:

python
Copiar
Editar
TICKERS = {
    "sp500": "^GSPC",
    "nasdaq": "^IXIC",
    "dowjones": "^DJI",
    "apple": "AAPL",
    "amazon": "AMZN",
    "google": "GOOG",
    "meta": "META",
    "netflix": "NFLX",
}
You can add or remove tickers as needed; ensure they are supported by Yahoo Finance.

Development Notes
Local Virtual Environment
If you prefer to run the project locally (outside Docker), create a Python 3.9 virtual environment:

bash
Copiar
Editar
python3.9 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
Run Migrations & Server Locally

bash
Copiar
Editar
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
Then access http://localhost:8000/ for local testing.

Static Files
When running locally, collect static files if you plan to serve them:

bash
Copiar
Editar
python manage.py collectstatic
By default, Django serves static assets only in DEBUG mode.

## Repository Structure
csharp
Copiar
Editar
fincompare/
├── app/
│   ├── migrations/
│   ├── templates/
│   │   └── app/
│   │       └── comparador.html
│   ├── static/
│   ├── utils.py
│   ├── views.py
│   ├── urls.py
│   └── ...
├── fincompare/                  # Django project folder
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── manage.py
└── README.md
How to Use the Live Microservice
Open your browser and go to:

cpp
Copiar
Editar
http://78.13.85.189/
Enter:

Amount (for example, 10000)

Years (for example, 10)

Click “Compare Returns”.

The page will display or fetch via AJAX a JSON object with the comparison results.

You can share this URL with anyone—anyone with a web browser and internet access to that Elastic IP can perform comparisons.

Thank you for exploring FinCompare. We welcome feedback and contributions via GitHub issues or pull requests.
