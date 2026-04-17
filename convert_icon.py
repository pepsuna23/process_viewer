from PIL import Image
import os

def create_ico():
    try:
        if not os.path.exists('system_monitor_icon.png'):
            print("Error: system_monitor_icon.png does not exist.")
            return

        img = Image.open('system_monitor_icon.png')
        img.save('app_icon.ico', format='ICO', sizes=[(256, 256)])
        print("Successfully created app_icon.ico")
    except Exception as e:
        print(f"Error converting image: {e}")

if __name__ == "__main__":
    create_ico()
