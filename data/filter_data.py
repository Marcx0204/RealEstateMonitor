import pandas as pd

def filter_by_date(df, start_date=None, end_date=None):
    """
    Filter the DataFrame rows based on Erwerbsdatum column.

    Parameters:
    - df (pandas.DataFrame): The DataFrame to filter.
    - start_date (str): The start date to filter by in YYYY-MM-DD format. Optional.
    - end_date (str): The end date to filter by in YYYY-MM-DD format. Optional.

    Returns:
    - pandas.DataFrame: The filtered DataFrame.
    """

    # Konvertieren der 'Erwerbsdatum'-Spalte in datetime, Fehler ignorieren und NaT für Fehler setzen
    df['Erwerbsdatum'] = pd.to_datetime(df['Erwerbsdatum'], errors='coerce')

    if start_date:
        # Konvertieren des Startdatums in datetime und Filtern der Daten
        start_date = pd.to_datetime(start_date)
        df = df[df['Erwerbsdatum'] >= start_date]

    if end_date:
        # Konvertieren des Enddatums in datetime und Filtern der Daten
        end_date = pd.to_datetime(end_date)
        df = df[df['Erwerbsdatum'] <= end_date]

    return df

def filter_by_zip(df, zip_code):
    return df[df['PLZ'] == zip_code]