# Лаба с задачей коммивояжера

## Как запустить
1. Проверить что установлен python 3.10+ 
    ```bash
    python --version
    ------
    Python 3.10.12
    ```
2. Из корневой папки проекта создать папку .venv
    ```bash
    mkdir .venv
    ```
3. Создать virtual environment
    ```bash
    python -m venv .venv
    ```
4. Активировать venv
    
    * [Windows]
        ```
        .venv\Scripts\activate
        ```

    * [Linux/MacOs]
        ```
        source .venv/bin/activate
        ```
5. Установить зависимости
    ```
    pip install -r requirements.txt
    ```
6. Запустить
    ```
    python main.py
    ```