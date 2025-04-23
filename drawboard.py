import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

class BoardRenderer:
    def __init__(self):
        # Define the numbers for the main game grid
        self.board_numbers = [
            [1, 2, 3, 4, 5, 6],
            [7, 8, 9, 10, 12, 14],
            [15, 16, 18, 20, 21, 24],
            [25, 27, 28, 30, 32, 35],
            [36, 40, 42, 45, 48, 49],
            [54, 56, 63, 64, 72, 81]
        ]
        
        # Player and computer markers
        self.player_marks = set()
        self.computer_marks = set()
        
        # Colors
        self.player_color = 'lightgreen'
        self.computer_color = 'purple'
        self.background_color = '#1E1E1E'
        self.cell_color = 'lightgray'
        self.text_color = 'black'
        self.highlight_color = 'yellow'
        
    def draw_game_board(self, highlight_cells=None):
        """
        Draw the main 6x6 game board with player and computer markings
        
        Args:
            highlight_cells: Optional list of (row, col) tuples to highlight
        """
        if highlight_cells is None:
            highlight_cells = []
            
        # Create a figure and axis
        fig, ax = plt.subplots(figsize=(8, 8))
        fig.patch.set_facecolor(self.background_color)
        ax.set_facecolor(self.background_color)
        
        # Hide the axes
        ax.axis('tight')
        ax.axis('off')
        
        # Create the table
        table = ax.table(
            cellText=[[str(self.board_numbers[i][j]) for j in range(6)] for i in range(6)],
            loc='center',
            cellLoc='center',
            edges='closed'
        )
        
        # Style the table
        table.auto_set_font_size(False)
        table.set_fontsize(14)
        table.scale(1, 1.5)
        
        # Style each cell
        for i in range(6):
            for j in range(6):
                cell = table[(i, j)]
                cell.set_text_props(weight='bold', color=self.text_color)
                cell.set_edgecolor('black')
                
                # Check if cell is marked by player or computer
                value = self.board_numbers[i][j]
                if value in self.player_marks:
                    cell.set_facecolor(self.player_color)
                elif value in self.computer_marks:
                    cell.set_facecolor(self.computer_color)
                elif (i, j) in highlight_cells:
                    cell.set_facecolor(self.highlight_color)
                else:
                    cell.set_facecolor(self.cell_color)
        
        # Add "YOUR TURN..." text above the board
        ax.text(0.5, 1.05, "YOUR TURN...", 
                fontsize=20, weight='bold', color='yellow', 
                ha='center', va='center', transform=ax.transAxes)
        
        plt.tight_layout()
        return fig, ax
    
    def draw_selector(self, selected_number=None):
        """
        Draw the horizontal number selector with triangles
        
        Args:
            selected_number: Optional number to highlight in the selector
        """
        # Create figure with black background
        fig, ax = plt.subplots(figsize=(10, 2))
        fig.patch.set_facecolor(self.background_color)
        ax.set_facecolor(self.background_color)
        
        # Hide axes
        ax.axis('off')
        
        # Create horizontal number boxes
        numbers = np.arange(1, 10).reshape(1, 9)  # Numbers 1-9 in a row
        
        # Create table for the numbers
        table = ax.table(
            cellText=[[str(num) for num in numbers[0]]],
            loc='center',
            cellLoc='center',
            edges='closed'
        )
        
        # Style the table cells
        for j in range(9):
            cell = table[(0, j)]
            cell.set_text_props(weight='bold', fontsize=16, color=self.text_color)
            cell.set_edgecolor('black')
            
            if selected_number == j + 1:  # Highlight the selected number
                cell.set_facecolor(self.highlight_color)
            else:
                cell.set_facecolor(self.cell_color)
                
            cell.set_height(0.5)  # Make cells square-ish
        
        table.scale(1, 2)  # Adjust height
        
        # Add yellow triangles
        # Top triangle (pointing down)
        top_triangle = Polygon([(0.1, 0.9), (0.18, 0.75), (0.02, 0.75)], 
                              closed=True, facecolor=self.highlight_color, edgecolor='none')
        ax.add_patch(top_triangle)
        
        # Bottom triangle (pointing up)
        bottom_triangle = Polygon([(0.1, 0.1), (0.18, 0.25), (0.02, 0.25)], 
                                 closed=True, facecolor=self.highlight_color, edgecolor='none')
        ax.add_patch(bottom_triangle)
        
        plt.tight_layout()
        return fig, ax
    
    def display_full_game_ui(self, selected_number=None, highlight_cells=None):
        """Display the complete game UI with board and selector"""
        fig = plt.figure(figsize=(10, 12), facecolor=self.background_color)
        
        # Main game board (top)
        ax1 = plt.subplot2grid((5, 1), (0, 0), rowspan=4)
        board_fig, _ = self.draw_game_board(highlight_cells)
        plt.close(board_fig)  # Close the separate figure
        plt.sca(ax1)
        ax1.axis('off')
        
        # Selector (bottom)
        ax2 = plt.subplot2grid((5, 1), (4, 0), rowspan=1)
        selector_fig, _ = self.draw_selector(selected_number)
        plt.close(selector_fig)  # Close the separate figure
        plt.sca(ax2)
        ax2.axis('off')
        
        # Game instructions
        plt.figtext(0.7, 0.7, "Move the markers on\nthe number line to\nmake products.\nFour in a row wins.", 
                   fontsize=12, color='white')
        
        # Player/Computer labels
        plt.figtext(0.8, 0.5, "PLAYER", fontsize=12, color='white')
        plt.figtext(0.8, 0.45, "COMPUTER", fontsize=12, color='white')
        
        # Player/Computer icons (represented as colored squares)
        player_square = plt.Rectangle((0.75, 0.5), 0.03, 0.03, color=self.player_color)
        computer_square = plt.Rectangle((0.75, 0.45), 0.03, 0.03, color=self.computer_color)
        ax1.add_patch(player_square)
        ax1.add_patch(computer_square)
        
        plt.tight_layout()
        return fig
    
    def update_markers(self, player_marks, computer_marks):
        """Update the markers on the board"""
        self.player_marks = set(player_marks)
        self.computer_marks = set(computer_marks)
    
    def save_board_image(self, filename="game_board.png"):
        """Save the game board as an image file"""
        fig, _ = self.draw_game_board()
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close(fig)
        return filename
        
    def save_selector_image(self, filename="number_selector.png"):
        """Save the selector as an image file"""
        fig, _ = self.draw_selector()
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close(fig)
        return filename

# Simple demo if the file is run directly
if __name__ == "__main__":
    renderer = BoardRenderer()
    
    # Example: Mark some cells
    renderer.update_markers([1, 8, 15], [5, 12, 21])
    
    # Display the game board with the full UI
    fig = renderer.display_full_game_ui(selected_number=3)
    plt.show()
    
    # Save the board and selector as separate images
    board_img = renderer.save_board_image()
    selector_img = renderer.save_selector_image()
    
    print(f"Created game board image: {board_img}")
    print(f"Created selector image: {selector_img}")