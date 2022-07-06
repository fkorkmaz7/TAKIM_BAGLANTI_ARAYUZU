
import json
from pathlib import Path


class PredictStatusSaver:
    def __init__(self) -> None:
        self.save_folder = "./_predict_status/"
        self.save_file_name = "last.json"
        Path(self.save_folder).mkdir(parents=True, exist_ok=True)
        self.save_data = self.get_saved_data()

    def addLastFrameIndex(self, index:int):
        #self.save_data["last_index"] = index
        if(index in self.save_data["sended_indexes"]): return
        self.save_data["sended_indexes"].append(index)
        with open(self.save_folder+self.save_file_name, 'w', encoding='utf-8') as f:
            json.dump(self.save_data, f, ensure_ascii=False, indent=4)

    def get_saved_data(self):
        data = {}
        with open(self.save_folder+self.save_file_name, "r+") as json_file:
            try:
                data = json.load(json_file)
            except json.decoder.JSONDecodeError:
                data = {
                    'sended_indexes': []
                }
                json.dump(data, json_file)
        return data
        
    def get_sended_indexes(self):
        return self.save_data["sended_indexes"]

    def clear(self):
        data = {
            'sended_indexes': []
        }
        with open(self.save_folder+self.save_file_name, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)