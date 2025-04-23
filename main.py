import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import numpy as np
import time
# Import our game modules
from drawboard import BoardRenderer
from move_validation import MoveValidator
from computer_move import ComputerPlayer
from game_logic import GameLogic

class MultiplicationGame:
    def __init__(self):
        # Define the game board
        self.board_numbers = [
            [1, 2, 3, 4, 5, 6],
            [7, 8, 9, 10, 12, 14],
            [15, 16, 18, 20, 21, 24],
            [25, 27, 28, 30, 32, 35],
            [36, 40, 42, 45, 48, 49],
            [54, 56, 63, 64, 72, 81]
        ]
       
        # Initialize game components
        self.renderer = BoardRenderer()
        self.validator = MoveValidator(self.board_numbers)
        self.computer = ComputerPlayer(self.board_numbers, self.validator)
        self.game_logic = GameLogic(self.board_numbers)
       
        # Game state
        self.player_marks = set()
        self.computer_marks = set()
        self.current_selector = None
        self.game_over = False
        self.player_turn = True
        self.message = "Make four in a line using multiplication."
        self.winning_cells = []
       
        # Set computer difficulty
        self.computer.set_difficulty("normal")
       
        # Setup UI
        self.setup_ui()
   
    def setup_ui(self):
        """Set up the interactive UI with matplotlib"""
        self.fig = plt.figure(figsize=(12, 10), facecolor='#1E1E1E')
       
        # Game board area
        self.board_ax = plt.subplot2grid((10, 10), (0, 0), colspan=7, rowspan=7)
        self.board_ax.axis('off')
       
        # Selector area
        self.selector_ax = plt.subplot2grid((10, 10), (8, 0), colspan=7, rowspan=1)
        self.selector_ax.axis('off')
       
        # Message area
        self.message_ax = plt.subplot2grid((10, 10), (7, 0), colspan=7, rowspan=1)
        self.message_ax.axis('off')
       
        # Game controls area
        self.controls_ax = plt.subplot2grid((10, 10), (0, 7), colspan=3, rowspan=9)
        self.controls_ax.axis('off')
       
        # Add new game button
        self.new_game_button_ax = plt.subplot2grid((10, 10), (9, 3), colspan=3, rowspan=1)
        self.new_game_button = Button(self.new_game_button_ax, 'NEW GAME', color='orange')
        self.new_game_button.on_clicked(self.new_game)
       
        # Setup click events
        self.fig.canvas.mpl_connect('button_press_event', self.on_click)
       
        # Set window title
        self.fig.canvas.manager.set_window_title('Multiplication Game')
       
        # Update the UI
        self.update_ui()
   
    def update_ui(self):
        """Update the game UI"""
        # Clear axes
        self.board_ax.clear()
        self.selector_ax.clear()
        self.message_ax.clear()
        self.controls_ax.clear()
       
        # Set backgrounds
        self.board_ax.set_facecolor('#1E1E1E')
        self.selector_ax.set_facecolor('#1E1E1E')
        self.message_ax.set_facecolor('#1E1E1E')
        self.controls_ax.set_facecolor('#1E1E1E')
       
        # Hide axes
        self.board_ax.axis('off')
        self.selector_ax.axis('off')
        self.message_ax.axis('off')
        self.controls_ax.axis('off')
       
        # Update markers
        self.renderer.update_markers(self.player_marks, self.computer_marks)
       
        # Draw the game board
        highlight_cells = []
        if hasattr(self, 'winning_cells'):
            highlight_cells = self.winning_cells
           
        board_fig = self.renderer.draw_game_board(highlight_cells)
        self.board_ax.imshow(self._fig_to_array(board_fig))
        plt.close(board_fig)
       
        # Draw the selector
        selector_fig = self.renderer.draw_selector(self.current_selector)
        self.selector_ax.imshow(self._fig_to_array(selector_fig))
        plt.close(selector_fig)
       
        # Show current message
        self.message_ax.text(0.5, 0.5, self.message, ha='center', va='center', 
                           color='white', fontsize=14, fontweight='bold')
        
        # Draw game controls
        self.draw_controls()
        
        # Refresh the figure
        self.fig.canvas.draw_idle()

    def draw_controls(self):
        """Draw game control information"""
        controls_text = [
            "CONTROLS:",
            "",
            "• Click on a number to select it",
            "• Click again to confirm placement",
            "• Make four in a line by multiplication",
            "",
            "Player: X (Blue)",
            "Computer: O (Red)",
            "",
            "Difficulty: Normal"
        ]
        
        for i, text in enumerate(controls_text):
            self.controls_ax.text(0.1, 0.9 - i * 0.08, text, color='white', 
                                fontsize=11, fontweight='bold' if i == 0 else 'normal')

    def _fig_to_array(self, fig):
        """Convert matplotlib figure to array for display"""
        fig.canvas.draw()
        data = np.frombuffer(fig.canvas.tostring_rgb(), dtype=np.uint8)
        data = data.reshape(fig.canvas.get_width_height()[::-1] + (3,))
        return data

    def on_click(self, event):
        """Handle click events"""
        if self.game_over:
            return
            
        if event.inaxes == self.board_ax:
            # Convert click position to board cell
            x, y = event.xdata, event.ydata
            board_width, board_height = self.board_ax.get_xlim()[1], self.board_ax.get_ylim()[0]
            col = int(x / (board_width / 6))
            row = int(y / (board_height / 6))
            
            if 0 <= row < 6 and 0 <= col < 6:
                self.handle_board_click(row, col)
                
        elif event.inaxes == self.selector_ax and self.current_selector is not None:
            # Handle selector click
            x = event.xdata
            selector_width = self.selector_ax.get_xlim()[1]
            selected_option = int(x / (selector_width / 2))
            
            if selected_option == 0:  # Confirm
                self.confirm_selection()
            else:  # Cancel
                self.cancel_selection()

    def handle_board_click(self, row, col):
        """Handle a click on the game board"""
        if not self.player_turn:
            self.message = "Wait for the computer's move!"
            self.update_ui()
            return
            
        clicked_number = self.board_numbers[row][col]
        cell_position = (row, col)
        
        # Check if the cell is already marked
        if cell_position in self.player_marks or cell_position in self.computer_marks:
            self.message = "That cell is already taken!"
            self.update_ui()
            return
            
        # If no current selection, make this the selection
        if self.current_selector is None:
            self.current_selector = {
                "number": clicked_number,
                "position": cell_position
            }
            self.message = f"Selected {clicked_number}. Confirm or cancel?"
            self.update_ui()
        else:
            # Check if this forms a valid multiplication with the current selection
            selected_number = self.current_selector["number"]
            selected_position = self.current_selector["position"]
            
            if self.validator.is_valid_move(selected_position, cell_position):
                # Mark both cells
                self.player_marks.add(selected_position)
                self.player_marks.add(cell_position)
                
                # Check for win
                winning_line = self.game_logic.check_win(self.player_marks)
                if winning_line:
                    self.winning_cells = winning_line
                    self.game_over = True
                    self.message = "You win! Congratulations!"
                    self.update_ui()
                    return
                    
                # Computer's turn
                self.current_selector = None
                self.message = "Computer is thinking..."
                self.update_ui()
                
                # Add a small delay to simulate computer thinking
                self.fig.canvas.start_event_loop(0.8)
                
                # Make computer move
                self.make_computer_move()
            else:
                self.message = f"{selected_number} × {clicked_number} is not a valid move!"
                self.update_ui()

    def confirm_selection(self):
        """Confirm the current selection"""
        if self.current_selector is None:
            return
            
        position = self.current_selector["position"]
        self.player_marks.add(position)
        self.current_selector = None
        
        # Check for win
        winning_line = self.game_logic.check_win(self.player_marks)
        if winning_line:
            self.winning_cells = winning_line
            self.game_over = True
            self.message = "You win! Congratulations!"
            self.update_ui()
            return
            
        # Computer's turn
        self.message = "Computer is thinking..."
        self.update_ui()
        
        # Add a small delay to simulate computer thinking
        self.fig.canvas.start_event_loop(0.8)
        
        # Make computer move
        self.make_computer_move()

    def cancel_selection(self):
        """Cancel the current selection"""
        self.current_selector = None
        self.message = "Selection canceled. Choose a number."
        self.update_ui()

    def make_computer_move(self):
        """Handle the computer's move"""
        self.player_turn = False
        
        # Get computer move
        move = self.computer.make_move(self.player_marks, self.computer_marks)
        
        if move:
            # Unpack the move (might be a single cell or a pair)
            if len(move) == 1:
                self.computer_marks.add(move[0])
                row, col = move[0]
                number = self.board_numbers[row][col]
                self.message = f"Computer placed at {number}."
            else:
                self.computer_marks.add(move[0])
                self.computer_marks.add(move[1])
                row1, col1 = move[0]
                row2, col2 = move[1]
                num1 = self.board_numbers[row1][col1]
                num2 = self.board_numbers[row2][col2]
                self.message = f"Computer placed at {num1} and {num2}."
            
            # Check for win
            winning_line = self.game_logic.check_win(self.computer_marks)
            if winning_line:
                self.winning_cells = winning_line
                self.game_over = True
                self.message = "Computer wins! Better luck next time."
                self.update_ui()
                return
                
            # Check for draw
            if len(self.player_marks) + len(self.computer_marks) == 36:
                self.game_over = True
                self.message = "Game over! It's a draw."
                self.update_ui()
                return
        else:
            self.message = "Computer couldn't find a move! Your turn."
        
        self.player_turn = True
        self.update_ui()

    def new_game(self, event=None):
        """Start a new game"""
        self.player_marks = set()
        self.computer_marks = set()
        self.current_selector = None
        self.game_over = False
        self.player_turn = True
        self.message = "New game! Make four in a line using multiplication."
        self.winning_cells = []
        self.update_ui()

def main():
    """Main function to start the game"""
    game = MultiplicationGame()
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()