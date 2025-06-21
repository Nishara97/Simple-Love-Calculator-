import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime
import random
import math

class CuteHeartAnimation:
    def __init__(self, canvas, x, y, size=8, color="#FF1493"):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.heart_id = None
        self.animation_id = None
        self.velocity_y = random.uniform(-2, -0.5)  # Slower, gentler movement
        self.velocity_x = random.uniform(-0.5, 0.5)  # Less horizontal movement
        self.gravity = 0.05  # Lighter gravity for cuter effect
        self.life = 120  # Longer life for smaller hearts
        self.pulse_factor = 0  # For pulsing effect
        self.pulse_speed = random.uniform(0.1, 0.3)  # Random pulse speed
        
    def draw_cute_heart(self):
        """Draw a smaller, cuter heart shape on canvas"""
        points = []
        # Make heart smaller and rounder for cuteness
        scale_factor = self.size / 20.0
        
        for t in range(0, 360, 8):  # Fewer points for smoother look
            rad = math.radians(t)
            # Modified heart equation for cuter shape
            x = scale_factor * 12 * math.sin(rad) ** 3
            y = -scale_factor * (10 * math.cos(rad) - 4 * math.cos(2*rad) - 1.5 * math.cos(3*rad) - 0.5 * math.cos(4*rad))
            
            # Add slight pulsing effect
            pulse = 1 + 0.1 * math.sin(self.pulse_factor)
            x *= pulse
            y *= pulse
            
            points.extend([self.x + x, self.y + y])
        
        if len(points) >= 4:
            # Create heart with softer outline
            self.heart_id = self.canvas.create_polygon(
                points, 
                fill=self.color, 
                outline="#FFB6C1", 
                width=1,
                smooth=True  # Smooth the edges
            )
    
    def animate(self):
        """Animate the cute heart floating up and fading"""
        if self.life <= 0:
            if self.heart_id:
                self.canvas.delete(self.heart_id)
            return
        
        # Update pulse factor
        self.pulse_factor += self.pulse_speed
        
        # Update position with gentler movement
        self.velocity_y -= self.gravity
        self.x += self.velocity_x
        self.y += self.velocity_y
        
        # Add slight wobble for cuteness
        wobble = 0.5 * math.sin(self.pulse_factor * 2)
        self.x += wobble * 0.1
        
        # Update life and opacity
        self.life -= 1.5  # Slower fade for smaller hearts
        opacity = self.life / 120.0
        
        # Redraw heart with new position and opacity
        if self.heart_id:
            self.canvas.delete(self.heart_id)
        
        # Adjust color based on opacity for cute fade effect
        if opacity > 0:
            self.draw_cute_heart()
            # Make hearts slightly transparent as they fade
            if opacity < 0.7:
                # Create a softer color for fading hearts
                soft_color = self.get_soft_color(opacity)
                self.canvas.itemconfig(self.heart_id, fill=soft_color)
        
        # Continue animation with slower refresh for smoother movement
        self.animation_id = self.canvas.after(60, self.animate)
    
    def get_soft_color(self, opacity):
        """Get a softer color based on opacity"""
        if self.color == "#FF1493":  # Deep pink
            return "#FFB6C1" if opacity < 0.5 else "#FFC0CB"
        elif self.color == "#FF69B4":  # Hot pink
            return "#FFC0CB" if opacity < 0.5 else "#FFE4E1"
        elif self.color == "#FFB6C1":  # Light pink
            return "#FFE4E1" if opacity < 0.5 else "#FFF0F5"
        else:  # Pale pink
            return "#FFF0F5" if opacity < 0.5 else "#FFFAFA"

class CuteCongratulationWindow:
    def __init__(self, parent, score, name1, name2):
        self.window = tk.Toplevel(parent)
        self.window.title("🎉 Congratulations! 🎉")
        self.window.geometry("400x350")  # Smaller window for cuteness
        self.window.configure(bg="#FFE6F2")
        self.window.resizable(False, False)
        
        # Center the window
        self.window.transient(parent)
        self.window.grab_set()
        
        # Create canvas for cute heart animations
        self.canvas = tk.Canvas(
            self.window,
            width=400,
            height=350,
            bg="#FFE6F2",
            highlightthickness=0
        )
        self.canvas.pack(fill="both", expand=True)
        
        # Hearts list
        self.hearts = []
        
        # Main content
        self.setup_cute_content(score, name1, name2)
        
        # Start cute heart animations
        self.animate_cute_hearts()
        
        # Auto-close after 6 seconds (longer for cuteness)
        self.window.after(6000, self.window.destroy)
    
    def setup_cute_content(self, score, name1, name2):
        """Setup the cute congratulation content"""
        # Main title with cute font
        title = self.canvas.create_text(
            200, 60,
            text="🎉 Yay! 🎉",
            font=("Arial", 18, "bold"),
            fill="#FF1493"
        )
        
        # Score display
        score_text = self.canvas.create_text(
            200, 100,
            text=f"Love Score: {score:.1f}%",
            font=("Arial", 16, "bold"),
            fill="#FF69B4"
        )
        
        # Names with cute spacing
        names_text = self.canvas.create_text(
            200, 140,
            text=f"{name1} 💕 {name2}",
            font=("Arial", 14, "bold"),
            fill="#FF1493"
        )
        
        # Cute message
        message = self.canvas.create_text(
            200, 180,
            text="You two are absolutely perfect together! ✨",
            font=("Arial", 11),
            fill="#FF69B4",
            justify="center"
        )
        
        # More cute decorative elements
        self.canvas.create_text(
            200, 220,
            text="🌟 ✨ 💖 ✨ 🌟",
            font=("Arial", 20),
            fill="#FFD700"
        )
        
        # Tiny hearts decoration
        self.canvas.create_text(
            200, 250,
            text="💕 💕 💕",
            font=("Arial", 16),
            fill="#FFB6C1"
        )
        
        # Cute close button
        close_btn = tk.Button(
            self.window,
            text="💕 Thanks! 💕",
            font=("Arial", 11, "bold"),
            bg="#FF1493",
            fg="white",
            relief="raised",
            bd=2,
            command=self.window.destroy,
            cursor="hand2"
        )
        close_btn_window = self.canvas.create_window(200, 300, window=close_btn)
    
    def animate_cute_hearts(self):
        """Create floating cute heart animations"""
        def create_cute_heart():
            if len(self.hearts) < 20:  # More hearts since they're smaller
                x = random.randint(30, 370)  # Adjusted for smaller window
                y = random.randint(320, 340)  # Start from bottom
                size = random.randint(6, 12)  # Smaller sizes for cuteness
                color = random.choice([
                    "#FF1493",  # Deep pink
                    "#FF69B4",  # Hot pink  
                    "#FFB6C1",  # Light pink
                    "#FFC0CB",  # Pale pink
                    "#FFE4E1"   # Misty rose
                ])
                
                heart = CuteHeartAnimation(self.canvas, x, y, size, color)
                heart.draw_cute_heart()
                heart.animate()
                self.hearts.append(heart)
            
            # Schedule next heart with random timing
            self.window.after(random.randint(150, 400), create_cute_heart)
        
        # Start creating cute hearts
        create_cute_heart()

class LoveCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("💕 Love Calculator - Chinese Fortune Method 💕")
        self.root.geometry("600x700")
        self.root.configure(bg="#FFE6F2")
        
        # Chinese love calculation method
        self.chinese_method = """
        Ancient Chinese Love Fortune Method:
        
        This calculator uses the mystical Chinese character counting method,
        where each character in your names is assigned a numerical value
        based on traditional Chinese numerology. The compatibility is
        calculated by analyzing the harmony between your name vibrations
        and the cosmic energy patterns described in ancient Chinese texts.
        
        The method combines:
        • Character stroke counting
        • Yin-Yang balance analysis
        • Five elements compatibility
        • Cosmic energy resonance
        """
        
        self.setup_ui()
        self.load_pairs()
    
    def setup_ui(self):
        # Main frame
        main_frame = tk.Frame(self.root, bg="#FFE6F2")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        title_label = tk.Label(
            main_frame,
            text="💕 Love Calculator 💕",
            font=("Arial", 24, "bold"),
            bg="#FFE6F2",
            fg="#FF1493"
        )
        title_label.pack(pady=10)
        
        # Subtitle
        subtitle_label = tk.Label(
            main_frame,
            text="Discover Your Love Compatibility",
            font=("Arial", 12, "italic"),
            bg="#FFE6F2",
            fg="#FF69B4"
        )
        subtitle_label.pack(pady=5)
        
        # Input frame
        input_frame = tk.Frame(main_frame, bg="#FFE6F2")
        input_frame.pack(pady=20)
        
        # Person 1 name
        tk.Label(
            input_frame,
            text="Your Name:",
            font=("Arial", 12, "bold"),
            bg="#FFE6F2",
            fg="#FF1493"
        ).pack(anchor="w")
        
        self.name1_entry = tk.Entry(
            input_frame,
            font=("Arial", 12),
            width=30,
            relief="solid",
            bd=2
        )
        self.name1_entry.pack(pady=5, fill="x")
        
        # Person 2 name
        tk.Label(
            input_frame,
            text="Partner's Name:",
            font=("Arial", 12, "bold"),
            bg="#FFE6F2",
            fg="#FF1493"
        ).pack(anchor="w", pady=(15, 0))
        
        self.name2_entry = tk.Entry(
            input_frame,
            font=("Arial", 12),
            width=30,
            relief="solid",
            bd=2
        )
        self.name2_entry.pack(pady=5, fill="x")
        
        # Calculate button
        self.calc_button = tk.Button(
            input_frame,
            text="🔮 Calculate Love Compatibility 🔮",
            font=("Arial", 14, "bold"),
            bg="#FF1493",
            fg="white",
            relief="raised",
            bd=3,
            command=self.calculate_love,
            cursor="hand2"
        )
        self.calc_button.pack(pady=20)
        
        # Result frame
        self.result_frame = tk.Frame(main_frame, bg="#FFE6F2")
        self.result_frame.pack(pady=20, fill="x")
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            self.result_frame,
            variable=self.progress_var,
            maximum=100,
            length=400,
            style="TProgressbar"
        )
        self.progress_bar.pack(pady=10)
        
        # Result label
        self.result_label = tk.Label(
            self.result_frame,
            text="",
            font=("Arial", 16, "bold"),
            bg="#FFE6F2",
            fg="#FF1493",
            wraplength=500
        )
        self.result_label.pack(pady=10)
        
        # Compatibility message
        self.compatibility_label = tk.Label(
            self.result_frame,
            text="",
            font=("Arial", 12),
            bg="#FFE6F2",
            fg="#FF69B4",
            wraplength=500
        )
        self.compatibility_label.pack(pady=10)
        
        # Method explanation
        method_frame = tk.Frame(main_frame, bg="#FFF0F5", relief="solid", bd=2)
        method_frame.pack(pady=20, fill="x")
        
        tk.Label(
            method_frame,
            text="📜 Ancient Chinese Love Fortune Method 📜",
            font=("Arial", 12, "bold"),
            bg="#FFF0F5",
            fg="#FF1493"
        ).pack(pady=5)
        
        method_text = tk.Text(
            method_frame,
            height=8,
            font=("Arial", 9),
            bg="#FFF0F5",
            fg="#333333",
            wrap="word",
            relief="flat"
        )
        method_text.pack(padx=10, pady=5, fill="x")
        method_text.insert("1.0", self.chinese_method)
        method_text.config(state="disabled")
        
        # View pairs button
        view_button = tk.Button(
            main_frame,
            text="💾 View Saved Pairs 💾",
            font=("Arial", 10, "bold"),
            bg="#FF69B4",
            fg="white",
            relief="raised",
            bd=2,
            command=self.view_pairs,
            cursor="hand2"
        )
        view_button.pack(pady=10)
    
    def chinese_love_algorithm(self, name1, name2):
        """Chinese-inspired love calculation algorithm"""
        # Convert names to numerical values based on character properties
        def name_to_value(name):
            value = 0
            for char in name.lower():
                if char.isalpha():
                    # Assign values based on character position and properties
                    char_val = ord(char) - ord('a') + 1
                    # Apply Chinese numerology principles
                    if char in 'aeiou':
                        char_val *= 2  # Vowels have stronger energy
                    if char in 'lmnr':
                        char_val *= 1.5  # Liquid consonants
                    value += char_val
            return value
        
        val1 = name_to_value(name1)
        val2 = name_to_value(name2)
        
        # Calculate compatibility using Chinese principles
        # Yin-Yang balance
        yin_yang_balance = abs(val1 - val2) / max(val1, val2)
        
        # Five elements harmony
        element_harmony = (val1 + val2) % 5
        
        # Cosmic resonance
        cosmic_resonance = (val1 * val2) % 100
        
        # Final calculation combining all factors
        base_compatibility = 50 + (cosmic_resonance * 0.3)
        balance_factor = (1 - yin_yang_balance) * 30
        element_factor = (element_harmony + 1) * 4
        
        final_score = min(100, max(0, base_compatibility + balance_factor + element_factor))
        
        # Add some randomness for mystical effect
        mystical_factor = random.uniform(-5, 5)
        final_score += mystical_factor
        
        return min(100, max(0, final_score))
    
    def get_compatibility_message(self, score):
        """Get compatibility message based on score"""
        if score >= 90:
            return "🌟 Soulmates! Your love is written in the stars! 🌟"
        elif score >= 80:
            return "💖 Perfect Match! You two are meant to be together! 💖"
        elif score >= 70:
            return "💕 Great Compatibility! Your love has strong potential! 💕"
        elif score >= 60:
            return "💝 Good Match! With effort, your love can flourish! 💝"
        elif score >= 50:
            return "💭 Moderate Compatibility! Communication is key! 💭"
        elif score >= 40:
            return "🤔 Challenging Match! Love requires patience and understanding! 🤔"
        elif score >= 30:
            return "⚠️ Difficult Compatibility! Consider if this is right for you! ⚠️"
        else:
            return "💔 Low Compatibility! The stars suggest looking elsewhere! 💔"
    
    def calculate_love(self):
        name1 = self.name1_entry.get().strip()
        name2 = self.name2_entry.get().strip()
        
        if not name1 or not name2:
            messagebox.showerror("Error", "Please enter both names!")
            return
        
        # Animate progress bar
        self.progress_var.set(0)
        self.root.update()
        
        # Simulate calculation process
        for i in range(101):
            self.progress_var.set(i)
            self.root.update()
            self.root.after(20)  # 20ms delay for animation
        
        # Calculate love score
        love_score = self.chinese_love_algorithm(name1, name2)
        
        # Display result
        self.result_label.config(text=f"Love Compatibility: {love_score:.1f}%")
        
        compatibility_msg = self.get_compatibility_message(love_score)
        self.compatibility_label.config(text=compatibility_msg)
        
        # Save the pair
        self.save_pair(name1, name2, love_score)
        
        # Show celebration for high scores with cute heart animations
        if love_score >= 80:
            # Create cute animated congratulation window
            CuteCongratulationWindow(self.root, love_score, name1, name2)
        elif love_score >= 70:
            # Show simple congratulation for good scores
            messagebox.showinfo("💕 Great Match! 💕", 
                              f"Wonderful compatibility! Your love score is {love_score:.1f}%!\n"
                              "The ancient Chinese wisdom sees great potential in your relationship!")
    
    def save_pair(self, name1, name2, score):
        """Save the name pair and score to a file"""
        pair_data = {
            "name1": name1,
            "name2": name2,
            "score": score,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        try:
            if os.path.exists("love_pairs.json"):
                with open("love_pairs.json", "r") as f:
                    pairs = json.load(f)
            else:
                pairs = []
            
            pairs.append(pair_data)
            
            with open("love_pairs.json", "w") as f:
                json.dump(pairs, f, indent=2)
                
        except Exception as e:
            print(f"Error saving pair: {e}")
    
    def load_pairs(self):
        """Load existing pairs from file"""
        try:
            if os.path.exists("love_pairs.json"):
                with open("love_pairs.json", "r") as f:
                    self.pairs = json.load(f)
            else:
                self.pairs = []
        except Exception as e:
            print(f"Error loading pairs: {e}")
            self.pairs = []
    
    def view_pairs(self):
        """Display saved pairs in a new window"""
        if not self.pairs:
            messagebox.showinfo("No Pairs", "No love pairs have been calculated yet!")
            return
        
        # Create new window
        pairs_window = tk.Toplevel(self.root)
        pairs_window.title("💕 Saved Love Pairs 💕")
        pairs_window.geometry("500x400")
        pairs_window.configure(bg="#FFE6F2")
        
        # Title
        tk.Label(
            pairs_window,
            text="💕 Your Love History 💕",
            font=("Arial", 16, "bold"),
            bg="#FFE6F2",
            fg="#FF1493"
        ).pack(pady=10)
        
        # Create text widget for pairs
        text_widget = tk.Text(
            pairs_window,
            font=("Arial", 10),
            bg="white",
            fg="#333333",
            wrap="word"
        )
        text_widget.pack(padx=20, pady=10, fill="both", expand=True)
        
        # Add scrollbar
        scrollbar = tk.Scrollbar(pairs_window, command=text_widget.yview)
        scrollbar.pack(side="right", fill="y")
        text_widget.config(yscrollcommand=scrollbar.set)
        
        # Display pairs
        for i, pair in enumerate(reversed(self.pairs), 1):
            text_widget.insert("end", f"{i}. {pair['name1']} 💕 {pair['name2']}\n")
            text_widget.insert("end", f"   Love Score: {pair['score']:.1f}%\n")
            text_widget.insert("end", f"   Date: {pair['timestamp']}\n")
            text_widget.insert("end", "-" * 50 + "\n\n")
        
        text_widget.config(state="disabled")

def main():
    root = tk.Tk()
    app = LoveCalculator(root)
    root.mainloop()

if __name__ == "__main__":
    main() 