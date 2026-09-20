import json
from pathlib import Path
def encode(vhod: list) -> tuple[list, list]:
    """
    Izvede kodiranje vhodnega sporočila z algoritmom BPE.

    Parameters
    ----------
    vhod : list
        Seznam vhodnih znakov ASCII.

    Returns
    -------
    (izhod, izhodS) : tuple[list, list]
        izhod : list
            Kodirano vhodno sporočilo v obliki indeksov.
        izhodS : list
            Seznam ASCII kod in parov indeksov.
    """
    
    simboli = [ord(c) for c in vhod]

    izhodS = list(range(256))
    izhod = []
    nova_koda = 256
    while True:
        if len(izhodS) >= 4096:
            break

        maxx = 0
        max_par = None
        frekvenca = {} 
   
        for i in range(len(simboli) - 1):
            par = (simboli[i], simboli[i+1])
            frekvenca[par] = frekvenca.get(par, 0) + 1

            if frekvenca[par] > maxx:
                maxx = frekvenca[par]
                max_par = par


        if maxx < 2:
            break
    
        izhodS.append([max_par[0], max_par[1]])

        menjava = []
        i = 0
        while i < len(simboli):
            if i < len(simboli) - 1 and (simboli[i], simboli[i + 1]) == max_par:
                menjava.append(nova_koda)
                i += 2
            else:
                menjava.append(simboli[i])
                i += 1

        simboli = menjava
        nova_koda += 1
    
    izhod = simboli


    return (izhod, izhodS)

#vhod = list("ABABABA")
#print(encode(vhod))

def decode(vhod: list, S: list) -> list:
    """
    Izvede dekodiranje vhodnega zaporedja indeksov z algoritmom BPE.
    Debug izpis pokaže st_parov in stanje po vsaki iteraciji.
    """

    st_parov = len(S) - 256

    izhod_kode = vhod.copy()


    for i in range(st_parov-1, -1, -1):

        iskana_koda = 256 + i
        par = S[256 + i]

        menjava = []

        for x in izhod_kode:
            if x == iskana_koda:
                menjava.append(par[0])
                menjava.append(par[1])
            else:
                menjava.append(x)

        izhod_kode = menjava

    # Prevedemo v znake šele na koncu
    izhod = [chr(x) for x in izhod_kode]
    return izhod

def compute_compression_ratio(vhod: list, izhod: list) -> float:
    """
    Izračuna kompresijsko razmerje.

    Parameters
    ----------
    vhod : list
        Vhodno zaporedje.
    izhod : list
        Izhodno zaporedje.
    mode : str
        Način izračuna.

    Returns
    -------
    R : float
        Kompresijsko razmerje.
    """

    R = float('nan')
    if len(izhod) > 0:
        R = (len(vhod)*8) / (len(izhod)*12)
    return R

# Vhodni niz
#vhod = list("abcabcabcabc xyzxyzxyzxyz 123123123123 abcabcabcabc xyzxyzxyzxyz 123123123123")

# Kodiranje
#izhod, izhodS = encode(vhod)
#print("Encode izhod:", izhod)
#print("Encode izhodS:", izhodS)

# Dekodiranje
#dekodirano = decode(izhod, izhodS)
#print("Decode izhod:", dekodirano)


def read_raw_text(path: str) -> list:
    """
    Prebere besedilno datoteko in vrne seznam znakov.

    Parameters
    ----------
    path : str
        Pot do vhodne datoteke .txt.

    Returns
    -------
    list
        Seznam znakov iz datoteke.
    """
    return list(Path(path).read_text(encoding="ascii"))


def write_raw_text(path: str, znaki: list) -> None:
    """
    Zapise seznam znakov v besedilno datoteko.

    Parameters
    ----------
    path : str
        Pot do izhodne datoteke .txt.
    znaki : list
        Seznam znakov za zapis.
    """
    Path(path).write_text("".join(znaki), encoding="ascii")


def read_coded_msg(path: str) -> tuple[list, list]:
    """
    Prebere JSON datoteko z izhodoma funkcije encode.

    Parameters
    ----------
    path : str
        Pot do vhodne datoteke .json.

    Returns
    -------
    tuple[list, list]
        Par seznamov (izhod, izhodS).
    """
    data = json.loads(Path(path).read_text(encoding="ascii"))
    return data["kodirano"], data["slovar"]

def write_coded_msg(path: str, izhod: list, izhodS: list) -> None:
    """
    Zapise izhoda funkcije encode v JSON datoteko.

    Parameters
    ----------
    path : str
        Pot do izhodne datoteke .json.
    izhod : list
        Kodirano sporocilo.
    izhodS : list
        Seznam ASCII kod in parov indeksov.
    """
    data = {
        "kodirano": izhod,
        "slovar": izhodS,
    }
    Path(path).write_text(
        json.dumps(data, ensure_ascii=False, indent=4),
        encoding="ascii",
    )


if __name__ == "__main__":
    
    vhod = read_raw_text("sample_transactions.txt")

    izhod, izhodS = encode(vhod)

    write_coded_msg(
        "compressed.json",
        izhod,
        izhodS
    )

    razmerje = compute_compression_ratio(vhod, izhod)

    print(f"Originalna dolžina: {len(vhod)}")
    print(f"Stisnjena dolžina: {len(izhod)}")
    print(f"Kompresijsko razmerje: {razmerje:.2f}x")

    dekodirano = decode(izhod, izhodS)

    assert dekodirano == vhod

    print("Dekodiranje uspešno, podatki so enaki originalu.")