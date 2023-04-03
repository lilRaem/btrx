from module.config import timing_decorator
import json



@timing_decorator
def iter():
    d = 0
    l = list()
    with open('large-file.json','r',encoding="utf-8") as f:
        data: list[dict] = json.loads(f.read())
    for dor in data:
        if dor.get("id") == 2489678842:
            l.append(dor)
    return l
    # d = [da for da in data if da.get("id") == 2489678842]
    # return d

def main():

    iter()

if __name__ == "__main__":
    main()
