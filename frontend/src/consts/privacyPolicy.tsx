import { Link } from "@mui/material";
import Typography from "@mui/material/Typography";

import { paths } from "src/routes/paths";

export const privacyPolicy = [
  {
    header: "§1 Postanowienia ogólne",
    content: (
      <Typography sx={{ textAlign: "justify" }}>
        <Typography>
          1. Ten dokument stanowi załącznik do Regulaminu. Korzystając z naszych usług, powierzasz
          nam swoje informacje. Niniejsza Polityka prywatności służy jedynie jako pomoc w
          zrozumieniu, jakie informacje i dane są zbierane i w jakim celu je wykorzystujemy. Te dane
          są bardzo dla nas ważne, dlatego prosimy o dokładne zapoznanie się z tym dokumentem gdyż
          określa on zasady oraz sposoby przetwarzania i ochrony danych osobowych.
        </Typography>
        <Typography>
          2. Niniejszym oświadczamy, że przestrzegamy zasad ochrony danych osobowych oraz wszelkich
          uregulowań prawnych, które są przewidziane Ustawą o ochronie danych osobowych oraz
          Rozporządzeniem Parlamentu Europejskiego i Rady (UE) 2016/679 z dnia 27 kwietnia 2016 r. w
          sprawie ochrony osób fizycznych w związku z przetwarzaniem danych osobowych i w sprawie
          swobodnego przepływu takich danych oraz uchylenia dyrektywy 95/46/WE.
        </Typography>
        <Typography>
          3. Osoba której dane osobowe są przetwarzane ma prawo zwrócić się do nas celem uzyskania
          wyczerpujących informacji w jaki sposób wykorzystujemy jego dane osobowe. Zawsze w jasny
          sposób staramy się poinformować o danych, które gromadzimy, w jaki sposób je
          wykorzystujemy, jakim celom mają służyć i komu je przekazujemy, jaką zapewniamy ochronę
          tych danych przy przekazaniu innym podmiotom oraz udzielamy informacji o instytucjach z
          którymi należy się skontaktować w razie wątpliwości.
        </Typography>
        <Typography>
          4. Serwis stosuje środki techniczne takie jak: środki ochrony fizycznej danych osobowych,
          środki sprzętowe infrastruktury informatycznej i telekomunikacyjnej, środki ochrony w
          ramach narzędzi programowych i baz danych oraz środki organizacyjne zapewniające należytą
          ochronę przetwarzanych danych osobowych, a w szczególności zabezpieczają dane osobowe
          przed udostępnieniem ich nieupoważnionym osobom trzecim, uzyskaniem przez osobę
          nieupoważnioną i wykorzystaniem ich w niewiadomym celu, a także przypadkową lub celową
          zmianą, utratą, uszkodzeniem lub zniszczeniem takich danych.
        </Typography>

        <Typography>
          5. Na zasadach określonych w Regulaminie oraz w niniejszym dokumencie posiadamy wyłączny
          dostęp do danych. Dostęp do danych osobowych może być również powierzony innym podmiotom
          za pomocą których dokonuje się płatności, które gromadzą, przetwarzają i przechowują dane
          osobowe zgodnie ze swoimi Regulaminami oraz podmioty, które mają za zadanie realizację
          zamówienia. Dostęp do danych osobowych jest udzielany w/w podmiotom w zakresie niezbędnym
          i tylko takim, który zapewni realizację usług.
        </Typography>
        <Typography>
          6. Dane osobowe są przetwarzane tylko w takich celach na jakie wyrazili Państwo zgodę
          poprzez kliknięcia w odpowiednie pola formularza zamieszczonego w Serwisie lub w inny
          wyraźny sposób. Podstawą prawną przetwarzania Państwa danych osobowych jest zgoda na
          przetwarzanie danych lub wymóg realizacji usługi (np. zamówienie produktu czy usługi,
          stosownie do artykułu 6 ust. 1 lit a i b Rozporządzenia Parlamentu Europejskiego i Rady
          (UE) 2016/679 z dnia 27 kwietnia 2016 r. w sprawie ochrony osób fizycznych w związku z
          przetwarzaniem danych osobowych i w sprawie swobodnego przepływu takich danych oraz
          uchylenia dyrektywy 95/46/WE (ogólne rozporządzenie o ochronie danych) - RODO.
        </Typography>
      </Typography>
    ),
  },
  {
    header: "§2 Zasady prywatności",
    content: (
      <Typography sx={{ textAlign: "justify" }}>
        {" "}
        <Typography>
          1. Poważnie traktujemy prywatność. Charakteryzuje nas szacunek dla prywatności oraz
          możliwie najpełniejsza i zagwarantowana wygoda z korzystania z naszego usług.
        </Typography>
        <Typography>
          2. Cenimy zaufanie, jakim obdarzają nas Użytkownicy, powierzając nam swoje dane osobowe w
          celu realizacji zamówienia. Zawsze korzystamy z danych osobowych w sposób uczciwy oraz
          tak, aby nie zawieść tego zaufania, tylko w zakresie niezbędnym do realizacji zamówienia w
          tym jego przetwarzania.
        </Typography>
        <Typography>
          3. Użytkownik ma prawo do uzyskania jasnych i pełnych informacji o tym, w jaki sposób
          wykorzystujemy jego dane osobowe i do jakich celów są potrzebne. Zawsze w jasny sposób
          informujemy o danych, które gromadzimy, w jaki sposób i komu je przekazujemy oraz
          udzielamy informacji o podmiotach, z którymi należy się skontaktować w razie wątpliwości,
          pytań, uwag.
        </Typography>
        <Typography>
          4. W razie wątpliwości odnośnie wykorzystywania przez nas danych osobowych Użytkownika,
          niezwłocznie podejmiemy działania w celu wyjaśnienia takich wątpliwości, w sposób pełny i
          wyczerpujący odpowiadamy na wszystkie pytania z tym związane.
        </Typography>
        <Typography>
          5. Podejmiemy wszystkie uzasadnione działania, aby chronić dane Użytkowników przed
          nienależytym i niekontrolowanym wykorzystaniem oraz zabezpieczyć je w sposób kompleksowy.
        </Typography>
        <Typography>
          6. Dane Administratora Państwa danych osobowych znajdują się na w zakładce{" "}
          <Link
            target="_blank"
            rel="noopener"
            href={paths.contact}
            color="text.primary"
            underline="always"
          >
            kontakt
          </Link>{" "}
          umiejscowionej na stronie internetowej.
        </Typography>
        <Typography>
          7. Podstawą prawną przetwarzania Państwa danych osobowych jest art. 6 ust. 1 lit. b) RODO.
          Podanie danych nie jest obowiązkowe, ale niezbędne do podjęcia odpowiednich czynności
          poprzedzających zawarcie umowy oraz jej realizację. Będziemy przekazywać Państwa dane
          osobowe innym odbiorcom, którym powierzono przetwarzanie danych osobowych w imieniu i na
          naszą rzecz. Państwa dane będą przekazywane na podstawie art. 6 ust. 1 lit. f) RODO, gdzie
          prawnie uzasadnionym interesem jest należyte wykonanie umów/zleceń. Ponadto będziemy
          udostępniać Państwa dane osobowe innym partnerom handlowym. Zebrane dane osobowe
          przechowujemy na terenie Europejskiego Obszaru Gospodarczego („EOG”), ale mogą one być
          także przesyłane do kraju spoza tego obszaru i tam przetwarzane. Każda operacja
          przesyłania danych osobowych jest wykonywana zgodnie z obowiązującym prawem. Jeśli dane są
          przekazywane poza obszar EOG, stosujemy standardowe klauzule umowne oraz tarczę
          prywatności jako środki zabezpieczające w odniesieniu do krajów, w przypadku których
          Komisja Europejska nie stwierdziła odpowiedniego poziomu ochrony danych.
        </Typography>
        <Typography>
          8. Państwa dane osobowe związane z zawarciem i realizacją umowy o realizacje umów
          przetwarzane będą przez okres ich realizacji, a także przez okres nie dłuższy niż
          przewidują to przepisy prawa, w tym przepisy Kodeksu cywilnego oraz ustawy o
          rachunkowości, tj. nie dłużej niż przez 10 lat, licząc od końca roku kalendarzowego w
          którym ostatnia umowa została wykonana.
        </Typography>
        <Typography>
          9. Państwa dane osobowe przetwarzane w celu zawarcia i wykonania przyszłych umów będą
          przetwarzane do czasu zgłoszenia sprzeciwu.
        </Typography>
        <Typography>
          10. Przysługuje Państwu prawo do: dostępu do swoich danych osobowych i otrzymania kopii
          danych osobowych podlegających przetwarzaniu, sprostowania swoich nieprawidłowych danych;
          żądania usunięcia danych (prawo do bycia zapomnianym) w przypadku wystąpienia okoliczności
          przewidzianych w art. 17 RODO; żądania ograniczenia przetwarzania danych w przypadkach
          wskazanych w art. 18 RODO, wniesienia sprzeciwu wobec przetwarzania danych w przypadkach
          wskazanych w art. 21 RODO, przenoszenia dostarczonych danych, przetwarzanych w sposób
          zautomatyzowany.
        </Typography>
        <Typography>
          11. Jeżeli uważacie Państwo, że dane osobowe są przetwarzane niezgodnie z prawem, możecie
          wnieść skargę do organu nadzorczego (Urząd Ochrony Danych Osobowych, ul. Stawki 2,
          Warszawa). Jeśli potrzebujecie Państwo dodatkowych informacji związanych z ochroną danych
          osobowych lub chcecie skorzystać z przysługujących praw, skontaktujcie się z nami
          listownie na adres korespondencyjny.
        </Typography>
        <Typography>
          12. Dokładamy wszelkich starań, aby chronić przed nieuprawnionym dostępem, nieautoryzowaną
          modyfikacją, ujawnieniem oraz zniszczeniem informacji znajdujących się w naszym
          posiadaniu. W szczególności:
          <Typography sx={{ ml: 6 }}>
            a) Kontrolujemy metody gromadzenia, przechowywania i przetwarzania informacji, w tym
            fizyczne środki bezpieczeństwa, aby chronić przed nieuprawnionym dostępem do systemu.{" "}
          </Typography>
          <Typography sx={{ ml: 6 }}>
            b) Dostępu do danych osobowych udzielamy jedynie tym pracownikom, kontrahentom oraz
            przedstawicielom, którzy muszą mieć do nich dostęp. Ponadto na mocy umowy są oni
            zobowiązani do zachowania ścisłej poufności, do umożliwienia nam kontroli i sprawdzenia
            jak wywiązują się z powierzonych obowiązków, a w przypadku niewypełnienia tych
            zobowiązań mogą ponieść konsekwencje.
          </Typography>
        </Typography>
        <Typography>
          13. Będziemy przestrzegać wszystkich obowiązujących przepisów i regulacji dotyczących
          ochrony danych i będziemy współpracować z organami zajmującymi się ochroną danych oraz
          uprawnionymi do tego organami ścigania. W przypadku braku przepisów dotyczących ochrony
          danych, będziemy postępować zgodnie z ogólnie przyjętymi zasadami ochrony danych, zasadami
          współżycia społecznego jak i ustalonymi zwyczajami.
        </Typography>
        <Typography>
          14. Dokładny sposób ochrony danych osobowych został zawarty w polityce ochrony danych
          osobowych (ODO: polityka bezpieczeństwa, regulamin ochrony danych osobowych, instrukcja
          zarządzania systemem informatycznym) Z przyczyn bezpieczeństwa, ze względu na opisane w
          niej procedury, jest ona do wglądu jedynie dla organów kontroli państwowej.
        </Typography>
        <Typography>
          15. W razie pytań, odnośnie sposobu, w jaki postępowania z danymi osobowymi, zapraszamy do
          kontaktu za pomocą strony, z której użytkownik został przekierowany do niniejszej Polityki
          prywatności. Prośba o kontakt zostanie niezwłocznie przekazana do odpowiedniej powołanej
          do tego osoby.
        </Typography>
        <Typography>
          16. Użytkownik ma zawsze prawo powiadomić nas, jeśli:
          <Typography sx={{ ml: 6 }}>
            a) nie chce w jakiejkolwiek formie już otrzymywać od nas informacji lub wiadomości;
          </Typography>
          <Typography sx={{ ml: 6 }}>
            b) pragnie otrzymać posiadaną przez nas kopię swoich danych osobowych;
          </Typography>
          <Typography sx={{ ml: 6 }}>
            c) poprawić, zaktualizować lub usunąć swoje dane osobowe znajdujące się w naszej
            ewidencji;
          </Typography>
          <Typography sx={{ ml: 6 }}>
            d) pragnie zgłosić naruszenia, nienależyte wykorzystanie bądź przetwarzanie swoich
            danych osobowych.
          </Typography>
        </Typography>
        <Typography>
          17. Aby ułatwić nam odpowiedź bądź ustosunkowanie się do podanych informacji, prosimy o
          podanie imienia i nazwiska oraz dalej idących szczegółów.{" "}
        </Typography>
      </Typography>
    ),
  },
  {
    header: "§3 Zakres i cel zbierania danych osobowych",
    content: (
      <Typography sx={{ textAlign: "justify" }}>
        <Typography>
          1. Przetwarzamy niezbędne dane osobowe w celu realizacji usług oraz w celach księgowych i
          tylko takich tj. :<Typography sx={{ ml: 6 }}>a) w celu złożenia zamówienia,</Typography>
          <Typography sx={{ ml: 6 }}>
            b) w celu zawarcia umowy, reklamacji oraz odstąpienia od umowy,
          </Typography>
          <Typography sx={{ ml: 6 }}>c) wystawienia faktury VAT lub innego paragonu. </Typography>
          <Typography sx={{ ml: 6 }}>
            d) monitorowania ruchu na naszych stronach internetowych;
          </Typography>
          <Typography sx={{ ml: 6 }}>
            e) zbieranie anonimowych statystyk, dla ustalenia, w jaki sposób użytkownicy korzystają
            z naszej strony internetowej;
          </Typography>
          <Typography sx={{ ml: 6 }}>
            f) ustalanie liczby anonimowych użytkowników naszych stron
          </Typography>
          <Typography sx={{ ml: 6 }}>
            g) kontrolowanie jak często pokazywana jest użytkownikom wybrana treść i jaka treść
            najczęściej;
          </Typography>
          <Typography sx={{ ml: 6 }}>
            h) kontrolowanie jak często użytkownicy wybierają daną usługę bądź z poziomu jakiej
            usługi następuje najczęściej kontakt;
          </Typography>
          <Typography sx={{ ml: 6 }}>i) badanie zapisów na newsletter i opcje kontaktu;</Typography>
          <Typography sx={{ ml: 6 }}>
            j) wykorzystanie systemu personalizowanych rekomendacji dla e-commerce;
          </Typography>
          <Typography sx={{ ml: 6 }}>
            k) wykorzystanie narzędzia do komunikacji zarówno mailowej jak i w następstwie czego
            telefonicznej;
          </Typography>
          <Typography sx={{ ml: 6 }}>l) integracja z portalem społecznościom;</Typography>
          <Typography sx={{ ml: 6 }}>m) ewentualne płatności internetowe.</Typography>
        </Typography>
        <Typography>
          2. Zbieramy, przetwarzamy i przechowujemy następujące dane użytkowników:
          <Typography sx={{ ml: 6 }}>a) imię i nazwisko,</Typography>
          <Typography sx={{ ml: 6 }}>b) adres zamieszkania,</Typography>
          <Typography sx={{ ml: 6 }}>c) adres poczty elektronicznej (e-mail),</Typography>
          <Typography sx={{ ml: 6 }}>d) numer telefonu,</Typography>
          <Typography sx={{ ml: 6 }}>e) datę urodzenia.</Typography>
        </Typography>
        <Typography>
          3. Podanie powyższych danych przez jest całkowicie dobrowolne ale także i niezbędne do
          pełnej realizacji usług.
        </Typography>
        <Typography>
          4. Cel gromadzenia i przetwarzania lub wykorzystania przez nas danych:
          <Typography sx={{ ml: 6 }}>
            a) marketing bezpośredni, cele archiwalne kampanii reklamowych;{" "}
          </Typography>
          <Typography sx={{ ml: 6 }}>
            b) realizacja obowiązków nałożonych przepisami prawa poprzez zbieranie informacji o
            niepożądanych działaniach;
          </Typography>
        </Typography>
        <Typography>
          5. Możemy przesyłać dane osobowe do serwerów znajdujących się poza krajem zamieszkania
          użytkownika lub do podmiotów powiązanych, stron trzecich z siedzibą w innych krajach w tym
          krajach z obszaru EOG (Europejski Obszar Gospodarczy, EOG ang. European Economic Area, EEA
          – strefa wolnego handlu i Wspólny Rynek, obejmujące państwa Unii Europejskiej i
          Europejskiego Stowarzyszenia Wolnego Handlu EFTA) w celu przetwarzania danych osobowych
          przez takie podmioty w naszym imieniu zgodnie z postanowieniami niniejszej Polityki
          prywatności oraz obowiązującymi przepisami prawa, zwyczajami jak i regulacjami dotyczącymi
          ochrony danych.
        </Typography>
        <Typography>
          6. Twoje dane osobowe przechowujemy nie dłużej niż są one potrzebne dla właściwej jakości
          obsługi i w zależności od trybu i celu ich pozyskania przechowujemy je na czas jej trwania
          oraz po jej zakończeniu w celach:
          <Typography sx={{ ml: 6 }}>
            a) realizacji obowiązków wynikających z przepisów prawa, przepisów podatkowych i
            rachunkowych;
          </Typography>
          <Typography sx={{ ml: 6 }}>b) zapobiegania nadużyciom lub przestępstwom;</Typography>
          <Typography sx={{ ml: 6 }}>c) statystycznych i archiwizacyjnych.</Typography>
          <Typography sx={{ ml: 6 }}>
            d) działania marketingowe – na czas trwania umowy, udzielenia odrębnej zgody na
            przetwarzanie takich danych – do czasu zakończenia działań związanych z obsługą
            transakcji, wniesienia przez Ciebie sprzeciwu wobec takiego przetwarzania lub wycofania
            zgody.
          </Typography>
          <Typography sx={{ ml: 6 }}>
            e) działania okołosprzedażowe i promocyjne – np. konkursy, akcje promocyjne – na czas
            trwania i rozliczenia takich akcji.
          </Typography>
          <Typography sx={{ ml: 6 }}>
            f) działalność operacyjna - do czasu przedawnienia obowiązków nałożonych przez
            Rozporządzenie RODO oraz odpowiednie przepisy krajowe, celem wykazania rzetelności w
            przetwarzaniu danych osobowych
          </Typography>
          <Typography sx={{ ml: 6 }}>
            g) dochodzenia Wszelkich roszczeń związanych ze zrealizowaną umową;
          </Typography>
        </Typography>
        <Typography>
          7. Mając na uwadze okoliczności, że w wielu krajach, do których są przesyłane niniejsze
          dane osobowe nie obowiązuje taki sam poziom ochrony prawnej danych osobowych, jaki
          obowiązuje w kraju użytkownika. Do danych osobowych użytkownika przechowywanych w innym
          kraju dostęp zgodnie z prawem tam obowiązującym, dostęp mogą uzyskać na przykład: sądy,
          organy odpowiedzialne za egzekwowanie prawa i bezpieczeństwo narodowe, zgodnie z
          przepisami obowiązującymi w tym kraju. Z zastrzeżeniem zgodnych z prawem próśb o
          ujawnienie danych, zobowiązujemy się wymagać od podmiotów przetwarzających dane osobowe
          poza krajem użytkownika podjęcia działań w celu ochrony danych w adekwatny sposób do
          regulacji ich prawa krajowego.
        </Typography>
      </Typography>
    ),
  },
  {
    header: "§4 Prawa i obowiązki",
    content: (
      <Typography sx={{ textAlign: "justify" }}>
        <Typography>
          1. Mamy prawo a w przypadkach prawem określonych także i ustawowy obowiązek do przekazania
          wybranych bądź wszystkich informacji dotyczących danych osobowych organom władzy
          publicznej bądź osobom trzecim, które zgłoszą takie żądanie udzielenia informacji na
          podstawie obowiązujących przepisów prawa polskiego.
        </Typography>
        <Typography>
          2. Użytkownik ma prawo dostępu do treści swoich danych osobowych, które udostępnia,
          Użytkownik może te dane poprawiać, uzupełniać w każdym czasie, a także ma prawo do żądania
          aby je usunięto ze swoich baz danych bądź zaprzestano je przetwarzać, bez podawania
          jakiekolwiek przyczyny. W celu realizacji swoich praw Użytkownik może w każdym czasie
          przesłać stosowną wiadomość na adres poczty elektronicznej bądź w inny sposób, który
          dostarczy/przekaże takie żądanie.
        </Typography>
        <Typography>
          3. Przetwarzanie danych osobowych osób fizycznych będących naszymi klientami opiera się
          na:
          <Typography sx={{ ml: 6 }}>
            a) usprawiedliwionym interesie jako administratora danych (np. w zakresie tworzenia bazy
            danych, czynności analitycznych i profilujących, w tym czynności dot. analizy
            korzystania z produktów, marketingu bezpośredniego produktów własnych, zabezpieczeniu
            dokumentacji na potrzeby obrony przed ewentualnymi roszczeniami lub na potrzeby
            dochodzenia roszczeń),
          </Typography>
          <Typography sx={{ ml: 6 }}>
            b) zgody (w tym w szczególności zgody na e-mail marketing lub telemarketing),
          </Typography>
          <Typography sx={{ ml: 6 }}>c) wykonania zawartej umowy,</Typography>
          <Typography sx={{ ml: 6 }}>
            d) obowiązków wynikających z prawa (np. prawa podatkowego lub przepisów o
            rachunkowości).
          </Typography>
        </Typography>
        <Typography>
          4. Przetwarzanie danych osobowych osób fizycznych będących potencjalnymi klientami opiera
          się na:
          <Typography sx={{ ml: 6 }}>
            a) usprawiedliwionym interesie administratora danych (np. w zakresie tworzenia bazy
            danych, marketingu bezpośrednim produktów własnych)
          </Typography>
          <Typography sx={{ ml: 6 }}>
            b) zgody (w tym w szczególności zgody na e-mail marketing lub telemarketing)
          </Typography>
        </Typography>
        <Typography>
          5. Żądanie ze strony Użytkownika usunięcia danych osobowych lub zaprzestania ich
          przetwarzania przez może skutkować całkowitym brakiem możliwości realizacji usług przez
          bądź ich poważnym ograniczeniem.
        </Typography>
        <Typography>
          6. Szczególną wagę przykładamy do kwestii profilowania i wskazujemy, że:
          <Typography sx={{ ml: 6 }}>
            a) na potrzeby profilowania przetwarzamy z reguły dane, które uprzednio podlegały
            szyfrowaniu ssl;
          </Typography>
          <Typography sx={{ ml: 6 }}>
            b) wykorzystujemy do tego typowe dane: adres e-mail i IP lub cookies
          </Typography>
          <Typography sx={{ ml: 6 }}>
            c) profilujemy w celu analizy lub prognozy osobistych preferencji oraz zainteresowań
            osób korzystających z naszych Serwisów lub produktów lub usług i dopasowywania treści
            znajdujących się w naszych Serwisach lub produktach do tych preferencji
          </Typography>
          <Typography sx={{ ml: 6 }}>
            d) profilujemy w celach marketingowych, tj. dopasowania oferty marketingowej do ww.
            preferencji.
          </Typography>
        </Typography>
        <Typography>
          7. Zobowiązujemy się postępować zgodnie z obowiązującymi przepisami prawa i zasadami
          współżycia społecznego.
        </Typography>
        <Typography>
          8. Informacja o pozasądowym rozpatrywaniu sporów konsumenckich. Podmiotem uprawnionym w
          rozumieniu ustawy o pozasądowym rozpatrywaniu sporów konsumenckich jest Rzecznik
          Finansowy, którego adres strony internetowej jest następujący: www.rf.gov.pl.
        </Typography>
      </Typography>
    ),
  },
  {
    header: "§5 Podstawowe zasady bezpieczeństwa",
    content: (
      <Typography sx={{ textAlign: "justify" }}>
        <Typography>
          1. Każdy użytkownik powinien dbać o swoje własne bezpieczeństwo danych oraz o
          bezpieczeństwo swoich urządzeń, które służą dostępowi do sieci Internet. Takie urządzenie
          powinno bezwzględnie posiadać program antywirusowy z aktualną regularnie uzupełnianą bazą
          definicji, typów i rodzajów wirusów, bezpieczną wersję przeglądarki internetowej z której
          korzysta oraz włączoną zaporę sieciową. Użytkownik powinien sprawdzać, czy system
          operacyjny i programy zainstalowane na nim posiadają najnowsze i kompatybilne
          aktualizacje, ponieważ w atakach wykorzystywane są błędy wykryte w zainstalowanym
          oprogramowaniu.
        </Typography>
        <Typography>
          2. Dane dostępowe do usług oferowanych w sieci Internet to – np. loginy, hasła, PIN,
          certyfikaty elektroniczne itp., – powinny być zabezpieczone w miejscu niedostępnym dla
          innych i niemożliwym do włamania z poziomu sieci internetowej. Nie należy ich ujawniać lub
          przechowywać na urządzeniu w formie, która umożliwia nieautoryzowany dostęp i odczyt przez
          osoby do tego nieuprawnione.
        </Typography>
        <Typography>
          3. Ostrożność podczas otwierania dziwnych załączników lub odnośników w wiadomościach
          mailowych, których się nie spodziewaliśmy np. od nieznanych nadawców, bądź z folderu spam.
        </Typography>
        <Typography>
          4. Zaleca się uruchomienie w przeglądarce internetowej filtrów antyphishingowych czyli
          narzędzi, które sprawdzają, czy wyświetlona strona internetowa jest autentyczna i nie
          służy wyłudzaniu informacji, np. poprzez podszywanie się pod osobę lub instytucję.
        </Typography>
        <Typography>
          5. Pliki powinny być pobierane tylko i wyłącznie z zaufanych miejsc, serwisów i stron. Nie
          zalecamy instalowania oprogramowania z niezweryfikowanych źródeł zwłaszcza od nieznanych
          wydawców o niesprawdzonej opinii. Dotyczy to również urządzeń przenośnych, np. smartfonów,
          tabletów.
        </Typography>
        <Typography>
          6. Podczas używania domowej sieci bezprzewodowej Wi-Fi należy ustalić takie hasło aby było
          bezpieczne i trudne do złamania, nie powinno być nim żaden wzór i ciąg znaków który jest
          łatwy do odgadnięcia (np. nazwa ulicy, imię gospodarza, data urodzin itp.). Rekomenduje
          się także korzystanie najwyższych możliwych standardów szyfrowania sieci bezprzewodowych
          Wi-Fi, które są możliwe do uruchomienia na posiadanym sprzęcie np. WPA2.{" "}
        </Typography>
      </Typography>
    ),
  },
  {
    header: "Nota o prawach autorskich do Regulaminu Sprzedaży",
    content: (
      <Typography>
        Właścicielem wszystkich materialnych praw autorskich do wzorca niniejszego Regulaminu
        Sprzedaży jest Kancelaria Prawna LEGATO, która udzieliła niniejszemu sklepowi niewyłącznego
        i niezbywalnego prawa do wykorzystywania tego Regulaminu Sprzedaży do celów związanych z
        własną działalnością handlową w Internecie oraz rozciąga ochronę prawną na w/w dokument na
        czas trwania umowy. Kopiowanie oraz rozpowszechnianie wzorca niniejszego Regulaminu
        Sprzedaży bez zgody Kancelarii Prawnej LEGATO jest zabronione i może podlegać
        odpowiedzialności zarówno karnej jak i cywilnej. Sprzedawcy internetowi mogą dowiedzieć się
        więcej o możliwości korzystania z wzorca Regulaminu Sprzedaży na stronie
        http://www.kancelaria-legato.pl/
      </Typography>
    ),
  },
];
