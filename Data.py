from math import log
from collections import Counter


class Data:
    def __init__(self):
        self.atribute = None

    def load_from_file(self, nume_fisier: str, nr_parametri: int):
        """
        Functie ce se ocupa cu incarcarea datele de antrenament din fisier in care fiecare linie
        reprezinta o instanta si are valorile fiecarui paramtru
        separate prin virgule
        :param nume_fisier:Numele fisierului din care vreau sa citesc datele de antrenament
        :param nr_parametri: Numarul de atribute , fara atributul de output
        :return: None
        """

        self.nr_parametri = nr_parametri + 1
        self.instante = [[] for _ in range(self.nr_parametri)]  # lista ce va contine valorile pt fiecare atribut
        fileObject = open(nume_fisier, 'r')
        linii = fileObject.readlines()
        fileObject.close()
        self.nr_instante = len(linii)  # numarul de instante
        for linie in linii:
            linie = linie[:-1]
            valori_instanta = linie.split(',')
            for i in range(self.nr_parametri):
                self.instante[i].append(valori_instanta[i])
        self.compute_basic()

    def entropy(self, results: Counter, nr_instante: int) -> float:
        """
            Functie ce se ocupa cu calculul entropiei
        :param results: [+9,5-] Clasificare datelor in functie de valorile atributului
        :param nr_instante: Numarul de instante
        :return: Entropia pentru clasificarea [9+,5-] atributului primit ca parametru
        """
        entropie = 0.0
        for r in results:
            r = float(r)
            entropie += (r / nr_instante) * log(nr_instante / r, 2) if r != 0.0 else 0
        return entropie

    def compute_basic(self):
        """
           Functie ce clasifica datele si calculeaza entropia pasului in care ne aflam
        :return:
        """
        self.counter = Counter(self.instante[-1])  # [9+,5-]
        self.data_entropy = self.entropy(self.counter.values(), self.nr_instante)

    def get_IG(self, atribut):
        """
            Functie ce calculeaza IG(Castigul de Informatii) pentru
            atributul primit ca si parametru
        :param atribut: Atributul pentru care doresc ca calculez IG
        :return:
        """

        # pentru fiecare atribut determin cate instante are fiecare valoare a atributului
        counts = Counter(self.instante[atribut])  # [9+,5-]
        information_gain = self.data_entropy
        for cheie, valoare in counts.items():
            count_result = Counter(
                [self.instante[-1][i] for i in range(self.nr_instante) if self.instante[atribut][i] == cheie])
            atr_entropy = self.entropy(count_result.values(), valoare)
            information_gain -= (float(valoare) / self.nr_instante) * atr_entropy

        return information_gain

    def get_all_IG(self):
        """
            Functie ce calculeaza toate castigurile de informatii
        :return: O lista cu toate castigurile de informatii
        """
        return [(i, self.get_IG(i)) for i in range(self.nr_parametri - 1)]

    def get_best_param(self):
        """
            Functie ce imi returneaza atributul cu cel mai mare castig de informatii
            atribut va fi un dictionar [0]-> numele atributului [1]->IG respectiv
        :return: Atriburul cu IG cel mai mare
        """
        return sorted(self.get_all_IG(), key=lambda atribut: atribut[1], reverse=True)[0][0]

    def is_final(self):
        """
            Functie ce verific daca am ajuns intr-o stare finala adica:
                -toate instantele sunt la fel (EX:[6+,0-])
                -sau nu a mai ramas nici un parametru , i-am folosit pe toti
        :return: True => daca sunt intr-o stare finala /n False altfel
        """
        return self.nr_instante in self.counter.values() or self.nr_parametri == 1

    def set_atribute(self, atribute: list):
        """
            Functie ce seteaza atributele disponibile
        :param atribute: Lista cu numele atributelor (fara atributul de output)
        :return:
        """
        self.atribute = atribute

        # def debug(self):
        #     s = ""
        #     for i in range(self.nr_instante):
        #         for j in range(self.nr_parametri):
        #             s += "\t" + self.data[j][i]
        #     print (s)


def create_from_other(other, parametru: int, valoare: str):
    """
        Functie ce  creeaza subarborele eliminand parametrul pe care tocmai l-am ales ca si atribut
        si pastrez numai acele instante unde atributul are valoarea specificata
    :param other:
    :param parametru: Parametrul pe care l-am ales ca si atribut la pasul anterior(indicile lui din lista de atribute)
    :param valoare: Valoarea atributului pe care l-am ales ca si atribut la pasul anterior
    :return: Datele necesare pentru construirea in continuare a arborelui ID3
    """
    data = Data()
    data.instante = [[] for _ in range(other.nr_parametri)]
    # Imi elimin din datele anterioare instantele atributului pe care l-am
    # ales la pasul anterior
    for i in range(other.nr_instante):
        if other.instante[parametru][i] == valoare:
            for j in range(other.nr_parametri):
                data.instante[j].append(other.instante[j][i])
    del data.instante[parametru]
    data.nr_parametri = other.nr_parametri - 1
    data.compute_basic()

    if other.atribute:  # debug only
        data.atribute = [p for p in other.atribute]
        del data.atribute[parametru]

    return data
