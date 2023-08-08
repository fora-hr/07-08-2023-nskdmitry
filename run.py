import sys
import json
import unicodedata
from ast import literal_eval
from os.path import join as path_join, dirname
from datetime import datetime

columns = ["id", "Name", "Surname", "time"]
def load_results(competitors: dict[str, dict]) -> dict:
    results = {}
    with open(path_join(dirname(__file__), "results_RUN.txt"), mode='r', encoding='utf-8-sig') as source:
        for token in source:
            parsed = list(token.split(' '))
            no = parsed[0]
            splited = parsed[2].split(",")
            record  = {"id": no, "time": datetime.strptime(splited[0], '%H:%M:%S'), "add": int(splited[1])}
            record |= competitors[no]
            if parsed[1] == "start":
                results[no] = record
            else:
                prev = results[no]
                results[no]["time"] = str(record["time"] - prev["time"])
                results[no]["add"] = str(record["add"] - prev["add"])
    return results

def print_table(results: dict[str, dict]) -> None:
    global columns
    def sorting(no):
        timestr = results[no]["time"]
        time = datetime.strptime(timestr, '%H:%M:%S')
        return int(time.timestamp())
    sorted(results, key=sorting)
    print("Place\t\tID\t\tName\t\tSurname\t\tResult")
    place = 1
    for i in results:
        datacols = " ".join(["\t{:7}".format(results[i][field]) for field in columns])
        line = "{}\t{},{}".format(place, datacols, results[i]["add"])
        print(line)
        place += 1

if __name__ == "__main__":
    with open(path_join(dirname(__file__), "competitors2.json"), mode='r', encoding='utf-8-sig') as source:
        competitors = json.load(source)
    results = load_results(competitors)
    print_table(results)
