from math import log
from collections import Counter


class Data:
    def __init__(self):
        self.atribute = None

    def load_from_file(self, nume_fisier, nr_parametri):
        """Incarca datele de antrenament din fisier in care fiecare linie
        reprezinta o instanta si are valorile fiecarui paramtru
        separate prin virgule
        """
        self.nr_parametri = nr_parametri + 1
        self.data = [[] for _ in range(self.nr_parametri)]  # empty list for each param + 1 one for label
        fileObject = open(nume_fisier, 'r')
        linii = fileObject.readlines()
        fileObject.close()
        self.nr_instante = len(linii)  # numarul de instante
        for linie in linii:
            linie = linie[:-1]
            valori_instanta = linie.split(',')
            for i in range(self.nr_parametri):
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
        """
            Clasifica datele si calculeaza entropia pasului in care ne aflam
        """
        self.counter = Counter(self.data[-1])  # [9+,5-]
        self.data_entropy = self.entropy(self.counter.values(), self.nr_instante)

    def get_IG(self, atribut):
        """Determina IG pentru atributul o"""

        counts = Counter(
            self.data[atribut])  # pentru fiecare atribut determin cate instante are fiecare valoare a atributului
        information_gain = self.data_entropy
        for k, v in counts.items():
            count_result = Counter([self.data[-1][i] for i in range(self.nr_instante) if self.data[atribut][i] == k])
            atr_entropy = self.entropy(count_result.values(), v)
            information_gain -= (float(v) / self.nr_instante) * atr_entropy

        return information_gain

    def get_all_IG(self):
        return [(i, self.get_IG(i)) for i in range(self.nr_parametri - 1)]

    def get_best_param(self):
        return sorted(self.get_all_IG(), key=lambda e: e[1], reverse=True)[0][0]

    def is_final(self):
        """Verific daca am ajuns intr-o stare finala adica:
            -toate instantele sunt la fel (EX:[6+,0-])
            -sau nu a mai ramas nici un parametru , i-am folosit pe toti
        """
        return self.nr_instante in self.counter.values() or self.nr_parametri == 1

    def set_atribute(self, p):
        self.atribute = p

    # def debug(self):
    #     s = ""
    #     for i in range(self.nr_instante):
    #         for j in range(self.nr_parametri):
    #             s += "\t" + self.data[j][i]
    #     print (s)


def create_from_other(other, parametru, valoare):
    """
        Creeaza subarborele eliminand parametrul pe care tocmai l-am ales ca si atribut
     si pastrez numai acele instante unde atributul are valoarea specificata
    """
    data = Data()
    data.data = [[] for _ in range(other.nr_parametri)]
    data.nr_instante = 0
    for i in range(other.nr_instante):
        if other.data[parametru][i] == valoare:
            data.nr_instante += 1
            for j in range(other.nr_parametri):
                data.data[j].append(other.data[j][i])
    del data.data[parametru]
    data.nr_parametri = other.nr_parametri - 1
    data.compute_basic()

    if other.atribute:  # debug only
        data.atribute = [p for p in other.atribute]
        del data.atribute[parametru]

    return data
