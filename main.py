import pandas as pd
from data.clean_data import clean_data
from data.processed.save_data import save_data


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


def display_data(path):
    try:
        df = pd.read_excel(path)
        print(df)
    except FileNotFoundError:
        print(f"Die Datei {path} wurde nicht gefunden. Bitte zuerst die Daten bereinigen und speichern.")


def main() -> object:
    while True:
        print("\nMenü:")
        print("1 - Daten bereinigen und speichern")
        print("2 - Bereinigte Daten ausgeben")
        print("3 - Entfernte Daten ausgeben")
        print("4 - Programm beenden")

        choice = input("Bitte wählen Sie eine Option (1, 2, 3, 4): ")

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
        else:
            print("Ungültige Eingabe. Bitte wählen Sie 1, 2, 3 oder 4.")


if __name__ == '__main__':
    main()
