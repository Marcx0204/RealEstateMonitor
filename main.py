import pandas as pd
from data.clean_data import clean_data
from data.processed.create_data import save_cleaned_data


def clean_and_save_data():
    df_cleaned = clean_data()
    save_path = 'data/processed/bereinigte_kaufpreissammlung.xlsx'
    save_cleaned_data(df_cleaned, save_path)
    print("Daten wurden bereinigt und gespeichert.")

def display_cleaned_data():
    save_path = 'data/processed/bereinigte_kaufpreissammlung.xlsx'
    try:
        df_saved = pd.read_excel(save_path)
        print(df_saved)
    except FileNotFoundError:
        print("Die Datei wurde nicht gefunden. Bitte zuerst die Daten bereinigen.")

def main():
    while True:
        print("\nMenü:")
        print("1 - Daten bereinigen und speichern")
        print("2 - Bereinigte Daten ausgeben")
        print("3 - Programm beenden")

        choice = input("Bitte wählen Sie eine Option (1, 2, 3): ")

        if choice == '1':
            clean_and_save_data()
        elif choice == '2':
            display_cleaned_data()
        elif choice == '3':
            print("Programm wird beendet.")
            break
        else:
            print("Ungültige Eingabe. Bitte wählen Sie 1, 2 oder 3.")

if __name__ == '__main__':
    main()