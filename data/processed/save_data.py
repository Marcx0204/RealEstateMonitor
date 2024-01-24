def save_data(cleaned_df, removed_df, save_path_cleaned, save_path_removed):
    cleaned_df.to_excel(save_path_cleaned, index=False)
    print(f"Bereinigte Daten wurden erfolgreich unter {save_path_cleaned} gespeichert.")

    removed_df.to_excel(save_path_removed, index=False)
    print(f"Entfernte Datensätze wurden erfolgreich unter {save_path_removed} gespeichert.")
