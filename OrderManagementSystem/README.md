
Here’s a sample `README.md` file for your Deribit trading API project. You can customize it further to suit your project's specific details.

```markdown
# Deribit Trading API

This project is a simple command-line application that interacts with the Deribit trading platform using its API. Users can place orders, cancel orders, modify orders, get the order book, and view current positions.

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

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

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
```

### Instructions for Customization
- **Project URL**: Replace `https://github.com/yourusername/deribit-trading-api.git` with the actual URL of your GitHub repository.
- **License Section**: If you choose a different license, adjust the license section accordingly.
- **Additional Features**: Add or modify the features section based on any additional functionality you may have implemented.
- **Dependencies**: If there are any specific versions of the libraries that are required, include that information in the installation section. 

You can copy this content into a file named `README.md` in your project's root directory.
