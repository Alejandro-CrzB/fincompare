import yfinance as yf

# Most popular indexes with their respective ticker
indexes = {
    "1": ("S&P 500", "^GSPC"),
    "2": ("Dow Jones Industrial Average", "^DJI"),
    "3": ("Nasdaq Composite", "^IXIC"),
    "4": ("Russell 2000", "^RUT"),
    "5": ("IPC Mexico (S&P/BMV IPC)", "^MXX"),
    "6": ("FTSE 100 (UK)", "^FTSE"),
    "7": ("DAX (Germany)", "^GDAXI"),
    "8": ("Nikkei 225 (Japan)", "^N225"),
    "9": ("Hang Seng Index (Hong Kong)", "^HSI"),
    "10": ("Shanghai Composite (China)", "000001.SS"),
}

# Display the options to the user
print("Select a stock market index to fetch data:")
for key, (name, _) in indexes.items():
    print(f"{key}. {name}")
choice = input("Enter the number of the index you want: ")

# Validate input
if choice in indexes:
    index_name, index_symbol = indexes[choice]
    print(f"\nFetching data for {index_name} ({index_symbol})...\n")

    # Fetch data for the selected index
    data = yf.download(index_symbol, period="1mo")  # Fetch data for the past month

    if not data.empty:
        print(data.tail())  # Show the last few rows of the data
    else:
        print("No data available for this index.")
else:
    print("Invalid selection. Please run the script again and choose a valid number.")
