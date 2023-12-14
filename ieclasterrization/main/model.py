from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import joblib
from datetime import datetime
from sklearn.cluster import KMeans


# Функция для загрузки данных из CSV
def load_csv(file_path, delimiter=','):
    return pd.read_csv(file_path, encoding="utf-8", delimiter=delimiter)


# Функция для поиска значения в таблице
def find_value_in_table(section, region, df):
    index = (df.iloc[:, 0] == region).idxmax()
    result = df[section.lower()][index]
    return float(str(result).replace(' ', '').replace(',', '.'))


# Функция для расчета коэффициента риска
def calculate_risk_ratio(date_str):
    date_obj = datetime.strptime(date_str, '%Y-%m-%d')
    today = datetime.today()
    days_difference = (today - date_obj).days
    years = int(days_difference / 365.25)
    if years < 3:
        return 0.5
    elif years < 10:
        return 0.8
    return 1.0


# Функция для получения данных
def get_data(date_str, section, region):
    BASE_DIR = Path(__file__).resolve().parent.parent
    valproduct_df = load_csv(BASE_DIR / 'main/data/correct_GROSS_REGIONAL_PRODUCT.csv')
    oborot_df = load_csv(BASE_DIR / 'main/data/correct1_TURNOVER_ORGANIZATIONS.csv')
    kolvo_df = load_csv(BASE_DIR / 'main/data/correct_DISTRIBUTION_NUMBER_ORGANIZATIONS.csv')

    risk_ratio = calculate_risk_ratio(date_str)
    valproduct = find_value_in_table(section, region, valproduct_df)
    oborot = find_value_in_table(section, region, oborot_df)
    kolvo = find_value_in_table(section, region, kolvo_df)

    # Нормализация данных
    Turnover_Risk_Coefficient_mean = 1351.642
    Turnover_Risk_Coefficient_std = 3979.585
    Gross_product_Number_of_enterprises_mean = 0.01085996
    Gross_product_Number_of_enterprises_std = 0.09158235
    Turnover_Risk_Coefficient = (oborot * risk_ratio - Turnover_Risk_Coefficient_mean) / Turnover_Risk_Coefficient_std
    Gross_product_Number_of_enterprises = (
                                                      valproduct / kolvo - Gross_product_Number_of_enterprises_mean) / Gross_product_Number_of_enterprises_std

    return Turnover_Risk_Coefficient, Gross_product_Number_of_enterprises


# Функция для визуализации данных
def plot(date_str, section, region):
    BASE_DIR = Path(__file__).resolve().parent.parent
    loaded_kmeans = joblib.load(BASE_DIR / "main/data/kmeans_model.pkl")
    df_clustering = load_csv(BASE_DIR / "main/data/normalized_data.csv").head(1000)
    param_one, param_two = get_data(date_str, section, region)

    new_data = pd.DataFrame({
        "Turnover X Risk Coefficient_T": [param_one],
        "Gross product / Number of enterprises_T": [param_two]
    })
    new_data["kmeans_4"] = loaded_kmeans.predict(new_data.iloc[:, :2])

    # Сохранение новых данных в файл
    new_data_path = BASE_DIR / 'main/data/new_data.csv'
    new_data.to_csv(new_data_path, index=False)

    plt.scatter(df_clustering["Turnover X Risk Coefficient_T"],
                df_clustering["Gross product / Number of enterprises_T"], c=df_clustering["kmeans_6"],
                label="Исходные данные")
    plt.scatter(new_data["Turnover X Risk Coefficient_T"], new_data["Gross product / Number of enterprises_T"], c="red",
                label="Новые данные")
    plt.legend()
    plt.title("Визуализация Кластеризации")
    plt.xlabel("Коэффициент Оборота и Риска")
    plt.ylabel("Валовой Продукт / Количество Предприятий")
    plt.xlim(-0.6, 8)
    plt.ylim(-0.6, 12)

    image_path = BASE_DIR / 'main/static/images/my_plot.png'
    plt.savefig(image_path)
    plt.close()
    return 'images/my_plot.png'


# Функция для фильтрации данных по региону и секции
def region(section, region):
    BASE_DIR = Path(__file__).resolve().parent.parent
    df = load_csv(BASE_DIR / "main/data/hackathon_modified.csv", delimiter=';')
    df_clustering = load_csv(BASE_DIR / "main/data/normalized_data.csv")

    if section and region:  # Фильтр по обоим параметрам
        df_filtered = df[
            df['region'].str.contains(region, case=False) & df['section'].str.contains(section, case=False)]
        df_filtered_clustering = df_clustering[
            df_clustering['region'].str.contains(region, case=False) & df_clustering['section'].str.contains(section,
                                                                                                             case=False)]
    elif region:  # Фильтр только по региону
        df_filtered = df[df['region'].str.contains(region, case=False)]
        df_filtered_clustering = df_clustering[df_clustering['region'].str.contains(region, case=False)]
    elif section:  # Фильтр только по секции
        df_filtered = df[df['section'].str.contains(section, case=False)]
        df_filtered_clustering = df_clustering[df_clustering['section'].str.contains(section, case=False)]

    kmeans = KMeans(n_clusters=3)
    kmeans.fit(df_filtered_clustering[["Turnover X Risk Coefficient_T", "Gross product / Number of enterprises_T"]])
    df_filtered_clustering["kmeans_4"] = kmeans.labels_

    new_data_path = BASE_DIR / 'main/data/new_data.csv'
    if new_data_path.exists():
        new_data = pd.read_csv(new_data_path)

    plt.scatter(df_filtered_clustering["Turnover X Risk Coefficient_T"],
                df_filtered_clustering["Gross product / Number of enterprises_T"], c=df_filtered_clustering["kmeans_4"])
    plt.scatter(new_data["Turnover X Risk Coefficient_T"], new_data["Gross product / Number of enterprises_T"], c="pink",
                label="Новые данные")
    plt.legend()
    plt.title("Распределение по Кластерам")
    plt.xlabel("Коэффициент Оборота и Риска")
    plt.ylabel("Валовой Продукт / Количество Предприятий")
    plt.gca().autoscale()

    image_path = BASE_DIR / 'main/static/images/filter.png'
    plt.savefig(image_path)
    plt.close()
    return 'images/filter.png'
