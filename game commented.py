# Import required libraries
import tkinter as tk  # Main GUI library
from tkinter import ttk  # Themed widgets from tkinter
import random  # For shuffling cards and random choices
from collections import defaultdict  # For organizing data (though not used in current code)

class CustomMessageBox(tk.Toplevel):
    """Custom dialog box class for displaying game messages"""
    def __init__(self, parent, title, message, message_type="info"):
        super().__init__(parent)  # Initialize parent class
        
        # Set up the window properties
        self.title(title)  # Set window title
        self.geometry("400x200")  # Set window size
        self.resizable(False, False)  # Disable window resizing
        
        # Define color scheme for different message types
        colors = {
            "info": "#2196F3",    # Blue for information messages
            "warning": "#FFA726",  # Orange for warnings
            "error": "#EF5350",    # Red for errors
            "success": "#66BB6A"   # Green for success messages
        }
        
        # Apply window styling
        self.configure(bg='white')  # Set background color
        self.color = colors.get(message_type, colors["info"])  # Get color based on message type
        
        # Create and arrange the window elements
        self.create_widgets(message)
        
        # Make window modal (user must interact with it before continuing)
        self.transient(parent)
        self.grab_set()
        
        # Center the window on screen
        self.center_window()

    def create_widgets(self, message):
        """Create and arrange all widgets in the message box"""
        # Create colored header bar
        header = tk.Frame(self, height=30, bg=self.color)
        header.pack(fill='x', pady=(0, 20))
        
        # Create frame for message text
        msg_frame = tk.Frame(self, bg='white')
        msg_frame.pack(expand=True, fill='both', padx=20, pady=(0, 20))
        
        # Create and configure message label
        msg_label = tk.Label(
            msg_frame,
            text=message,
            font=('Arial', 12),
            wraplength=350,  # Wrap text if too long
            bg='white'
        )
        msg_label.pack(expand=True)
        
        # Create frame for buttons
        btn_frame = tk.Frame(self, bg='white')
        btn_frame.pack(fill='x', padx=20, pady=(0, 20))
        
        # Configure button style
        style = ttk.Style()
        style.configure('Custom.TButton', 
                       padding=10, 
                       font=('Arial', 10))
        
        # Create OK button
        ok_btn = ttk.Button(
            btn_frame,
            text="OK",
            style='Custom.TButton',
            command=self.destroy  # Close window when clicked
        )
        ok_btn.pack(side='right')

    def center_window(self):
        """Center the message box on the screen"""
        self.update_idletasks()  # Ensure window size is updated
        
        # Get screen dimensions
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        
        # Calculate position for center of screen
        x = (screen_width - self.winfo_width()) // 2
        y = (screen_height - self.winfo_height()) // 2
        
        # Set window position
        self.geometry(f"+{x}+{y}")

class Card:
    """Class representing a playing card with rank and suit"""
    def __init__(self, rank, suit):
        self.rank = rank  # Card rank (2-10, J, Q, K, A)
        self.suit = suit  # Card suit (Hearts, Diamonds, Clubs, Spades)
        
    def __str__(self):
        """String representation of the card (e.g., '2 of Hearts')"""
        return f"{self.rank} of {self.suit}"
        
    def get_symbol(self):
        """Returns card with unicode symbol (e.g., '2♥')"""
        # Dictionary mapping suits to their unicode symbols
        suit_symbols = {'Hearts': '♥', 'Diamonds': '♦', 'Clubs': '♣', 'Spades': '♠'}
        return f"{self.rank}{suit_symbols[self.suit]}"

class BluffGameGUI:
    """Main game class handling the GUI and game logic"""
    def __init__(self, root):
        self.root = root  # Store the main window reference
        self.root.title("Bluff Card Game")  # Set window title
        self.root.geometry("1024x768")  # Set initial window size
        self.root.configure(bg='#1e4d2b')  # Set dark green background
        
        # Define card properties
        self.ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']  # All possible card ranks
        self.suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']  # All possible card suits
        
        # Initialize game components
        self.setup_game()  # Set up initial game state
        self.create_gui()  # Create the graphical interface
        
        # Wait for window to render before updating display
        self.root.update()
        self.update_display()
        
        # Bind window resize event to update display
        self.root.bind('<Configure>', lambda e: self.update_display())

    def setup_game(self):
        """Initialize the game state and deal cards"""
        # Create and shuffle deck
        self.deck = [Card(rank, suit) for rank in self.ranks for suit in self.suits]
        random.shuffle(self.deck)
        
        # Initialize game variables
        self.player_hand = []  # Player's cards
        self.computer_hand = []  # Computer's cards
        self.pile = []  # Cards played in the current round
        self.current_rank = '2'  # Starting rank
        self.selected_cards = set()  # Currently selected cards in GUI
        
        # Deal cards alternately to player and computer
        while len(self.deck) > 0:
            if len(self.deck) > 0:
                self.player_hand.append(self.deck.pop())
            if len(self.deck) > 0:
                self.computer_hand.append(self.deck.pop())
        
        # Sort player's initial hand by rank and suit
        self.player_hand.sort(key=lambda card: (self.ranks.index(card.rank), self.suits.index(card.suit)))

    def create_gui(self):
        """Create and arrange all graphical user interface elements"""
        # Create top information frame
        self.info_frame = tk.Frame(self.root, bg='#1e4d2b')  # Dark green background
        self.info_frame.pack(fill='x', pady=10, padx=20)
        
        # Create left section of info frame for current rank display
        self.info_left = tk.Frame(self.info_frame, bg='#1e4d2b')
        self.info_left.pack(side='left')
        
        # Create label showing current rank in play
        self.current_rank_label = tk.Label(
            self.info_left,
            text="Current Rank: 2",
            font=('Arial Bold', 16),
            bg='#1e4d2b',
            fg='white'  # White text
        )
        self.current_rank_label.pack()
        
        # Create counter showing number of computer's cards (top right)
        self.computer_counter = tk.Label(
            self.info_frame,
            text="Computer's Cards: 26",
            font=('Arial Bold', 16),
            bg='#1e4d2b',
            fg='white'
        )
        self.computer_counter.pack(side='right')
        
        # Create label for displaying game messages (e.g., "Computer calls bluff!")
        self.message_label = tk.Label(
            self.root,
            text="",
            font=('Arial Bold', 16),
            bg='#1e4d2b',
            fg='#ff4444',  # Red text for visibility
            wraplength=800  # Wrap text if too long
        )
        self.message_label.pack(pady=(0, 20))
        
        # Create main frame for displaying cards
        self.scroll_frame = tk.Frame(self.root, bg='#1e4d2b')
        self.scroll_frame.pack(expand=True, fill='both', padx=20)
        
        # Create canvas for drawing cards
        self.cards_canvas = tk.Canvas(
            self.scroll_frame, 
            bg='#1e4d2b', 
            height=430,  # Fixed height for card display area
            highlightthickness=0  # Remove border
        )
        self.cards_canvas.pack(expand=True, fill='both')
        
        # Configure style for game buttons
        style = ttk.Style()
        style.configure('Game.TButton',
                       padding=10,
                       font=('Arial Bold', 12),
                       background='#8B0000',  # Dark red
                       foreground='white')
        
        # Create separator line between cards and menu bar
        separator = tk.Frame(self.root, height=2, bg='black')
        separator.pack(side='bottom', fill='x')
        
        # Create bottom menu bar with dark red background
        self.menu_bar = tk.Frame(self.root, bg='#8B0000', height=150)
        self.menu_bar.pack(side='bottom', fill='x')
        self.menu_bar.pack_propagate(False)  # Prevent size changes
        
        # Create frame for selected cards counter (left side)
        self.counter_frame = tk.Frame(self.menu_bar, bg='#8B0000')
        self.counter_frame.pack(side='left', padx=30)
        
        # Create label showing number of selected cards
        self.selected_count_label = tk.Label(
            self.counter_frame,
            text="Selected: 0",
            font=('Arial Bold', 16),
            bg='#8B0000',
            fg='white'
        )
        self.selected_count_label.pack()
        
        # Create frame for player's cards counter (right side)
        self.your_cards_frame = tk.Frame(self.menu_bar, bg='#8B0000')
        self.your_cards_frame.pack(side='right', padx=30)
        
        # Create label showing number of player's cards
        self.your_cards_label = tk.Label(
            self.your_cards_frame,
            text="Your Cards: 26",
            font=('Arial Bold', 16),
            bg='#8B0000',
            fg='white'
        )
        self.your_cards_label.pack()
        
        # Create center button frame for main game controls
        self.button_frame = tk.Frame(self.menu_bar, bg='#8B0000')
        self.button_frame.pack(expand=True, fill='both')
        
        # Create container for buttons with fixed height to ensure proper centering
        button_container = tk.Frame(self.button_frame, bg='#8B0000', height=150)
        button_container.pack(expand=True, fill='both')
        button_container.pack_propagate(False)  # Prevent container from shrinking to fit content
        
        # Create inner frame for precise button positioning
        inner_button_frame = tk.Frame(button_container, bg='#8B0000')
        # Place frame exactly in center using relative coordinates (0.5 = middle)
        inner_button_frame.place(relx=0.5, rely=0.5, anchor='center')
        
        # Create main "Play Cards" button with custom styling
        self.play_button = tk.Button(
            inner_button_frame,
            text="Play Cards",
            font=('Arial Bold', 20),  # Large, bold font for visibility
            bg='white',  # White background
            fg='black',  # Black text
            activebackground='#e0e0e0',  # Slightly darker when clicked
            activeforeground='black',    # Text stays black when clicked
            relief='raised',  # 3D effect for button
            borderwidth=3,    # Thick border for better visibility
            padx=50,  # Horizontal padding
            pady=20,  # Vertical padding
            command=self.play_cards  # Method called when button is clicked
        )
        self.play_button.pack(side=tk.LEFT, padx=50)  # Pack to left with spacing
        
        # Create "Call Bluff" button with matching styling
        self.call_bluff_button = tk.Button(
            inner_button_frame,
            text="Call Bluff",
            font=('Arial Bold', 20),
            bg='white',
            fg='black',
            activebackground='#e0e0e0',
            activeforeground='black',
            relief='raised',
            borderwidth=3,
            padx=50,
            pady=20,
            command=self.call_bluff  # Method called to challenge opponent's play
        )
        self.call_bluff_button.pack(side=tk.LEFT, padx=50)
        
        # Add hover effects to both buttons using event bindings
        # Lambda functions are used to pass both the event and button reference
        for button in (self.play_button, self.call_bluff_button):
            # <Enter> event occurs when mouse enters button area
            button.bind('<Enter>', lambda e, b=button: b.configure(bg='#e0e0e0'))
            # <Leave> event occurs when mouse leaves button area
            button.bind('<Leave>', lambda e, b=button: b.configure(bg='white'))
        
        # Bind left mouse click on canvas to card selection handler
        self.cards_canvas.bind('<Button-1>', self.on_card_click)

    def show_message(self, title, message, message_type="info"):
        """Display a temporary game message to the player
        
        Args:
            title (str): Message title (not currently displayed in message label)
            message (str): The message to display
            message_type (str): Type of message - affects styling (not currently used in message label)
        """
        # Update message label with new text
        self.message_label.config(text=message)
        # Force update to ensure message is displayed immediately
        self.root.update()
        # Schedule message removal after 3 seconds (3000 milliseconds)
        self.root.after(3000, lambda: self.message_label.config(text=""))

    def update_display(self):
        """Update the game display and redraw all cards
        
        This method handles:
        1. Updating all counter labels
        2. Calculating card layout based on window size
        3. Drawing cards in a responsive grid layout
        4. Handling card selection highlighting
        5. Adding click detection areas
        
        The cards are drawn in rows, automatically adjusting based on window width.
        Each card shows its rank and suit with appropriate coloring and selection state.
        """
        # Update all counter labels with current game state
        self.your_cards_label.config(text=f"Your Cards: {len(self.player_hand)}")
        self.computer_counter.config(text=f"Computer's Cards: {len(self.computer_hand)}")
        self.current_rank_label.config(text=f"Current Rank: {self.current_rank}")
        
        # Clear the canvas before redrawing
        self.cards_canvas.delete('all')
        
        # Define card dimensions and spacing
        card_width = 80  # Width of each card in pixels
        card_height = 120  # Height of each card in pixels
        spacing = 10  # Horizontal space between cards
        padding = 20  # Padding from canvas edges
        
        # Calculate layout based on window size
        window_width = self.cards_canvas.winfo_width()
        # Determine maximum cards that can fit in one row
        cards_per_row = max(1, (window_width - padding) // (card_width + spacing))
        
        # Calculate number of rows needed
        num_cards = len(self.player_hand)
        num_rows = (num_cards + cards_per_row - 1) // cards_per_row
        
        # Calculate starting position to center cards horizontally
        total_width = min(cards_per_row, num_cards) * (card_width + spacing) - spacing
        x_start = (window_width - total_width) / 2
        
        # Calculate vertical positioning
        row_spacing = card_height + 20  # Vertical space between rows
        total_height = num_rows * row_spacing - 20
        y_start = (430 - total_height) / 2  # Center vertically in canvas
        
        # Draw each card
        for i, card in enumerate(self.player_hand):
            # Calculate card position in grid
            row = i // cards_per_row  # Determine which row
            col = i % cards_per_row   # Determine position in row
            x = x_start + col * (card_width + spacing)  # Calculate x position
            y = y_start + row * row_spacing            # Calculate y position
            
            # Draw card background with selection state
            color = '#e0e0e0' if i in self.selected_cards else 'white'
            self.cards_canvas.create_rectangle(
                x, y,
                x + card_width, y + card_height,
                fill=color, outline='black', width=2
            )
            
            # Add green highlight border for selected cards
            if i in self.selected_cards:
                self.cards_canvas.create_rectangle(
                    x + 2, y + 2,
                    x + card_width - 2, y + card_height - 2,
                    outline='#4CAF50',  # Green highlight color
                    width=3
                )
            
            # Draw card symbol with appropriate color
            text_color = 'red' if card.suit in ['Hearts', 'Diamonds'] else 'black'
            font_size = 20  # Size of card text
            self.cards_canvas.create_text(
                x + card_width/2,  # Center text horizontally
                y + card_height/2, # Center text vertically
                text=card.get_symbol(),
                font=('Arial', font_size),
                fill=text_color
            )
            
            # Create invisible rectangle for click detection
            # Tagged with card index for selection handling
            self.cards_canvas.create_rectangle(
                x, y,
                x + card_width, y + card_height,
                tags=f'card_{i}',
                outline=''  # Invisible outline
            )

    def on_card_click(self, event):
        """Handle mouse clicks on cards in the play area
        
        Args:
            event: The mouse click event containing coordinates
        
        This method handles card selection/deselection when clicked and updates the UI accordingly.
        Cards can be selected multiple times to toggle their selection state.
        """
        # Convert canvas coordinates to scrolled coordinates (in case of future scrolling implementation)
        canvas_x = self.cards_canvas.canvasx(event.x)
        canvas_y = event.y
        
        # Find all canvas objects at the clicked position
        overlapping = self.cards_canvas.find_overlapping(canvas_x, canvas_y, canvas_x, canvas_y)
        
        # Check each overlapping object for card tags
        for item in overlapping:
            tags = self.cards_canvas.gettags(item)
            for tag in tags:
                # Check if the object is a card (has 'card_X' tag)
                if tag.startswith('card_'):
                    # Extract card index from tag
                    card_index = int(tag.split('_')[1])
                    
                    # Toggle card selection
                    if card_index in self.selected_cards:
                        self.selected_cards.remove(card_index)  # Deselect if already selected
                    else:
                        self.selected_cards.add(card_index)  # Select if not selected
                    
                    # Update the selection counter in the UI
                    self.selected_count_label.config(text=f"Selected: {len(self.selected_cards)}")
                    # Redraw the cards to show updated selection state
                    self.update_display()
                    return  # Exit after handling the topmost card

    def play_cards(self):
        """Handle the player's attempt to play cards
        
        This method is called when the player clicks the "Play Cards" button.
        It validates the play, adds cards to the pile, and handles the computer's response.
        
        Game Rules:
        - Players must select at least one card to play
        - Cards played must match the current rank (or player can bluff)
        - Computer may call bluff after cards are played
        """
        # Validate that cards are selected
        if not self.selected_cards:
            self.show_message("Error", "Please select cards to play!")
            return
            
        # Get the selected cards and remove them from player's hand
        cards_to_play = [self.player_hand[i] for i in sorted(self.selected_cards, reverse=True)]
        for card in cards_to_play:
            self.player_hand.remove(card)  # Remove from hand
            self.pile.append(card)  # Add to play pile
        
        # Clear the selection after playing
        self.selected_cards.clear()
        
        # Sort remaining cards for better organization
        self.player_hand.sort(key=lambda card: (self.ranks.index(card.rank), self.suits.index(card.suit)))
        
        # Let computer decide whether to call bluff
        if self.computer_decide_bluff(len(cards_to_play)):
            self.show_message("Bluff Called!", "Computer calls BLUFF!")
            
            # Check if player was actually bluffing
            bluff_called = any(card.rank != self.current_rank for card in cards_to_play)
            
            if bluff_called:
                # Player was caught bluffing
                self.show_message("Caught!", "You were caught bluffing! Taking the pile...")
                self.player_hand.extend(self.pile)  # Player must take all cards
            else:
                # Computer was wrong
                self.show_message("Wrong!", "Computer was wrong! They take the pile...")
                self.computer_hand.extend(self.pile)  # Computer must take all cards
            
            self.pile = []  # Clear the pile
            self.next_rank()  # Advance to next rank only after pile is taken
        
        # Computer takes their turn
        self.computer_turn()
        
        # Update the display to reflect changes
        self.update_display()
        
        # Check if game is over after play
        self.check_game_over()

    def computer_decide_bluff(self, num_cards_claimed):
        """Determine if the computer should call the player's bluff
        
        Args:
            num_cards_claimed (int): Number of cards the player claims to be playing
            
        Returns:
            bool: True if computer decides to call bluff, False otherwise
            
        Strategy:
        1. Calculate how many cards of current rank could exist outside computer's hand
        2. Call bluff if player claims more cards than possible
        3. Increase chance of calling bluff for larger plays
        """
        # Threshold for random bluff calling (70% chance to let it pass)
        probability_threshold = 0.7
        
        # Count how many cards of the current rank computer has
        cards_of_rank = len([card for card in self.computer_hand if card.rank == self.current_rank])
        
        # Calculate maximum possible cards player could have of this rank
        # (4 cards per rank in a deck - cards computer has)
        total_possible = 4 - cards_of_rank
        
        # Always call bluff if player claims more cards than possible
        if num_cards_claimed > total_possible:
            return True
        # Randomly call bluff on larger plays (3+ cards) with 30% chance
        elif num_cards_claimed > 2 and random.random() > probability_threshold:
            return True
        return False

    def computer_turn(self):
        """Handle the computer's turn
        
        Returns:
            bool: True if computer is bluffing, False if playing honestly
            
        Strategy:
        1. Play matching cards if available
        2. Bluff with random cards if no matching cards
        3. Limit bluff plays to 3 cards maximum
        """
        # Find all cards in computer's hand matching current rank
        cards_of_rank = [card for card in self.computer_hand if card.rank == self.current_rank]
        
        if cards_of_rank:
            # If computer has matching cards, play 1 to all of them
            num_to_play = random.randint(1, len(cards_of_rank))
            cards_to_play = cards_of_rank[:num_to_play]
            bluffing = False  # Playing honestly
        else:
            # If no matching cards, bluff with 1-3 random cards
            num_to_play = random.randint(1, min(3, len(self.computer_hand)))
            cards_to_play = random.sample(self.computer_hand, num_to_play)
            bluffing = True  # Playing a bluff
        
        # Remove played cards from hand and add to pile
        for card in cards_to_play:
            self.computer_hand.remove(card)
            self.pile.append(card)
        
        # Notify player of computer's play
        self.show_message(
            "Computer's Turn",
            f"Computer plays {num_to_play} card(s) of rank {self.current_rank}"
        )
        
        # Update display to reflect changes
        self.update_display()
        return bluffing

    def call_bluff(self):
        """Handle player's attempt to call computer's bluff
        
        Game Rules:
        1. Can't call bluff if no cards in pile
        2. Only the most recent play can be challenged
        3. If bluff called correctly, computer takes pile
        4. If bluff called wrongly, player takes pile
        5. Rank advances after pile is taken
        """
        # Validate there are cards to call bluff on
        if len(self.pile) == 0:
            self.show_message("Error", "No cards in the pile to call bluff on!")
            return
        
        # Check the last played card(s)
        last_cards = self.pile[-1]
        # Determine if the computer was bluffing
        if any(card.rank != self.current_rank for card in [last_cards]):
            # Computer was caught bluffing
            self.show_message(
                "Caught!",
                "You caught the computer bluffing! Computer takes the pile..."
            )
            self.computer_hand.extend(self.pile)  # Computer takes all cards
        else:
            # Computer was honest
            self.show_message(
                "Wrong!",
                "Computer was honest! You take the pile..."
            )
            self.player_hand.extend(self.pile)  # Player takes all cards
            
        # Clear the pile and advance to next rank
        self.pile = []
        self.next_rank()  # Advance rank after pile is taken
        
        # Update display and check for game end
        self.update_display()
        self.check_game_over()

    def next_rank(self):
        """Advance to the next rank in the sequence
        
        The rank sequence goes from 2 through 10, then J, Q, K, A.
        After A, it wraps back to 2.
        """
        # Find the index of current rank in the ranks list
        current_index = self.ranks.index(self.current_rank)
        # Calculate next rank using modulo to wrap around to start
        self.current_rank = self.ranks[(current_index + 1) % len(self.ranks)]

    def check_game_over(self):
        """Check if either player has won the game
        
        Win condition: A player wins when they have no cards left in their hand.
        This method creates the appropriate GameOverScreen when a winner is determined.
        """
        if len(self.player_hand) == 0:
            # Player wins if they have no cards
            GameOverScreen(self.root, "Congratulations! You win!")
        elif len(self.computer_hand) == 0:
            # Computer wins if it has no cards
            GameOverScreen(self.root, "Computer wins! Better luck next time!")

class GameOverScreen(tk.Toplevel):
    """A modal window displayed when the game ends
    
    This window shows the game result and provides options to play again or quit.
    It appears centered on top of the main game window.
    """
    def __init__(self, parent, message):
        super().__init__(parent)
        
        # Configure window properties
        self.title("Game Over")  # Window title
        self.geometry("400x300")  # Fixed window size
        self.resizable(False, False)  # Prevent window resizing
        self.configure(bg='#1e4d2b')  # Match main game's green background
        
        # Make window modal (blocks interaction with main window)
        self.transient(parent)
        self.grab_set()
        
        # Create and configure the "GAME OVER" header
        tk.Label(
            self,
            text="GAME OVER",
            font=('Arial Bold', 24),
            bg='#1e4d2b',
            fg='white'  # White text for contrast
        ).pack(pady=20)
        
        # Create and configure the result message
        tk.Label(
            self,
            text=message,
            font=('Arial', 16),
            bg='#1e4d2b',
            fg='white',
            wraplength=350  # Wrap text if too long
        ).pack(pady=20)
        
        # Create "Play Again" button with bright styling
        tk.Button(
            self,
            text="Play Again",
            font=('Arial Bold', 14),
            bg='white',
            fg='black',
            command=self.play_again,  # Method to restart game
            padx=20,
            pady=10
        ).pack(pady=20)
        
        # Create "Quit" button with dark red styling
        tk.Button(
            self,
            text="Quit",
            font=('Arial Bold', 14),
            bg='#8B0000',  # Dark red background
            fg='white',    # White text
            command=self.quit_game,  # Method to exit game
            padx=20,
            pady=10
        ).pack(pady=10)
        
        # Center the window on screen
        self.center_window()
    
    def center_window(self):
        """Center the game over window on the screen"""
        self.update_idletasks()  # Ensure window size is updated
        
        # Get screen dimensions
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        
        # Calculate center position
        x = (screen_width - self.winfo_width()) // 2
        y = (screen_height - self.winfo_height()) // 2
        
        # Set window position
        self.geometry(f"+{x}+{y}")
    
    def play_again(self):
        """Handle the "Play Again" button click
        
        This method:
        1. Quits the current game instance
        2. Creates a new game instance
        3. Closes the game over screen
        """
        self.master.quit()  # Quit current game
        game = BluffGameGUI(self.master)  # Create new game
        self.destroy()  # Close game over screen
    
    def quit_game(self):
        """Handle the "Quit" button click
        
        Exits the game completely by quitting the main window
        """
        self.master.quit()  # Quit the entire game

# Entry point of the program
if __name__ == "__main__":
    root = tk.Tk()  # Create the main window
    game = BluffGameGUI(root)  # Create game instance
    root.mainloop()  # Start the game loop