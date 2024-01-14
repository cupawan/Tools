# Weather Checker with Selenium

This Python script utilizes Selenium to scrape real-time weather information from Google for a specified location. The script supports both single and multiple location queries, and the data is saved in a CSV file for future reference.

## Prerequisites

Before running the script, make sure you have the following dependencies installed:

- Python 3.x
- Selenium
- ChromeDriverManager
- pandas
- tabulate
- tqdm

You can install the required dependencies using the following command:

```bash
pip install selenium ChromeDriverManager pandas tabulate tqdm
```

## Usage

### Single Location Query

To check the weather for a single location, run the script with the following command:

```bash
python weather_updated.py <location>
```

Replace `<location>` with the desired location.

### Multiple Location Queries

To check the weather for multiple locations and save the data in a CSV file, run the script with the following command:

```bash
python weather_updated.py --multiple <location1> <location2> <location3> ...
```

Replace `<location1> <location2> <location3> ...` with the desired locations separated by spaces.

### Options

- `--multiple`: Use this option when querying multiple locations.

## Example

```bash
python weather_updated.py New York
```

This will display the weather information for New York and save it in the `scraped_data.csv` file.

```bash
python weather_updated.py --multiple London Paris Berlin
```

This will check the weather for London, Paris, and Berlin, and save the data in the `scraped_data.csv` file.

## Notes

- The script uses Chrome in headless mode for web scraping.
- Make sure to provide a valid path for saving the CSV file.

