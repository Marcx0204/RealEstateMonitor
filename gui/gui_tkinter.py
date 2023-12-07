import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkintermapview

class GUIApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Einfache GUI")

        # Configure main window size
        screen_width = root.winfo_screenwidth() * 0.9
        screen_height = root.winfo_screenheight() * 0.9
        root.geometry("1300x850")

        # Metabar
        metabar_height = int(screen_height * 0.08)
        metabar_frame = tk.Frame(root, height=metabar_height, bg="#333333")  # Dark gray background
        metabar_frame.grid(row=0, column=0, columnspan=3, sticky="ew")

        # Add logo to the left corner of the metabar with dynamic width
        logo_image = tk.PhotoImage(file="REMonitor_Logo.png").subsample(3,
                                                                           3)  # Replace with the path to your logo image
        logo_label = tk.Label(metabar_frame, image=logo_image, bg="#2c3e50")  # Darker color
        logo_label.image = logo_image
        logo_label.pack(side="left", padx=10, pady=10, anchor="w")

        # Navigationsbereich
        navigation_width = int(screen_width * 0.25)
        navigation_frame = tk.Frame(root, width=navigation_width, bg="#222222", bd=2, relief=tk.RAISED)  # Dark background with border
        navigation_frame.grid(row=1, column=0, sticky="ns")
        self.root.grid_columnconfigure(0, weight=0)  # Column 0 won't expand

        # Filterbereich
        self.filter_width = int(screen_width * 0.2)
        filter_height = main_height = screen_height - metabar_height
        self.filter_frame = tk.Frame(root, width=self.filter_width, height=filter_height, bg="#ffffff", bd=2, relief=tk.RAISED)  # White background with border
        self.filter_frame.grid(row=1, column=1, sticky="nsew")
        self.root.grid_columnconfigure(1, weight=0)  # Column 1 won't expand
        self.root.grid_rowconfigure(1, weight=1)  # Row 1 will expand vertically

        # Diagrammbereich
        chart_width = screen_width - navigation_width - self.filter_width - 50  # Adjust this value to make it wider
        chart_height = main_height - 100
        self.chart_frame = tk.Frame(root, bg="#ffffff", width=chart_width, height=chart_height, bd=2, relief=tk.RAISED)  # White background with border
        self.chart_frame.grid(row=1, column=2, sticky="nsew")
        self.root.grid_columnconfigure(2, weight=1)  # Column 2 will expand horizontally
        self.root.grid_rowconfigure(1, weight=1)  # Row 1 will expand vertically

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
            self.update_dropdown_text('Filter auswählen')  # Reset the dropdown text for other views
            # Embed the map view in the Tkinter window
            map_widget = tkintermapview.TkinterMapView(self.chart_frame, width=800, height=600, corner_radius=0)
            map_widget.pack(fill="both", expand=True)

            # Set Wien tile server
            map_widget.set_tile_server(
                "https://maps.wien.gv.at/basemap/geolandbasemap/normal/google3857/{z}/{y}/{x}.png", max_zoom=22)

            # Set current position and zoom to Wien
            map_widget.set_position(48.2082, 16.3738, marker=False)  # Vienna, Austria
            map_widget.set_zoom(12)

            # Coordinates for an approximate outline of the 22nd district of Vienna (PLZ 1220)
            district_22_polygon = [
                (48.22663, 16.37513),
                (48.23053, 16.40023),
                (48.24523, 16.41293),
                (48.24623, 16.41413),
                (48.24623, 16.41543)
            ]

            # Set a polygon for the 22nd district
            district_22 = map_widget.set_polygon(district_22_polygon, fill_color="green", command=self.polygon_click,
                                                 name="district_22_polygon")

        elif view == "Preisvergleich":
            # Draw line chart for Preisvergleich
            self.draw_line_chart()
            self.update_dropdown_text('Zuordnung auswählen')  # Reset the dropdown text for other views

        elif view == "Regionsanalyse":
            # Draw bar chart for Regionsanalyse
            self.draw_bar_chart()
            self.update_dropdown_text('Filter auswählen')  # Reset the dropdown text for other views

    def draw_line_chart(self):
        # Example data for a line chart
        x_values = [1, 2, 3, 4, 5]
        y_values = [10, 15, 7, 12, 9]

        # Create a figure and axis
        fig, ax = plt.subplots()

        # Plot the line chart
        ax.plot(x_values, y_values, label='Line Chart')

        # Set labels and title
        ax.set_xlabel('X-axis')
        ax.set_ylabel('Y-axis')
        ax.set_title('Line Chart Example')

        # Add a legend
        ax.legend()

        # Embed the chart in the Tkinter window
        canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()

    def draw_bar_chart(self):
        # Example data for a bar chart
        categories = ['Category A', 'Category B', 'Category C', 'Category D', 'Category E']
        values = [15, 24, 10, 30, 18]

        # Create a figure and axis
        fig, ax = plt.subplots()

        # Plot the bar chart
        ax.bar(categories, values, label='Bar Chart')

        # Set labels and title
        ax.set_xlabel('Categories')
        ax.set_ylabel('Values')
        ax.set_title('Bar Chart Example')

        # Add a legend
        ax.legend()

        # Embed the chart in the Tkinter window
        canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()

    def update_dropdown_text(self, text):
        # Update the text of the filter_dropdown
        self.filter_dropdown['values'] = ['Ein-, Zweifamilienhaus', 'Betriebsobjekt', 'Kleingarten']
        self.filter_dropdown.set(text)  # Set the initial value

if __name__ == "__main__":
    root = tk.Tk()
    app = GUIApp(root)
    root.mainloop()
