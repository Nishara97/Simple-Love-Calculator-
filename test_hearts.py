import tkinter as tk
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

class HeartTestWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("💕 Cute Heart Animation Test 💕")
        self.root.geometry("400x350")
        self.root.configure(bg="#FFE6F2")
        
        # Create canvas
        self.canvas = tk.Canvas(
            self.root,
            width=400,
            height=350,
            bg="#FFE6F2",
            highlightthickness=0
        )
        self.canvas.pack(fill="both", expand=True)
        
        # Hearts list
        self.hearts = []
        
        # Title
        self.canvas.create_text(
            200, 50,
            text="💕 Cute Heart Animation 💕",
            font=("Arial", 16, "bold"),
            fill="#FF1493"
        )
        
        # Instructions
        self.canvas.create_text(
            200, 80,
            text="Watch the cute hearts float up!",
            font=("Arial", 12),
            fill="#FF69B4"
        )
        
        # Start heart animations
        self.animate_hearts()
        
        # Close button
        close_btn = tk.Button(
            self.root,
            text="💕 Close 💕",
            font=("Arial", 12, "bold"),
            bg="#FF1493",
            fg="white",
            relief="raised",
            bd=2,
            command=self.root.destroy,
            cursor="hand2"
        )
        close_btn_window = self.canvas.create_window(200, 320, window=close_btn)
    
    def animate_hearts(self):
        """Create floating cute heart animations"""
        def create_heart():
            if len(self.hearts) < 15:  # Limit number of hearts
                x = random.randint(30, 370)
                y = random.randint(320, 340)
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
            
            # Schedule next heart
            self.root.after(random.randint(200, 500), create_heart)
        
        # Start creating hearts
        create_heart()

def main():
    app = HeartTestWindow()
    app.root.mainloop()

if __name__ == "__main__":
    main() 