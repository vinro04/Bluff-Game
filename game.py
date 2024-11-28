import tkinter as tk
from tkinter import ttk
import random
from collections import defaultdict

class CustomMessageBox(tk.Toplevel):
    def __init__(self, parent, title, message, message_type="info"):
        super().__init__(parent)
        
        # Window setup
        self.title(title)
        self.geometry("400x200")
        self.resizable(False, False)
        
        # Colors based on message type
        colors = {
            "info": "#2196F3",    # Blue
            "warning": "#FFA726",  # Orange
            "error": "#EF5350",    # Red
            "success": "#66BB6A"   # Green
        }
        
        # Style
        self.configure(bg='white')
        self.color = colors.get(message_type, colors["info"])
        
        # Create widgets
        self.create_widgets(message)
        
        # Make modal
        self.transient(parent)
        self.grab_set()
        
        # Center the window
        self.center_window()

    def create_widgets(self, message):
        # Header
        header = tk.Frame(self, height=30, bg=self.color)
        header.pack(fill='x', pady=(0, 20))
        
        # Message
        msg_frame = tk.Frame(self, bg='white')
        msg_frame.pack(expand=True, fill='both', padx=20, pady=(0, 20))
        
        msg_label = tk.Label(
            msg_frame,
            text=message,
            font=('Arial', 12),
            wraplength=350,
            bg='white'
        )
        msg_label.pack(expand=True)
        
        # Button
        btn_frame = tk.Frame(self, bg='white')
        btn_frame.pack(fill='x', padx=20, pady=(0, 20))
        
        style = ttk.Style()
        style.configure('Custom.TButton', 
                       padding=10, 
                       font=('Arial', 10))
        
        ok_btn = ttk.Button(
            btn_frame,
            text="OK",
            style='Custom.TButton',
            command=self.destroy
        )
        ok_btn.pack(side='right')

    def center_window(self):
        self.update_idletasks()
        
        # Get screen dimensions
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        
        # Calculate position
        x = (screen_width - self.winfo_width()) // 2
        y = (screen_height - self.winfo_height()) // 2
        
        self.geometry(f"+{x}+{y}")

class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
        
    def __str__(self):
        return f"{self.rank} of {self.suit}"
        
    def get_symbol(self):
        suit_symbols = {'Hearts': '♥', 'Diamonds': '♦', 'Clubs': '♣', 'Spades': '♠'}
        return f"{self.rank}{suit_symbols[self.suit]}"

class BluffGameGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Bluff Card Game")
        self.root.geometry("1024x768")
        self.root.configure(bg='#1e4d2b')
        
        self.ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        self.suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        
        self.setup_game()
        self.create_gui()
        self.update_display()

    def setup_game(self):
        # Initialize game state
        self.deck = [Card(rank, suit) for rank in self.ranks for suit in self.suits]
        random.shuffle(self.deck)
        
        self.player_hand = []
        self.computer_hand = []
        self.pile = []
        self.current_rank = '2'
        self.selected_cards = set()
        
        # Deal cards
        while len(self.deck) > 0:
            if len(self.deck) > 0:
                self.player_hand.append(self.deck.pop())
            if len(self.deck) > 0:
                self.computer_hand.append(self.deck.pop())

    def create_gui(self):
        # Create frames
        self.info_frame = tk.Frame(self.root, bg='#1e4d2b')
        self.info_frame.pack(pady=10)
        
        # Create scrollable frame for cards
        self.scroll_frame = tk.Frame(self.root, bg='#1e4d2b')
        self.scroll_frame.pack(expand=True, fill='both', padx=20)
        
        # Add horizontal scrollbar
        self.scrollbar = tk.Scrollbar(self.scroll_frame, orient='horizontal')
        self.scrollbar.pack(side=tk.BOTTOM, fill='x')
        
        # Create canvas with scrollbar
        self.cards_canvas = tk.Canvas(self.scroll_frame, 
                                    bg='#1e4d2b', 
                                    height=500,
                                    highlightthickness=0,
                                    xscrollcommand=self.scrollbar.set)
        self.cards_canvas.pack(expand=True, fill='both')
        
        # Configure scrollbar
        self.scrollbar.config(command=self.cards_canvas.xview)
        
        # Control frame at bottom
        self.control_frame = tk.Frame(self.root, bg='#1e4d2b')
        self.control_frame.pack(pady=10)
        
        # Info labels
        self.status_label = tk.Label(self.info_frame, text="", font=('Arial', 14), bg='#1e4d2b', fg='white')
        self.status_label.pack()
        
        self.current_rank_label = tk.Label(self.info_frame, text="", font=('Arial', 14), bg='#1e4d2b', fg='white')
        self.current_rank_label.pack()
        
        # Control buttons
        style = ttk.Style()
        style.configure('Game.TButton', padding=5, font=('Arial', 12))
        
        self.num_cards_var = tk.StringVar(value="1")
        self.num_cards_spinbox = ttk.Spinbox(
            self.control_frame,
            from_=1,
            to=10,
            width=5,
            textvariable=self.num_cards_var,
            font=('Arial', 12)
        )
        self.num_cards_spinbox.pack(side=tk.LEFT, padx=5)
        
        self.play_button = ttk.Button(
            self.control_frame,
            text="Play Cards",
            style='Game.TButton',
            command=self.play_cards
        )
        self.play_button.pack(side=tk.LEFT, padx=5)
        
        self.call_bluff_button = ttk.Button(
            self.control_frame,
            text="Call Bluff",
            style='Game.TButton',
            command=self.call_bluff
        )
        self.call_bluff_button.pack(side=tk.LEFT, padx=5)
        
        # Sort button
        self.sort_button = ttk.Button(
            self.control_frame,
            text="Sort Cards",
            style='Game.TButton',
            command=self.sort_cards
        )
        self.sort_button.pack(side=tk.LEFT, padx=5)
        
        # Bind card selection
        self.cards_canvas.bind('<Button-1>', self.on_card_click)

    def show_message(self, title, message, message_type="info"):
        dialog = CustomMessageBox(self.root, title, message, message_type)
        self.root.wait_window(dialog)

    def sort_cards(self):
        # Sort by rank (using the order in self.ranks) and then by suit
        self.player_hand.sort(key=lambda card: (self.ranks.index(card.rank), self.suits.index(card.suit)))
        self.selected_cards.clear()
        self.update_display()

    def update_display(self):
        self.cards_canvas.delete('all')
        
        # Update info labels
        self.status_label.config(
            text=f"Your Cards: {len(self.player_hand)} | Computer's Cards: {len(self.computer_hand)} | Pile: {len(self.pile)}"
        )
        self.current_rank_label.config(text=f"Current Rank: {self.current_rank}")
        
        # Draw player's cards
        card_width = 80
        card_height = 120
        x_start = 50
        y_position = 300
        
        # Calculate total width needed
        total_width = x_start + len(self.player_hand) * (card_width + 10) + 50
        
        # Configure canvas scrolling
        self.cards_canvas.config(scrollregion=(0, 0, total_width, 500))
        
        for i, card in enumerate(self.player_hand):
            x = x_start + i * (card_width + 10)
            
            # Draw card background
            color = '#e0e0e0' if i in self.selected_cards else 'white'
            self.cards_canvas.create_rectangle(
                x, y_position,
                x + card_width, y_position + card_height,
                fill=color, outline='black', width=2
            )
            
            # Draw card text
            text_color = 'red' if card.suit in ['Hearts', 'Diamonds'] else 'black'
            self.cards_canvas.create_text(
                x + card_width/2,
                y_position + card_height/2,
                text=card.get_symbol(),
                font=('Arial', 20),
                fill=text_color
            )
            
            # Store card coordinates for click detection
            self.cards_canvas.create_rectangle(
                x, y_position,
                x + card_width, y_position + card_height,
                tags=f'card_{i}',
                outline=''
            )

    def on_card_click(self, event):
        # Convert canvas coordinates to scrolled coordinates
        canvas_x = self.cards_canvas.canvasx(event.x)
        canvas_y = event.y
        
        # Find clicked card
        overlapping = self.cards_canvas.find_overlapping(canvas_x, canvas_y, canvas_x, canvas_y)
        for item in overlapping:
            tags = self.cards_canvas.gettags(item)
            for tag in tags:
                if tag.startswith('card_'):
                    card_index = int(tag.split('_')[1])
                    if card_index in self.selected_cards:
                        self.selected_cards.remove(card_index)
                    else:
                        self.selected_cards.add(card_index)
                    self.update_display()
                    return

    def play_cards(self):
        if not self.selected_cards:
            self.show_message("Error", "Please select cards to play!", "error")
            return
            
        num_cards_claimed = int(self.num_cards_var.get())
        if len(self.selected_cards) != num_cards_claimed:
            self.show_message("Error", "Number of selected cards must match claimed number!", "error")
            return
        
        # Play the selected cards
        cards_to_play = [self.player_hand[i] for i in sorted(self.selected_cards, reverse=True)]
        for card in cards_to_play:
            self.player_hand.remove(card)
            self.pile.append(card)
        
        self.selected_cards.clear()
        
        # Computer decides whether to call bluff
        if self.computer_decide_bluff(num_cards_claimed):
            self.show_message("Bluff Called!", "Computer calls BLUFF!", "warning")
            bluff_called = any(card.rank != self.current_rank for card in cards_to_play)
            
            if bluff_called:
                self.show_message("Caught!", "You were caught bluffing! Taking the pile...", "error")
                self.player_hand.extend(self.pile)
            else:
                self.show_message("Wrong!", "Computer was wrong! They take the pile...", "success")
                self.computer_hand.extend(self.pile)
            self.pile = []
        
        self.computer_turn()
        self.update_display()
        self.check_game_over()

    def computer_decide_bluff(self, num_cards_claimed):
        probability_threshold = 0.7
        cards_of_rank = len([card for card in self.computer_hand if card.rank == self.current_rank])
        total_possible = 4 - cards_of_rank
        
        if num_cards_claimed > total_possible:
            return True
        elif num_cards_claimed > 2 and random.random() > probability_threshold:
            return True
        return False

    def computer_turn(self):
        cards_of_rank = [card for card in self.computer_hand if card.rank == self.current_rank]
        if cards_of_rank:
            num_to_play = random.randint(1, len(cards_of_rank))
            cards_to_play = cards_of_rank[:num_to_play]
            bluffing = False
        else:
            num_to_play = random.randint(1, min(3, len(self.computer_hand)))
            cards_to_play = random.sample(self.computer_hand, num_to_play)
            bluffing = True
        
        for card in cards_to_play:
            self.computer_hand.remove(card)
            self.pile.append(card)
        
        self.show_message(
            "Computer's Turn",
            f"Computer plays {num_to_play} card(s) of rank {self.current_rank}",
            "info"
        )
        self.next_rank()
        self.update_display()
        return bluffing

    def call_bluff(self):
        if len(self.pile) == 0:
            self.show_message("Error", "No cards in the pile to call bluff on!", "error")
            return
            
        last_cards = self.pile[-1]
        if any(card.rank != self.current_rank for card in [last_cards]):
            self.show_message(
                "Caught!",
                "You caught the computer bluffing! Computer takes the pile...",
                "success"
            )
            self.computer_hand.extend(self.pile)
        else:
            self.show_message(
                "Wrong!",
                "Computer was honest! You take the pile...",
                "error"
            )
            self.player_hand.extend(self.pile)
        self.pile = []
        
        self.update_display()
        self.check_game_over()

    def next_rank(self):
        current_index = self.ranks.index(self.current_rank)
        self.current_rank = self.ranks[(current_index + 1) % len(self.ranks)]

    def check_game_over(self):
        if len(self.player_hand) == 0:
            self.show_message("Game Over", "Congratulations! You win!", "success")
            self.root.quit()
        elif len(self.computer_hand) == 0:
            self.show_message("Game Over", "Computer wins! Better luck next time!", "warning")
            self.root.quit()
            
if __name__ == "__main__":
    root = tk.Tk()
    game = BluffGameGUI(root)
    root.mainloop()