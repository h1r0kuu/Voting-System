<div class="titlepage">

**System głosowania online**

|                      |                      |
|:--------------------:|:--------------------:|
|   Robert Glapiński   |      Vasyl Kin       |

Warszawa 2024

</div>

- [Wstęp](#wstp)
   * [Cel i zakres pracy](#cel-i-zakres-pracy)
- [Specyfikacja wymagań](#specyfikacja-wymaga)
   * [System Kworum](#system-kworum)
   * [Glosowania](#glosowania)
      + [Zwykle](#zwykle)
      + [Opcjonalne](#opcjonalne)
   * [Uprawnienia użytkowników](#uprawnienia-uytkowników)
      + [Administrator](#administrator)
      + [Sekretarz](#sekretarz)
      + [Uzytkownik](#uzytkownik)
   * [Generowanie raportów](#generowanie-raportów)
      + [Ogólny raport za dany okres](#ogólny-raport-za-dany-okres)
      + [Szczegółowy raport jednego głosowania](#szczegóowy-raport-jednego-gosowania)
   * [Symulator](#symulator)
- [Diagramy](#diagramy)
   * [Diagram scenariuszów użycia](#diagram-scenariuszów-uycia)
   * [Diagram ERD](#diagram-erd)
- [Instalacja i uruchomienie projektu](#instalacja-i-uruchomienie-projektu)
   * [Instalacja pythona](#instalacja-pythona)
   * [Instalacja projektu](#instalacja-projektu)
   * [Instalacja zależności](#instalacja-zalenoci)
   * [Tworzenie migracji](#tworzenie-migracji)
   * [Zastosowanie migracji](#zastosowanie-migracji)
   * [Tworzenie super użytkownika(Opcjonalnie)](#tworzenie-super-uytkownikaopcjonalnie)
   * [Uruchomienie serwera](#uruchomienie-serwera)
- [Jak nadać uprawnienia?](#jak-nada-uprawnienia)
- [Jak zgenerować raport?](#jak-zgenerowa-raport)
         - [Procedura generowania raportów](#procedura-generowania-raportów)
- [Jak uruchomić symulację?](#jak-uruchomi-symulacj)
- [Zrzuty ekranów](#zrzuty-ekranów)
   * [Strona główna](#strona-gówna)
      + [Widok dekstopowy ](#widok-dekstopowy)
      + [Widok mobilny](#widok-mobilny)
   * [Strona głosowania](#strona-gosowania)
      + [Widok dekstopowy](#widok-dekstopowy-1)
      + [Widok mobilny](#widok-mobilny-1)
   * [Strong ustawień użytkownika](#strong-ustawie-uytkownika)
      + [Widok dekstopowy](#widok-dekstopowy-2)
      + [Widok mobilny](#widok-mobilny-2)
   * [Strona paneli administracyjnej](#strona-paneli-administracyjnej)
      + [Widok dekstopowy](#widok-dekstopowy-3)
      + [Widok mobilny](#widok-mobilny-3)
   * [Strona listy objektów w paneli administracyjnej](#strona-listy-objektów-w-paneli-administracyjnej)
      + [Widok dekstopowy](#widok-dekstopowy-4)
      + [Widok mobilny](#widok-mobilny-4)
   * [Stronia tworzenia objekta](#stronia-tworzenia-objekta)
      + [Widok dekstopowy](#widok-dekstopowy-5)
      + [Widok mobilny](#widok-mobilny-5)

<!-- TOC end -->

<!-- TOC --><a name="wstp"></a>
# Wstęp

Rozpoczynamy od przedstawienia kontekstu, w którym projekt ma swoje
miejsce. Obecnie, w erze cyfrowej, rozwój systemów online staje się
coraz bardziej istotny. W tym kontekście pojawia się potrzeba stworzenia
efektywnego systemu głosowania online, który może znacząco ułatwić i
usprawnić procesy decyzyjne.

<!-- TOC --><a name="cel-i-zakres-pracy"></a>
## Cel i zakres pracy

Celem tej dokumentacji jest przedstawienie kompleksowego projektu
systemu głosowania online, który spełni różnorodne potrzeby
użytkowników. Kluczowe cele projektu:

1.  **Usprawnienie procesu decyzyjnego:** Stworzenie systemu, który
    umożliwi szybkie i bezpieczne głosowanie online.

2.  **Zarządzanie uprawnieniami:** Zaimplementowanie hierarchii
    uprawnień, aby skutecznie kontrolować dostęp do funkcji systemu i
    zapewnić bezpieczeństwo operacji.

3.  **Obsługa różnych typów głosowań:** Stworzenie elastycznego systemu,
    który umożliwi przeprowadzenie zarówno prostych głosowań zwykłych,
    jak i bardziej złożonych głosowań na opcje, uwzględniając różne
    scenariusze decyzyjne.

4.  **Odporność na błędy:** Zaprojektowanie systemu w taki sposób, aby
    był odporny na błędy, a także aby umożliwiał łatwe odnajdywanie i
    naprawianie ewentualnych usterek.

5.  **Generowanie raportów:** Umożliwienie sekretarzowi efektywnego
    zarządzania poprzez generowanie czytelnych raportów, które zawierają
    istotne informacje o przeprowadzonych głosowaniach.

Szczególny nacisk w tej pracę kładziemy na osiągnięcie wyżej
wymienionych celów w celu stworzenia nowoczesnego i efektywnego systemu
głosowania online.

<!-- TOC --><a name="specyfikacja-wymaga"></a>
# Specyfikacja wymagań

<!-- TOC --><a name="system-kworum"></a>
## System Kworum

System musi wspierać system kworum. Przy tworzeniu głosowania powinien
być wybór kworum. Aby głosowanie było ważne, liczba głosujących musi być
większa od kworum.

<!-- TOC --><a name="glosowania"></a>
## Glosowania

<!-- TOC --><a name="zwykle"></a>
### Zwykle

Głosowanie zwykłe powinno umożliwiać wybór spośród trzech opcji: "tak",
"nie" oraz "wstrzymuję się". Aby głosowanie było ważne, konieczne jest
spełnienie warunków:

-   **Większość bezwzględna:** Liczba głosujących "ZA" musi być większa
    niż suma głosujących "PRZECIW" i "WSTRZYMUJĘ SIĘ".

-   **Większość względna:** Liczba głosujących "ZA" musi być większa niż
    liczba głosujących "PRZECIW".

<!-- TOC --><a name="opcjonalne"></a>
### Opcjonalne

Głosowanie na opcje powinno umożliwiać wybór spośród maksymalnie pięciu
opcji, a także dodatkowej opcji "wstrzymuję się". Ten rodzaj głosowania
może być wykorzystywany na przykład do wyboru kandydata na dyrektora
spośród 5 zgłoszonych.

<!-- TOC --><a name="uprawnienia-uytkowników"></a>
## Uprawnienia użytkowników

<!-- TOC --><a name="administrator"></a>
### Administrator

Administrator powinien mieć pełne uprawnienia do systemu, umożliwiając
mu zarządzanie użytkownikami, tworzenie, uruchamianie i zatrzymywanie
głosowań, a także generowanie raportów

<!-- TOC --><a name="sekretarz"></a>
### Sekretarz

Sekretarz powinien mieć możliwość tworzenia obu rodzajów głosowań,
definiowania kworum oraz zarządzania otwieraniem i zamykaniem głosowań.
Nie powinien mieć dostępu do funkcji administracyjnych związanych z
zarządzaniem użytkownikami.

<!-- TOC --><a name="uzytkownik"></a>
### Uzytkownik

Użytkownik może głosować tylko wtedy, gdy głosowanie jest otwarte. Ma
również możliwość zmiany swojego głosu w czasie trwania otwartego
głosowania.

<!-- TOC --><a name="generowanie-raportów"></a>
## Generowanie raportów

System powinien posiadać funkcjonalność generowania raportów, dostępną
dla roli sekretarza oraz administratora. Generowane raporty powinny być
w formacie PDF i obejmować dwie główne kategorie: ogólny za dany okres
oraz szczegółowy.

<!-- TOC --><a name="ogólny-raport-za-dany-okres"></a>
### Ogólny raport za dany okres

Sekretarz powinien mieć możliwość wygenerowania ogólnego raportu za
określony okres czasu. Raport ten powinien zawierać:

-   Zestawienie wszystkich przeprowadzonych głosowań w podanym okresie.

-   Liczbę głosujących w każdym z głosowań.

-   Datę przeprowadzenia każdego z głosowań.

-   Wynik każdego z głosowań.

<!-- TOC --><a name="szczegóowy-raport-jednego-gosowania"></a>
### Szczegółowy raport jednego głosowania

Dodatkowo, sekretarz powinien mieć możliwość generowania szczegółowego
raportu dotyczącego pojedynczego głosowania. Ten raport powinien
zawierać pełne dane związane z danym głosowaniem, obejmujące:

-   Szczegóły dotyczące typu głosowania (czy to głosowanie zwykłe czy na
    opcje).

-   Listę opcji w przypadku głosowania na opcje.

-   Liczbę głosujących i ich głosy.

-   Datę przeprowadzenia głosowania.

-   Wyniki głosowania.

<!-- TOC --><a name="symulator"></a>
## Symulator

System powinien także umożliwiać stworzenie zabezpieczonego hasłem pliku
archiwum zawierającego dane z bazy (np. w formie archiwum tar.gz lub
zip). Plik ten będzie dostępny dla sekretarza i administratora, który
poda hasło podczas procesu generowania.

<!-- TOC --><a name="diagramy"></a>
# Diagramy

<!-- TOC --><a name="diagram-scenariuszów-uycia"></a>
## Diagram scenariuszów użycia

<!-- TOC --><a name="diagram-erd"></a>
## Diagram ERD

W tym diagramie nie wykorzystano standardowych modeli, które tworzy
Django(oprócz modeli Group).

<!-- TOC --><a name="instalacja-i-uruchomienie-projektu"></a>
# Instalacja i uruchomienie projektu

<!-- TOC --><a name="instalacja-pythona"></a>
## Instalacja pythona

Aby zainstalować Pythona, należy odwiedzić oficjalną stronę Pythona pod
adresem [](https://www.python.org/downloads/) i pobrać najnowszą wersję.
Po pobraniu pliku instalacyjnego, uruchom go i postępuj zgodnie z
instrukcjami na ekranie, aby zainstalować Pythona.

<!-- TOC --><a name="instalacja-projektu"></a>
## Instalacja projektu

Aby zainstalować projekt Django, najpierw musisz go pobrać. Możesz to
zrobić, odwiedzając stronę projektu na GitHubie pod adresem
[](https://github.com/h1r0kuu/Voting-System) i klikając przycisk "Code"
możesz pobrać archiwum z kodem, lub skopiować link do repozytorium i
użyć go w terminalu z komendą git clone.

``` shell-session
git clone https://github.com/h1r0kuu/Voting-System
```

<!-- TOC --><a name="instalacja-zalenoci"></a>
## Instalacja zależności

Po zainstalowaniu projektu, musisz zainstalować wszystkie zależności
wymagane przez projekt. Zależności te są zazwyczaj wymienione w pliku
requirements.txt w głównym katalogu projektu. Aby zainstalować
zależności, otwórz terminal, przejdź do katalogu projektu i wpisz
komendę:

``` shell-session
pip install -r requirements.txt
```

<!-- TOC --><a name="tworzenie-migracji"></a>
## Tworzenie migracji

Django używa systemu migracji do śledzenia zmian w modelach i do
tworzenia odpowiednich tabel w bazie danych. Komenda makemigrations
tworzy nowe migracje na podstawie zmian, które wprowadziłeś w modelach.

``` shell-session
python manage.py makemigrations
```

<!-- TOC --><a name="zastosowanie-migracji"></a>
## Zastosowanie migracji

Komenda migrate stosuje (lub odwraca) migracje, które zostały utworzone.
To oznacza, że wprowadza zmiany w bazie danych zgodnie z instrukcjami
zawartymi w migracjach.

``` shell-session
python manage.py migrate
```

<!-- TOC --><a name="tworzenie-super-uytkownikaopcjonalnie"></a>
## Tworzenie super użytkownika(Opcjonalnie)

Django umożliwia tworzenie super użytkownika (administratora), który ma
pełny dostęp do strony administracyjnej projektu. Aby utworzyć super
użytkownika, otwórz terminal, przejdź do katalogu projektu i wpisz
komendę:

``` shell-session
python manage.py createsuperuser
```

Następnie postępuj zgodnie z instrukcjami na ekranie, aby ustawić nazwę
użytkownika, adres e-mail(nieobowiązkowo) i hasło dla super użytkownika.
Aby uzyskać dostęp do panelu administracyjnego, przejdź na stronę
[](http://127.0.0.1:8000/admin).

<!-- TOC --><a name="uruchomienie-serwera"></a>
## Uruchomienie serwera

Wreszcie, po zastosowaniu wszystkich migracji, powinieneś być w stanie
uruchomić serwer projektu.

``` shell-session
python manage.py runserver
```

<!-- TOC --><a name="jak-nada-uprawnienia"></a>
# Jak nadać uprawnienia?

W celu nadania uprawnień, należy postępować zgodnie z poniższymi
krokami:

1.  Zaloguj się do panelu administracyjnego
    [](http://127.0.0.1:8000/admin).

2.  Przejdź do sekcji "Użytkownicy".

3.  Znajdź i wybierz użytkownika, któremu chcesz nadać uprawnienia.
    <img src="https://github.com/h1r0kuu/Voting-System/assets/25689732/efff8ae3-f6bb-429a-ace1-2c0b9b305c27" alt="image" />

4.  W sekcji "Grupy" wybierz odpowiednie uprawnienia dla danego
    użytkownika. <img src="https://github.com/h1r0kuu/Voting-System/assets/25689732/6f0948a8-97c7-4c0c-8676-2cbe05db5f26" alt="image" />

5.  Zapisz zmiany.

Pamiętaj, że uprawnienia mogą obejmować takie działania jak zarządzanie
głosowaniami lub użytkownikami. Staraj się nadawać uprawnienia zgodnie z
potrzebami i odpowiedzialnościami poszczególnych użytkowników.

<!-- TOC --><a name="jak-zgenerowa-raport"></a>
# Jak zgenerować raport?

<!-- TOC --><a name="procedura-generowania-raportów"></a>
#### Procedura generowania raportów

Sekretarz może generować raporty poprzez wykonanie następujących kroków
w panelu administracyjnym:

1.  Przejdź do panelu administracyjnego [](http://127.0.0.1:8000/admin)

2.  Przejście do sekcji "Głosowania".

3.  Z listy dostępnych głosowań, wybierz jedno lub kilka głosowań.

4.  Wybieranie opcji "Wygeneruj raport".

5.  Naciśnięcie przycisku "Wykonaj".

6.  Pobieranie wygenerowanego pliku PDF-raportu.

W przypadku generowania raportów dla wielu głosowań jednocześnie, system
umożliwia pobranie archiwum z zestawem plików PDF dla każdego z
wybranych raportów. <img src="https://github.com/h1r0kuu/Voting-System/assets/25689732/1f6ec749-7908-43c3-8e0e-420f8879c34b" alt="image" />

<!-- TOC --><a name="jak-uruchomi-symulacj"></a>
# Jak uruchomić symulację?

Aby uruchomić symulację, można użyć następującego polecenia w terminalu:

``` shell-session
python manage.py simulate
```

Przykład tego, jak powinno to wyglądać w terminalu:
<img src="https://github.com/h1r0kuu/Voting-System/assets/25689732/4d9a67ed-e489-47e2-8564-c81c386e96f6" alt="image" /> Opis tego, co dzieje się po
wywołaniu tego polecenia:

1.  **Usuwanie starych danych:** Polecenie rozpoczyna się od usunięcia
    wszystkich starych danych z modeli `Vote`, `User`, `Voting` i
    `VotingOption`. Nie usuwa jednak użytkowników, którzy są
    superużytkownikami.

2.  **Tworzenie nowych danych:** Następnie polecenie tworzy nowe dane
    dla modeli. Rozpoczyna się od utworzenia grup użytkowników o nazwach
    "admin", "sekretarz" i "użytkownik".

3.  **Tworzenie nowych użytkowników:** Tworzy określoną liczbę
    użytkowników (`100`) i losowo przypisuje ich do jednej z grup.

4.  **Tworzenie nowych głosowań:** Tworzy określoną liczbę głosowań
    (`50`). Jeśli typ głosowania to "O", tworzy również opcje głosowania
    dla każdego głosowania.

5.  **Tworzenie głosów użytkownika:** Dla każdego głosowania losowo
    decyduje, czy każdy użytkownik zagłosuje, czy nie. Jeśli użytkownik
    zagłosuje, losowo wybierana jest opcja, na którą użytkownik
    zagłosuje.

<!-- TOC --><a name="zrzuty-ekranów"></a>
# Zrzuty ekranów

<!-- TOC --><a name="strona-gówna"></a>
## Strona główna

<!-- TOC --><a name="widok-dekstopowy"></a>
### Widok dekstopowy 

<img src="https://github.com/h1r0kuu/Voting-System/assets/25689732/80aea415-9df5-4a6a-9145-02bc3bed1a3c" alt="image" />

<!-- TOC --><a name="widok-mobilny"></a>
### Widok mobilny

<img src="https://github.com/h1r0kuu/Voting-System/assets/25689732/2a6eff0a-34f9-4f70-9988-8580f104dc73" alt="image" />

<!-- TOC --><a name="strona-gosowania"></a>
## Strona głosowania

<!-- TOC --><a name="widok-dekstopowy-1"></a>
### Widok dekstopowy

<img src="https://github.com/h1r0kuu/Voting-System/assets/25689732/f706811d-9675-45a2-af16-e2e42cc46f09" alt="image" />

<!-- TOC --><a name="widok-mobilny-1"></a>
### Widok mobilny

<img src="https://github.com/h1r0kuu/Voting-System/assets/25689732/3a0d8bae-e764-4028-af5d-cc1b3b49f0f8" alt="image" />

<!-- TOC --><a name="strong-ustawie-uytkownika"></a>
## Strong ustawień użytkownika

<!-- TOC --><a name="widok-dekstopowy-2"></a>
### Widok dekstopowy

<img src="https://github.com/h1r0kuu/Voting-System/assets/25689732/082386fb-bc59-461c-9c09-df65c91d2b5d" alt="image" />

<!-- TOC --><a name="widok-mobilny-2"></a>
### Widok mobilny

<img src="https://github.com/h1r0kuu/Voting-System/assets/25689732/73cf93f8-82f5-49ef-8594-47b8cd62eac8" alt="image" />

<!-- TOC --><a name="strona-paneli-administracyjnej"></a>
## Strona paneli administracyjnej

<!-- TOC --><a name="widok-dekstopowy-3"></a>
### Widok dekstopowy

<img src="https://github.com/h1r0kuu/Voting-System/assets/25689732/c3e30f86-affb-4cb3-9c0e-b2e81d0464db" alt="image" />

<!-- TOC --><a name="widok-mobilny-3"></a>
### Widok mobilny

<img src="https://github.com/h1r0kuu/Voting-System/assets/25689732/3b98bb15-61ed-4d11-991e-fad56cad16bc" alt="image" />

<!-- TOC --><a name="strona-listy-objektów-w-paneli-administracyjnej"></a>
## Strona listy objektów w paneli administracyjnej

<!-- TOC --><a name="widok-dekstopowy-4"></a>
### Widok dekstopowy

<img src="https://github.com/h1r0kuu/Voting-System/assets/25689732/b5671f24-ad59-4ab3-b99f-8646589eba70" alt="image" />

<!-- TOC --><a name="widok-mobilny-4"></a>
### Widok mobilny

<img src="https://github.com/h1r0kuu/Voting-System/assets/25689732/fce268b9-c3b6-44a5-bbee-6380ac6c5056" alt="image" />

<!-- TOC --><a name="stronia-tworzenia-objekta"></a>
## Stronia tworzenia objekta

<!-- TOC --><a name="widok-dekstopowy-5"></a>
### Widok dekstopowy

<img src="https://github.com/h1r0kuu/Voting-System/assets/25689732/4842049c-f24b-4ca5-aff4-5e11eb41ac24" alt="image" />

<!-- TOC --><a name="widok-mobilny-5"></a>
### Widok mobilny

<img src="https://github.com/h1r0kuu/Voting-System/assets/25689732/b0e96d66-3b22-46bf-a87e-90c20f0f92d6" alt="image" />
