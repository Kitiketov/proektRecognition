import Levenshtein


TEST_COUNT = 7
FOLDERS = ["My solution","Base model(without algo)","Yandex","Convertio"]

print(f"testN |{'   '.join(FOLDERS)}")

for i in range(1,TEST_COUNT+1):
    f1 = open(f"testing/tests/test{i}/text.txt")
    a = ''.join(f1.readlines())
    n = len(a)

    result = []

    for folder in FOLDERS:
        f2 = open(f"testing/result/{folder}/test{i}.txt")
        b = ''.join(f2.readlines())

        l = Levenshtein.distance(a,b)

        percent = f'{l/(n):<{len(folder)}.1%}'
        result.append(percent)

    print(f"  {i}   |{'   '.join(result)}")

