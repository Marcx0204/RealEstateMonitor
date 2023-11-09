import pandas as pd
from data.clean_data import clean_data
from data.processed.save_data import save_data
from data.filter_data import filter_by_date
from data.filter_data import filter_by_zip
from data.filter_data import filter_by_bausperre
from data.filter_data import filter_by_price_range


def save_data(cleaned_df, removed_df, cleaned_path, removed_path):
    try:
        cleaned_df.to_excel(cleaned_path, index=False)
        print(f"Bereinigte Daten wurden erfolgreich unter {cleaned_path} gespeichert.")

        removed_df.to_excel(removed_path, index=False)
        print(f"Entfernte Datensätze wurden erfolgreich unter {removed_path} gespeichert.")
    except Exception as e:
        print(f"Fehler beim Speichern der Daten: {e}")


def clean_and_save_data():
    df_cleaned, df_removed = clean_data()  # clean_data should only return two DataFrames
    cleaned_path = 'data/processed/bereinigte_kaufpreissammlung.xlsx'
    removed_path = 'data/processed/entfernte_kaufpreissammlung.xlsx'
    save_data(df_cleaned, df_removed, cleaned_path, removed_path)
    print("Daten wurden bereinigt und gespeichert.")


def display_cleaned_data():
    save_path = 'data/processed/bereinigte_kaufpreissammlung.xlsx'
    try:
        df_saved = pd.read_excel(save_path)
        print(df_saved)
    except FileNotFoundError:
        print("Die Datei wurde nicht gefunden. Bitte zuerst die Daten bereinigen.")


def filter_data_by_date():
    start_date = input("Bitte Startdatum eingeben (YYYY-MM-DD): ")
    end_date = input("Bitte Enddatum eingeben (YYYY-MM-DD): ")

    df_cleaned, _ = clean_data()
    df_filtered = filter_by_date(df_cleaned, start_date, end_date)

    # Ausgabe der gefilterten Daten
    display_data(df_filtered)  # Now it works with a DataFrame

def filter_data_by_zip():
    zip_code = input("Bitte geben Sie die PLZ ein: ")

    df_cleaned, _ = clean_data()  # Wir ignorieren den df_removed für diese Funktion
    df_filtered_by_zip = filter_by_zip(df_cleaned, zip_code)  # Ändern Sie PLZ in zip_code

    # Ausgabe der gefilterten Daten
    display_data(df_filtered_by_zip)  # Verwenden Sie die display_data Funktion für Konsistenz


def filter_data_by_bausperre():
    bausperre_status = input("Geben Sie den Bausperre Status ein ('true' oder 'false'): ")
    df_cleaned, _ = clean_data()
    df_filtered_by_bausperre = filter_by_bausperre(df_cleaned, bausperre_status)

    if df_filtered_by_bausperre is not None:
        display_data(df_filtered_by_bausperre)
    else:
        print("Keine Daten zum Anzeigen.")


def filter_data_by_price():
    """Ermöglicht dem Benutzer, Daten nach einem Preisbereich zu filtern."""
    min_price = float(input("Geben Sie den Mindestpreis ein: "))
    max_price = float(input("Geben Sie den Höchstpreis ein: "))

    df_cleaned, _ = clean_data()
    df_filtered_by_price = filter_by_price_range(df_cleaned, min_price, max_price)

    display_data(df_filtered_by_price)

def display_data(data):
    if isinstance(data, pd.DataFrame):
        print(data)
    else:
        try:
            df = pd.read_excel(data)
            print(df)
        except FileNotFoundError:
            print(f"Die Datei {data} wurde nicht gefunden. Bitte zuerst die Daten bereinigen und speichern.")








def main():
    while True:
        print("\nMenü:")
        print("1 - Daten bereinigen und speichern")
        print("2 - Bereinigte Daten ausgeben")
        print("3 - Entfernte Daten ausgeben")
        print("4 - Daten nach Datum filtern")
        print("5 - Daten nach PLZ filtern")
        print("6 - Daten nach Bausperre filtern")
        print("7 - Daten nach Preis filtern")
        print("8 - Programm beenden")

        choice = input("Bitte wählen Sie eine Option (1, 2, 3, 4, 5, 6, 7, 8): ")

        if choice == '1':
            clean_and_save_data()
        elif choice == '2':
            cleaned_path = 'data/processed/bereinigte_kaufpreissammlung.xlsx'
            display_data(cleaned_path)
        elif choice == '3':
            removed_path = 'data/processed/entfernte_kaufpreissammlung.xlsx'
            display_data(removed_path)
        elif choice == '4':
            filter_data_by_date()
        elif choice == '5':
            filter_data_by_zip()
        elif choice == '6':
            filter_data_by_bausperre()
        elif choice == '7':
            filter_data_by_price()
        elif choice == '8':
            print("Programm wird beendet.")
            break
        else:
            print("Ungültige Eingabe. Bitte wählen Sie 1, 2, 3, 4, 5, oder 6.")

if __name__ == '__main__':
    main()