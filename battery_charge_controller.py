import tkinter as tk
import psutil
import threading
import time
from pync import Notifier
from pystray import Icon, MenuItem, Menu
from PIL import Image, ImageDraw

class BatteryManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MacBook Battery Manager")
        self.root.geometry("300x200")
        self.battery_threshold = 80
        self.low_battery_warning = 20
        self.tray_icon = None
        self.create_widgets()
        self.create_tray_icon()
        self.monitor_battery()

    def create_widgets(self):
        # Battery Level Slider
        tk.Label(self.root, text="Set Battery Charge Limit (%)").pack(pady=10)

        self.battery_slider = tk.Scale(
            self.root, from_=50, to=100, orient="horizontal", command=self.update_threshold
        )
        self.battery_slider.set(self.battery_threshold)
        self.battery_slider.pack()

        # Current Battery Level Display
        self.battery_level_label = tk.Label(self.root, text="Current Battery Level: --%")
        self.battery_level_label.pack(pady=10)

        # Hide Button
        tk.Button(self.root, text="Minimize to Tray", command=self.hide_window).pack(pady=10)

    def update_threshold(self, val):
        try:
            self.battery_threshold = int(val)
        except ValueError as e:
            print(f"Error updating threshold: {e}")
            tk.messagebox.showerror("Error", "Invalid battery threshold value.")

    def monitor_battery(self):
        def check_battery():
            while True:
                try:
                    battery = psutil.sensors_battery()
                    if battery:
                        percent = battery.percent
                        plugged = battery.power_plugged

                        self.battery_level_label.config(
                            text=f"Current Battery Level: {percent}%"
                        )

                        # Notify when to unplug charger
                        if percent >= self.battery_threshold and plugged:
                            self.notify_stop_charging()

                        # Notify to charge when below 20%
                        if percent <= self.low_battery_warning and not plugged:
                            self.notify_start_charging()

                        # Update tray icon
                        self.update_tray_icon(percent)

                except Exception as e:
                    print(f"Error in battery monitoring: {e}")

                time.sleep(60)  # Check every minute

        battery_thread = threading.Thread(target=check_battery, daemon=True)
        battery_thread.start()

    def notify_start_charging(self):
        try:
            Notifier.notify(
                "Battery level is below 20%. Please charge your MacBook.",
                title="Low Battery Warning"
            )
        except Exception as e:
            print(f"Notification error: {e}")

    def notify_stop_charging(self):
        try:
            Notifier.notify(
                f"Battery level reached {self.battery_threshold}%. Please unplug the charger.",
                title="Stop Charging"
            )
        except Exception as e:
            print(f"Notification error: {e}")

    def create_tray_icon(self):
        try:
            # Create a simple icon for the system tray
            icon_image = Image.new('RGB', (64, 64), (255, 255, 255))
            draw = ImageDraw.Draw(icon_image)
            draw.rectangle([16, 16, 48, 48], fill='black')

            self.tray_icon = Icon("Battery Manager", icon_image, menu=self.create_tray_menu())
            tray_thread = threading.Thread(target=self.tray_icon.run, daemon=True)
            tray_thread.start()
        except Exception as e:
            print(f"Error creating tray icon: {e}")

    def update_tray_icon(self, percent):
        try:
            if self.tray_icon:
                # Create a new icon image with the current battery percentage
                icon_image = Image.new('RGB', (64, 64), (255, 255, 255))
                draw = ImageDraw.Draw(icon_image)
                draw.rectangle([16, 16, 48, 48], fill='black')
                draw.text((22, 22), f"{percent}%", fill='white')

                # Update the icon
                self.tray_icon.icon = icon_image
        except Exception as e:
            print(f"Error updating tray icon: {e}")

    def create_tray_menu(self):
        return Menu(
            MenuItem("Open", self.show_window),
            MenuItem("Exit", self.quit_app)
        )

    def show_window(self, icon, item):
        try:
            self.root.deiconify()
        except Exception as e:
            print(f"Error showing window: {e}")

    def hide_window(self):
        try:
            self.root.withdraw()
        except Exception as e:
            print(f"Error hiding window: {e}")

    def quit_app(self, icon, item):
        try:
            self.root.quit()
            icon.stop()
        except Exception as e:
            print(f"Error quitting application: {e}")

if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = BatteryManagerApp(root)
        root.mainloop()
    except Exception as e:
        print(f"Error initializing application: {e}")