from math import log
from collections import Counter


class Data:
    def __init__(self):
        self.atribute = None

    def load_from_file(self, file_name, nr_params):
        """Incarca datele de antrenament din fisier in care fiecare linie
        reprezinta o instanta si are valorile fiecarui paramtru
        separate prin virgule
        """
        self.n = nr_params + 1
        self.data = [[] for _ in range(self.n)]  # empty list for each param + 1 one for label        
        f = open(file_name, 'r')
        lines = f.readlines()
        f.close()
        self.nr = len(lines)
        for line in lines:
            line = line[:-1]
            valori_instanta = line.split(',')
            for i in range(self.n):
                self.data[i].append(valori_instanta[i])
        self.compute_basic()

    def entropy(self, results, nr):
        """Calcululul entropiei
        """
        entropie = 0.0
        for r in results:
            r = float(r)
            entropie += (r / nr) * log(nr / r, 2) if r != 0.0 else 0
        return entropie

    def compute_basic(self):
        """Count the evaluation result and the data's overall entropy
        """
        self.counter = Counter(self.data[-1]) #[9+,5-]
        self.data_entropy = self.entropy(self.counter.values(), self.nr)

    def get_IG(self, atribut):
        """Determina IG pentru atributul o"""

        counts = Counter(self.data[atribut])  # pentru fiecare atribut determin cate instante are fiecare valoare a atributului
        information_gain = self.data_entropy
        for k, v in counts.items():
            count_result = Counter([self.data[-1][i] for i in range(self.nr) if self.data[atribut][i] == k])
            atr_entropy = self.entropy(count_result.values(), v)
            information_gain -= (float(v) / self.nr) * atr_entropy

        return information_gain

    def get_all_IG(self):
        return [(i, self.get_IG(i)) for i in range(self.n - 1)]

    def get_best_param(self):
        return sorted(self.get_all_IG(), key=lambda e: e[1], reverse=True)[0][0]

    def is_final(self):
        """Final state if all instance are the same
        or there is no parameter left
        [6,0] sau m-am folosit de toti parametri
        """
        return self.nr in self.counter.values() or self.n == 1

    def set_atribute(self, p):
        self.atribute = p

    # def debug(self):
    #     s = ""
    #     for i in range(self.nr):
    #         for j in range(self.n):
    #             s += "\t" + self.data[j][i]
    #     print s


def create_from_other(other, param, value):
    """Load training data set from other data set while eliminating
    the parameter param and keeping only the instances where param 
    had the specificated value. 
    """
    data = Data()
    data.data = [[] for _ in range(other.n)]
    data.nr = 0
    for i in range(other.nr):
        if other.data[param][i] == value:
            data.nr += 1
            for j in range(other.n):
                data.data[j].append(other.data[j][i])
    del data.data[param]
    data.n = other.n - 1
    data.compute_basic()

    if other.atribute:  # debug only
        data.atribute = [p for p in other.atribute]
        del data.atribute[param]

    return data
