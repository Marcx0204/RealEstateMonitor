import pandas as pd
from data.clean_data import clean_data
from data.processed.save_data import save_data
from data.filter_data import filter_by_date
from data.filter_data import filter_by_zip


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


def display_data(data):
    if isinstance(data, pd.DataFrame):
        print(data)
    else:
        try:
            df = pd.read_excel(data)
            print(df)
        except FileNotFoundError:
            print(f"Die Datei {data} wurde nicht gefunden. Bitte zuerst die Daten bereinigen und speichern.")

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




def main():
    while True:
        print("\nMenü:")
        print("1 - Daten bereinigen und speichern")
        print("2 - Bereinigte Daten ausgeben")
        print("3 - Entfernte Daten ausgeben")
        print("4 - Programm beenden")
        print("5 - Daten nach Datum filtern")
        print("6 - Daten nach PLZ filtern")

        choice = input("Bitte wählen Sie eine Option (1, 2, 3, 4, 5): ")

        if choice == '1':
            clean_and_save_data()
        elif choice == '2':
            cleaned_path = 'data/processed/bereinigte_kaufpreissammlung.xlsx'
            display_data(cleaned_path)
        elif choice == '3':
            removed_path = 'data/processed/entfernte_kaufpreissammlung.xlsx'
            display_data(removed_path)
        elif choice == '4':
            print("Programm wird beendet.")
            break
        elif choice == '5':
            filter_data_by_date()
        elif choice == '6':
            filter_data_by_zip()
        else:
            print("Ungültige Eingabe. Bitte wählen Sie 1, 2, 3, 4 oder 5.")

if __name__ == '__main__':
    main()