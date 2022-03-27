base_path = "./"
appdata_path = f"{base_path}/__appdata__"
data_path = f"{base_path}/data"
logs_path = f"{appdata_path}/log"
settings_path = f"{appdata_path}/settings.json"
lines_path = f"{data_path}/translations/ru_RU.json"

def _show_paths():
    import os
    print(f"base_path = {os.path.abspath(base_path)}")
    print(f"appdata_path = {os.path.abspath(appdata_path)}")
    print(f"data_path = {os.path.abspath(data_path)}")
    print(f"logs_path = {os.path.abspath(logs_path)}")
    print(f"settings_path = {os.path.abspath(settings_path)}")
    print(f"text_path = {os.path.abspath(lines_path)}")

if __name__ == "__main__":
    _show_paths()
