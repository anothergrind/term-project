import random

class ComputerPlayer:
    def __init__(self, board_numbers, validator):
        """
        Initialize the computer player
        
        Args:
            board_numbers: 2D list of board numbers
            validator: MoveValidator object
        """
        self.board_numbers = board_numbers
        self.validator = validator
        self.difficulty = "normal"  # Options: "easy", "normal", "hard"
    
    def set_difficulty(self, difficulty):
        """Set the difficulty level of the computer player"""
        if difficulty in ["easy", "normal", "hard"]:
            self.difficulty = difficulty
        else:
            raise ValueError("Difficulty must be 'easy', 'normal', or 'hard'")
    
    def choose_selector_number(self, player_marks, computer_marks):
        """Choose a selector number (1-9) based on the current game state"""
        # Count how many valid moves each selector number gives
        selector_options = {}
        for selector in range(1, 10):
            valid_moves = self.validator.get_valid_moves(selector, player_marks, computer_marks)
            selector_options[selector] = len(valid_moves)
        
        if self.difficulty == "easy":
            # Easy: Pick a selector with at least one valid move, but not necessarily the best
            possible_selectors = [s for s, count in selector_options.items() if count > 0]
            if possible_selectors:
                return random.choice(possible_selectors)
            return random.randint(1, 9)  # Fallback
            
        elif self.difficulty == "normal":
            # Normal: Prefer selectors with more valid moves
            max_moves = max(selector_options.values(), default=0)
            if max_moves > 0:
                good_selectors = [s for s, count in selector_options.items() 
                                 if count >= max_moves * 0.7]  # At least 70% as good as the best
                return random.choice(good_selectors)
            return random.randint(1, 9)  # Fallback
            
        else:  # Hard
            # Hard: Always pick the selector with the most valid moves
            max_moves = max(selector_options.values(), default=0)
            if max_moves > 0:
                best_selectors = [s for s, count in selector_options.items() 
                                 if count == max_moves]
                return random.choice(best_selectors)
            return random.randint(1, 9)  # Fallback
    
    def choose_move(self, selector_num, player_marks, computer_marks, game_logic=None):
        """
        Choose a move for the computer based on the selector number
        
        Args:
            selector_num: Number selected from the selector (1-9)
            player_marks: Set of values already marked by the player
            computer_marks: Set of values already marked by the computer
            game_logic: Optional GameLogic object for win detection
            
        Returns:
            target_value: The value on the board to place a marker on
        """
        valid_moves = self.validator.get_valid_moves(selector_num, player_marks, computer_marks)
        
        if not valid_moves:
            return None  # No valid moves available
            
        # If we have game logic and are playing on hard, look for winning moves
        if game_logic and self.difficulty == "hard":
            # Check if any move would result in a win
            for _, product in valid_moves:
                # Simulate marking this position
                test_marks = computer_marks.copy()
                test_marks.add(product)
                if game_logic.check_win(test_marks):
                    return product  # This move wins!
            
            # Check if any move would block the player from winning
            for _, product in valid_moves:
                # Simulate the player marking this position
                test_marks = player_marks.copy()
                test_marks.add(product)
                if game_logic.check_win(test_marks):
                    return product  # Block this winning move!
        
        # Otherwise, make a random choice among valid moves
        _, target_value = random.choice(valid_moves)
        return target_value

# Test the computer player if run as a script
if __name__ == "__main__":
    # Import needed modules for testing
    import sys
    sys.path.append('.')
    from move_validation import MoveValidator
    
    # Example board
    board_numbers = [
        [1, 2, 3, 4, 5, 6],
        [7, 8, 9, 10, 12, 14],
        [15, 16, 18, 20, 21, 24],
        [25, 27, 28, 30, 32, 35],
        [36, 40, 42, 45, 48, 49],
        [54, 56, 63, 64, 72, 81]
    ]
    
    validator = MoveValidator(board_numbers)
    computer = ComputerPlayer(board_numbers, validator)
    
    # Test with empty board
    selector = computer.choose_selector_number(set(), set())
    move = computer.choose_move(selector, set(), set())
    
    print(f"Computer chose selector: {selector}")
    print(f"Computer chose move: {move}")
    
    # Test with some marked positions
    player_marks = {9, 16, 25}
    computer_marks = {4, 10, 21}
    
    computer.set_difficulty("hard")
    selector = computer.choose_selector_number(player_marks, computer_marks)
    move = computer.choose_move(selector, player_marks, computer_marks)
    
    print(f"\nWith some marks on the board:")
    print(f"Computer chose selector: {selector}")
    print(f"Computer chose move: {move}")