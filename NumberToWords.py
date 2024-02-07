def kwota_slownie(liczba):
    zl = int(liczba)
    gr = round((liczba - zl) * 100)

    if zl % 10 in [1, 5, 6, 7, 8, 9, 0]:
        waluta1 = "złotych"
    else:
        waluta1 = "złote"

    if gr % 10 in [1, 5, 6, 7, 8, 9, 0]:
        waluta2 = "groszy"
    else:
        waluta2 = "grosze"

    zl_slownie = liczba_slownie(zl)
    gr_slownie = liczba_slownie(gr)

    result =  f"{zl_slownie} {waluta1} {gr_slownie} {waluta2}"
    result = ' '.join(result.split())

    return result

def liczba_slownie(liczba):
    jednosci = ['', 'jeden', 'dwa', 'trzy', 'cztery', 'pięć', 'sześć', 'siedem', 'osiem', 'dziewięć']
    nascie = ['', 'jedenaście', 'dwanaście', 'trzynaście', 'czternaście', 'piętnaście', 'szesnaście', 'siedemnaście', 'osiemnaście', 'dziewiętnaście']
    dziesiatki = ['', 'dziesięć', 'dwadzieścia', 'trzydzieści', 'czterdzieści', 'pięćdziesiąt', 'sześćdziesiąt', 'siedemdziesiąt', 'osiemdziesiąt', 'dziewięćdziesiąt']
    setki = ['', 'sto', 'dwieście', 'trzysta', 'czterysta', 'pięćset', 'sześćset', 'siedemset', 'osiemset', 'dziewięćset']

    grupy = [
        ('', '', ''),
        (' tysiąc', ' tysiące', ' tysięcy'),
        (' milion', ' miliony', ' milionów'),
        (' miliard', ' miliardy', ' miliardów'),
        (' bilion', ' biliony', ' bilionów'),
        (' biliard', ' biliardy', ' biliardów'),
        (' trylion', ' tryliony', ' trylionów')
    ]

    if liczba == 0:
        return 'zero'

    if liczba < 0:
        znak = 'minus'
        liczba = -liczba
    else:
        znak = ''

    wynik = ''
    g = 0

    while liczba != 0:
        s = liczba % 1000 // 100
        d = liczba % 100 // 10
        j = liczba % 10

        if d == 1 and j > 0:
            n = j
            d = 0
            j = 0
        else:
            n = 0

        if j == 1 and s + d + n == 0:
            k = 0
        elif 2 <= j <= 4:
            k = 1
        else:
            k = 2

        if s + d + n + j > 0:
            wynik = setki[s] + ' ' + dziesiatki[d] + ' ' + nascie[n] + ' ' + jednosci[j] + grupy[g][k] + ' ' + wynik

        g += 1
        liczba //= 1000

    return znak + wynik.strip()