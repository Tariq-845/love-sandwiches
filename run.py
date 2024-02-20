import gspread 
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('love_sandwiches')

def get_sales_data():
  """
  Get sales figures input from the user.
  Run while loop to collect valid string data from the user
  through the terminal, which must contain exactly 6 values
  and they must be integers. The loop will keep running until
  user inputs valid data.
  """
  while True:
    print('Please enter sales data from the last market.')
    print('Data should be six numbers, separated by commas.')
    print('Example: 10,20,30,40,50,60\n')

    data_str = input('Enter data here:\n')

    sales_data = data_str.split(',')

    if validate_data(sales_data):
      print('Data is valid!')
      break
    
  return sales_data

def validate_data(values):
  """
  Inside the try, converts all string values into integers. 
  Raises ValueError if strings cannot be converted into int,
  or if there aren't exactly 6 values.
  """
  
  try:
    [int(value) for value in values]
    if len(values) != 6:
      raise ValueError(
        f'Exactly 6 values required, you provided {len(values)}'
      )

  except ValueError as e:
    print(f'Invalid data: {e}, please try again.\n')
    return False
  
  return True

def update_worksheet(data, worksheet):
  """
  Receives a list of integers to be inserted into a worksheet and
  updates the relevant worksheet with the data provided
  """
  print(f'Updating {worksheet} worksheet...\n')
  worksheet_to_update = SHEET.worksheet(worksheet)
  worksheet_to_update.append_row(data)
  print(f'{worksheet} worksheet updated successfully.\n')

def calculate_surplus_data(sales_row):
  """
  Compare sales with stock and calcualte the surplus for each 
  item type.

  The surplus is defined as the sales figure subtracted from the stock:
  - Positive surplus indicates a waste (more stock than sold)
  - Negative surplus indicates extras made (less stock than sold)
  """

  print('Calculating surplus data...\n')
  stock_data = SHEET.worksheet('stock').get_all_values()
  stock_row = stock_data[-1]
  print(f'stock row: {stock_row}\nsales row: {sales_row}\n')

  surplus_data = []
  for stock, sales in zip(stock_row, sales_row):
    surplus = int(stock) - sales
    surplus_data.append(surplus)

  return surplus_data

def get_last_five_entries_sales():
  """
  Collects last 5 entries for each sandwich in the sales
  worksheet and returns the data as a list of lists.
  """
  sales = SHEET.worksheet('sales')

  columns = []
  for i in range(1, 7):
    column = sales.col_values(i)
    columns.append(column[-5:])

  return columns

def calculate_stock_data(data):
  """
  Calculate the average stock for each item type, adding 10%
  """
  print('Calculating stock data...\n')
  new_stock_data = []

  for column in data:
    int_column = [int(num) for num in column]
    average = sum(int_column) / len(int_column)
    stock_num = average * 1.1
    new_stock_data.append(round(stock_num))
  
  return new_stock_data

def main():
  """
  Run all program functions
  """
  data = get_sales_data()
  sales_data = [int(num) for num in data]
  update_worksheet(sales_data, 'sales')
  new_surplus_data = calculate_surplus_data(sales_data)
  update_worksheet(new_surplus_data, 'surplus')
  sales_columns = get_last_five_entries_sales()
  stock = calculate_stock_data(sales_columns)
  update_worksheet(stock, 'stock')

print('Welcome to Love Sandwiches Data Automation')
main()