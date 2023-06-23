from module.config import timing_decorator,memoize
import json
import os


@timing_decorator
def iter():
    d = 0
    l = list()
    for dor in os.listdir("module/template_generator/ready/expertnayaCep_VO/expertnayaCep_VO_pp"):

        l.append(dor)
        dor = dor.replace(".html","")

        print(dor)
        with open('ekspertn_VO_pp_list_names.txt','a',encoding="utf-8") as f:
            f.write(f"\"{dor}\"\n")

    return l
    # d = [da for da in data if da.get("id") == 2489678842]
    # return d

def main():

    iter()

if __name__ == "__main__":
    main()
