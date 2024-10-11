import json

class JsonDB:
    def __init__(self, name: str, path: str = ''):
        self.name = name if name.endswith(".json") else f"{name}.json"
        self.path = path

    def get_data(self):
        try:
            with open(self.path + self.name, "r", encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}

    def save_data(self, data: dict):
        with open(self.path + self.name, "w", encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)


            