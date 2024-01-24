import tkinter as tk
import openpyxl
import pandas as pd
from tkinter import ttk
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkintermapview
from PIL import ImageGrab
import numpy as np
import datetime
import matplotlib.dates as mdates
from tkinter import filedialog, messagebox
import os

from data.filter_data import filter_by_zip

file_path = '../data/processed/bereinigte_kaufpreissammlung.xlsx'
class GUIApp:
    def __init__(self, root):
        self.df = pd.read_excel(file_path)
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
        logo_image = tk.PhotoImage(file="REMonitor_Logo.png").subsample(5,
                                                                        5)  # Replace with the path to your logo image
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
        stadtplan_button = ttk.Button(navigation_frame, text="Stadtplan", command=lambda: self.create_content("Stadtplan"),
                                      style="TButton")  # Added style
        stadtplan_button.pack(pady=10)

        preisentwicklung_button = ttk.Button(navigation_frame, text="Preisentwicklung",
                                           command=lambda: self.create_content("Preisentwicklung"),
                                           style="TButton")  # Added style
        preisentwicklung_button.pack(pady=10)

        regionsanalyse_button = ttk.Button(navigation_frame, text="Regionsanalyse",
                                           command=lambda: self.create_content("Regionsanalyse"),
                                           style="TButton")  # Added style
        regionsanalyse_button.pack(pady=10)

        # Create content and submit button
        self.create_content(view="Stadtplan")

        # Style configuration for buttons and combobox
        style = ttk.Style()
        style.configure("TButton", background="#3498db", font=("Helvetica", 12), borderwidth=5,
                        relief='raised', padding=10, width=15)  # Blue button with white text, larger, and rounded
        style.configure("TCombobox", background="#ecf0f1", fieldbackground="#ecf0f1",
                        font=("Helvetica", 12))  # Light gray combobox

    def create_content(self, view):
        # Höchstes und niedrigstes Datum erheben
        # Konvertiere die Spalte "Erwerbsdatum" in ein Datetime-Format
        self.df['Erwerbsdatum'] = pd.to_datetime(self.df['Erwerbsdatum'])
        # Finde das niedrigste Datum in der Spalte "Erwerbsdatum"
        min_date = self.df['Erwerbsdatum'].min()
        # Extrahiere das Jahr aus dem niedrigsten Datum
        min_year = int(min_date.year)
        print(f"Das niedrigste Datum ist: {min_date}")
        print(f"Das Jahr vom niedrigsten Datum ist: {min_year}")


        # Konvertiere die Spalte "Erwerbsdatum" in ein Datetime-Format
        self.df['Erwerbsdatum'] = pd.to_datetime(self.df['Erwerbsdatum'])
        # Finde das niedrigste Datum in der Spalte "Erwerbsdatum"
        max_date = self.df['Erwerbsdatum'].max()
        # Extrahiere das Jahr aus dem höchsten Datum
        max_year = int(max_date.year)+1
        print(f"Das höchste Datum ist: {max_date}")
        print(f"Das Jahr vom niedrigsten Datum ist: {max_year}")

        self.create_dropdowns(view, min_year, max_year)
        self.show_chart(view)
        self.create_submit_button(view)
        self.create_screenshot_button(view)
        # save filtered data
        self.create_save_button(view)

    def create_screenshot_button(self, view):
        # Create a button for taking a screenshot
        screenshot_button = ttk.Button(self.filter_frame, text="Screenshot", command=lambda: self.take_screenshot(view))
        screenshot_button.grid(row=17, pady=10, padx=10)

    def take_screenshot(self, view):
        # Get the current timestamp
        current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        # Prompt user to choose a directory for saving the screenshot
        folder_path = filedialog.askdirectory(title="Choose a folder to save the screenshot")

        if folder_path:
            # Construct the screenshot file name with the timestamp
            screenshot_filename = f"screenshot_{view}_{current_time}.png"

            # Get the position of the chart_frame relative to the screen
            x, y, width, height = self.chart_frame.winfo_rootx(), self.chart_frame.winfo_rooty(), self.chart_frame.winfo_width(), self.chart_frame.winfo_height()

            # Take a screenshot of the chart_frame
            screenshot = ImageGrab.grab(bbox=(x, y, x + width, y + height))

            # Save the screenshot to the specified folder path
            screenshot_path = os.path.join(folder_path, screenshot_filename)
            screenshot.save(screenshot_path, "PNG")

            # display a message to the user
            messagebox.showinfo("Screenshot Saved", f"Screenshot saved to: {screenshot_path}")

    def create_submit_button(self, view):
        if view == "Stadtplan":
            submit_button = ttk.Button(self.filter_frame, text="Filter anwenden", command=self.apply_filters_Stadtplan)
            submit_button.grid(row=16, pady=10, padx=10)
        elif view == "Preisentwicklung":
            submit_button = ttk.Button(self.filter_frame, text="Filter anwenden", command=self.apply_filters_Preis)
            submit_button.grid(row=16, pady=10, padx=10)
        elif view == "Regionsanalyse":
            submit_button = ttk.Button(self.filter_frame, text="Filter anwenden", command=self.apply_filters_Region)
            submit_button.grid(row=16, pady=10, padx=10)

    def create_dropdowns(self, view, min_year, max_year):

        dropdown_font = ("Helvetica", 12)
        for widget in self.filter_frame.winfo_children():
            widget.grid_forget()  # Hide all dropdowns initially

        if view == "Stadtplan":
        # Preis, Zuordnung, Zeitraum


            # Preis
            self.preis_dropdown = ttk.Combobox(self.filter_frame, values=['absolut', 'relativ'], style="TCombobox", font=dropdown_font)
            self.preis_dropdown.set('Preis auswählen')
            self.preis_dropdown.grid(row=0, pady=10, padx=10, sticky="w")

            # Zuordnung
            zuordnung_values = sorted(self.df['zuordnung'].unique())
            self.zuordnung_dropdown = ttk.Combobox(self.filter_frame, values=zuordnung_values, style="TCombobox", font=dropdown_font)
            self.zuordnung_dropdown.set('Zuordnung auswählen')  # Set the initial value
            self.zuordnung_dropdown.grid(row=1, pady=10, padx=10, sticky="w")

            # Zeitraum
            # Dropdowns für "Von: Monat und Jahr"
            von_label = tk.Label(self.filter_frame, text="Von:", font=dropdown_font)
            von_label.grid(row=2, pady=5, padx=10, sticky="w")

            self.von_month_dropdown = ttk.Combobox(self.filter_frame, values=['Jan', 'Feb', 'Mar', 'Apr', 'Mai', 'Jun',
                                                                         'Jul', 'Aug', 'Sep', 'Okt', 'Nov', 'Dez'],
                                              style="TCombobox", font=dropdown_font)
            self.von_month_dropdown.set('Monat auswählen')
            self.von_month_dropdown.grid(row=3, pady=5, padx=10, sticky="w")

            self.von_year_dropdown = ttk.Combobox(self.filter_frame, values=list(range(min_year, max_year)),
                                             style="TCombobox", font=dropdown_font)
            self.von_year_dropdown.set('Jahr auswählen')
            self.von_year_dropdown.grid(row=4, pady=5, padx=10, sticky="w")

            # Dropdowns für "Bis: Monat und Jahr"
            bis_label = tk.Label(self.filter_frame, text="Bis:", font=dropdown_font)
            bis_label.grid(row=5, pady=5, padx=10, sticky="w")

            self.bis_month_dropdown = ttk.Combobox(self.filter_frame, values=['Jan', 'Feb', 'Mar', 'Apr', 'Mai', 'Jun',
                                                                         'Jul', 'Aug', 'Sep', 'Okt', 'Nov', 'Dez'],
                                              style="TCombobox", font=dropdown_font)
            self.bis_month_dropdown.set('Monat auswählen')
            self.bis_month_dropdown.grid(row=6, pady=5, padx=10, sticky="w")

            self.bis_year_dropdown = ttk.Combobox(self.filter_frame, values=list(range(min_year, max_year)),
                                             style="TCombobox", font=dropdown_font)
            self.bis_year_dropdown.set('Jahr auswählen')
            self.bis_year_dropdown.grid(row=7, pady=10, padx=10, sticky="w")

        elif view == "Preisentwicklung":
        # Preis, Bezirk, Zuordnung, Zeitraum

            # Preis
            self.preis_dropdown = ttk.Combobox(self.filter_frame, values=['absolut', 'relativ'], style="TCombobox",
                                               font=dropdown_font)
            self.preis_dropdown.set('Preis auswählen')
            self.preis_dropdown.grid(row=0, pady=10, padx=10, sticky="w")

            # Bezirk
            bezirk_values = ['Alle Bezirke'] + sorted(self.df['PLZ'].unique())
            self.bezirk_dropdown = ttk.Combobox(self.filter_frame,
                                                values=bezirk_values,
                                                style="TCombobox", font=dropdown_font)
            self.bezirk_dropdown.set('Bezirk auswählen')
            self.bezirk_dropdown.grid(row=1, pady=10, padx=10, sticky="w")

            # Zuordnung
            zuordnung_values = sorted(self.df['zuordnung'].unique())
            self.zuordnung_dropdown = ttk.Combobox(self.filter_frame, values=zuordnung_values, style="TCombobox", font=dropdown_font)
            self.zuordnung_dropdown.set('Zuordnung auswählen')  # Set the initial value
            self.zuordnung_dropdown.grid(row=2, pady=10, padx=10, sticky="w")

            # Zeitraum
            # Dropdowns für "Von: Monat und Jahr"
            von_label = tk.Label(self.filter_frame, text="Von:", font=dropdown_font)
            von_label.grid(row=3, pady=5, padx=10, sticky="w")

            self.von_month_dropdown = ttk.Combobox(self.filter_frame, values=['Jan', 'Feb', 'Mar', 'Apr', 'Mai', 'Jun',
                                                                         'Jul', 'Aug', 'Sep', 'Okt', 'Nov', 'Dez'],
                                              style="TCombobox", font=dropdown_font)
            self.von_month_dropdown.set('Monat auswählen')
            self.von_month_dropdown.grid(row=4, pady=5, padx=10, sticky="w")

            self.von_year_dropdown = ttk.Combobox(self.filter_frame, values=list(range(min_year, max_year)),
                                             style="TCombobox", font=dropdown_font)
            self.von_year_dropdown.set('Jahr auswählen')
            self.von_year_dropdown.grid(row=5, pady=5, padx=10, sticky="w")

            # Dropdowns für "Bis: Monat und Jahr"
            bis_label = tk.Label(self.filter_frame, text="Bis:", font=dropdown_font)
            bis_label.grid(row=6, pady=5, padx=10, sticky="w")

            self.bis_month_dropdown = ttk.Combobox(self.filter_frame, values=['Jan', 'Feb', 'Mar', 'Apr', 'Mai', 'Jun',
                                                                         'Jul', 'Aug', 'Sep', 'Okt', 'Nov', 'Dez'],
                                              style="TCombobox", font=dropdown_font)
            self.bis_month_dropdown.set('Monat auswählen')
            self.bis_month_dropdown.grid(row=7, pady=5, padx=10, sticky="w")

            self.bis_year_dropdown = ttk.Combobox(self.filter_frame, values=list(range(min_year, max_year)),
                                             style="TCombobox", font=dropdown_font)
            self.bis_year_dropdown.set('Jahr auswählen')
            self.bis_year_dropdown.grid(row=8, pady=10, padx=10, sticky="w")

        elif view == "Regionsanalyse":
        # Bezirk, Filter, Zeitraum

            # Bezirk
            bezirk_values = sorted(self.df['PLZ'].unique())
            self.bezirk_dropdown = ttk.Combobox(self.filter_frame,
                                                values=bezirk_values,
                                                style="TCombobox", font=dropdown_font)
            self.bezirk_dropdown.set('Bezirk auswählen')
            self.bezirk_dropdown.grid(row=1, pady=10, padx=10, sticky="w")

            # Filter
            self.filter_dropdown = ttk.Combobox(self.filter_frame,
                                                values=['Zuordnung', 'Erwerbsart', 'Bausperre'],
                                                style="TCombobox", font=dropdown_font)
            self.filter_dropdown.set('Filter auswählen')
            self.filter_dropdown.grid(row=1, pady=10, padx=10, sticky="w")

            # Zeitraum
            # Dropdowns für "Von: Monat und Jahr"
            von_label = tk.Label(self.filter_frame, text="Von:", font=dropdown_font)
            von_label.grid(row=2, pady=5, padx=10, sticky="w")

            self.von_month_dropdown = ttk.Combobox(self.filter_frame, values=['Jan', 'Feb', 'Mar', 'Apr', 'Mai', 'Jun',
                                                                         'Jul', 'Aug', 'Sep', 'Okt', 'Nov', 'Dez'],
                                              style="TCombobox", font=dropdown_font)
            self.von_month_dropdown.set('Monat auswählen')
            self.von_month_dropdown.grid(row=3, pady=5, padx=10, sticky="w")

            self.von_year_dropdown = ttk.Combobox(self.filter_frame, values=list(range(min_year, max_year)),
                                             style="TCombobox", font=dropdown_font)
            self.von_year_dropdown.set('Jahr auswählen')
            self.von_year_dropdown.grid(row=4, pady=5, padx=10, sticky="w")

            # Dropdowns für "Bis: Monat und Jahr"
            bis_label = tk.Label(self.filter_frame, text="Bis:", font=dropdown_font)
            bis_label.grid(row=5, pady=5, padx=10, sticky="w")

            self.bis_month_dropdown = ttk.Combobox(self.filter_frame, values=['Jan', 'Feb', 'Mar', 'Apr', 'Mai', 'Jun',
                                                                         'Jul', 'Aug', 'Sep', 'Okt', 'Nov', 'Dez'],
                                              style="TCombobox", font=dropdown_font)
            self.bis_month_dropdown.set('Monat auswählen')
            self.bis_month_dropdown.grid(row=6, pady=5, padx=10, sticky="w")

            self.bis_year_dropdown = ttk.Combobox(self.filter_frame, values=list(range(min_year, max_year)),
                                             style="TCombobox", font=dropdown_font)
            self.bis_year_dropdown.set('Jahr auswählen')
            self.bis_year_dropdown.grid(row=7, pady=10, padx=10, sticky="w")

    def apply_filters_Preis(self):
        selected_bezirk = self.bezirk_dropdown.get()
        von_month = self.von_month_dropdown.get()
        von_year = self.von_year_dropdown.get()
        bis_month = self.bis_month_dropdown.get()
        bis_year = self.bis_year_dropdown.get()
        selected_zuordnung = self.zuordnung_dropdown.get()

        # Überprüfen und Einstellen der Datumsfilter
        start_date, end_date = None, None
        if von_month != 'Monat auswählen' and von_year != 'Jahr auswählen':
            start_date = f"{von_year}-{self.month_to_number(von_month)}-01"
        if bis_month != 'Monat auswählen' and bis_year != 'Jahr auswählen':
            end_date = f"{bis_year}-{self.month_to_number(bis_month)}-01"

        # Filtern des DataFrames nach Datum
        filtered_df = self.filter_dataframe_by_date(start_date, end_date)

        # Filtern nach Bezirk
        if selected_bezirk not in ['Bezirk auswählen', 'Alle Bezirke']:
            filtered_df = filter_by_zip(filtered_df, int(selected_bezirk))

        # Filtern nach Zuordnung, falls ausgewählt
        if selected_zuordnung and selected_zuordnung != 'Zuordnung auswählen':
            filtered_df = filtered_df[filtered_df['zuordnung'] == selected_zuordnung]

        # Zeichnen des Liniendiagramms mit dem gefilterten DataFrame
        self.draw_line_chart(filtered_df)

        print("Filtered Data:")
        print(filtered_df)
        return filtered_df

    def apply_filters_Stadtplan(self):
        # Abrufen der ausgewählten Werte aus den Dropdowns
        print(f"DataFrame vor dem Filtern: {self.df.head()}")

        von_month = self.von_month_dropdown.get()
        von_year = self.von_year_dropdown.get()
        bis_month = self.bis_month_dropdown.get()
        bis_year = self.bis_year_dropdown.get()
        selected_zuordnung = self.zuordnung_dropdown.get()  # Get the selected Zuordnung
        selected_preis = self.preis_dropdown.get()

        # Umwandlung der Werte in ein Datumsformat
        start_date = f"{von_year}-{self.month_to_number(von_month)}-01" if von_month != 'Monat auswählen' else None
        end_date = f"{bis_year}-{self.month_to_number(bis_month)}-01" if bis_month != 'Monat auswählen' else None

        # Filtern des DataFrames nach Datum und Zuordnung
        filtered_df = self.filter_dataframe_by_date(start_date, end_date)
        if selected_zuordnung != 'Zuordnung auswählen':
            filtered_df = filtered_df[filtered_df['zuordnung'] == selected_zuordnung]

        if selected_preis == 'relativ':
            self.draw_stadtPlanRelativ(filtered_df)
        else:
            # Zeichnen des Stadtplans mit dem gefilterten DataFrame
            self.draw_stadtPlan(filtered_df)
        # Optionale Ausgabe zur Überprüfung
        print("Filtered Data:")
        print(filtered_df)
        return filtered_df

    def draw_stadtPlanRelativ(self, filtered_df):
        # Clear existing content in chart_frame
        for widget in self.chart_frame.winfo_children():
            widget.destroy()
        # Read the GeoJSON file into a GeoDataFrame
        gdf = gpd.read_file('../data/raw/BEZIRKSGRENZEOGDPolygon.geojson')

        # Embed the map view in the Tkinter window
        map_widget = tkintermapview.TkinterMapView(self.chart_frame, width=800, height=600, corner_radius=0)
        map_widget.pack(fill="both", expand=True)

        # Set Wien tile server
        map_widget.set_tile_server(
            "https://maps.wien.gv.at/basemap/geolandbasemap/normal/google3857/{z}/{y}/{x}.png", max_zoom=22)

        # Set current position and zoom to Wien
        map_widget.set_position(48.2082, 16.3738, marker=False)  # Vienna, Austria
        map_widget.set_zoom(11)

        print(filtered_df)

        # Create a legend dictionary for color mapping
        legend_mapping = {
            "lightgreen": "Preis pro m² <= 300",
            "yellow": "300 < Preis pro m² <= 600",
            "red": "Preis pro m² > 600",
            "lightgrey": "Nicht genügend gütlige Daten vorhanden"
        }

        # Create a legend on the map
        legend_frame = tk.Frame(self.chart_frame, bg="white")
        legend_frame.pack(side="bottom", fill="x", pady=10, padx=10)

        for color, label in legend_mapping.items():
            legend_label = tk.Label(legend_frame, text=label, bg=color)
            legend_label.pack(side="left", padx=5)

        def polygon_click(polygon):
            print(f"polygon clicked - text: {polygon.name}")

        # Iterate over all districts
        for bezirk_number in gdf['BEZNR'].unique():
            # Extract coordinates for the current district
            district_geometry = gdf[gdf['BEZNR'] == bezirk_number]['geometry'].iloc[0]
            coordinates = list(district_geometry.exterior.coords)

            # Convert coordinates to latitude and longitude
            district_polygon = [(y, x) for x, y in coordinates]

            # Get the PLZ corresponding to the BEZNR
            plz_for_bezirk = bezirk_number * 10 + 1000;

            # Convert 'BEZNR' to string before concatenation
            # plz_for_bezirk = str(plz_for_bezirk)

            # Calculate median 'Kaufpreis €' for the current district
            district_median_price = filtered_df[filtered_df['PLZ'] == plz_for_bezirk]['€/m² Gfl.'].median()

            print(plz_for_bezirk)
            print(bezirk_number)
            print(district_median_price)
            # Set fill and border colors based on median 'Kaufpreis €'
            if 0 < district_median_price <= 300:
                fill_color = "lightgreen"
                outline_color = "green"
            elif 200 < district_median_price <= 600:
                fill_color = "yellow"
                outline_color = "orange"
            elif district_median_price > 600:
                fill_color = "red"
                outline_color = "red"
            else:
                fill_color = "lightgrey"
                outline_color = "grey"

            # Set a polygon for the current district
            district_name = f"district_{bezirk_number}_polygon"
            map_widget.set_polygon(district_polygon, fill_color=fill_color, outline_color=outline_color,
                                   border_width=2, command=polygon_click, name=district_name)



    def draw_stadtPlan(self, filtered_df):


        # Clear existing content in chart_frame
        for widget in self.chart_frame.winfo_children():
            widget.destroy()
        # Read the GeoJSON file into a GeoDataFrame
        gdf = gpd.read_file('../data/raw/BEZIRKSGRENZEOGDPolygon.geojson')

        # Embed the map view in the Tkinter window
        map_widget = tkintermapview.TkinterMapView(self.chart_frame, width=800, height=600, corner_radius=0)
        map_widget.pack(fill="both", expand=True)

        # Set Wien tile server
        map_widget.set_tile_server(
            "https://maps.wien.gv.at/basemap/geolandbasemap/normal/google3857/{z}/{y}/{x}.png", max_zoom=22)

        # Set current position and zoom to Wien
        map_widget.set_position(48.2082, 16.3738, marker=False)  # Vienna, Austria
        map_widget.set_zoom(11)

        print(filtered_df)

        # Create a legend dictionary for color mapping
        legend_mapping = {
            "lightgreen": "absoluter Kaufpreis <= 300,000",
            "yellow": "300,000 < absoluter Kaufpreis <= 500,000",
            "red": "absoluter Kaufpreis > 500,000",
            "lightgrey": "Nicht genügend gütlige Daten vorhanden"
        }

        # Create a legend on the map
        legend_frame = tk.Frame(self.chart_frame, bg="white")
        legend_frame.pack(side="bottom", fill="x", pady=10, padx=10)

        for color, label in legend_mapping.items():
            legend_label = tk.Label(legend_frame, text=label, bg=color)
            legend_label.pack(side="left", padx=5)

        def polygon_click(polygon):
            print(f"polygon clicked - text: {polygon.name}")

        # Iterate over all districts
        for bezirk_number in gdf['BEZNR'].unique():
            # Extract coordinates for the current district
            district_geometry = gdf[gdf['BEZNR'] == bezirk_number]['geometry'].iloc[0]
            coordinates = list(district_geometry.exterior.coords)

            # Convert coordinates to latitude and longitude
            district_polygon = [(y, x) for x, y in coordinates]

            # Get the PLZ corresponding to the BEZNR
            plz_for_bezirk = bezirk_number * 10 + 1000;

            # Convert 'BEZNR' to string before concatenation
            # plz_for_bezirk = str(plz_for_bezirk)

            # Calculate median 'Kaufpreis €' for the current district
            district_median_price = filtered_df[filtered_df['PLZ'] == plz_for_bezirk]['Kaufpreis €'].median()

            print(plz_for_bezirk)
            print(bezirk_number)
            print(district_median_price)
            # Set fill and border colors based on median 'Kaufpreis €'
            if 0 < district_median_price <= 300000:
                fill_color = "lightgreen"
                outline_color = "green"
            elif 300000 < district_median_price <= 500000:
                fill_color = "yellow"
                outline_color = "orange"
            elif district_median_price > 500000:
                fill_color = "red"
                outline_color = "red"
            else:
                fill_color = "lightgrey"
                outline_color = "grey"

            # Set a polygon for the current district
            district_name = f"district_{bezirk_number}_polygon"
            map_widget.set_polygon(district_polygon, fill_color=fill_color, outline_color=outline_color,
                                   border_width=2, command=polygon_click, name=district_name)




    def apply_filters_Region(self):
        # Abrufen der ausgewählten Werte aus den Dropdowns
        selected_bezirk = self.bezirk_dropdown.get()
        # Debugging-Ausgaben
        print(f"Ausgewählter Bezirk: {selected_bezirk}")
        print(f"DataFrame vor dem Filtern: {self.df.head()}")

        von_month = self.von_month_dropdown.get()
        von_year = self.von_year_dropdown.get()
        bis_month = self.bis_month_dropdown.get()
        bis_year = self.bis_year_dropdown.get()

        # Umwandlung der Werte in ein Datumsformat
        start_date = f"{von_year}-{self.month_to_number(von_month)}-01" if von_month != 'Monat auswählen' else None
        end_date = f"{bis_year}-{self.month_to_number(bis_month)}-01" if bis_month != 'Monat auswählen' else None

        # Filtern des DataFrames nach Datum
        filtered_df = self.filter_dataframe_by_date(start_date, end_date)

        # Überprüfen, ob der ausgewählte Bezirk gültig ist
        if selected_bezirk not in ['Bezirk auswählen', 'Alle Bezirke']:
            filtered_df = filter_by_zip(self.df, int(selected_bezirk))

        # Zeichnen des Liniendiagramms mit dem gefilterten DataFrame
        self.draw_bar_chart(filtered_df)

        # Optionale Ausgabe zur Überprüfung
        print("Filtered Data:")
        print(filtered_df)
        return filtered_df

    def month_to_number(self, month_name):
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'Mai', 'Jun', 'Jul', 'Aug', 'Sep', 'Okt', 'Nov', 'Dez']
        return str(months.index(month_name) + 1).zfill(2)

    def filter_dataframe_by_date(self, start_date, end_date):
        filtered_df = self.df.copy()
        filtered_df['Erwerbsdatum'] = pd.to_datetime(filtered_df['Erwerbsdatum'], errors='coerce')

        if start_date:
            start_date = pd.to_datetime(start_date)
            start_date = pd.to_datetime(start_date)
            filtered_df = filtered_df[filtered_df['Erwerbsdatum'] >= start_date]

        if end_date:
            end_date = pd.to_datetime(end_date)
            filtered_df = filtered_df[filtered_df['Erwerbsdatum'] <= end_date]

        return filtered_df

    def create_save_button(self, view):
        # Create a button for saving filtered data
        save_button = ttk.Button(self.filter_frame, text="Daten speichern",
                                 command=lambda: self.save_filtered_data(view))
        save_button.grid(row=18, pady=10, padx=10)

    def save_filtered_data(self, view):
        # Get the filtered data based on the current view
        if view == "Stadtplan":
            filtered_df = self.apply_filters_Stadtplan()
        elif view == "Preisentwicklung":
            filtered_df = self.apply_filters_Preis()
        elif view == "Regionsanalyse":
            filtered_df = self.apply_filters_Region()
        else:
            # Add additional branches for other views if needed
            return

        # Get the current timestamp
        current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        data_filename = f"filtered_data_{view}_{current_time}.xlsx"

        # Prompt user to choose a folder path for saving the Excel file
        folder_path = tk.filedialog.askdirectory(title="Select Folder to Save Filtered Data")

        if folder_path:
            # Construct the file path based on the selected folder and save the Excel file
            file_path = os.path.join(folder_path, data_filename)
            filtered_df.to_excel(file_path, index=False)
            print(f"Filtered data saved to: {file_path}")

            # display a message to the user
            messagebox.showinfo("Data saved in xlsx", f"Data saved to: {file_path}")


    def show_chart(self, view):
        # Clear existing content in chart_frame
        for widget in self.chart_frame.winfo_children():
            widget.destroy()

        # Update chart_frame content based on the selected view
        if view == "Stadtplan":
            self.draw_stadtPlan(self.df)

        # Add the missing indented block for the elif statement
        elif view == "Preisvergleich":
            # Draw line chart for Preisvergleich
            pass  # Placeholder; add your code here

        elif view == "Regionsanalyse":
            # Draw bar chart for Regionsanalyse
            filtered_df = self.apply_filters_Region()
            self.draw_bar_chart(filtered_df)



    def polygon_click(self, polygon):
        print(f"Polygon clicked - text: {polygon.name}")

    def get_district_fill_color(self, district_number):
        # Add your logic here to determine the fill color based on the district number
        # For example, you can use a dictionary to map district numbers to colors
        district_color_mapping = {
            "22": "green",
            # Add more entries as needed
        }

        # Return the fill color for the given district number, defaulting to a color if not found in the mapping
        return district_color_mapping.get(district_number, "blue")

    def draw_line_chart(self, filtered_df):

        for widget in self.chart_frame.winfo_children():
            widget.destroy()

        # Stellen Sie sicher, dass der DataFrame die notwendigen Spalten enthält
        if 'Erwerbsdatum' in filtered_df.columns and 'Kaufpreis €' in filtered_df.columns:
            # Extrahieren Sie die Daten für die X- und y-Achse
            x_values = pd.to_datetime(filtered_df['Erwerbsdatum'])
            # Gruppieren Sie die Daten nach Jahr (oder Monat) und berechnen Sie den Durchschnittspreis
            df_grouped = filtered_df.groupby(filtered_df['Erwerbsdatum'].dt.year)['Kaufpreis €'].mean()

            # Erstellen Sie die X- und Y-Werte für das Diagramm
            x_values = df_grouped.index
            y_values = df_grouped.values

            # Erstellen Sie eine Figur und eine Achse
            fig, ax = plt.subplots()

            # Zeichnen Sie das Liniendiagramm
            ax.plot(x_values, y_values, label='Durchschnittlicher Preis')

            # Setzen Sie Beschriftungen und Titel
            ax.set_xlabel('Erwerbsdatum')
            ax.set_ylabel('Durchschnittspreis in €')
            ax.set_title('Durchschnittliche Preisentwicklung über Zeit')

            # Fügen Sie eine Legende hinzu
            ax.legend()

            # Binden Sie das Diagramm in das Tkinter-Fenster ein
            canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
            canvas.draw()
            canvas.get_tk_widget().pack()

    def draw_bar_chart(self, filtered_df):
        # Clear existing content in chart_frame
        for widget in self.chart_frame.winfo_children():
            widget.destroy()

        # Group the data by 'PLZ' and calculate the mean of 'Kaufpreis €'
        grouped_data = filtered_df.groupby('PLZ')['Kaufpreis €'].mean()

        # PLZ (districts) and their average prices
        districts = grouped_data.index
        avg_prices = grouped_data.values

        # Create a figure and axis
        fig, ax = plt.subplots()

        # Plot the bar chart
        ax.bar(districts, avg_prices, color='skyblue')

        # Set labels and title
        ax.set_xlabel('Bezirk (PLZ)')
        ax.set_ylabel('Durchschnittlicher Kaufpreis €')
        ax.set_title('Durchschnittliche Kaufpreise pro Bezirk')

        # Rotate x-axis labels for better readability
        plt.xticks(rotation=45)

        # Embed the chart in the Tkinter window
        canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()

if __name__ == "__main__":
    root = tk.Tk()
    app = GUIApp(root)
    root.mainloop()
