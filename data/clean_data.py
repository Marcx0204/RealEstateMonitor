import pandas as pd
from data.raw.read_data import read_data
from datetime import datetime


def clean_data():
    df = read_data()

    df_initial = df.copy()  # Eine Kopie der ursprünglichen Daten zur späteren Verwendung.

    # Doppelte Einträge entfernen
    df = df.drop_duplicates()

    columns_to_drop = [
        'KG.Code', 'EZ', 'ON', 'Gst.', 'Gst.Fl.', 'Widmung', 'Bauklasse', 'Gebäudehöhe', 'Bauweise',
        'Zusatz', 'Schutzzone', 'Wohnzone', 'öZ', 'seit/bis', 'Geschoße', 'parz.', 'VeräußererCode',
        'Erwerbercode', 'Zähler', 'Nenner', 'BJ', 'TZ', 'AbbruchfixEU', 'm³ Abbruch',
        'AbbruchkostEU', 'FreimachfixEU', 'Freimachfläche', 'FreimachkostEU', 'Baureifgest', '% Widmung',
        'Baurecht', 'Bis', 'auf EZ', 'Stammeinlage', 'sonst_wid', 'sonst_wid_prz', 'ber. Kaufpreis', 'Bauzins'
    ]

    # Spalten aus dem DataFrame entfernen
    df_cleaned = df.drop(columns=columns_to_drop)

    # Bereinigen der PLZ
    # Kopieren des DataFrames, um die SettingWithCopyWarning zu vermeiden
    df_no_outliers = df_cleaned.copy()

    # Bereinigen der PLZ: Entfernen von Dezimalstellen
    df_no_outliers['PLZ'] = df_no_outliers['PLZ'].astype(str).str.replace(r'\.0$', '', regex=True)

    # Mapping von Katastralgemeinde auf PLZ
    katastralgemeinde_plz_mapping = {
        'Alsergrund': '1090',
        'Innere Stadt': '1010',
        'Josefstadt': '1080',
        'Landstraße': '1030',
        'Margarethen': '1050',
        'Mariahilf': '1060',
        'Neubau': '1070',
        'Wieden': '1040',
        'Favoriten': '1100',
        'Inzersdorf': '1230',
        'Inzersdorf Stadt': '1230',
        'Kaiserebersdorf': '1110',
        'Oberlaa Land': '1100',
        'Oberlaa Stadt': '1100',
        'Rothneusiedl': '1100',
        'Simmering': '1110',
        'Unterlaa': '1100',
        'Albern': '1110',
        'Auhof': '1130',
        'Breitensee': '1140',
        'Hacking': '1130',
        'Hadersdorf': '1140',
        'Hietzing': '1130',
        'Hütteldorf': '1140',
        'Lainz': '1130',
        'Oberbaumgarten': '1140',
        'Ober St. Veit': '1130',
        'Ober St.Veit': '1130',
        'Penzing': '1140',
        'Rosenberg': '1130',
        'Schönbrunn': '1130',
        'Speising': '1130',
        'Unterbaumgarten': '1140',
        'Unter St. Veit': '1130',
        'Weidlingau': '1140',
        'Altmannsdorf': '1120',
        'Fünfhaus': '1150',
        'Gaudenzdorf': '1120',
        'Hetzendorf': '1120',
        'Meidling': '1120',
        'Rudolfsheim': '1150',
        'Sechshaus': '1150',
        'Dornbach': '1170',
        'Hernals': '1170',
        'Neulerchenfeld': '1160',
        'Neuwaldegg': '1170',
        'Ottakring': '1160',
        'Gersthof': '1180',
        'Grinzing': '1190',
        'Heiligenstadt': '1190',
        'Josefsdorf': '1190',
        'Kahlenbergerdorf': '1190',
        'Neustift am Walde': '1190',
        'Nußdorf': '1190',
        'Oberdöbling': '1190',
        'Obersievering': '1190',
        'Pötzleinsdorf': '1180',
        'Salmannsdorf': '1190',
        'Unterdöbling': '1190',
        'Untersievering': '1190',
        'Währing': '1180',
        'Weinhaus': '1180',
        'Donaufeld': '1210',
        'Floridsdorf': '1210',
        'Großjedlersdorf I': '1210',
        'Groß Jedlersdorf I': '1210',
        'Großjedlersdorf II': '1210',
        'Groß Jedlersdorf II': '1210',
        'Jedlesee': '1210',
        'Leopoldau': '1210',
        'Schwarze Lackenau': '1210',
        'Stammersdorf': '1210',
        'Strebersdorf': '1210',
        'Brigittenau': '1200',
        'Aspern': '1220',
        'Breitenlee': '1220',
        'Eßling': '1220',
        'Leopoldstadt': '1020',
        'Hirschstetten': '1220',
        'Kagran': '1220',
        'Kaisermühlen': '1220',
        'Lobau': '1220',
        'Neueßling': '1220',
        'Stadlau': '1220',
        'Zwerchäcker': '1220',
        'Mauer': '1230',
        'Süßenbrunn': '1220',
        'Liesing': '1230',
        'Rodaun': '1230',
        'Atzgersdorf': '1230',
        'Siebenhirten': '1230',
        'Erlaa': '1230',
        'Kalksburg': '1230',

    }

    # Erstellen einer Liste gültiger PLZ für Wien (inklusive 1230)
    valid_plz = [
        "1010", "1020", "1030", "1040", "1050", "1060", "1070", "1080", "1090",
        "1100", "1110", "1120", "1130", "1140", "1150", "1160", "1170", "1180",
        "1190", "1200", "1210", "1220", "1230"
    ]

    def is_valid_plz(plz):
        return plz in valid_plz

    # Erweitern Sie die `update_plz_if_invalid`-Funktion, um eine Flag für Änderungen zurückzugeben
    def update_plz_if_invalid(row, mapping, valid_plzs):
        kstrlgmnd = row['Katastralgemeinde']
        plz = row['PLZ']
        if plz not in valid_plzs and kstrlgmnd in mapping:
            return mapping[kstrlgmnd], True  # Gibt das neue PLZ und ein Flag für die Änderung zurück
        return plz, False  # Keine Änderung, gibt das Flag False zurück

    # Aktualisieren der PLZ und markieren, wenn Änderungen vorgenommen wurden
    for index, row in df_no_outliers.iterrows():
        new_plz, changed = update_plz_if_invalid(row, katastralgemeinde_plz_mapping, valid_plz)
        df_no_outliers.at[index, 'PLZ'] = new_plz
        # df_no_outliers.at[index, 'PLZ_Changed'] = changed

    # Sicherung des DataFrames vor dem Entfernen von Zeilen
    df_before_removal = df_no_outliers.copy()

    # Entfernen der Einträge, die keine gültige PLZ haben
    df_no_outliers = df_no_outliers[df_no_outliers['PLZ'].isin(valid_plz)]

    # Konvertieren der 'Erwerbsdatum'-Spalte in datetime, Fehler ignorieren und NaT für Fehler setzen
    df_no_outliers['Erwerbsdatum'] = pd.to_datetime(df_no_outliers['Erwerbsdatum'], errors='coerce')

    # Setzen Sie hier die Grenzen für das gültige Datum fest
    min_valid_date = pd.to_datetime('1900-01-01')
    max_valid_date = pd.to_datetime(datetime.now())

    # Entfernen von Zeilen mit ungültigen Daten
    df_no_outliers = df_no_outliers[(df_no_outliers['Erwerbsdatum'] >= min_valid_date) &
                                    (df_no_outliers['Erwerbsdatum'] <= max_valid_date)]

    # Entfernen von Zeilen, wo 'ErwArt' oder 'Erwerbsdatum' fehlen
    df_missing_values = df_no_outliers[df_no_outliers[['ErwArt', 'Erwerbsdatum']].isna().any(axis=1)]
    df_no_outliers = df_no_outliers.dropna(subset=['ErwArt', 'Erwerbsdatum'])

    df_removed = pd.concat([df_initial[~df_initial.index.isin(df_cleaned.index)],
                            df_before_removal[~df_before_removal.index.isin(df_no_outliers.index)],
                            df_missing_values])

    return df_no_outliers, df_removed
