# Inventory Management System

## Overview

This Inventory Management System (IMS) is a Python-based application designed to help users efficiently manage their product inventory. It provides functionalities for adding, updating, deleting, and searching for products, as well as processing incoming and outgoing goods. The application also allows for QR code generation for easy product identification.

## Features

- **Product Management**
  - Add new products with details such as name, quantity, price, and description.
  - Update existing product details.
  - Delete products from the inventory.
  - Search for products by ID or name.

- **Stock Management**
  - Process incoming goods and update stock levels.
  - Process outgoing goods and remove stock as needed.

- **QR Code Generation**
  - Create QR codes for products for easy identification and tracking.

## Technology Stack

- **Programming Language:** Python
- **GUI Library:** Tkinter
- **Data Handling:** Custom inventory management logic (implement as needed)
- **Image Generation:** QR code library

## Prerequisites

Make sure you have the following installed:

- Python 3.x

## Requirements
To run this application, ensure you have the following Python packages installed:

- `tkinter`: For creating the graphical user interface.
- `sqlite3`: For database management.
- `qrcode`: For generating QR codes.
- `csv`: For handling CSV file operations.
- `shutil`: For file operations (copying and moving files).
- `datetime`: For handling date and time functions.
- `openpyxl`: For working with Excel files.

### Installation


## Installation

1. Clone this repository to your local machine:
   ```bash
   git clone https://github.com/GoldenxSun/InventoryManagementSystem.git
   cd InventoryManagementSystem
   ```

2. Install the required libraries:
    ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python ims_gui.pyw
   ```

## Usage

1. **Add Product:**
   - Click on the "Add Product" button and fill in the required fields.

2. **Edit Product:**
   - Select a products and click on the "Edit Product" button.

3. **Delete Product:**
   - Select a product and click the "Delete Product" button to remove it from the inventory.

4. **Search for Product:**
   - Enter the product ID or name in the search bar and press Enter to find the product.

5. **Process Incoming Goods:**
   - Click on "Process Incoming Goods," enter the product ID and quantity, and click "Add."

6. **Process Outgoing Goods:**
   - Click on "Process Outgoing Goods," enter the product ID and quantity, and click "Remove."

7. **Generate QR Code:**
   - Double-click on a product to generate its QR code.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
