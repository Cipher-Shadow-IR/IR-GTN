import tkinter as tk
from PIL import ImageTk, Image
import random

class NGGame:
    def __init__(self, root):
        self.root = root
        self.root.title("IR's Number Guessing Game")

        # Set fullscreen
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.root.geometry(f"{screen_width}x{screen_height}")
        self.root.attributes("-fullscreen", True)

        # Toggle fullscreen with keys
        self.root.bind("<Escape>", lambda e: self.root.attributes("-fullscreen", False))
        self.root.bind("<F11>", lambda e: self.root.attributes("-fullscreen", True))

        # Load initial UI
        self.bground("assets/background/bg1.jpg")
        self.animate_text("IR's Number Guessing Game")
        self.show_start_buttons()
        self.animation_job = None


    def bground(self, img_path=None):
        self.bg_image = Image.open(img_path)

        # Only create canvas once
        if not hasattr(self, "canvas"):
            self.canvas = tk.Canvas(self.root, highlightthickness=0)
            self.canvas.pack(fill="both", expand=True)

        # Create or reset the bg_item
        dummy_img = ImageTk.PhotoImage(Image.new("RGB", (1, 1)))
        if not hasattr(self, "bg_item") or not self.canvas.find_withtag(self.bg_item):
            self.bg_item = self.canvas.create_image(0, 0, anchor="nw", image=dummy_img)
        self.canvas.image = dummy_img  # prevent garbage collection

        # Trigger background resize
        self.root.bind("<Configure>", self.resize_bg)
        self.root.after(100, self.resize_bg)


    def resize_bg(self, event=None):
        w, h = self.root.winfo_width(), self.root.winfo_height()

        # Resize background image
        resized = self.bg_image.resize((w, h), Image.LANCZOS)
        new_bg = ImageTk.PhotoImage(resized)
        self.canvas.itemconfig(self.bg_item, image=new_bg)
        self.canvas.image = new_bg

        # Force canvas resize to match root
        self.canvas.config(width=w, height=h)

        # Reposition all UI elements
        self.position_ui_elements()



    def blink_text(self):
        if hasattr(self, "title_item"):
            current_color = self.canvas.itemcget(self.title_item, "fill")
            new_color = "cyan" if current_color == "black" else "black"
            self.canvas.itemconfig(self.title_item, fill=new_color)
            self.root.after(500, self.blink_text)

    def animate_text(self, text, i=0):
        if i == 0:
            self.title_item = self.canvas.create_text(
                self.root.winfo_width() // 2,
                self.root.winfo_height() // 2 - 150,
                text="",
                fill="cyan",
                font=("Cambria", 30, "bold"),
                tags=("title",)
            )

        if i < len(text):
            self.canvas.itemconfig(self.title_item, text=text[:i + 1])
            self.animation_job = self.root.after(80, self.animate_text, text, i + 1)
            self.blink_text()
        


    def show_start_buttons(self):
        self.start_btn = tk.Button(self.canvas, text="Start", width=10, command=self.launch_game)
        self.exit_btn = tk.Button(self.canvas, text="Exit", width=10, command=self.root.quit)

        # Tag buttons for deletion
        self.start_btn_window = self.canvas.create_window(0, 0, window=self.start_btn, tags="buttons")
        self.exit_btn_window = self.canvas.create_window(0, 0, window=self.exit_btn, tags="buttons")

        self.position_ui_elements()

    def position_ui_elements(self):
        w = self.root.winfo_width()
        h = self.root.winfo_height()

        # Font sizes based on window height
        title_font_size = max(30, h // 30)
        label_font_size = max(30, h // 35)
        entry_font_size = max(18, h // 40)

        # Update title position
        if hasattr(self, 'title_item'):
            self.canvas.coords(self.title_item, w // 2, h // 6)
            self.canvas.itemconfig(self.title_item, font=("Cambria", title_font_size, "bold"))

        # Buttons
        if hasattr(self, 'start_btn_window'):
            self.canvas.coords(self.start_btn_window, w // 2 - w // 10, h // 2 + h // 8)
        if hasattr(self, 'exit_btn_window'):
            self.canvas.coords(self.exit_btn_window, w // 2 + w // 10, h // 2 + h // 8)

        # Labels and entries
        if hasattr(self, 'min_label'):
            self.canvas.coords(self.min_label, w * 0.3, h * 0.3)
            self.canvas.itemconfig(self.min_label, font=("Helvetica", label_font_size, "bold", "italic"))
        if hasattr(self, 'max_label'):
            self.canvas.coords(self.max_label, w * 0.7, h * 0.3)
            self.canvas.itemconfig(self.max_label, font=("Helvetica", label_font_size, "bold", "italic"))
        if hasattr(self, 'min_entry_window'):
            self.canvas.coords(self.min_entry_window, w * 0.3, h * 0.45)
            self.min_entry.config(font=("Helvetica", entry_font_size), width=int(w * 0.01))
        if hasattr(self, 'max_entry_window'):
            self.canvas.coords(self.max_entry_window, w * 0.7, h * 0.45)
            self.max_entry.config(font=("Helvetica", entry_font_size), width=int(w * 0.01))
        if hasattr(self, 'submit_btn_window'):
            self.canvas.coords(self.submit_btn_window, w // 2, h * 0.6)
        if hasattr(self, 'instr_gm'):
            self.canvas.coords(self.instr_gm, w // 2, h * 0.6)

    def launch_game(self):
        self.bg_image = Image.open("assets/background/bg2.jpg")
        self.resize_bg()

        if self.animation_job:
            self.root.after_cancel(self.animation_job)
        self.canvas.delete("title")
        self.canvas.delete("buttons")

        self.show_input_fields()

    def show_input_fields(self):
        self.min_entry = tk.Entry(self.canvas, justify="center", bg="#3868f6", fg="white")
        self.max_entry = tk.Entry(self.canvas, justify="center", bg="#3868f6", fg="white")

        self.min_label = self.canvas.create_text(0, 0, text="Enter Min Number", fill="cyan", anchor="center")
        self.max_label = self.canvas.create_text(0, 0, text="Enter Max Number", fill="cyan", anchor="center")

        self.min_entry_window = self.canvas.create_window(0, 0, window=self.min_entry)
        self.max_entry_window = self.canvas.create_window(0, 0, window=self.max_entry)

        # Submit Button
        self.submit_btn = tk.Button(self.canvas, text="Submit", command=self.read_user_input, bg="#00ffaa", font=("Helvetica", 14, "bold"))
        self.submit_btn_window = self.canvas.create_window(0, 0, window=self.submit_btn)

        self.position_ui_elements()
        self.max_entry.bind("<Return>", self.start_btn)

    def read_user_input(self):
        max_val = self.max_entry.get()
        min_val = self.min_entry.get()
        try:
            min_val = int(min_val)
            max_val = int(max_val)
            if min_val >= max_val:
                print("Error: Min should be less than Max.")
            else:
                self.canvas.delete("all")
                self.bground("assets/background/bg2.jpg")
                # Show final message
                message = f"So\nThe Range is from {min_val} to {max_val}"
                self.instr_gm = self.canvas.create_text(
                    self.root.winfo_width() // 2,
                    self.root.winfo_height() // 2,
                    text=message,
                    fill="cyan",
                    font=("Helvetica", 28, "bold"),
                    anchor="center",
                    justify="center"
                )
                self.root.after(2000, lambda: self.transition_to_gameplay(min_val, max_val))
        except ValueError:
            print("Please enter valid integers.")
    


    
    def transition_to_gameplay(self, min_val, max_val):
        self.canvas.delete("all")
        self.bground("assets/background/bg3.jpg")

        self.target_number = random.randint(min_val, max_val)
        self.guess_count = 0

        # Instruction Text
        self.guess_instr = self.canvas.create_text(
            self.root.winfo_width() // 2,
            self.root.winfo_height() // 3.5,
            text="Enter Your Guess",
            fill="cyan",
            font=("Cambria", 32, "bold italic"),
            anchor="center"
        )

        # Entry Field
        self.guess_entry = tk.Entry(self.canvas, justify="center", bg="#1e1e1e", fg="white", insertbackground="white",
                                    highlightthickness=2, relief="flat")
        self.guess_entry_window = self.canvas.create_window(
            self.root.winfo_width() // 2,
            self.root.winfo_height() // 2.5,
            window=self.guess_entry,
            width=200
        )

        # Guess Button
        self.guess_btn = tk.Button(
            self.canvas, text="Guess", bg="#00ffaa", fg="black", font=("Helvetica", 14, "bold"),
            command=lambda: self.check_guess(min_val, max_val)
        )
        self.guess_btn_window = self.canvas.create_window(
            self.root.winfo_width() // 2,
            self.root.winfo_height() // 2,
            window=self.guess_btn
        )

        # Feedback Text
        self.feedback_text = self.canvas.create_text(
            self.root.winfo_width() // 2,
            self.root.winfo_height() // 1.5,
            text="",
            fill="yellow",
            font=("Helvetica", 24, "bold"),
            anchor="center"
        )

    def check_guess(self, min_val, max_val):
        guess = self.guess_entry.get()
        try:
            guess = int(guess)
            self.guess_count += 1
            diff = abs(guess - self.target_number)

            if guess == self.target_number:
                self.canvas.itemconfig(
                    self.feedback_text,
                    text=f"🎉 Correct in {self.guess_count} guesses!"
                )
            elif diff == 1:
                self.canvas.itemconfig(self.feedback_text, text="🔥 Super close!")
            elif diff <= 2:
                self.canvas.itemconfig(self.feedback_text, text="🌟 Very near!")
            elif guess < self.target_number:
                self.canvas.itemconfig(self.feedback_text, text="Too Low!")
            else:
                self.canvas.itemconfig(self.feedback_text, text="Too High!")
        except ValueError:
            self.canvas.itemconfig(self.feedback_text, text="Enter a valid number.")

if __name__ == "__main__":
    root = tk.Tk()
    app = NGGame(root)
    root.mainloop()
