import Levenshtein


TEST_COUNT = 5
FOLDERS = ["My solution","Base model(without algo)","Base model(with algo)","Yandex","Convertio"]

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

"""
90.68%
82.67%
100.00%
87.79%
99.36%
"""
"""
87.30%
77.89%
93.67%
80.30%
78.39%
"""
"""
84.09%
82.23%
90.99%
78.55%
75.97%
"""