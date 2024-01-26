# Weather and News Email Automation

This project is designed to automate the sending of weather and news updates to specified email addresses using Python. It consists of two main components: Weather and News.

## Weather Component

### Description
The Weather component fetches real-time weather information for a specified location and sends an email containing the weather details.

### Usage
1. Run the `weather_email.py` script.
2. Enter the email address to receive the weather report.

## News Component

### Description
The News component fetches the latest news from Dainik Bhaskar for a specified category and sends an email containing the headlines and news snippets.

### Usage
1. Run the `news_email.py` script.
2. Enter the email address to receive the news report.
3. Choose a news category (e.g., national, international, sports).

## EmailWithPython Class

### Description
The `EmailWithPython` class is a utility class that handles the configuration and sending of emails. It reads email configuration from the `config.yaml` file.

### Usage
1. Instantiate the class with the path to the `config.yaml` file.
2. Use the `send_email` method to send emails with customizable content.

## Configuration

### config.yaml
The `config.yaml` file contains the email configuration, including the sender's email address and Gmail password. Fill in the necessary details before running the scripts.

## Dependencies

- Selenium: Web scraping tool for fetching weather information.
- Beautiful Soup: HTML parsing library for extracting news content.
- Tabulate: Creating formatted tables from DataFrame.
- TQDM: Displaying progress bars for loops.
- Webdriver Manager: Managing browser drivers for Selenium.

## How to Run

1. Install the required dependencies using `pip install -r requirements.txt`.
2. Fill in the necessary details in the `config.yaml` file.
3. Run the `weather_email.py` or `news_email.py` script.
4. Enter the recipient's email address when prompted.

Note: Ensure that you have the required web drivers installed for Selenium. The project uses the Chrome browser for web scraping.

