def save_cleaned_data(df_cleaned, save_path):
    df_cleaned.to_excel(save_path, index=False)