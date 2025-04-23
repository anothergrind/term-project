class MoveValidator:
    def __init__(self, board_numbers):
        self.board_numbers = board_numbers
        self.board_values = {}
        
        # Create a dictionary mapping values to their board positions
        for i in range(len(board_numbers)):
            for j in range(len(board_numbers[i])):
                self.board_values[board_numbers[i][j]] = (i, j)
    
    def is_valid_selection(self, number):
        """Check if the selected number (1-9) is valid"""
        return 1 <= number <= 9
    
    def get_product(self, selector_num, board_num):
        """Calculate the product of the selector number and a board number"""
        return selector_num * board_num
    
    def find_products_on_board(self, selector_num):
        """Find all products on the board that can be made with the selected number"""
        products = []
        for row in self.board_numbers:
            for num in row:
                product = selector_num * num
                if product in self.board_values:
                    products.append((num, product))
        return products
    
    def is_valid_move(self, selector_num, target_value, player_marks, computer_marks):
        """
        Check if placing a marker on target_value using the selector_num is valid
        
        Args:
            selector_num: Number selected from the selector (1-9)
            target_value: Value on the board to place a marker on
            player_marks: Set of values already marked by the player
            computer_marks: Set of values already marked by the computer
            
        Returns:
            (is_valid, reason): Tuple with boolean validity and reason string if invalid
        """
        # Check if the target is already marked
        if target_value in player_marks or target_value in computer_marks:
            return False, "This position is already marked"
        
        # Check if the target value exists on the board
        if target_value not in self.board_values:
            return False, "This value doesn't exist on the board"
        
        # Check if the target value can be created as a product
        valid_products = self.find_products_on_board(selector_num)
        valid_targets = [product for _, product in valid_products]
        
        if target_value not in valid_targets:
            return False, f"Cannot create {target_value} using {selector_num} as a multiplier"
            
        return True, ""
    
    def get_valid_moves(self, selector_num, player_marks, computer_marks):
        """Get all valid moves for a given selector number"""
        all_marked = player_marks.union(computer_marks)
        valid_products = self.find_products_on_board(selector_num)
        
        # Filter out products that are already marked
        valid_moves = [(multiplicand, product) for multiplicand, product in valid_products 
                      if product not in all_marked]
        
        return valid_moves

# Test the move validator if run as a script
if __name__ == "__main__":
    # Example board from the game
    board_numbers = [
        [1, 2, 3, 4, 5, 6],
        [7, 8, 9, 10, 12, 14],
        [15, 16, 18, 20, 21, 24],
        [25, 27, 28, 30, 32, 35],
        [36, 40, 42, 45, 48, 49],
        [54, 56, 63, 64, 72, 81]
    ]
    
    validator = MoveValidator(board_numbers)
    
    # Test finding products
    print("Products using 3 as selector:")
    products = validator.find_products_on_board(3)
    for multiplicand, product in products:
        print(f"3 × {multiplicand} = {product}")
    
    # Test valid move
    is_valid, reason = validator.is_valid_move(3, 9, set(), set())
    print(f"\nIs 3×3=9 a valid move? {is_valid}, {reason if not is_valid else 'Valid move'}")
    
    # Test invalid move (already marked)
    is_valid, reason = validator.is_valid_move(3, 9, {9}, set())
    print(f"Is 3×3=9 valid if 9 is already marked? {is_valid}, {reason}")