from PIL import Image, ImageDraw, ImageFont
import os

def create_ico():
    try:
        # Create a new image with a dark background
        size = (256, 256)
        img = Image.new('RGB', size, color='#2c3e50')
        d = ImageDraw.Draw(img)
        
        # Draw a simple "monitor" shape or just text
        # Draw a screen rectangle
        screen_color = '#367C2B' # detailed green
        d.rectangle([40, 40, 216, 180], outline=screen_color, width=10)
        
        # Draw a stand
        d.rectangle([118, 180, 138, 220], fill=screen_color)
        d.rectangle([80, 220, 176, 230], fill=screen_color)
        
        # Draw a "pulse" line on screen
        points = [
            (50, 110), (90, 110), (105, 80), (120, 140), 
            (135, 110), (175, 110), (200, 110)
        ]
        d.line(points, fill='#e74c3c', width=5)

        # Save as ICO
        img.save('app_icon.ico', format='ICO', sizes=[(256, 256)])
        print("Successfully created app_icon.ico programmatically")
    except Exception as e:
        print(f"Error creating icon: {e}")

if __name__ == "__main__":
    create_ico()
