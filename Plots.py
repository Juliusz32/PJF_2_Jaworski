import glob
import pandas as pd
def prepare_plots():
    files = glob.glob(f"data/invoices/invoice_products_from_data_*.csv")
    dfs_to_concat = []
    for file in files:
        df = pd.read_csv(file, usecols=["Nazwa", "Cena netto", "Ilość"])
        df_grouped = df.groupby(["Nazwa", "Cena netto"]).agg({"Ilość": "sum"}).reset_index()
        dfs_to_concat.append(df_grouped)
    df_products = pd.concat(dfs_to_concat, ignore_index=True)
    df_products = df_products.groupby(["Nazwa", "Cena netto"]).agg({"Ilość": "sum"}).reset_index()
    df_products["Cena łącznie"] = df_products["Cena netto"] * df_products["Ilość"]

    files_2 = glob.glob(f"data/invoices/invoice_from_data_*.csv")
    dfs_to_concat_2 = []
    for file in files_2:
        df = pd.read_csv(file)
        selected_columns = df[["buyer_name", "buyer_city"]]
        dfs_to_concat_2.append(selected_columns)
    df_buyers = pd.concat(dfs_to_concat_2, ignore_index=True)

    df_plot_1 = df_products.groupby('Nazwa')['Cena łącznie'].sum().reset_index()
    df_plot_1.columns = ['Nazwa', 'Cena']
    df_plot_1 = df_plot_1.sort_values(by='Cena', ascending=False)
    df_plot_1 = df_plot_1.head(5)

    df_plot_2 = df_buyers.groupby('buyer_name').size().reset_index(name='Ilość')
    df_plot_2.columns = ['Klient', 'Ilość']
    df_plot_2 = df_plot_2.sort_values(by='Ilość', ascending=False)
    df_plot_2 = df_plot_2.head(5)

    return df_plot_1, df_plot_2