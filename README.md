# Competitor Watcher

Unveil your competitors' pricing strategies with Competitor Watcher, a sophisticated Python tool crafted to dissect competitor pricing data meticulously. Powered by DuckDB for streamlined database management and Loguru for crystal-clear logging, this tool is your gateway to proactive market strategies. Stay informed with real-time email alerts for significant price reductions, keeping you steps ahead in the competitive landscape.


## Features

- **Adaptive Storage Solutions**: Whether you need the muscular prowess of PostgreSQL for large-scale data management or prefer the nimbleness of a local DuckDB setup for smaller, more personal projects, Competitor Watcher flexes to fit your storage needs.

- **Comprehensive Price Monitoring**: Dive deep into the pricing tactics of your competitors. Competitor Watcher not only tracks pricing changes but also analyzes them in one fluid operation. Opt for automated, continuous tracking with integrations like Cron or Airflow, ensuring you never miss a beat.

- **Real-Time Alerts**: Be the first to know about critical price drops with instant email notifications. These alerts empower you to react swiftly to market changes, ensuring your pricing strategy remains competitive.

- **Advanced Inventory Forecasting** *(Currently in Development)*: Enhance your market readiness with predictive insights based on historical inventory trends. This forthcoming feature aims to forecast stock durations and prepare you for replenishments, ensuring you’re always inventory-ready without overstocking.


## Project Structure

```
competitor_watcher/
├── .env
├── .gitignore
├── config.json
├── pdm.lock
├── pyproject.toml
├── README.md
├── src/
│   ├── competitor_watcher/
│   │   ├── __init__.py
│   │   ├── __main__.py
│   │   ├── data_analysis/
│   │   │   ├── __init__.py
│   │   │   └── analyzer.py
│   │   ├── data_loading/
│   │   │   └── transform_raw_data.py
│   │   └── utils/
│   │       ├── config_loader.py
│   │       ├── db_management.py
│   │       └── email_sender.py
└── tests/
```


## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/mag1cfrog/idara_competitor_watcher.git
    cd competitor_watcher
    ```

2. Install dependencies using PDM:
    ```sh
    pdm install
    ```

3. Set up your environment variables and configuration settings as detailed in the [Configuration](#configuration) section below.


## Configuration

### `config.json`

Configure the application by editing the `config.json` file as follows:

```json
{
    "competitor_asin_dict": {
        "YourProductASIN1": ["CompetitorASIN1", "CompetitorASIN2", "CompetitorASIN3"],
        "YourProductASIN2": ["CompetitorASIN4", "CompetitorASIN5", "CompetitorASIN6"]
    },
    "notification_email": "your_email@example.com",
    "email_sender": "your_email@example.com"
}
```
This structure maps each of your product ASINs to a list of corresponding competitor product ASINs that you are monitoring. notification_email is the email address to receive alerts, and email_sender is the email address used to send these notifications.

### `.env`
Set up the environment variables necessary for operation by creating a `.env` file in the project root directory:

```
# Choose the storage type: 'POSTGRES' for PostgreSQL, any other value defaults to DuckDB
STORAGE_TYPE=duckdb
# Directory where DuckDB files will be stored (only used if STORAGE_TYPE is not 'POSTGRES')
STORAGE_DIRECTORY=./data

# PostgreSQL settings (only used if STORAGE_TYPE='POSTGRES')
POSTGRES_PASSWORD=your_password_here
POSTGRES_HOST=your_host_here
POSTGRES_PORT=5432
POSTGRES_DBNAME=competitors

# Amazon SP-API settings
sp_api_refresh_token=your_sp_api_refresh_token_here
sp_api_lwa_app_id=your_sp_api_lwa_app_id_here
sp_api_lwa_client_secret=your_sp_api_lwa_client_secret_here

# Gmail sender password (used for sending email notifications)
gmail_sender_password=your_gmail_password_here
```


## Usage

To start using the Competitor Watcher, follow these steps after installation:

1. **Configuration Setup:**
   - Ensure your `config.json` and `.env` files are properly set up as described in the [Configuration](#configuration) section.
   - Make sure that the database connection details and SP-API credentials are correct.

2. **Running the Tool:**
   - To start the monitoring and analysis process, use the following command:
     ```sh
     pdm run python -m competitor_watcher
     ```
   - This command will initiate the sequence to fetch competitor prices, analyze for significant discounts, and send out email notifications if applicable.

3. **Scheduling Regular Runs:**
   - For ongoing monitoring, consider setting up a scheduler like Cron (for Linux/Mac) or Task Scheduler (for Windows). Here is an example of a Cron job that runs every day at 5 AM:
     ```
     0 5 * * * /path/to/pdm run python -m competitor_watcher
     ```
   - Adjust the schedule according to your needs.

4. **Monitoring and Logs:**
   - Check the logs generated by Loguru to monitor the application’s performance and catch any potential errors. The logs can help you understand the flow and any issues that arise during execution.

5. **Updating Competitor Lists:**
   - Regularly update the `competitor_asin_dict` in `config.json` to ensure that you are monitoring the most relevant products.

### Advanced Options

- **Switching Storage:**
  - To switch from DuckDB to PostgreSQL:
    - Update `STORAGE_TYPE` in the `.env` file to 'POSTGRES' and ensure all PostgreSQL connection details are correct.
  - Rerun the installation commands to ensure all dependencies are adjusted accordingly.

- **Modifying Notification Settings:**
  - To change the email settings, update the `email_settings` in `config.json` and ensure the SMTP settings in `.env` are correct to allow emails to be sent successfully.

Use these instructions to get the most out of Competitor Watcher, keeping your competitive analysis sharp and timely.


## Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Commit your changes (`git commit -am 'Add new feature'`).
5. Push to the branch (`git push origin feature-branch`).
6. Create a new Pull Request.

