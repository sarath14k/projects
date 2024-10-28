

```markdown
# Deribit Trading API

This project is a simple command-line application that interacts with the Deribit trading platform using its API. Users can place orders, cancel orders, modify orders, get the order book, and view current positions.

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)

## Features

- Place market orders for specified instruments.
- Cancel existing orders by order ID.
- Modify existing orders by order ID, including amount and price adjustments.
- Retrieve the order book for specified instruments and depth.
- View current positions in the account.

## Requirements

- C++17 or later
- `libcurl` library
- `nlohmann/json` library for JSON parsing

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/deribit-trading-api.git
   cd deribit-trading-api
   ```

2. Build the project:
   ```bash
   make
   ```

3. Ensure that you have the necessary libraries installed:
   - For Ubuntu, you can install `libcurl` and `nlohmann/json` with:
     ```bash
     sudo apt-get install libcurl4-openssl-dev
     sudo apt-get install nlohmann-json3-dev
     ```

## Usage

1. Run the application:
   ```bash
   make run
   ```

2. Follow the prompts to select an option:
   - **1**: Place Order
   - **2**: Cancel Order
   - **3**: Modify Order
   - **4**: Get Order Book
   - **5**: View Current Positions
   - **6**: Exit

3. Input the required details based on your selected option.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request if you have suggestions or improvements.

