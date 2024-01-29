<div class="titlepage">

**System głosowania online**

|                      |                      |
|:--------------------:|:--------------------:|
|   Robert Glapiński   |      Vasyl Kin       |
| numer albumu: 157155 | numer albumu: 158609 |

Warszawa 2024

</div>

# Wstęp

Rozpoczynamy od przedstawienia kontekstu, w którym projekt ma swoje
miejsce. Obecnie, w erze cyfrowej, rozwój systemów online staje się
coraz bardziej istotny. W tym kontekście pojawia się potrzeba stworzenia
efektywnego systemu głosowania online, który może znacząco ułatwić i
usprawnić procesy decyzyjne.

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

# Specyfikacja wymagań

## System Kworum

System musi wspierać system kworum. Przy tworzeniu głosowania powinien
być wybór kworum. Aby głosowanie było ważne, liczba głosujących musi być
większa od kworum.

## Glosowania

### Zwykle

Głosowanie zwykłe powinno umożliwiać wybór spośród trzech opcji: "tak",
"nie" oraz "wstrzymuję się". Aby głosowanie było ważne, konieczne jest
spełnienie warunków:

-   **Większość bezwzględna:** Liczba głosujących "ZA" musi być większa
    niż suma głosujących "PRZECIW" i "WSTRZYMUJĘ SIĘ".

-   **Większość względna:** Liczba głosujących "ZA" musi być większa niż
    liczba głosujących "PRZECIW".

### Opcjonalne

Głosowanie na opcje powinno umożliwiać wybór spośród maksymalnie pięciu
opcji, a także dodatkowej opcji "wstrzymuję się". Ten rodzaj głosowania
może być wykorzystywany na przykład do wyboru kandydata na dyrektora
spośród 5 zgłoszonych.

## Uprawnienia użytkowników

### Administrator

Administrator powinien mieć pełne uprawnienia do systemu, umożliwiając
mu zarządzanie użytkownikami, tworzenie, uruchamianie i zatrzymywanie
głosowań, a także generowanie raportów

### Sekretarz

Sekretarz powinien mieć możliwość tworzenia obu rodzajów głosowań,
definiowania kworum oraz zarządzania otwieraniem i zamykaniem głosowań.
Nie powinien mieć dostępu do funkcji administracyjnych związanych z
zarządzaniem użytkownikami.

### Uzytkownik

Użytkownik może głosować tylko wtedy, gdy głosowanie jest otwarte. Ma
również możliwość zmiany swojego głosu w czasie trwania otwartego
głosowania.

## Generowanie raportów

System powinien posiadać funkcjonalność generowania raportów, dostępną
dla roli sekretarza oraz administratora. Generowane raporty powinny być
w formacie PDF i obejmować dwie główne kategorie: ogólny za dany okres
oraz szczegółowy.

### Ogólny raport za dany okres

Sekretarz powinien mieć możliwość wygenerowania ogólnego raportu za
określony okres czasu. Raport ten powinien zawierać:

-   Zestawienie wszystkich przeprowadzonych głosowań w podanym okresie.

-   Liczbę głosujących w każdym z głosowań.

-   Datę przeprowadzenia każdego z głosowań.

-   Wynik każdego z głosowań.

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

## Symulator

System powinien także umożliwiać stworzenie zabezpieczonego hasłem pliku
archiwum zawierającego dane z bazy (np. w formie archiwum tar.gz lub
zip). Plik ten będzie dostępny dla sekretarza i administratora, który
poda hasło podczas procesu generowania.

# Diagramy

## Diagram scenariuszów użycia

## Diagram ERD

W tym diagramie nie wykorzystano standardowych modeli, które tworzy
Django(oprócz modeli Group).

# Instalacja i uruchomienie projektu

## Instalacja pythona

Aby zainstalować Pythona, należy odwiedzić oficjalną stronę Pythona pod
adresem [](https://www.python.org/downloads/) i pobrać najnowszą wersję.
Po pobraniu pliku instalacyjnego, uruchom go i postępuj zgodnie z
instrukcjami na ekranie, aby zainstalować Pythona.

## Instalacja projektu

Aby zainstalować projekt Django, najpierw musisz go pobrać. Możesz to
zrobić, odwiedzając stronę projektu na GitHubie pod adresem
[](https://github.com/h1r0kuu/Voting-System) i klikając przycisk "Code"
możesz pobrać archiwum z kodem, lub skopiować link do repozytorium i
użyć go w terminalu z komendą git clone.

``` shell-session
git clone https://github.com/h1r0kuu/Voting-System
```

## Instalacja zależności

Po zainstalowaniu projektu, musisz zainstalować wszystkie zależności
wymagane przez projekt. Zależności te są zazwyczaj wymienione w pliku
requirements.txt w głównym katalogu projektu. Aby zainstalować
zależności, otwórz terminal, przejdź do katalogu projektu i wpisz
komendę:

``` shell-session
pip install -r requirements.txt
```

## Tworzenie migracji

Django używa systemu migracji do śledzenia zmian w modelach i do
tworzenia odpowiednich tabel w bazie danych. Komenda makemigrations
tworzy nowe migracje na podstawie zmian, które wprowadziłeś w modelach.

``` shell-session
python manage.py makemigrations
```

## Zastosowanie migracji

Komenda migrate stosuje (lub odwraca) migracje, które zostały utworzone.
To oznacza, że wprowadza zmiany w bazie danych zgodnie z instrukcjami
zawartymi w migracjach.

``` shell-session
python manage.py migrate
```

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

## Uruchomienie serwera

Wreszcie, po zastosowaniu wszystkich migracji, powinieneś być w stanie
uruchomić serwer projektu.

``` shell-session
python manage.py runserver
```

# Jak nadać uprawnienia?

W celu nadania uprawnień, należy postępować zgodnie z poniższymi
krokami:

1.  Zaloguj się do panelu administracyjnego
    [](http://127.0.0.1:8000/admin).

2.  Przejdź do sekcji "Użytkownicy".

3.  Znajdź i wybierz użytkownika, któremu chcesz nadać uprawnienia.
    <img src="user-list.png" alt="image" />

4.  W sekcji "Grupy" wybierz odpowiednie uprawnienia dla danego
    użytkownika. <img src="uprawnienia.png" alt="image" />

5.  Zapisz zmiany.

Pamiętaj, że uprawnienia mogą obejmować takie działania jak zarządzanie
głosowaniami lub użytkownikami. Staraj się nadawać uprawnienia zgodnie z
potrzebami i odpowiedzialnościami poszczególnych użytkowników.

# Jak zgenerować raport?

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
wybranych raportów. <img src="Raport.png" alt="image" />

# Jak uruchomić symulację?

Aby uruchomić symulację, można użyć następującego polecenia w terminalu:

``` shell-session
python manage.py simulate
```

Przykład tego, jak powinno to wyglądać w terminalu:
<img src="simulate.jpg" alt="image" /> Opis tego, co dzieje się po
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

# Zrzuty ekranów

## Strona główna

### Widok dekstopowy 

<img src="home.png" alt="image" />

### Widok mobilny

<img src="home_mobile.png" alt="image" />

## Strona głosowania

### Widok dekstopowy

<img src="vote_detail.png" alt="image" />

### Widok mobilny

<img src="vote_detail_mobile.png" alt="image" />

## Strong ustawień użytkownika

### Widok dekstopowy

<img src="settings.png" alt="image" />

### Widok mobilny

<img src="settings_mobile.png" alt="image" />

## Strona paneli administracyjnej

### Widok dekstopowy

<img src="admin_panel.png" alt="image" />

### Widok mobilny

<img src="admin_panel_mobile.png" alt="image" />

## Strona listy objektów w paneli administracyjnej

### Widok dekstopowy

<img src="model_detail.png" alt="image" />

### Widok mobilny

<img src="model_detail_mobile.png" alt="image" />

## Stronia tworzenia objekta

### Widok dekstopowy

<img src="voting_creation.png" alt="image" />

### Widok mobilny

<img src="voting_creation_mobile.png" alt="image" />
