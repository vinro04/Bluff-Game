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
        
        # Wait for window to be rendered before updating display
        self.root.update()
        self.update_display()
        
        # Bind window resize to update display
        self.root.bind('<Configure>', lambda e: self.update_display())

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
        
        # Sort initial hand
        self.player_hand.sort(key=lambda card: (self.ranks.index(card.rank), self.suits.index(card.suit)))

    def create_gui(self):
        # Create frames
        self.info_frame = tk.Frame(self.root, bg='#1e4d2b')
        self.info_frame.pack(fill='x', pady=10, padx=20)
        
        # Create left side of info frame for current rank
        self.info_left = tk.Frame(self.info_frame, bg='#1e4d2b')
        self.info_left.pack(side='left')
        
        # Current rank label
        self.current_rank_label = tk.Label(
            self.info_left,
            text="Current Rank: 2",
            font=('Arial Bold', 16),
            bg='#1e4d2b',
            fg='white'
        )
        self.current_rank_label.pack()
        
        # Computer's cards counter (top right)
        self.computer_counter = tk.Label(
            self.info_frame,
            text="Computer's Cards: 26",
            font=('Arial Bold', 16),
            bg='#1e4d2b',
            fg='white'
        )
        self.computer_counter.pack(side='right')
        
        # Message label for game messages
        self.message_label = tk.Label(
            self.root,
            text="",
            font=('Arial Bold', 16),
            bg='#1e4d2b',
            fg='#ff4444',
            wraplength=800
        )
        self.message_label.pack(pady=(0, 20))
        
        # Rest of the GUI creation
        self.scroll_frame = tk.Frame(self.root, bg='#1e4d2b')
        self.scroll_frame.pack(expand=True, fill='both', padx=20)
        
        self.cards_canvas = tk.Canvas(self.scroll_frame, 
                                    bg='#1e4d2b', 
                                    height=430,
                                    highlightthickness=0)
        self.cards_canvas.pack(expand=True, fill='both')
        
        # Style configuration for game-like buttons
        style = ttk.Style()
        style.configure('Game.TButton',
                       padding=10,
                       font=('Arial Bold', 12),
                       background='#8B0000',
                       foreground='white')
        
        # Black border separator
        separator = tk.Frame(self.root, height=2, bg='black')
        separator.pack(side='bottom', fill='x')
        
        # Create bottom menu bar with dark red background
        self.menu_bar = tk.Frame(self.root, bg='#8B0000', height=150)
        self.menu_bar.pack(side='bottom', fill='x')
        self.menu_bar.pack_propagate(False)
        
        # Selected counter frame on the left
        self.counter_frame = tk.Frame(self.menu_bar, bg='#8B0000')
        self.counter_frame.pack(side='left', padx=30)
        
        # Selected count label
        self.selected_count_label = tk.Label(
            self.counter_frame,
            text="Selected: 0",
            font=('Arial Bold', 16),
            bg='#8B0000',
            fg='white'
        )
        self.selected_count_label.pack()
        
        # Your cards counter frame on the right
        self.your_cards_frame = tk.Frame(self.menu_bar, bg='#8B0000')
        self.your_cards_frame.pack(side='right', padx=30)
        
        # Your cards count label
        self.your_cards_label = tk.Label(
            self.your_cards_frame,
            text="Your Cards: 26",
            font=('Arial Bold', 16),
            bg='#8B0000',
            fg='white'
        )
        self.your_cards_label.pack()
        
        # Center button frame
        self.button_frame = tk.Frame(self.menu_bar, bg='#8B0000')
        self.button_frame.pack(expand=True, fill='both')
        
        # Container for buttons to center them
        button_container = tk.Frame(self.button_frame, bg='#8B0000', height=150)
        button_container.pack(expand=True, fill='both')
        button_container.pack_propagate(False)
        
        # Inner frame to hold buttons
        inner_button_frame = tk.Frame(button_container, bg='#8B0000')
        inner_button_frame.place(relx=0.5, rely=0.5, anchor='center')
        
        # Play button with new styling
        self.play_button = tk.Button(
            inner_button_frame,
            text="Play Cards",
            font=('Arial Bold', 20),
            bg='white',
            fg='black',
            activebackground='#e0e0e0',
            activeforeground='black',
            relief='raised',
            borderwidth=3,
            padx=50,
            pady=20,
            command=self.play_cards
        )
        self.play_button.pack(side=tk.LEFT, padx=50)
        
        # Call bluff button with new styling
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
            command=self.call_bluff
        )
        self.call_bluff_button.pack(side=tk.LEFT, padx=50)
        
        # Bind hover effects for buttons
        for button in (self.play_button, self.call_bluff_button):
            button.bind('<Enter>', lambda e, b=button: b.configure(bg='#e0e0e0'))
            button.bind('<Leave>', lambda e, b=button: b.configure(bg='white'))
        
        # Bind card selection
        self.cards_canvas.bind('<Button-1>', self.on_card_click)

    def show_message(self, title, message, message_type="info"):
        self.message_label.config(text=message)
        self.root.update()
        # Clear message after 3 seconds
        self.root.after(3000, lambda: self.message_label.config(text=""))

    def update_display(self):
        # Update counters
        self.your_cards_label.config(text=f"Your Cards: {len(self.player_hand)}")
        self.computer_counter.config(text=f"Computer's Cards: {len(self.computer_hand)}")
        self.current_rank_label.config(text=f"Current Rank: {self.current_rank}")
        
        self.cards_canvas.delete('all')
        
        # Set fixed card dimensions
        card_width = 80  # Fixed card width
        card_height = 120  # Fixed card height
        spacing = 10  # Space between cards
        padding = 20  # Total horizontal padding
        
        # Calculate cards per row based on window width and fixed card size
        window_width = self.cards_canvas.winfo_width()
        cards_per_row = max(1, (window_width - padding) // (card_width + spacing))
        
        # Calculate number of rows needed
        num_cards = len(self.player_hand)
        num_rows = (num_cards + cards_per_row - 1) // cards_per_row
        
        # Calculate starting position to center the cards
        total_width = min(cards_per_row, num_cards) * (card_width + spacing) - spacing
        x_start = (window_width - total_width) / 2
        
        # Calculate y positions for rows
        row_spacing = card_height + 20
        total_height = num_rows * row_spacing - 20
        y_start = (430 - total_height) / 2  # Center vertically in the 430px canvas
        
        # Draw player's cards
        for i, card in enumerate(self.player_hand):
            row = i // cards_per_row
            col = i % cards_per_row
            x = x_start + col * (card_width + spacing)
            y = y_start + row * row_spacing
            
            # Draw card background
            color = '#e0e0e0' if i in self.selected_cards else 'white'
            self.cards_canvas.create_rectangle(
                x, y,
                x + card_width, y + card_height,
                fill=color, outline='black', width=2
            )
            
            # Add highlight border for selected cards
            if i in self.selected_cards:
                self.cards_canvas.create_rectangle(
                    x + 2, y + 2,
                    x + card_width - 2, y + card_height - 2,
                    outline='#4CAF50',  # Green highlight
                    width=3
                )
            
            # Draw card text
            text_color = 'red' if card.suit in ['Hearts', 'Diamonds'] else 'black'
            font_size = 20  # Fixed font size
            self.cards_canvas.create_text(
                x + card_width/2,
                y + card_height/2,
                text=card.get_symbol(),
                font=('Arial', font_size),
                fill=text_color
            )
            
            # Store card coordinates for click detection
            self.cards_canvas.create_rectangle(
                x, y,
                x + card_width, y + card_height,
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
                    
                    # Update the selected count label
                    self.selected_count_label.config(text=f"Selected: {len(self.selected_cards)}")
                    self.update_display()
                    return

    def play_cards(self):
        if not self.selected_cards:
            self.show_message("Error", "Please select cards to play!")
            return
            
        # Play the selected cards
        cards_to_play = [self.player_hand[i] for i in sorted(self.selected_cards, reverse=True)]
        for card in cards_to_play:
            self.player_hand.remove(card)
            self.pile.append(card)
        
        self.selected_cards.clear()
        
        # Sort remaining cards
        self.player_hand.sort(key=lambda card: (self.ranks.index(card.rank), self.suits.index(card.suit)))
        
        # Computer decides whether to call bluff
        if self.computer_decide_bluff(len(cards_to_play)):
            self.show_message("Bluff Called!", "Computer calls BLUFF!")
            bluff_called = any(card.rank != self.current_rank for card in cards_to_play)
            
            if bluff_called:
                self.show_message("Caught!", "You were caught bluffing! Taking the pile...")
                self.player_hand.extend(self.pile)
            else:
                self.show_message("Wrong!", "Computer was wrong! They take the pile...")
                self.computer_hand.extend(self.pile)
            self.pile = []
            self.next_rank()  # Only advance rank after pile is taken
        
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
            f"Computer plays {num_to_play} card(s) of rank {self.current_rank}"
        )
        # Removed self.next_rank() from here
        self.update_display()
        return bluffing

    def call_bluff(self):
        if len(self.pile) == 0:
            self.show_message("Error", "No cards in the pile to call bluff on!")
            return
            
        last_cards = self.pile[-1]
        if any(card.rank != self.current_rank for card in [last_cards]):
            self.show_message(
                "Caught!",
                "You caught the computer bluffing! Computer takes the pile..."
            )
            self.computer_hand.extend(self.pile)
        else:
            self.show_message(
                "Wrong!",
                "Computer was honest! You take the pile..."
            )
            self.player_hand.extend(self.pile)
        self.pile = []
        self.next_rank()  # Advance rank after pile is taken
        
        self.update_display()
        self.check_game_over()

    def next_rank(self):
        current_index = self.ranks.index(self.current_rank)
        self.current_rank = self.ranks[(current_index + 1) % len(self.ranks)]

    def check_game_over(self):
        if len(self.player_hand) == 0:
            GameOverScreen(self.root, "Congratulations! You win!")
        elif len(self.computer_hand) == 0:
            GameOverScreen(self.root, "Computer wins! Better luck next time!")

class GameOverScreen(tk.Toplevel):
    def __init__(self, parent, message):
        super().__init__(parent)
        
        # Window setup
        self.title("Game Over")
        self.geometry("400x300")
        self.resizable(False, False)
        self.configure(bg='#1e4d2b')
        
        # Make modal
        self.transient(parent)
        self.grab_set()
        
        # Create widgets
        tk.Label(
            self,
            text="GAME OVER",
            font=('Arial Bold', 24),
            bg='#1e4d2b',
            fg='white'
        ).pack(pady=20)
        
        tk.Label(
            self,
            text=message,
            font=('Arial', 16),
            bg='#1e4d2b',
            fg='white',
            wraplength=350
        ).pack(pady=20)
        
        # Play Again button
        tk.Button(
            self,
            text="Play Again",
            font=('Arial Bold', 14),
            bg='white',
            fg='black',
            command=self.play_again,
            padx=20,
            pady=10
        ).pack(pady=20)
        
        # Quit button
        tk.Button(
            self,
            text="Quit",
            font=('Arial Bold', 14),
            bg='#8B0000',
            fg='white',
            command=self.quit_game,
            padx=20,
            pady=10
        ).pack(pady=10)
        
        # Center the window
        self.center_window()
    
    def center_window(self):
        self.update_idletasks()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - self.winfo_width()) // 2
        y = (screen_height - self.winfo_height()) // 2
        self.geometry(f"+{x}+{y}")
    
    def play_again(self):
        # Since master is the root window, we can directly quit
        self.master.quit()
        # Create a new game instance
        game = BluffGameGUI(self.master)
        self.destroy()
    
    def quit_game(self):
        # Since master is the root window, we can directly quit
        self.master.quit()

if __name__ == "__main__":
    root = tk.Tk()
    game = BluffGameGUI(root)
    root.mainloop()
