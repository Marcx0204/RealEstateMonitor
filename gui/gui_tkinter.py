import tkinter as tk
from tkinter import ttk

class GUIApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Einfache GUI")

        # Configure main window size
        screen_width = root.winfo_screenwidth() * 0.9
        screen_height = root.winfo_screenheight() * 0.9
        root.geometry(f"{int(screen_width)}x{int(screen_height)}")

        # Metabar
        metabar_height = int(screen_height * 0.08)
        metabar_frame = tk.Frame(root, height=metabar_height, bg="#333333")  # Dark gray background
        metabar_frame.pack(fill="x")

        # Add logo to the left corner of the metabar with dynamic width
        logo_image = tk.PhotoImage(file="REMonitor_Logo.png").subsample(3,
                                                                           3)  # Replace with the path to your logo image
        logo_label = tk.Label(metabar_frame, image=logo_image, bg="#2c3e50")  # Darker color
        logo_label.image = logo_image
        logo_label.pack(side="left", padx=10, pady=10, anchor="w")

        # Navigationsbereich
        navigation_width = int(screen_width * 0.25)
        navigation_frame = tk.Frame(root, width=navigation_width, bg="#222222", bd=2, relief=tk.RAISED)  # Dark background with border
        navigation_frame.pack(side="left", fill="y")

        # Filterbereich
        self.filter_width = int(screen_width * 0.2)
        filter_height = main_height = screen_height - metabar_height
        self.filter_frame = tk.Frame(root, width=self.filter_width, height=filter_height, bg="#ffffff", bd=2, relief=tk.RAISED)  # White background with border
        self.filter_frame.pack(side="left", fill="both", padx=25, pady=25)

        # Diagrammbereich
        chart_width = screen_width - navigation_width - self.filter_width - 50  # Adjust this value to make it wider
        chart_height = main_height - 100
        self.chart_frame = tk.Frame(root, bg="#ffffff", width=chart_width, height=chart_height, bd=2, relief=tk.RAISED)  # White background with border
        self.chart_frame.pack(side="left", fill="both", padx=25, pady=50)

        # Create buttons for Stadtplan, Preisvergleich, and Regionsanalyse
        stadtplan_button = ttk.Button(navigation_frame, text="Stadtplan", command=lambda: self.show_chart("Stadtplan"),
                                      style="TButton")  # Added style
        stadtplan_button.pack(pady=10)

        preisvergleich_button = ttk.Button(navigation_frame, text="Preisvergleich",
                                           command=lambda: self.show_chart("Preisvergleich"),
                                           style="TButton")  # Added style
        preisvergleich_button.pack(pady=10)

        regionsanalyse_button = ttk.Button(navigation_frame, text="Regionsanalyse",
                                           command=lambda: self.show_chart("Regionsanalyse"),
                                           style="TButton")  # Added style
        regionsanalyse_button.pack(pady=10)

        # Create dropdowns for each view
        self.create_dropdowns()

        # Style configuration for buttons and combobox
        style = ttk.Style()
        style.configure("TButton", background="#3498db", font=("Helvetica", 12), borderwidth=5,
                        relief='raised', padding=10, width=15)  # Blue button with white text, larger, and rounded
        style.configure("TCombobox", background="#ecf0f1", fieldbackground="#ecf0f1",
                        font=("Helvetica", 12))  # Light gray combobox

    def create_dropdowns(self):
        # Define a custom font for the dropdowns
        dropdown_font = ("Helvetica", 12)

        # DropDown-Menüs für "Bezirk" hinzufügen
        self.bezirk_dropdown = ttk.Combobox(self.filter_frame, values=['1. Bezirk', '2. Bezirk', '3. Bezirk'],
                                            style="TCombobox", font=dropdown_font)
        self.bezirk_dropdown.set('Bezirk auswählen')  # Set the initial value
        self.bezirk_dropdown.grid(row=0, pady=(10, 0), padx=10, sticky="w")  # Adjusted padding

        # DropDown-Menüs für "Preis" hinzufügen
        self.preis_dropdown = ttk.Combobox(self.filter_frame, values=['absolut', 'relativ'], style="TCombobox",
                                           font=dropdown_font)
        self.preis_dropdown.set('Preis auswählen')  # Set the initial value
        self.preis_dropdown.grid(row=1, pady=10, padx=10, sticky="w")

        # DropDown-Menüs für "Filter" hinzufügen
        self.filter_dropdown = ttk.Combobox(self.filter_frame,
                                            values=['Ein-, Zweifamilienhaus', 'Betriebsobjekt', 'Kleingarten'],
                                            style="TCombobox", font=dropdown_font)
        self.filter_dropdown.set('Filter auswählen')  # Set the initial value
        self.filter_dropdown.grid(row=2, pady=10, padx=10, sticky="w")

    def show_chart(self, view):
        # Clear existing content in chart_frame
        for widget in self.chart_frame.winfo_children():
            widget.destroy()

        # Update chart_frame content based on the selected view
        if view == "Stadtplan":
            tk.Label(self.chart_frame, text="Stadtplan Content", font=("Helvetica", 16)).pack(pady=20)
            self.update_dropdown_text('Filter auswählen')  # Reset the dropdown text for other views

        elif view == "Preisvergleich":
            tk.Label(self.chart_frame, text="Preisvergleich Content", font=("Helvetica", 16)).pack(pady=20)
            self.update_dropdown_text('Zuordnung auswählen')  # Change the dropdown text for Preisvergleich

        elif view == "Regionsanalyse":
            tk.Label(self.chart_frame, text="Regionsanalyse Content", font=("Helvetica", 16)).pack(pady=20)
            self.update_dropdown_text('Filter auswählen')  # Reset the dropdown text for other views

    def update_dropdown_text(self, text):
        # Update the text of the filter_dropdown
        self.filter_dropdown['values'] = ['Ein-, Zweifamilienhaus', 'Betriebsobjekt', 'Kleingarten']
        self.filter_dropdown.set(text)  # Set the initial value

    def draw_line_chart(self):
        # Your implementation for drawing line chart
        pass

    def draw_bar_chart(self):
        # Your implementation for drawing bar chart
        pass

if __name__ == "__main__":
    root = tk.Tk()
    app = GUIApp(root)
    root.mainloop()
