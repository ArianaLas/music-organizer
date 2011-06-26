MP3 Organizer
=============

Automatycznie organizuj, sortuj lub zminiaj nazwy plików Twojej kolekcji muzycznej.

Wymagania
=========

* Python 3
* PyQt4 (opcjonalnie - do interfejsu graficznego)
* stagger (http://code.google.com/p/stagger/)

W Arch Linux po prostu napisz:

	# pacman -Sy python pyqt
	$ yaourt -S python3-stagger-svn

Jeżeli nie korzystasz z Yaourta, pobierz **PKGBUILD** dla paczki **python3-stagger-svn** z AUR i ręcznie stwórz pakiet:
	
	$ makepkg

Następnie pakiet ten zainstaluj korzystająć z  **pacman -U**.

W przypadku innych dystrybucji proszę zwrócić uwagę na **wersję Pythona**, wymagana jest **3.X** lub nowsza.

Wymagania - Windows
===================

W systemie Windows wymagania są te same, postaram się w skrócie opisać proces instalacji każdego z nich.

* Python 3
	* Po prostu pobierz i zainstaluj odpowiednią dla Twojej wersji systemu wersję Pythona (http://python.org/download/releases/3.2/).
* PyQt
	* Pobierz odpowiednią paczkę z sekcji "Binary Packages" ze strony: http://www.riverbankcomputing.co.uk/software/pyqt/download
* stagger
	* Tutaj sprawa jest trochę bardziej skomplikowana, potrzebujemy pobrać źródła biblioteki i "ręcznie" ją zainstlować.
	* Pobierzmy bibliotekę: http://pypi.python.org/pypi/stagger
	* Uruchamiamy terminal (Start->Uruchom i wpisujemy `cmd`)
	* W terminalu przechodzimy do miejsca gdzie rozpakowaliśmy pliki biblioteki (chodzi o miejsce w którym znajduje się plik setup.py) np. `cd C:\stagger\dist`
	* Uruchamiamy *instalator* biblioteki: `setup.py build`, następnie: `setup.py install`

W przyszłości postaram się te kroki uprościć lub całkowicie wyeliminować (własny instalator).

Użycie
======

Uruchom bez żadnych opcji aby włączyć tryb z interfejsem graficznym:

	$ ./mp3-organizer.py 

Aby skorzystać z interfejsu tekstowego wystarczy podać jedną z obsługowanych opcji, ich listę można wyświetlić w ten sposób:

	$ ./mp3-organizer.py --help

Opis opcji
==========

* **-t** lub **--target-directory** - sprecyzuj gdzie przenosić/kopiować napotkane pliki MP3
* **-p** lub **--path** - sprecyzuj gdzie szukać plików MP3
* **-d** lub **--delete** - próbuj usuwać przejrzane katalogi po przeniesieniu/skopiowaniu muzyki (tylko jeżeli puste)
* **-f** lub **--force** - agresywnie usuwaj przejrzane katalogi (nawet jeżeli zawierają inne pliki)
* **-r** lub **--recursive** - rekurencyjnie przeglądaj katalogi (szukaj również w katagach katalogów itd.)
* **-c** lub **--copy** - kopiuj zamiast przenosić
* **-s** lub **--scheme** - sprecyzuj schemat działania; *domyślnie*: **{artist}/{album}/{title}**; *dostępne*: {artist} {album} {date} {title} {old-file-name} {genre} {track}
* **-h** lub **--help** - wyświetl pomoc
* **-v** lub **--verbose** - wypisuj dokładnie co robisz
* **--recognize-covers** - próbuj wykrywać okładki (przenoś również obrazki)
* **--follow** - podążaj również za dowiązaniami (linkami/skrótami)

Przykłady
=========

	$ mp3-organizer -p ~/Music/ -t ~/Music/ -r --recognize-covers

Rekurencyjnie (przeglądaj również katalogi w katalogach) organizuj katalog *~/Music/* (opcja -p), pliki wynikowe składuj w tym samym katalogu (opcja -t). Dodatkowo próbuj rozpoznawać okładki (opcja --recognize-covers).

	$ mkdir ~/Music # (tworzenie pustego katalogu ~/Music)
	$ mp3-organizer -v -p ~/ -t ~/Music/ -r -d

Znajdź wszystkie pliki MP3 w katalogu domowym i przenieś je do ~/Music, wypisuj dokładnie co robisz (opcja -v). Próbuj usuwać katalogi z których przeniesiono muzykę (tylko jeżeli są puste).

	$ mp3-organizer -v -c -p ~/Music/Iron\ Maiden/ -t /media/TELEFON/Muzyka --scheme {artist}-{album}/{track}-{title}

Skopiuj (opcja -c) wszystkie pliki MP3 z katalogu *~/Music/Iron Maiden/* do katalogu */media/TELEFON/Muzyka/*, jako schemat przyjmij *{artist}-{album}/{track}-{title}*

Przykładowy plik:

> ~/Music/Iron Maiden/When-the-Wild-Wind-Blows.mp3

Zostanie skopiowany do:

> /media/TELEFON/Muzyka/**Iron Maiden-The Final Frontier/10-When the Wild Wind Blows.mp3**

Podrubiona część powstała w wyniku zstosowania schematu (opcja --scheme).

Domyślnym schematem programu jest:
	
	{artist}/{album}/{title}

Więcej przykładów
=================

Aktualny stan katalogu:

	$ tree
	.
	└── Muzyka
	    ├── image.jpg
	    ├── test-1.mp3
	    ├── test-2.mp3
	    ├── test-3.mp3
	    ├── test-4.mp3
	    ├── test-5.mp3
	    ├── test-6.mp3
	    ├── test-7.mp3
	    ├── test-8.mp3
	    ├── test-9.mp3
	    └── test.mp3
	 1 directory, 11 files

Cel: **Posortowanie plików MP3 w katalogu Muzyka wg wzorca: wykonawca/tytul**

Realizacj za pomocą **mp3-organizer**:

	$ mp3-organizer -v -p Muzyka/ -t Muzyka/ --recognize-covers --scheme {artist}/{title}

Standardowe wyjście:

	[V] Setting path as Muzyka/...
	[V] Setting target as Muzyka/...
	[V] Setting option recognize-covers...
	[V] Setting scheme: {artist}/{title}...
	[V] Preparing directories...
	[V] Checking path...
	[V] Checking target...
	[V] Checking access in target directory...
	[V] Creating output directories...
	[V] Moving Muzyka/test-9.mp3 -> Muzyka/Iron Maiden/The Wicker Man.mp3
	[V] Moving Muzyka/test-8.mp3 -> Muzyka/Iron Maiden/Ghost of the Navigator.mp3
	[V] Moving Muzyka/test-7.mp3 -> Muzyka/Iron Maiden/Brave New World.mp3
	[V] Moving Muzyka/test-6.mp3 -> Muzyka/Iron Maiden/Blood Brothers.mp3
	[V] Moving Muzyka/test-5.mp3 -> Muzyka/Iron Maiden/The Mercenary.mp3
	[V] Moving Muzyka/test-4.mp3 -> Muzyka/Iron Maiden/Dream of Mirrors.mp3
	[V] Moving Muzyka/test-3.mp3 -> Muzyka/Iron Maiden/The Fallen Angel.mp3
	[V] Moving Muzyka/test-2.mp3 -> Muzyka/Iron Maiden/The Nomad.mp3
	[V] Moving Muzyka/test-1.mp3 -> Muzyka/Iron Maiden/Out of The Silent Planet.mp3
	[V] Moving Muzyka/test.mp3 -> Muzyka/Iron Maiden/The Thin Line Between Love and.mp3
	[V] Found cover Muzyka/image.jpg...
	[V] Moving cover Muzyka/image.jpg -> Muzyka/Iron Maiden/cover.jpg

Stan katalogu:

	$ tree
	.
	└── Muzyka
		└── Iron Maiden
			├── Blood Brothers.mp3
			├── Brave New World.mp3
			├── cover.jpg
			├── Dream of Mirrors.mp3
			├── Ghost of the Navigator.mp3
			├── Out of The Silent Planet.mp3
			├── The Fallen Angel.mp3
			├── The Mercenary.mp3
			├── The Nomad.mp3
			├── The Thin Line Between Love and.mp3
			└── The Wicker Man.mp3
	2 directories, 11 files

Po jakimś czasie zmieniamy zdanie, chcemy by cała nasza kolekcja była w postaci: **rok-wydania-plyty/artysta/album/tytuł**. Z **mp3-organizer** to żaden problem. Wystarczy:

	$ mp3-organizer -v -d -r -p Muzyka/ -t Muzyka/ --recognize-covers --scheme {date}/{artist}/{album}/{title}

Zostały zostosowane dodatkowe opcje: **-d**, **-r**. Ich opis znajduje się wyżej.

Po wykonaniu powyższego polecenia nasz katalog wygląda tak:

	$ tree
	.
	└── Muzyka
		└── 2000
			└── Iron Maiden
				└── Brave New World
					├── Blood Brothers.mp3
					├── Brave New World.mp3
					├── cover.jpg
					├── Dream of Mirrors.mp3
					├── Ghost of the Navigator.mp3
					├── Out of The Silent Planet.mp3
					├── The Fallen Angel.mp3
					├── The Mercenary.mp3
					├── The Nomad.mp3
					├── The Thin Line Between Love and.mp3
					└── The Wicker Man.mp3
	4 directories, 11 files

Oczywiście jeżeli chcemy przywrócić kolekcję do stanu pierwotnego - nie ma problemu:

	$ mp3-organizer -v -d -r -p Muzyka/ -t Muzyka/ --scheme test --recognize-covers	

License
=======

Copyright (C)
* Patryk Jaworski <skorpion9312@gmail.com>
* Ariana Las <ariana.las@gmail.com>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see http://www.gnu.org/licenses.

License - PL
============

Copyright (C)
* Patryk Jaworski <skorpion9312@gmail.com>
* Ariana Las <ariana.las@gmail.com>

Niniejszy program jest wolnym oprogramowaniem - możesz go rozpowszechniać dalej
i/lub modyfikować na warunkach Powszechnej Licencji Publicznej GNU wydanej przez
Fundację Wolnego Oprogramowania, według wersji 3 tej Licencji lub dowolnej
z późniejszych wersji.

Niniejszy program rozpowszechniany jest z nadzieją, iż będzie on użyteczny - jednak
BEZ ŻADNEJ GWARANCJI, nawet domyślnej gwarancji PRZYDATNOŚCI HANDLOWEJ
albo PRZYDATNOŚCI DO OKREŚLONYCH ZASTOSOWAŃ. Bliższe informacje na ten temat
można uzyskać z Powszechnej Licencji Publicznej GNU.

Kopia Powszechnej Licencji Publicznej GNU powinna zostać ci dostarczona razem
z tym programem. Jeżeli nie została dostarczona, odwiedź http://www.gnu.org/licenses.

Nieoficjalne, tłumaczenie licencji znajdziesz pod adresem: http://itlaw.computerworld.pl/index.php/gpl-3/
