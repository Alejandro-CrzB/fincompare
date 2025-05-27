## Fincompare
# Abstract
This project is an investment return comparator. It compares historical data of returns of public retirement options in Mexico against historical returns of various stock markets. **FinCompare** is a cloud-based microservice designed as a Minimum Viable Product (MVP) for a Cloud Computing course. It allows users to simulate and compare the returns of saving a fixed amount of money in a traditional savings account (AFORE, Mexico's retirement system) versus investing it in various stock market assets, including major indices and individual stocks (e.g., FAANG companies).

This project focuses on backend functionality, using Django to serve real-time comparisons via a simple API endpoint.

# Introduction
In Mexico, retirement fund options are very limited, confusing, or dispersed. It is difficult for the average person to be aware of all the options available in the public and private sectors. So this project arises as an option where they can see a lot of options, and compare yields of various investment options beyond the public ones, some low risk and secure but also low yields or some that are more high risk but higher yields. See what option is more suitable for you and help you make a better decision.
# Importance
This project aims to inspire users to invest and build financial independence. In Mexico, investment culture is limited, so our mission is to promote it and empower individuals with information so they can make conscious decisions.
# Features
- Calculates and compares investment growth over a user-defined period.
- Uses a fixed rate of return for AFORE (5% annually compounded).
- Uses historical financial data via the Yahoo Finance API for:
  - Major indices: S&P 500, NASDAQ, DOW JONES
  - Popular stocks: Apple, Amazon, Google, Meta, Netflix
- Returns a clean JSON response.
- Fully dockerized for easy deployment on cloud platforms (e.g., AWS EC2).
## Technologies Used

- Python 3.9
- Django 5.x
- Docker & Docker Compose
- Yahoo Finance API via `yfinance`
- Git & GitHub
- AWS EC2 (Ubuntu Server)
