"""For our group project, we have created a bluff card game that can be played against a computer.

The Rules of the game are as follows:

Objective: Be the first player to get rid of all your cards by playing correctly or bluffing.

Play Order:
Cards are played in sequential rank order, starting from Twos, then Threes, Fours, and so on, up to Aces.

Starting Turn:
The first player starts by playing Twos (if they have any).
If they don't have any Twos, they can bluff by playing 1 to 4 cards of a different rank and declaring "Two(s)".

Bluffing:
If a player doesn't have the required rank, they can bluff by playing cards of a different rank.

Calling Bluff:
The opponent can call bluff to challenge a suspected bluff before the next turn starts.
If the bluff is true (cards don't match the announced rank), the bluffing player takes all the cards in the pile.
If the bluff is false (cards match the declared rank), the challenger takes all the cards in the pile.

Played Cards:
Cards are not shown until challenged.
If a bluff is called, the cards played by the previous player are revealed.

Next Turn:
Play continues with the next rank in sequence (e.g., after Twos, play moves to Threes).
If a bluff was called, the next rank begins with the player that won the previous round.

Winning the Game:
Be the first player to get rid of all your cards.


How we proceeded to program the game:

We started by looking at popular card games that could be played with only two players like "Go Fish" and "Uno" to understand how they work and how they were coded.
We took inspiration from these codes and used the ideas we learned to write the bluff card game from scratch.
To make the game more fun, we added a graphical user interface (GUI) so it looks better and is more enjoyable to play.
While writing the code, we fixed most problems ourselves by testing and trying different solutions.
If we couldn't solve a problem, we used AI as a last option to help fix bugs or improve the code.
"""



# Import the main tkinter library for creating the graphical user interface (GUI)
import tkinter as tk
# Import themed widgets from tkinter for better-looking buttons
from tkinter import ttk
# Import random module for shuffling cards and making random choices
import random

# Define a custom message box class that inherits from tkinter's Toplevel window
class CustomMessageBox(tk.Toplevel):
    # Initialize the message box with parent window, title, message and type
    def __init__(self, parent, title, message, message_type="info"):
        # Call the parent class's initializer
        super().__init__(parent)
        
        # Set the window title
        self.title(title)
        # Set the window size to 400x200 pixels
        self.geometry("400x200")
        # Disable window resizing in both directions
        self.resizable(False, False)
        
        # Define color scheme for different message types using hex color codes
        colors = {
            "info": "#2196F3",    # Blue color for information messages
            "warning": "#FFA726",  # Orange color for warning messages
            "error": "#EF5350",    # Red color for error messages
            "success": "#66BB6A"   # Green color for success messages
        }
        
        # Set the window background to white
        self.configure(bg="white")
        # Get the color based on message type, default to info color if type not found
        self.color = colors.get(message_type, colors["info"])
        
        # Create and set up all the widgets in the message box
        self.create_widgets(message)
        
        # Make the window modal (blocks interaction with parent window)
        self.transient(parent)
        # Grab all events (force focus on this window)
        self.grab_set()
        
        # Center the window on the screen
        self.center_window()

    def create_widgets(self, message):
        # Create a colored header frame at the top of the message box
        header = tk.Frame(self, height=30, bg=self.color)
        # Pack the header frame to fill horizontally with padding below
        header.pack(fill="x", pady=(0, 20))
        
        # Create a frame to contain the message text with white background
        msg_frame = tk.Frame(self, bg="white")
        # Pack the message frame to expand and fill available space with padding
        msg_frame.pack(expand=True, fill="both", padx=20, pady=(0, 20))
        
        # Create a label to display the message text
        msg_label = tk.Label(
            msg_frame,            # Place label in the message frame
            text=message,         # Set the message text
            font=("Arial", 12),   # Use Arial font, size 12
            wraplength=350,       # Wrap text if it exceeds 350 pixels
            bg="white"           # White background to match frame
        )
        # Pack the message label to expand and center in its frame
        msg_label.pack(expand=True)
        
        # Create a frame for the OK button with white background
        btn_frame = tk.Frame(self, bg="white")
        # Pack the button frame to fill horizontally with padding
        btn_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        # Create a style configuration for the button
        style = ttk.Style()
        # Configure custom button style with padding and font
        style.configure("Custom.TButton", 
                       padding=10,           # Add padding around button text
                       font=("Arial", 10))   # Set button font and size
        
        # Create the OK button with custom style
        ok_btn = ttk.Button(
            btn_frame,              # Place button in button frame
            text="OK",             # Set button text
            style="Custom.TButton", # Apply custom style
            command=self.destroy    # Close window when clicked
        )
        # Pack the button to the right side of its frame
        ok_btn.pack(side="right")

    def center_window(self):
        # Update window's geometry information
        self.update_idletasks()
        
        # Get the screen's width and height
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        
        # Calculate the x and y coordinates for the window to be centered
        x = (screen_width - self.winfo_width()) // 2    # Center horizontally
        y = (screen_height - self.winfo_height()) // 2  # Center vertically
        
        # Set the window position using geometry string
        self.geometry(f"+{x}+{y}")  # + prefix sets position instead of size

class Card:
    # Initialize a new card with a rank (2-A) and suit (Hearts, Diamonds, Clubs, Spades)
    def __init__(self, rank, suit):
        # Store the card's rank (2, 3, 4, 5, 6, 7, 8, 9, 10, J, Q, K, or A)
        self.rank = rank
        # Store the card's suit (Hearts, Diamonds, Clubs, or Spades)
        self.suit = suit
    
    # Define string representation of the card (e.g., "2 of Hearts")
    def __str__(self):
        # Return formatted string with rank and suit
        return f"{self.rank} of {self.suit}"
    
    # Get the card's symbol representation (e.g., "2♥")
    def get_symbol(self):
        # Dictionary mapping suit names to their unicode symbols
        suit_symbols = {
            "Hearts": "♥",    # Red heart symbol
            "Diamonds": "♦",  # Red diamond symbol
            "Clubs": "♣",     # Black club symbol
            "Spades": "♠"     # Black spade symbol
        }
        # Return the card's rank followed by its suit symbol
        return f"{self.rank}{suit_symbols[self.suit]}"

class BluffGameGUI:
    # Initialize the main game window and set up the game
    def __init__(self, root):
        # Store the root window reference
        self.root = root
        # Set the window title
        self.root.title("Bluff Card Game")
        # Set the initial window size
        self.root.geometry("1024x768")
        # Set the background color to dark green
        self.root.configure(bg="#1e4d2b")
        
        # Define all possible card ranks in order from lowest to highest
        self.ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
        # Define all possible card suits (red suits first, then black suits)
        self.suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
        
        # Initialize the game state (deck, hands, etc.)
        self.setup_game()
        # Create and set up the graphical user interface
        self.create_gui()
        
        # Wait for window to be rendered before updating display
        self.root.update()
        # Draw the initial game state
        self.update_display()
        
        # Bind the window resize event to update the display
        self.root.bind("<Configure>", lambda e: self.update_display())

    def setup_game(self):
        # Create a complete deck of 52 cards using list comprehension
        # Creates one Card object for each combination of rank and suit
        self.deck = [Card(rank, suit) for rank in self.ranks for suit in self.suits]
        # Randomly shuffle the deck of cards
        random.shuffle(self.deck)
        
        # Initialize empty lists/sets for game components
        self.player_hand = []      # List to store player's cards
        self.computer_hand = []    # List to store computer's cards
        self.pile = []            # List to store cards played in current round
        self.current_rank = "2"    # Start game with rank of 2
        self.selected_cards = set() # Set to track which cards player has selected
        
        # Deal cards alternately to player and computer until deck is empty
        while len(self.deck) > 0:
            # Deal one card to player if deck isn't empty
            if len(self.deck) > 0:
                self.player_hand.append(self.deck.pop())
            # Deal one card to computer if deck isn't empty
            if len(self.deck) > 0:
                self.computer_hand.append(self.deck.pop())
        
        # Sort player's initial hand by rank first, then by suit
        # Uses lambda function to create sort key from rank and suit indices
        self.player_hand.sort(key=lambda card: (self.ranks.index(card.rank), self.suits.index(card.suit)))

    def create_gui(self):
        # Create main information frame at top of window
        self.info_frame = tk.Frame(self.root, bg="#1e4d2b")  # Dark green background
        # Pack frame to fill horizontally with padding
        self.info_frame.pack(fill='x', pady=10, padx=20)
        
        # Create left section of info frame for current rank display
        self.info_left = tk.Frame(self.info_frame, bg="#1e4d2b")
        # Pack frame to left side
        self.info_left.pack(side="left")
        
        # Create label showing current rank in play
        self.current_rank_label = tk.Label(
            self.info_left,           # Place in left info frame
            text="Current Rank: 2",    # Initial text showing rank 2
            font=("Arial Bold", 16),   # Bold Arial font, size 16
            bg="#1e4d2b",             # Dark green background
            fg="white"                # White text color
        )
        # Pack the rank label
        self.current_rank_label.pack()
        
        # Create counter showing number of computer's cards (top right)
        self.computer_counter = tk.Label(
            self.info_frame,                  # Place in info frame
            text="Computer's Cards: 26",      # Initial text showing 26 cards
            font=("Arial Bold", 16),          # Bold Arial font, size 16
            bg="#1e4d2b",                    # Dark green background
            fg="white"                       # White text color
        )
        # Pack counter to right side
        self.computer_counter.pack(side="right")
        
        # Create message label for displaying game notifications (e.g., "Computer calls bluff!")
        self.message_label = tk.Label(
            self.root,                # Place in main window
            text="",                  # Initially empty
            font=("Arial Bold", 16),  # Bold Arial font, size 16
            bg="#1e4d2b",            # Dark green background to match window
            fg="#ff4444",            # Red text color for visibility
            wraplength=800           # Wrap text if longer than 800 pixels
        )
        # Pack message label with vertical padding
        self.message_label.pack(pady=(0, 20))
        
        # Create frame for scrollable card display area
        self.scroll_frame = tk.Frame(self.root, bg="#1e4d2b")
        # Pack frame to expand and fill available space with horizontal padding
        self.scroll_frame.pack(expand=True, fill="both", padx=20)
        
        # Create canvas for drawing cards
        self.cards_canvas = tk.Canvas(
            self.scroll_frame,        # Place in scroll frame
            bg="#1e4d2b",            # Dark green background
            height=430,              # Fixed height for card display
            highlightthickness=0     # Remove canvas border
        )
        # Pack canvas to expand and fill available space
        self.cards_canvas.pack(expand=True, fill="both")
        
        # Configure style for game buttons
        style = ttk.Style()
        # Set custom button style with dark red theme
        style.configure("Game.TButton",
                       padding=10,                # Add padding around button text
                       font=("Arial Bold", 12),   # Bold Arial font, size 12
                       background="#8B0000",      # Dark red background
                       foreground="white")        # White text
        
        # Create black separator line between cards and menu bar
        separator = tk.Frame(self.root, height=2, bg="black")
        # Pack separator at bottom of window
        separator.pack(side="bottom", fill="x")
        
        # Create bottom menu bar with dark red background
        self.menu_bar = tk.Frame(self.root, bg="#8B0000", height=150)
        # Pack menu bar at bottom with fixed height
        self.menu_bar.pack(side="bottom", fill="x")
        # Prevent menu bar from resizing
        self.menu_bar.pack_propagate(False)
        
        # Create frame for selected cards counter on the left side
        self.counter_frame = tk.Frame(self.menu_bar, bg="#8B0000")  # Dark red background
        # Pack frame to left side with padding
        self.counter_frame.pack(side="left", padx=30)
        
        # Create label to show number of currently selected cards
        self.selected_count_label = tk.Label(
            self.counter_frame,        # Place in counter frame
            text="Selected: 0",        # Initial text showing no cards selected
            font=("Arial Bold", 16),   # Bold Arial font, size 16
            bg="#8B0000",             # Dark red background
            fg="white"                # White text color
        )
        # Pack the selected count label
        self.selected_count_label.pack()
        
        # Create frame for player's cards counter on the right side
        self.your_cards_frame = tk.Frame(self.menu_bar, bg="#8B0000")
        # Pack frame to right side with padding
        self.your_cards_frame.pack(side="right", padx=30)
        
        # Create label to show number of cards in player's hand
        self.your_cards_label = tk.Label(
            self.your_cards_frame,     # Place in cards frame
            text="Your Cards: 26",     # Initial text showing 26 cards
            font=("Arial Bold", 16),   # Bold Arial font, size 16
            bg="#8B0000",             # Dark red background
            fg="white"                # White text color
        )
        # Pack the cards count label
        self.your_cards_label.pack()
        
        # Create center frame for main game buttons
        self.button_frame = tk.Frame(self.menu_bar, bg="#8B0000")
        # Pack frame to expand and fill remaining space
        self.button_frame.pack(expand=True, fill="both")
        
        # Create container to center buttons vertically
        button_container = tk.Frame(self.button_frame, bg="#8B0000", height=150)
        # Pack container to fill space
        button_container.pack(expand=True, fill="both")
        # Prevent container from shrinking to fit content
        button_container.pack_propagate(False)
        
        # Create inner frame for precise button positioning
        inner_button_frame = tk.Frame(button_container, bg="#8B0000")
        # Place frame exactly in center of container
        inner_button_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        # Create main "Play Cards" button with custom styling
        self.play_button = tk.Button(
            inner_button_frame,          # Place in centered inner frame
            text="Play Cards",           # Button text
            font=("Arial Bold", 20),     # Large bold font for visibility
            bg="white",                  # White background
            fg="black",                  # Black text
            activebackground="#e0e0e0",  # Slightly darker when clicked
            activeforeground="black",    # Text stays black when clicked
            relief="raised",             # 3D effect for button
            borderwidth=3,               # Thick border for better visibility
            padx=50,                     # Horizontal internal padding
            pady=20,                     # Vertical internal padding
            command=self.play_cards      # Function to call when clicked
        )
        # Pack play button to the left with spacing
        self.play_button.pack(side=tk.LEFT, padx=50)
        
        # Create "Call Bluff" button with matching styling
        self.call_bluff_button = tk.Button(
            inner_button_frame,          # Place in centered inner frame
            text="Call Bluff",           # Button text
            font=("Arial Bold", 20),     # Large bold font
            bg="white",                  # White background
            fg="black",                  # Black text
            activebackground="#e0e0e0",  # Slightly darker when clicked
            activeforeground="black",    # Text stays black when clicked
            relief="raised",             # 3D effect
            borderwidth=3,               # Thick border
            padx=50,                     # Horizontal padding
            pady=20,                     # Vertical padding
            command=self.call_bluff      # Function to call when clicked
        )
        # Pack bluff button to the left of play button with spacing
        self.call_bluff_button.pack(side=tk.LEFT, padx=50)
        
        # Add hover effects to both game buttons
        for button in (self.play_button, self.call_bluff_button):
            # Bind mouse enter event to change background color
            button.bind("<Enter>", 
                       lambda e, b=button: b.configure(bg="#e0e0e0"))  # Darken when hovered
            # Bind mouse leave event to restore original color
            button.bind("<Leave>", 
                       lambda e, b=button: b.configure(bg="white"))    # Return to white when mouse leaves
        
        # Bind left mouse click on canvas to handle card selection
        self.cards_canvas.bind("<Button-1>", self.on_card_click)

    def show_message(self, title, message, message_type="info"):
        """Display a temporary message in the game interface
        
        message: The message to display
        """
        # Update the message label with new text
        self.message_label.config(text=message)
        # Force update to show message immediately
        self.root.update()
        # Schedule message removal after 3 seconds (3000 milliseconds)
        self.root.after(3000, lambda: self.message_label.config(text=""))

    def update_display(self):
        # Update all counter labels with current game state
        self.your_cards_label.config(text=f"Your Cards: {len(self.player_hand)}")
        self.computer_counter.config(text=f"Computer's Cards: {len(self.computer_hand)}")
        self.current_rank_label.config(text=f"Current Rank: {self.current_rank}")
        
        # Clear the entire canvas before redrawing
        self.cards_canvas.delete("all")
        
        # Define fixed dimensions for card display
        card_width = 80    # Width of each card in pixels
        card_height = 120  # Height of each card in pixels
        spacing = 10      # Horizontal space between cards
        padding = 20      # Padding from canvas edges
        
        # Calculate how many cards can fit in one row based on window width
        window_width = self.cards_canvas.winfo_width()
        # Ensure at least 1 card per row, otherwise calculate maximum that fit
        cards_per_row = max(1, (window_width - padding) // (card_width + spacing))
        
        # Calculate how many rows are needed to display all cards
        num_cards = len(self.player_hand)
        # Use integer division and round up to get number of rows
        num_rows = (num_cards + cards_per_row - 1) // cards_per_row
        
        # Calculate starting x position to center cards horizontally
        # Use minimum of cards_per_row and actual number of cards to handle last row
        total_width = min(cards_per_row, num_cards) * (card_width + spacing) - spacing
        x_start = (window_width - total_width) / 2
        
        # Calculate vertical spacing and positioning
        row_spacing = card_height + 20  # Vertical space between rows
        total_height = num_rows * row_spacing - 20  # Total height needed
        # Center cards vertically in the 430px high canvas
        y_start = (430 - total_height) / 2
        
        # Draw each card in the player's hand
        for i, card in enumerate(self.player_hand):
            # Calculate row and column position for this card
            row = i // cards_per_row  # Integer division for row number
            col = i % cards_per_row   # Remainder for column position
            
            # Calculate pixel coordinates for card placement
            x = x_start + col * (card_width + spacing)  # X position in grid
            y = y_start + row * row_spacing            # Y position in grid
            
            # Draw card background rectangle
            # Use grey for selected cards, white for unselected
            color = "#e0e0e0" if i in self.selected_cards else "white"
            self.cards_canvas.create_rectangle(
                x, y,                          # Top-left corner
                x + card_width, y + card_height, # Bottom-right corner
                fill=color,                     # Background color
                outline="black",                # Border color
                width=2                         # Border width
            )
            
            # Add highlight border for selected cards
            if i in self.selected_cards:
                self.cards_canvas.create_rectangle(
                    x + 2, y + 2,                    # Top-left corner (inset by 2 pixels)
                    x + card_width - 2, y + card_height - 2,  # Bottom-right corner (inset by 2 pixels)
                    outline="#4CAF50",               # Green highlight color
                    width=3                          # Thick highlight border
                )
            
            # Draw card symbol (e.g., "2♥") on the card
            text_color = "red" if card.suit in ["Hearts", "Diamonds"] else "black"  # Red for hearts/diamonds
            font_size = 20  # Fixed font size for card symbols
            self.cards_canvas.create_text(
                x + card_width/2,                    # Center horizontally in card
                y + card_height/2,                   # Center vertically in card
                text=card.get_symbol(),              # Get card's symbol representation
                font=("Arial", font_size),           # Arial font with fixed size
                fill=text_color                      # Red or black based on suit
            )
            
            # Create invisible rectangle for click detection
            self.cards_canvas.create_rectangle(
                x, y,                               # Top-left corner
                x + card_width, y + card_height,    # Bottom-right corner
                tags=f"card_{i}",                   # Tag with card index for identification
                outline=""                          # Invisible outline
            )

    def on_card_click(self, event):
        """Handle mouse clicks on cards in the play area
        
        event: The mouse click event containing x,y coordinates
        """
        # Convert canvas coordinates to scrolled coordinates (for future scrolling implementation)
        canvas_x = self.cards_canvas.canvasx(event.x)
        canvas_y = event.y
        
        # Find all canvas objects at the clicked position
        overlapping = self.cards_canvas.find_overlapping(canvas_x, canvas_y, canvas_x, canvas_y)
        
        # Check each overlapping object for card tags
        for item in overlapping:
            tags = self.cards_canvas.gettags(item)
            for tag in tags:
                # Check if the object is a card (has 'card_X' tag)
                if tag.startswith("card_"):
                    # Extract card index from tag
                    card_index = int(tag.split("_")[1])
                    
                    # Toggle card selection
                    if card_index in self.selected_cards:
                        self.selected_cards.remove(card_index)  # Deselect if already selected
                    else:
                        self.selected_cards.add(card_index)     # Select if not selected
                    
                    # Update the selected count label
                    self.selected_count_label.config(text=f"Selected: {len(self.selected_cards)}")
                    # Redraw the cards to show updated selection state
                    self.update_display()
                    return  # Exit after handling the topmost card

    def play_cards(self):
        """Handle player's attempt to play cards
        
        Validates the play, adds cards to the pile, and handles computer's response.
        Cards are removed from player's hand and added to the play pile.
        Computer may call bluff after cards are played.
        """
        # Check if any cards are selected to play
        if not self.selected_cards:
            self.show_message("Error", "Please select cards to play!")
            return
            
        # Get the selected cards and remove them from player's hand
        # Sort in reverse order to avoid index issues when removing multiple cards
        cards_to_play = [self.player_hand[i] for i in sorted(self.selected_cards, reverse=True)]
        for card in cards_to_play:
            self.player_hand.remove(card)  # Remove card from player's hand
            self.pile.append(card)         # Add card to the play pile
        
        # Clear the selection after playing cards
        self.selected_cards.clear()
        
        # Sort remaining cards in player's hand by rank and suit
        self.player_hand.sort(key=lambda card: (self.ranks.index(card.rank), self.suits.index(card.suit)))
        
        # Let computer decide whether to call bluff
        if self.computer_decide_bluff(len(cards_to_play)):
            # Computer decides to call bluff
            self.show_message("Bluff Called!", "Computer calls BLUFF!")
            # Check if any played cards don't match the current rank
            bluff_called = any(card.rank != self.current_rank for card in cards_to_play)
            
            if bluff_called:
                # Player was caught bluffing - must take all cards
                self.show_message("Caught!", "You were caught bluffing! Taking the pile...")
                self.player_hand.extend(self.pile)
            else:
                # Computer was wrong - must take all cards
                self.show_message("Wrong!", "Computer was wrong! They take the pile...")
                self.computer_hand.extend(self.pile)
            # Clear the pile after cards are taken
            self.pile = []
            # Advance to next rank only after pile is taken
            self.next_rank()
        
        # Computer takes their turn
        self.computer_turn()
        # Update the display to reflect all changes
        self.update_display()
        # Check if game is over after play
        self.check_game_over()

    def computer_decide_bluff(self, num_cards_claimed):
        """Determine if computer should call player's bluff
        
        num_cards_claimed: Number of cards player claims to be playing
            
        Returns boolean:
        True if computer decides to call bluff, False otherwise
        """
        # Threshold for random bluff calling (70% chance to let it pass)
        probability_threshold = 0.7
        
        # Count how many cards of current rank computer has
        cards_of_rank = len([card for card in self.computer_hand if card.rank == self.current_rank])
        
        # Calculate maximum possible cards player could have of this rank
        # (4 cards per rank in deck - cards computer has)
        total_possible = 4 - cards_of_rank
        
        # Always call bluff if player claims more cards than possible
        if num_cards_claimed > total_possible:
            return True
        # Randomly call bluff on larger plays (3+ cards) with 30% chance
        elif num_cards_claimed > 2 and random.random() > probability_threshold:
            return True
        # Otherwise, accept the play
        return False

    def computer_turn(self):
        """Handle the computer's turn in the game
        
        Computer will either:
        1. Play matching cards if it has them
        2. Bluff with random cards if it has no matching cards
        
        Returns boolean:
        True if computer is bluffing, False if playing honestly
        """
        # Find all cards in computer's hand that match the current rank
        cards_of_rank = [card for card in self.computer_hand if card.rank == self.current_rank]
        
        if cards_of_rank:
            # If computer has matching cards, randomly choose how many to play
            num_to_play = random.randint(1, len(cards_of_rank))
            # Take the first n cards from matching cards
            cards_to_play = cards_of_rank[:num_to_play]
            bluffing = False  # Not bluffing since playing matching cards
        else:
            # If no matching cards, bluff with 1-3 random cards
            num_to_play = random.randint(1, min(3, len(self.computer_hand)))
            # Randomly select cards to bluff with
            cards_to_play = random.sample(self.computer_hand, num_to_play)
            bluffing = True   # Playing non-matching cards, so bluffing
        
        # Remove played cards from computer's hand and add to pile
        for card in cards_to_play:
            self.computer_hand.remove(card)  # Remove from hand
            self.pile.append(card)          # Add to play pile
        
        # Show message about computer's play
        self.show_message(
            "Computer's Turn",
            f"Computer plays {num_to_play} card(s) of rank {self.current_rank}"
        )
        
        # Update display to show new game state
        self.update_display()
        # Return whether computer was bluffing
        return bluffing

    def call_bluff(self):
        """Handle player's attempt to call computer's bluff
        
        Checks if the computer's last play was honest:
        - If computer was bluffing, computer takes the pile
        - If computer was honest, player takes the pile
        """
        # Validate there are cards to call bluff on
        if len(self.pile) == 0:
            self.show_message("Error", "No cards in the pile to call bluff on!")
            return
            
        # Get the last card(s) played
        last_cards = self.pile[-1]
        # Check if any of the last played cards don't match current rank
        if any(card.rank != self.current_rank for card in [last_cards]):
            # Computer was caught bluffing
            self.show_message(
                "Caught!",
                "You caught the computer bluffing! Computer takes the pile..."
            )
            # Computer must take all cards in the pile
            self.computer_hand.extend(self.pile)
        else:
            # Computer was playing honestly
            self.show_message(
                "Wrong!",
                "Computer was honest! You take the pile..."
            )
            # Player must take all cards in the pile
            self.player_hand.extend(self.pile)
            
        # Clear the pile after cards are taken
        self.pile = []
        # Advance to next rank after pile is taken
        self.next_rank()
        
        # Update display to show new game state
        self.update_display()
        # Check if game is over after play
        self.check_game_over()

    def next_rank(self):
        """Advance to the next rank in the sequence
        
        Moves to the next rank in order (2->3->4->...->K->A->2)
        Uses modulo to wrap around to beginning when reaching the end
        """
        # Find the current rank's position in the ranks list
        current_index = self.ranks.index(self.current_rank)
        # Set current_rank to next rank, wrapping around to start if at end
        self.current_rank = self.ranks[(current_index + 1) % len(self.ranks)]

    def check_game_over(self):
        """Check if either player has won the game
        
        Win condition: A player wins when they have no cards left
        Creates appropriate GameOverScreen when game ends
        """
        # Player wins if they have no cards
        if len(self.player_hand) == 0:
            GameOverScreen(self.root, "Congratulations! You win!")
        # Computer wins if it has no cards
        elif len(self.computer_hand) == 0:
            GameOverScreen(self.root, "Computer wins! Better luck next time!")

class GameOverScreen(tk.Toplevel):
    """Modal window displayed when game ends
    
    Shows game result and provides options to:
    1. Play again (starts new game)
    2. Quit (closes application)
    """
    def __init__(self, parent, message):
        # Initialize parent class (Toplevel window)
        super().__init__(parent)
        
        # Configure window properties
        self.title("Game Over")           # Set window title
        self.geometry("400x300")          # Set window size
        self.resizable(False, False)      # Prevent window resizing
        self.configure(bg="#1e4d2b")      # Set dark green background
        
        # Make window modal (blocks interaction with main window)
        self.transient(parent)
        self.grab_set()
        
        # Create "GAME OVER" header label
        tk.Label(
            self,                         # Place in this window
            text="GAME OVER",             # Header text
            font=("Arial Bold", 24),      # Large bold font
            bg="#1e4d2b",                # Match window background
            fg="white"                    # White text color
        ).pack(pady=20)
        
        # Create result message label
        tk.Label(
            self,
            text=message,                 # Win/lose message
            font=("Arial", 16),           # Medium size font
            bg="#1e4d2b",                # Match window background
            fg="white",                   # White text color
            wraplength=350               # Wrap text if too long
        ).pack(pady=20)
        
        # Create "Play Again" button
        tk.Button(
            self,
            text="Play Again",            # Button text
            font=("Arial Bold", 14),      # Bold font
            bg="white",                   # White background
            fg="black",                   # Black text
            command=self.play_again,      # Method to call when clicked
            padx=20,                      # Horizontal padding
            pady=10                       # Vertical padding
        ).pack(pady=20)
        
        # Create "Quit" button
        tk.Button(
            self,
            text="Quit",                  # Button text
            font=("Arial Bold", 14),      # Bold font
            bg="#8B0000",                # Dark red background
            fg="white",                   # White text
            command=self.quit_game,       # Method to call when clicked
            padx=20,                      # Horizontal padding
            pady=10                       # Vertical padding
        ).pack(pady=10)
        
        # Center window on screen
        self.center_window()
    
    def center_window(self):
        """Center the game over window on the screen
        
        Calculates the position to place window in center of screen
        based on screen dimensions and window size
        """
        # Update window's geometry information before calculating position
        self.update_idletasks()
        
        # Get the screen dimensions
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        
        # Calculate center position
        x = (screen_width - self.winfo_width()) // 2   # Center horizontally
        y = (screen_height - self.winfo_height()) // 2  # Center vertically
        
        # Set window position using geometry string
        self.geometry(f"+{x}+{y}")  # + prefix sets position instead of size
    
    def play_again(self):
        """Handle the Play Again button click
        
        Closes current game and starts a new game instance:
        1. Quits current game
        2. Creates new game instance
        3. Closes game over screen
        """
        # Quit the current game instance
        self.master.quit()
        # Create a new game instance with same root window
        game = BluffGameGUI(self.master)
        # Close the game over screen
        self.destroy()
    
    def quit_game(self):
        """Handle the Quit button click
        
        Exits the game completely by closing the main window
        """
        # Quit the entire application
        self.master.quit()

# Program entry point
if __name__ == "__main__":
    # Create the main application window
    root = tk.Tk()
    # Create the game instance
    game = BluffGameGUI(root)
    # Start the main event loop
    # This blocks until the window is closed
    root.mainloop()