import os
import pickle

import pandas as pd
import uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from google_auth_oauthlib.flow import InstalledAppFlow
from starlette.requests import Request
from google.oauth2.service_account import Credentials
import gspread
from matplotlib import pyplot as plt
from starlette.responses import RedirectResponse

# Ініціалізація FastAPI
app = FastAPI(debug=True)

# Підключення статичних файлів
app.mount("/tables", StaticFiles(directory="tables"), name="tables")


# Ініціалізація Google Sheets
gc = gspread.service_account(filename='credentials.json')

# Тека для збереження графіків
os.makedirs("tables", exist_ok=True)


@app.get("/", include_in_schema=False)
async def root():
    """Перенаправлення на документацію."""
    return RedirectResponse("/docs")



@app.get("/data")
def get_financial_data():
    """Отримання сум доходів з усіх сторінок Google Sheets за конкретною клітинкою."""
    try:
        # Підключення до таблиці
        sheet_id = "1rL3woivfOHpVd_r1UzpEz584Y4EIBpxNhaStiRIuPqM"
        sh = gc.open_by_key(sheet_id)

        # Список для збереження доходів за сторінками
        income_data = []

        # Місяці для кожної сторінки
        # Список місяців для відображення
        months = ["Січень", "Лютий", "Березень", "Квітень", "Травень", "Червень",
                  "Липень", "Серпень", "Вересень", "Жовтень", "Листопад", "Грудень"]

        # Перевірка, скільки сторінок доступно
        worksheets = sh.worksheets()

        # Перевірка, чи є достатньо сторінок для 12 місяців
        if len(worksheets) < 12:
            return JSONResponse({"error": "В таблиці менше 12 сторінок, необхідно 12."}, status_code=400)

        income_data = []

        # Обробляємо кожну сторінку
        for index, worksheet in enumerate(worksheets[:12]):  # Обробляємо лише перші 12 сторінок
            try:
                # Зчитування значення клітинки AG4
                cell_value = worksheet.acell("AG4").value
                # Перевірка на порожнє значення та обробка NaN або None
                if cell_value is None or cell_value == '' or cell_value == 'NaN':
                    income = 0.0  # Якщо клітинка порожня або NaN, встановлюємо 0
                else:
                    try:
                        income = float(cell_value)
                    except ValueError:
                        income = 0.0  # Якщо значення не можна конвертувати в число, встановлюємо 0

                # Додаємо дані для кожного місяця
                income_data.append({"Month": months[index], "Income": income})
            except Exception as e:
                print(f"Помилка обробки сторінки №{index + 1}: {e}")

        # Якщо дані не були отримані
        if not income_data:
            return JSONResponse({"error": "Не вдалося завантажити дані з жодної сторінки."}, status_code=400)

        # Створення DataFrame
        df = pd.DataFrame(income_data)

        # Перевірка на NaN значення у DataFrame і заміна їх на 0
        df['Income'] = df['Income'].fillna(0)

        # Створення кругової діаграми
        plt.figure(figsize=(8, 8))
        plt.pie(df["Income"], labels=df["Month"], autopct='%1.1f%%', startangle=140)
        plt.title("Income Distribution by Month")
        chart_path = "tables/pie_chart.png"
        plt.savefig(chart_path)
        plt.close()
        return JSONResponse({"message": "Візуалізація діаграми створена", "Перейдіть до коду і відкрийте діаграму за цим шляхом": f"/{chart_path}"})
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)


if __name__ == "__main__":
    uvicorn.run(f"{__name__}:app", reload=True)
