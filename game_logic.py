class GameLogic:
    def __init__(self, board_numbers):
        """
        Initialize the game logic
        
        Args:
            board_numbers: 2D list of the board numbers
        """
        self.board_numbers = board_numbers
        self.rows = len(board_numbers)
        self.cols = len(board_numbers[0])
        
        # Create position mapping from values to coordinates
        self.value_positions = {}
        for i in range(self.rows):
            for j in range(self.cols):
                self.value_positions[board_numbers[i][j]] = (i, j)
        
        # Initialize win patterns
        self.win_patterns = self._generate_win_patterns()
    
    def _generate_win_patterns(self):
        """Generate all possible winning patterns (4 in a row)"""
        patterns = []
        
        # Horizontal wins
        for i in range(self.rows):
            for j in range(self.cols - 3):
                pattern = [self.board_numbers[i][j+k] for k in range(4)]
                patterns.append(pattern)
        
        # Vertical wins
        for i in range(self.rows - 3):
            for j in range(self.cols):
                pattern = [self.board_numbers[i+k][j] for k in range(4)]
                patterns.append(pattern)
        
        # Diagonal wins (top-left to bottom-right)
        for i in range(self.rows - 3):
            for j in range(self.cols - 3):
                pattern = [self.board_numbers[i+k][j+k] for k in range(4)]
                patterns.append(pattern)
        
        # Diagonal wins (bottom-left to top-right)
        for i in range(3, self.rows):
            for j in range(self.cols - 3):
                pattern = [self.board_numbers[i-k][j+k] for k in range(4)]
                patterns.append(pattern)
                
        return patterns
    
    def check_win(self, marked_positions):
        """
        Check if the marked positions form a winning pattern
        
        Args:
            marked_positions: Set of board values that are marked
            
        Returns:
            (is_win, winning_cells): Tuple with win status and list of winning positions
        """
        for pattern in self.win_patterns:
            if all(pos in marked_positions for pos in pattern):
                # Get the coordinates of the winning cells
                winning_cells = [self.value_positions[pos] for pos in pattern]
                return True, winning_cells
                
        return False, []
    
    def check_draw(self, player_marks, computer_marks):
        """Check if the game is a draw (board is full)"""
        total_cells = self.rows * self.cols
        total_marked = len(player_marks) + len(computer_marks)
        return total_marked == total_cells
    
    def get_winning_move(self, marks, selector_num, validator):
        """
        Find a move that would lead to a win
        
        Args:
            marks: Set of currently marked positions
            selector_num: Current selector number
            validator: MoveValidator object
            
        Returns:
            winning_value or None if no winning move exists
        """
        valid_moves = validator.get_valid_moves(selector_num, marks, set())
        
        for _, target in valid_moves:
            # Simulate this move
            test_marks = marks.copy()
            test_marks.add(target)
            
            is_win, _ = self.check_win(test_marks)
            if is_win:
                return target
                
        return None
    
    def get_potential_win_paths(self, marks):
        """
        Find paths that are close to winning (3 in a row)
        
        Args:
            marks: Set of currently marked positions
            
        Returns:
            List of tuples (pattern, missing_value) for paths with 3 marks
        """
        potential_wins = []
        
        for pattern in self.win_patterns:
            # Count how many positions in this pattern are marked
            marked_count = sum(1 for pos in pattern if pos in marks)
            
            if marked_count == 3:
                # Find the missing position
                missing = next(pos for pos in pattern if pos not in marks)
                potential_wins.append((pattern, missing))
                
        return potential_wins

# Test the game logic if run as a script
if __name__ == "__main__":
    # Example board
    board_numbers = [
        [1, 2, 3, 4, 5, 6],
        [7, 8, 9, 10, 12, 14],
        [15, 16, 18, 20, 21, 24],
        [25, 27, 28, 30, 32, 35],
        [36, 40, 42, 45, 48, 49],
        [54, 56, 63, 64, 72, 81]
    ]
    
    game_logic = GameLogic(board_numbers)
    
    # Print all win patterns
    print(f"Total winning patterns: {len(game_logic.win_patterns)}")
    
    # Test a horizontal win
    horizontal_marks = {1, 2, 3, 4}
    is_win, winning_cells = game_logic.check_win(horizontal_marks)
    print(f"\nHorizontal win test: {is_win}")
    if is_win:
        print(f"Winning cells: {winning_cells}")
    
    # Test a vertical win
    vertical_marks = {3, 9, 18, 28}
    is_win, winning_cells = game_logic.check_win(vertical_marks)
    print(f"\nVertical win test: {is_win}")
    if is_win:
        print(f"Winning cells: {winning_cells}")
    
    # Test a diagonal win
    diagonal_marks = {7, 16, 28, 45}
    is_win, winning_cells = game_logic.check_win(diagonal_marks)
    print(f"\nDiagonal win test: {is_win}")
    if is_win:
        print(f"Winning cells: {winning_cells}")
    
    # Test almost winning (3 in a row)
    almost_win = {1, 2, 3, 10, 15}
    potential_wins = game_logic.get_potential_win_paths(almost_win)
    print(f"\nPotential win paths: {len(potential_wins)}")
    for pattern, missing in potential_wins:
        print(f"Almost complete pattern: {pattern}, Missing: {missing}")