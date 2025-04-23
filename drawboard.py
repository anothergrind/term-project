def multiplication_table(number, rows):
    """Prints a multiplication table for a given number up to a specified number of rows."""
    for i in range(1, rows + 1):
        result = number * i
        print(f"{number} x {i} = {result}")

def main():
    """Main function to execute the multiplication table."""
    number = int(input("Enter a number to generate its multiplication table: "))
    rows = int(input("Enter the number of rows for the multiplication table: "))
    multiplication_table(number, rows)