# Cryptocurrency Exchange API Intergation and Trading Platform
This is a cryptocurrency trading web application that interfaces with a cryptocurrency exchange API. It gives customers real-time market data, allows them to place buy/sell orders, and keeps track of their portfolio. The platform is designed with the Python Django framework and interfaces with two APIs: the Coinpaprika API from RapidAPI and the Binance API from Binance.

## Features

- Real-time market data: The platform fetches real-time market data from Coinpaprika API, providing users with up-to-date information on cryptocurrency prices, market trends, and other relevant data.

- User authentication: Users can create accounts, log in, and log out. The platform implements secure user authentication mechanisms to protect user accounts and sensitive information.

- Buy/Sell orders: Users can place buy and sell orders for cryptocurrencies through the Binance API. The platform handles the order processing and communicates with the exchange to execute the orders.

- Portfolio tracking: Users can view and track their cryptocurrency portfolio, including the current value of their holdings, profit/loss calculations, and historical performance.

- Responsive frontend interface: The platform features a responsive and user-friendly frontend interface. Users can view market data, place orders, and monitor their portfolio performance. Real-time updates are implemented for price changes and order status.

- Security measures: The platform implements security measures such as two-factor authentication (2FA) to enhance user account security. Sensitive user information is protected through appropriate encryption and secure data handling practices. API rate limits are also taken into consideration to avoid exceeding usage limits.

## Setup and Installation

1. Clone the repository: `git clone https://github.com/your-username/cryptotrading-platform.git`
2. Navigate to the project directory: `cd cryptotrading-platform`
3. Create and activate a virtual environment (recommended): 
   - `python -m venv venv` (create a virtual environment)
   - `source venv/bin/activate` (activate the virtual environment)
4. Install all the dependencies: `pip install -r requirements.txt`
5. Set up API keys:
   - Coinpaprika API: Obtain an API key from RapidAPI and configure it in the settings.
   - Binance API: Obtain an API key and secret from Binance and configure them in the settings.
6. Set up Gmail for SMTP.
7. collect static files: `python manage.py collectstatic`
8. Run database migrations: `python manage.py migrate`
9. Start the development server: `python manage.py runserver`
10. Access the platform in a web browser: `http://localhost:8000`

## Usage

- Create a new account or log in to an existing account.
- Navigate through the platform to view market data, place buy/sell orders, and track your portfolio.
- Use the provided interfaces to interact with the platform's features, such as searching for cryptocurrencies, placing orders, and viewing portfolio performance.
- the two-factor authentication (2FA) is auto enabled to enhanced account security.
- Ensure to stay within API rate limits to avoid interruptions in data retrieval and order processing.

## Contribution

Contributions to the project are most welcome. If you encounter any issues or have suggestions for improvements, please submit a GitHub issue or pull request.

## License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).
