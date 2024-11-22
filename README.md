# Інструкція для отримання доступу до Google Sheets API

Для того, щоб ваш FastAPI додаток міг працювати з Google Sheets і отримувати дані, вам потрібно створити обліковий запис Google Cloud і отримати файл облікових даних (credentials.json). Ось кроки для цього:

## 1. Створення облікового запису Google Cloud

1. Перейдіть на [Google Cloud Console](https://console.cloud.google.com/).
2. Якщо у вас ще немає акаунта, створіть його.
3. Виберіть або створіть новий проект:
   - Натисніть на меню вгорі ліворуч, оберіть **Project** та створіть новий проект.

## 2. Увімкнення Google Sheets API

1. Виберіть проект, до якого ви хочете підключити API.
2. Перейдіть на сторінку **API & Services** > **Library**.
3. Знайдіть **Google Sheets API** і натисніть **Enable**.
4. Також увімкніть **Google Drive API**, якщо ви хочете зберігати та обробляти файли Google Sheets.

## 3. Створення облікових даних

1. Перейдіть до **APIs & Services** > **Credentials**.
2. Натисніть **Create Credentials** та оберіть **Service Account**.
3. Дайте назву сервісному акаунту та вкажіть роль **Editor** (це дасть йому доступ для читання/запису до таблиць Google Sheets).
4. Створіть файл облікових даних (JSON):
   - Після створення сервісного акаунту натисніть на нього і перейдіть до вкладки **Keys**.
   - Натисніть **Add Key** > **Create New Key** і виберіть формат **JSON**.
   - Завантажте файл облікових даних, який буде збережено на вашому комп'ютері.

## 4. Поділитися доступом до Google Sheets

1. Відкрийте Google Sheets документ, з яким ви хочете працювати.
2. Поділіться доступом до цього документа з сервісним акаунтом:
   - Відкрийте файл і натисніть на **Share**.
   - У полі **Share with people and groups** додайте електронну пошту сервісного акаунту (це електронна пошта, яку ви отримали під час створення облікових даних, зазвичай вона виглядає як `your-service-account@project-id.iam.gserviceaccount.com`).
   - Задайте рівень доступу **Editor**.

## 5. Додавання `credentials.json` у ваш проєкт

1. Перемістіть файл `credentials.json` в каталог вашого проєкту.
2. Не забувайте додати цей файл до `.gitignore`, щоб він не потрапив в GitHub:
