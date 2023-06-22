from module.config import timing_decorator,memoize
import json



@timing_decorator
def iter():
    d = 0
    l = list()
    with open('docForparse\\Аккред ОТ 2021 ОБЩЕЕ.json','r',encoding="utf-8") as f:
        data: list[dict] = json.loads(f.read())
    for dor in data:
        try:
            dor['spec'] = dor['spec'].strip()
        except:
            dor['spec'] = None
        try:
            dor['job'] = dor['job'].strip().split(";")
        except:
             dor['job'] = None
        try:
            dor['pp'] = dor['pp'].strip().split(";")
        except:
            dor['pp'] = None
        l.append(dor)


        print(dor)
    with open('docForparse\\Аккред ОТ 2021 ОБЩЕЕedit.json','w',encoding="utf-8") as f:
        json.dump(l,f,ensure_ascii=False,indent=4)

    return l
    # d = [da for da in data if da.get("id") == 2489678842]
    # return d

def main():

    iter()

if __name__ == "__main__":
    main()
