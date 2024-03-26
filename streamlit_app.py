import streamlit as st
import pandas as pd
import requests

# Пользовательский CSS для стилизации бокового меню
custom_css = """
<style>
/* Стилизация радио-кнопок как кнопок */
.stRadio > div {
    display: flex;
    flex-direction: column;
}

.stRadio > div > label {
    background-color: #4e73df; /* Цвет фона кнопки */
    color: white; /* Цвет текста */
    border-radius: 20px; /* Закругление углов */
    padding: 10px 15px; /* Внутренний отступ */
    margin: 5px 0; /* Отступы между кнопками */
    border: 1px solid #4e73df; /* Граница кнопки */
    cursor: pointer; /* Курсор в виде указателя */
}

.stRadio > div > label:hover {
    background-color: #5a5c69; /* Цвет фона кнопки при наведении */
    border-color: #5a5c69; /* Цвет границы при наведении */
}

/* Стиль для активного состояния (когда опция выбрана) */
.stRadio > div > label > div:first-child {
    display: none;
}

.stRadio > div > label > div:last-child {
    color: white !important;
}
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)

# Стилизация бокового меню
st.sidebar.title("Навигация")
st.sidebar.markdown("---")  # Добавляем горизонтальный разделитель

# Функция для получения данных из JSON по URL
def get_json_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Вызовет исключение для статусов 4xx/5xx
        return response.json()
    except Exception as e:
        st.sidebar.error(f"Не удалось получить данные из {url}. Ошибка: {e}")
        return None


# Функция для отображения таблицы с данными устройств
def display_device_table(data1, data2):
    # Инициализация пустых DataFrame
    df_devices1 = pd.DataFrame()
    df_devices2 = pd.DataFrame()

    # Обработка данных из первого источника, если они доступны
    if data1 is not None:
        devices1 = data1.get('device_list', [])
        df_devices1 = pd.DataFrame(devices1)
        if not df_devices1.empty:
            df_devices1['last_iterrate'] = pd.to_numeric(df_devices1['last_iterrate'], errors='coerce').fillna(0).astype(int)

    # Обработка данных из второго источника, если они доступны
    if data2 is not None:
        devices2 = [data2]  # Второй JSON представляет собой один объект
        df_devices2 = pd.DataFrame(devices2)
        df_devices2 = df_devices2.drop(columns=['average'], errors='ignore')

    # Объединение DataFrame, если хотя бы один не пустой
    if not df_devices1.empty or not df_devices2.empty:
        df_devices1.rename(columns={'label': 'Device', 'last_iterrate': 'Iterrate', 'solutions': 'Solutions'}, inplace=True, errors='ignore')
        df_devices2.rename(columns={'label': 'Device', 'last_iterrate': 'Iterrate', 'solutions': 'Solutions'}, inplace=True, errors='ignore')
        df_combined = pd.concat([df_devices1, df_devices2], ignore_index=True)
        st.table(df_combined)
    else:
        st.write("Нет доступных данных об устройствах.")






# Определение страниц приложения
def main_page():
    st.header("ГЛАВНАЯ СТРАНИЦА")
    st.markdown("Добро пожаловать в приложение!")

def mining_page():
    st.title('Информация о Майнинге')

    # URL с данными JSON
    url1 = "https://pooltemp.qubic.solutions/info?miner=QCBHVTJYNBIEPAXEUJJLNZJONVACFJXTMRTZVIPXKFNLCPGYTUMSWUVAJWFG&list=true"
    url2 = "http://188.235.1.241/hive/qubic/qubic.json"

    # Получение данных из первого JSON файла
    json_data1 = get_json_data(url1)

    # Получение данных из второго JSON файла
    json_data2 = get_json_data(url2)

    # Отображение таблицы
    display_device_table(json_data1, json_data2)

    # Кнопка для обновления данных
    if st.button('Обновить'):
        st.experimental_rerun()  # Этот метод перезапустит ваше приложение Streamlit, обновив данные


# Создание боковой панели для навигации
page = st.sidebar.radio(
    "Выберите страницу:",
    ("Главная", "Майнинг"),
    format_func=lambda x: "🏠 Главная" if x == "Главная" else "⛏ Майнинг"
)

# Отображение выбранной страницы
if page == "Главная":
    main_page()
elif page == "Майнинг":
    mining_page()

# Добавим нижний колонтитул с информацией о приложении
st.sidebar.markdown("---")
st.sidebar.info("Streamlit App v1.0")

