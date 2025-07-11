import datetime


def keep_records(result, filepath):
    today = datetime.date.today().strftime("%Y-%m-%d")
    with open(filepath, "a+", encoding="utf-8") as file:
        file.write(f"[{today}] {result}\n")