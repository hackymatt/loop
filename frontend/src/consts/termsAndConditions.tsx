import { Link } from "@mui/material";
import Typography from "@mui/material/Typography";

import { paths } from "src/routes/paths";

export const termsAndConditions = [
  {
    header: "§1 Podstawowe definicje",
    content: (
      <Typography sx={{ textAlign: "justify" }}>
        <Typography>
          1. Serwis internetowy – serwis znajdujący się pod adresem niniejszej strony internetowej,
          za pośrednictwem którego Sprzedawca świadczy usługi drogą elektroniczną.
        </Typography>
        <Typography>
          2. Sprzedawca – właściciel strony internetowej – loop Mateusz Szczepek, NIP: 6861677925,
          REGON: 529269876, e-mail:{" "}
          <Link color="inherit" href="mailto:info@loop.edu.pl">
            info@loop.edu.pl
          </Link>
          .
        </Typography>
        <Typography>
          3. Adres Sprzedawcy – ilekroć w Regulaminie jest mowa o adresie Sprzedawcy, rozumie się
          przez to adres mailowy (zakładka{" "}
          <Link target="_blank" rel="noopener" href={paths.contact} color="text.primary">
            kontakt
          </Link>
          ).
        </Typography>
        <Typography>
          4. Klient – osoba fizyczna posiadająca pełną zdolność do czynności prawnych, a w
          przypadkach przewidzianych przez przepisy powszechnie obowiązujące także osoba fizyczna
          posiadająca ograniczoną zdolność do czynności prawnych, osoba prawna albo jednostka
          organizacyjna nieposiadająca osobowości prawnej, której ustawa przyznaje zdolność prawną,
          która zawarła lub zamierza zawrzeć umowę o świadczenie usług.
        </Typography>
        <Typography>
          5. Konsument – art. 221 KC: osoba fizyczna dokonująca ze Sprzedawcą czynności prawnej
          niezwiązanej bezpośrednio z jej działalnością gospodarczą lub zawodową.
        </Typography>
        <Typography>
          6. Umowa o świadczenie usług – umowa dotycząca usługi zamieszczonej na stronie Serwisu
          internetowego zawierana albo zawarta między Klientem a Sprzedawcą za pośrednictwem Serwisu
          internetowego.
        </Typography>
        <Typography>
          7. Usługa – usługa, którą Klient nabywa za pośrednictwem Serwisu internetowego.
        </Typography>
        <Typography>
          8. Zamówienie – oświadczenie woli Klienta, złożone za pośrednictwem Serwisu internetowego
          określające: rodzaj i zakres Usługi dostępnej w Serwisie internetowym w chwili składania
          zamówienia, sposób zapłaty oraz dane Klienta.
        </Typography>
        <Typography>
          9. Formularz zamówienia – elektroniczna usługa, formularz na nośniku elektronicznym
          dostępny w Serwisie internetowym, umożliwiający złożenie i realizację Zamówienia.
        </Typography>
        <Typography>
          10. Czas realizacji zamówienia – czas, w jakim zamówienie złożone przez Klienta Serwisu
          internetowego zostanie zrealizowane przez Sprzedawcę.
        </Typography>
        <Typography>
          11. Dzień roboczy – jeden dzień od poniedziałku do piątku z wyłączeniem dni ustawowo
          wolnych od pracy.
        </Typography>
        <Typography>
          12. Ceny – ceny usług w Serwisie są stałe w danym czasie i nie wpływają na nie żadne
          algorytmy ustalania cen, niezależnie od tego, jak Klient trafia na stronę, jakich
          przeglądarek używa, oraz nie ma znaczenia płeć, wiek itp.
        </Typography>
        <Typography>
          13. Ustawa o prawach Konsumenta, ustawa – ustawa z dnia 30 maja 2014 r. o prawach
          Konsumenta (Dz.U. z 2014 r. poz. 827 z późniejszymi zmianami).
        </Typography>
        <Typography>
          14. RODO – Rozporządzenie Rady UE 2016/679 (z dnia 27 kwietnia 2016 r.).
        </Typography>
      </Typography>
    ),
  },
  {
    header: "§2 Postanowienia ogólne",
    content: (
      <Typography sx={{ textAlign: "justify" }}>
        <Typography>
          1. Sprzedawca oświadcza, że przestrzega wszelkich wymaganych zasad ochrony danych
          osobowych Klientów, przewidzianych między innymi Ustawą o ochronie danych osobowych,
          zgodnie z przepisami RODO. Klient wyraża zgodę na gromadzenie, przechowywanie i
          przetwarzanie przez Sprzedawcę danych osobowych wyłącznie w celu bezpośrednio związanym z
          realizacją zamówionej usługi w Serwisie internetowym. Szczegółowe warunki gromadzenia,
          przetwarzania oraz ochrony danych osobowych przez Sprzedawcę określone zostały w „Polityce
          prywatności” Serwisu internetowego.
        </Typography>
        <Typography>
          2. Sprzedawca oświadcza, że usługi są zgodne z umową, w aspektach takich jak opis, rodzaj,
          jakość i funkcjonalność, a w odniesieniu do usług cyfrowych – również kompatybilność,
          interoperacyjność i dostępność aktualizacji; ale również przydatność do szczególnego celu,
          do którego jest potrzebny konsumentowi, o którym konsument powiadomił przedsiębiorcę
          najpóźniej w momencie zawarcia umowy i który przedsiębiorca zaakceptował. Ponadto, aby
          usługa została uznana za zgodną z umową.
        </Typography>
        <Typography>
          3. Sprzedawca oświadcza, że w związku z wejściem w życie w całej Europie rozporządzenia
          prawnego dotyczącego opinii (transpozycja dyrektywy (UE) 2019/2161 do prawa krajowego):
          przedsiębiorcy, którzy udostępniają opinie, muszą poinformować, czy i w jaki sposób
          zapewniono, aby publikowane opinie pochodziły od konsumentów, którzy używali danej usługi
          lub z niej skorzystali. Środki podjęte w tym celu muszą być konkretnie wymienione.
        </Typography>
        <Typography>
          4. Oświadczamy, że opinie zamieszczone na naszej stronie pochodzą od rzeczywistych
          klientów, którzy zakupili i używali nasze usługi. Opinie zostały wystawione zgodnie z
          przesłaną prośbą o ich wystawienie po potwierdzeniu, że usługa została wykonana.
          Obiecujemy dopełnić wszelkich formalności i starań, by opinie były rzeczywiste i
          odpowiadały prawdzie, a te wystawione nienależycie były usuwane.
        </Typography>
        <Typography>
          5. Obowiązkowe podstawy prawne w/w uregulowań:{" "}
          <Typography sx={{ ml: 3 }}>
            • Dyrektywa Parlamentu Europejskiego i Rady (UE) 2019/2161 z dnia 27 listopada 2019 r.
            zmieniająca dyrektywę Rady 93/13/EWG i dyrektywy Parlamentu Europejskiego i Rady
            98/6/WE, 2005/29/WE oraz 2011/83/UE w odniesieniu do lepszego egzekwowania i
            unowocześnienia unijnych przepisów dotyczących ochrony konsumenta, OJ L 328, 18.12.2019,
            s. 7–28.{" "}
          </Typography>
          <Typography sx={{ ml: 3 }}>
            • Fałszowanie opinii w Internecie – doświadczenia konsumentów, na podstawie badania PBS
            Sp. z o.o. na zlecenie UOKIK, publikacja dostępna
            https://uokik.gov.pl/aktualnosci.php?news_id=17411{" "}
          </Typography>
          <Typography sx={{ ml: 3 }}>
            • Dyrektywa 2005/29/WE Parlamentu Europejskiego i Rady z dnia 11 maja 2005 r. dotycząca
            nieuczciwych praktyk handlowych stosowanych przez przedsiębiorstwa wobec konsumentów na
            rynku wewnętrznym oraz zmieniająca dyrektywę Rady 84/450/EWG, dyrektywy 97/7/WE,
            98/27/WE i 2002/65/WE Parlamentu Europejskiego i Rady oraz rozporządzenie (WE) nr
            2006/2004 Parlamentu Europejskiego i Rady („Dyrektywa o nieuczciwych praktykach
            handlowych”) (OJ L 149, 11.06.2005, p. 22–39, z późn. zmianami).{" "}
          </Typography>
          <Typography sx={{ ml: 3 }}>
            • Zawiadomienie Komisji – Wytyczne dotyczące wykładni i stosowania dyrektywy 2005/29/WE
            Parlamentu Europejskiego i Rady dotyczącej nieuczciwych praktyk handlowych stosowanych
            przez przedsiębiorstwa wobec konsumentów na rynku wewnętrznym, OJ C 526, 29.12.2021, s.
            1–129.{" "}
          </Typography>
          <Typography sx={{ ml: 3 }}>
            • Dyrektywa Parlamentu Europejskiego i Rady 2011/83/UE z dnia 25 października 2011 r. w
            sprawie praw konsumentów, zmieniająca dyrektywę Rady 93/13/EWG i dyrektywę 1999/44/WE
            Parlamentu Europejskiego i Rady oraz uchylająca dyrektywę Rady 85/577/EWG i dyrektywę
            97/7/WE Parlamentu Europejskiego i Rady (OJ L 304, 22.11.2011, p. 64–88, z późn.
            zmianami).
          </Typography>
        </Typography>
        <Typography>
          6. Składając zamówienia w Serwisie, Klient ma możliwość zapoznania się z Regulaminem,
          akceptując jego treść poprzez oznaczenie odpowiedniego pola w formularzu. Do realizacji
          zamówienia konieczna jest akceptacja postanowień Regulaminu. Informujemy, że zawarcie
          Umowy o świadczenie usług za pośrednictwem Internetu i akceptacja regulaminu pociąga za
          sobą obowiązek zapłaty za zamówioną usługę.
        </Typography>
        <Typography>
          7. Administrator danych stosuje odpowiednie środki techniczne i organizacyjne zapewniające
          ochronę danych osobowych odpowiednio do zagrożeń oraz kategorii danych objętych ochroną.
          Przede wszystkim chroni dane przed ich udostępnieniem, zabraniem, przetwarzaniem, utratą,
          zmianą, uszkodzeniem lub zniszczeniem przez osoby do tego nieuprawnione. Szczegółowy
          zakres ochrony uregulowany został zgodnie z wymaganiami w polityce Ochrony Danych
          osobowych (polityka bezpieczeństwa, regulamin ochrony danych osobowych, instrukcja
          zarządzania systemem informatycznym).
        </Typography>
        <Typography>
          8. Dane Administrator Państwa danych osobowych znajdują się na w zakładce{" "}
          <Link target="_blank" rel="noopener" href={paths.contact} color="text.primary">
            kontakt
          </Link>{" "}
          umiejscowionej na stronie internetowej.
        </Typography>
        <Typography>
          9. Każdej osobie, której dane są przetwarzane przysługuje prawo do:{" "}
          <Typography sx={{ ml: 3 }}>
            • Nadzorowania i kontroli przetwarzania danych osobowych, dla których sprzedawca
            prowadzi zbiór danych klientów w/w sklepu;{" "}
          </Typography>
          <Typography sx={{ ml: 3 }}>
            • Ustalenia kto jest administratorem danych, ustalenia jego adresu, siedziby, nazwy, w
            sytuacji, gdy administratorem jest osoba fizyczna do ustalenia jej imienia i nazwiska
            oraz miejsca zamieszkania;{" "}
          </Typography>
          <Typography sx={{ ml: 3 }}>
            • Uzyskania informacji o celu, zakresie, sposobie, czasie przetwarzania danych zawartych
            w takim zbiorze;{" "}
          </Typography>
          <Typography sx={{ ml: 3 }}>
            • Uzyskania informacji w powszechnie zrozumiałej formie treści tych danych;{" "}
          </Typography>
          <Typography sx={{ ml: 3 }}>
            • Poznania źródła, z którego pochodzą dane, które jej dotyczą, chyba że administrator
            danych jest zobowiązany do zachowania w tym zakresie w tajemnicy informacji niejawnych
            lub zachowania tajemnicy zawodowej;{" "}
          </Typography>
          <Typography sx={{ ml: 3 }}>
            • Żądania uzupełnienia, uaktualnienia, sprostowania danych osobowych, czasowego
            zawieszenia lub ich usunięcia, jeżeli są one niekompletne, nieaktualne, nieprawdziwe lub
            zostały zebrane z naruszeniem ustawy albo są już zbędne do realizacji celu, dla którego
            zostały zebrane.
          </Typography>
        </Typography>
        <Typography>
          10. Klientowi zgodnie z punktem 9 przysługuje prawo wglądu w treść przetwarzanych danych
          osobowych, ich poprawiania, a także żądania usunięcia tych danych. Administrator danych
          osobowych jest obowiązany, do uzupełnienia, uaktualnienia, sprostowania danych, czasowego
          lub stałego wstrzymania przetwarzania lub ich usunięcia ze zbioru na bieżąco i od razu po
          zgłoszeniu, chyba że żądanie dotyczy danych osobowych, co do których tryb ich
          uzupełnienia, uaktualnienia lub sprostowania określają odrębne przepisy prawa w tym
          ustawy.
        </Typography>
        <Typography>
          11. Klient w procesie finalizacji zamówienia wyraża zgodę na gromadzenie i przetwarzanie
          przez Sprzedawcę danych osobowych w rozumieniu ustawy o ochronie danych osobowych. Dane
          mogą być przekazywane innemu podmiotowi tylko w sytuacji prawem wymaganych bądź
          niezbędnych dla realizacji składanego zamówienia.
        </Typography>
        <Typography>
          12. Klient może wyrazić zgodę na otrzymywanie od Sprzedawcy informacji o charakterze
          reklamowym i handlowym drogą elektroniczną przez zapisanie się do NEWSLETTERA.
        </Typography>
        <Typography>
          13. Klient korzystający z Usług Sprzedawcy realizowanych za pośrednictwem Serwisu
          internetowego zobowiązany jest do przestrzegania niniejszego Regulaminu w zakresie jaki
          jest niezbędny do realizacji złożonego zamówienia i nie jest sprzeczny z obowiązującym
          prawem oraz z zasadami współżycia społecznego.
        </Typography>
        <Typography>
          14. Sprzedawca Serwisu internetowego oświadcza, że Usługi dostępne i sprzedawane w jego
          Serwisie internetowym są zgodne z opisem i nie zawierają wad prawnych. Usługi w pełni
          odpowiadają właściwościom, które są opisane na stronie Serwisu internetowego.
        </Typography>
        <Typography>
          15. Sprzedawca realizuje zamówienia na terytorium Polski oraz zamówienia składane przez
          Konsumentów w Europie, a po uprzednim ustaleniu warunków także w innych krajach.
        </Typography>
        <Typography>
          16. Informacje dotyczące Usług znajdujące się na stronie Serwisu internetowego stanowią
          zaproszenie do zawarcia umowy w rozumieniu art. 71 ustawy z dnia 23 kwietnia 1964 r.
          Kodeksu cywilnego.
        </Typography>
        <Typography>
          17. Wszystkie ceny Usług podane na stronie Serwisu internetowego podawane są w walucie
          polskiej (polskich złotych) i są cenami brutto zawierającymi podatek VAT oraz inne
          składniki prawem nakładane.
        </Typography>
        <Typography>
          18. Przedsiębiorca prowadzący jednoosobowo działalność gospodarczą, jeśli dokona zakupu,
          który nie ma związku z prowadzoną przez niego działalnością posiada prawo do odstąpienia
          od umowy w terminie 14 dni kalendarzowych od momentu zawarcia umowy.
        </Typography>
        <Typography>
          19. Przepisy dotyczące konsumenta, z wyjątkiem art. 558 § 1 zdanie drugie kodeksu
          cywilnego, stosuje się do osoby fizycznej zawierającej umowę bezpośrednio związaną z jej
          działalnością gospodarczą, gdy z treści tej umowy wynika, że nie posiada ona dla tej osoby
          charakteru zawodowego, wynikającego w szczególności z przedmiotu wykonywanej przez nią
          działalności gospodarczej, udostępnionego na podstawie przepisów o Centralnej Ewidencji i
          Informacji o Działalności Gospodarczej.
        </Typography>
        <Typography>
          20. Weryfikacja tego, czy dana czynność ma zawodowy charakter, będzie odbywać się w
          oparciu o CEiDG — Centralną Ewidencję i Informację o Działalności Gospodarczej — a
          konkretnie o wpisane tam kody PKD określające rodzaje działalności gospodarczej.
        </Typography>
        <Typography>
          21. Przedsiębiorcy prowadzący jednoosobowo działalność uzyskają uprawnienia w zakresie:{" "}
          <Typography sx={{ ml: 3 }}>
            • Niedozwolonych klauzul stosowanych we wzorcach umownych;{" "}
          </Typography>
          <Typography sx={{ ml: 3 }}>• Rękojmi za wady rzeczy sprzedanej; </Typography>
          <Typography sx={{ ml: 3 }}>
            • Roszczenia regresowego do poprzedniego sprzedawcy w związku z wykonaniem reklamacji
            konsumenta;{" "}
          </Typography>
          <Typography sx={{ ml: 3 }}>
            • Prawa odstąpienia od umowy zawartej na odległość lub poza lokalem przedsiębiorstwa w
            terminie 14 dni.
          </Typography>
        </Typography>
        <Typography>
          22. Przepisy dotyczące konsumenta, zawarte w art. 385(1) -385(3) k.c. [dotyczących
          niedozwolonych postanowień umownych] stosuje się do osoby fizycznej zawierającej umowę
          bezpośrednio związaną z jej działalnością gospodarczą, gdy z treści tej umowy wynika, że
          nie posiada ona dla niej charakteru zawodowego, wynikającego w szczególności z przedmiotu
          wykonywanej przez nią działalności gospodarczej, udostępnionego na podstawie przepisów o
          Centralnej Ewidencji i Informacji o Działalności Gospodarczej.
        </Typography>
        <Typography>
          23. Art. 385(5) k.c. dotyczy tylko niedozwolonych postanowień umownych (klauzul
          abuzywnych). Przepisy o klauzulach abuzywnych są po 1 stycznia 2021 r. stosowane do
          jednoosobowych przedsiębiorców. Katalog przykładowych dwudziestu trzech klauzul abuzywnych
          zawarty jest w art. 385(3) k.c.
        </Typography>
        <Typography>
          24. Przedsiębiorcy prowadzący jednoosobowo działalność gospodarczą po zmianach opisanych
          powyżej nadal nie mogą korzystać z pomocy instytucji wspierających konsumentów w ochronie
          ich praw, w tym z pomocy Powiatowych/Miejskich Rzeczników Konsumenta czy UOKIK.
        </Typography>
      </Typography>
    ),
  },
  {
    header: "§3 Warunki świadczenia usług",
    content: (
      <Typography sx={{ textAlign: "justify" }}>
        <Typography>
          1. Serwis internetowy świadczy usługi drogą elektroniczną, warunkiem przystąpienia do
          umowy jest wypełnienie formularza zamówienia w celu zawarcia umowy o świadczenie usług.
          Przystąpienie do zawarcia umowy jest dobrowolne.
        </Typography>
        <Typography>
          2. Umowa o świadczenie usług zawierana jest drogą elektroniczną w postaci umożliwienia
          wypełnienia formularza zamówienia Klientowi Serwisu internetowego. Umowa zawierana jest na
          czas oznaczony w momencie przystąpienia przez Klienta do wypełnienia formularza oraz ulega
          rozwiązaniu z chwilą odstąpienia od wypełnienia formularza lub z chwilą przesłania
          wypełnionego formularza Sprzedawcy. Proces wypełniania formularza zamówienia jest
          zorganizowany tak, aby każdy Klient miał możliwość zapoznania się z nim przed podjęciem
          decyzji o zawarciu umowy albo o dokonaniu zmiany umowy.
        </Typography>
        <Typography>
          3. Usługa określona w pkt. 1 świadczona jest nieodpłatnie, może wymagać jednak dostępu do
          sieci internetowej.
        </Typography>
        <Typography>
          4. Zamówienie drogą elektroniczną można składać 24 godziny na dobę 7 dni w tygodniu.
        </Typography>
        <Typography>
          5. Klient finalizując zakup w odpowiednim okienku zamówienia zaznacza opcję „Wyrażam zgodę
          na przetwarzanie moich danych osobowych zawartych w formularzu w celu i zakresie
          niezbędnym do realizacji usługi i tylko w takim celu.” – jest ona niezbędna do zawarcia
          umowy. Podanie przez Państwa danych osobowych jest niezbędne do złożenia zamówienia,
          niepodanie danych osobowych będzie równoznaczne z odstąpieniem od zawarcia umowy.
        </Typography>
        <Typography>
          6. Zgodnie z art. 8 ust. 2 RODO, administrator, uwzględniając dostępną technologię,
          podejmuje rozsądne starania, by zweryfikować, czy osoba sprawująca władzę rodzicielską lub
          opiekę nad dzieckiem (poniżej 16 lat) wyraziła zgodę lub ją zaaprobowała.
        </Typography>
        <Typography>
          7. Koszty Klienta związane z dostępem do sieci Internet i transmisją danych ponoszone są
          wyłącznie przez Klienta zgodnie z taryfą swojego dostawcy, z którym klient podpisał umowę
          o świadczenie usług internetowych.
        </Typography>
      </Typography>
    ),
  },
  {
    header: "§4 Warunki umowy",
    content: (
      <Typography sx={{ textAlign: "justify" }}>
        <Typography>
          1. Dla dokonania zawarcia ważnej i wiążącej strony Umowy o świadczenie usług, Klient
          dokonuje wyboru zgodnie z wyświetloną ofertą Serwisu internetowego określając ilość Usług
          jakie zamierza nabyć oraz w razie takiej możliwości wskazując cechy zamawianej Usługi oraz
          odpowiednio jej specyfikację. Łącznie z wyborem Usługi, Klient wypełnia formularz
          zamówienia, wskazując w nim dane niezbędne do realizacji zamówienia przez Sprzedawcę takie
          jak na przykład ilości, miejsce dostawy oraz formy płatności, w oparciu o wyświetlane
          Klientowi komunikaty i informacje dostępne na stronie oraz zawarte w niniejszym
          Regulaminie.
        </Typography>
        <Typography>
          2. Zamówienia można składać w poprzez formularz dostępny na stronie internetowej Serwisu (
          <Link target="_blank" rel="noopener" href={paths.cart} color="text.primary">
            koszyk
          </Link>
          ).
        </Typography>
        <Typography>
          3. Warunkiem realizacji zamówienia jest podanie przez Klienta/Przedsiębiorcy danych
          pozwalających na weryfikację Klienta/Przedsiębiorcę i odbiorcy usługi. Serwis potwierdza
          przyjęcie zamówienia poprzez wysłanie na podany podczas składania zamówienia adres e-mail,
          wiadomości opisującej przedmiot zamówienia. W przypadku podania niepełnych, błędnych,
          sprzecznych informacji przez Klienta/Przedsiębiorcę podczas składania zamówienia, Serwis
          skontaktuje się z Klientem/Przedsiębiorcą w celu usunięcia błędów.
        </Typography>
        <Typography>
          4. Rejestracja Konta Klienta w Serwisie internetowym jest wymagana w celu realizacji
          usługi i jest nieodpłatna.
        </Typography>
        <Typography>
          5. W przypadku udostępnienia przez Sprzedawcę możliwości zamówienia Usługi, której
          właściwości polegają na tym, że jest ona wykonywana na indywidualne zamówienie Klienta,
          Klient przesyła wraz z formularzem zamówienia treści niezbędne do wykonania Usługi tj.
          tekst, grafikę, wymiary itp., zgodnie z wymaganiami technicznymi zawartymi przy opisie
          Usługi bądź wybiera odpowiednią specyfikację Usługi z podanych przez Sprzedawcę wariantów
          dostępnych możliwości konfiguracji danej Usługi.
        </Typography>
        <Typography>
          6. Niezwłocznie po otrzymaniu zamówienia Sprzedawca przesyła Klientowi drogą elektroniczną
          na podany w trakcie składania zamówienia adres poczty elektronicznej oświadczenie o
          przyjęciu zamówienia stanowiące równocześnie jego potwierdzenie. Z chwilą otrzymania
          wiadomości przez Klienta dochodzi do zawarcia umowy o świadczenie usług.
        </Typography>
        <Typography>
          7. Wiadomość podsumowująca i potwierdzająca zamówienie zawiera wszystkie wcześniej
          ustalone warunki umowy o świadczenie usług, a w szczególności ilość oraz rodzaj zamówionej
          Usługi, jej specyfikację w przypadku zamówienia Usług o indywidualnych właściwościach
          określonych przez Klienta Serwisu internetowego, całkowitą cenę do zapłaty (określoną w
          polskich złotych) wraz z kosztami dodatkowymi oraz wysokością przyznanych rabatów (o ile
          dotyczy).
        </Typography>
        <Typography>
          8. W przypadku posiadania przez Klienta większej ilości rabatów pochodzących z kilku
          źródeł/promocji podlegają one łączeniu/sumowaniu tylko w sytuacji gdy jest to wyraźnie
          określone w Regulaminie promocji. W przypadku braku zapisu co do sposobu łączenia różnych
          promocji/rabatów można wybrać tylko jeden rabat (jedną promocję) przy danym zakupie.
        </Typography>
      </Typography>
    ),
  },
  {
    header: "§5 Realizacja zamówienia",
    content: (
      <Typography sx={{ textAlign: "justify" }}>
        <Typography>
          1. Sprzedawca rzetelnie realizuje zamówienia Klienta według kolejności ich wpłynięcia –
          każde zamówienie jest dla nas priorytetowe i bardzo ważne!
        </Typography>
        <Typography>
          2. Czas realizacji zamówienia dla pojedynczego Klienta określany jest na stronie produktu.
          Czas dostępu do usługi zależy od jej specyfiki i jest określony w opisie usługi.
        </Typography>
        <Typography>
          3. W przypadku zaistnienia wyjątkowych okoliczności lub braku możliwości realizacji
          zamówienia we wskazanym w pkt. 2 terminie, Sprzedawca niezwłocznie kontaktuje się z
          Klientem w celu ustalenia dalszego trybu postępowania w tym ustalenia innego terminu
          realizacji zamówienia.
        </Typography>
      </Typography>
    ),
  },
  {
    header: "§6 Dostawa",
    content: (
      <Typography sx={{ textAlign: "justify" }}>
        <Typography>
          1. Dostawa w rozumieniu niniejszego regulaminu odnosi się do dostarczenia usługi, co może
          obejmować dostęp do materiałów szkoleniowych, transmisji online lub innego rodzaju
          świadczenia na odległość.
        </Typography>
        <Typography>
          2. Usługa zostanie udostępniona w sposób i w terminie określonym w zamówieniu i
          potwierdzeniu przez Sprzedawcę.
        </Typography>
        <Typography>
          3. Usługa zawsze jest udostępniona w sposób odpowiadający jej właściwościom, tak aby była
          dostępna w pełnym zakresie i zgodna z opisem.
        </Typography>
        <Typography>
          4. Klient na bieżąco jest informowany o kosztach dodatkowych związanych z realizacją
          usługi, są one podawane w trakcie wypełniania przez Klienta formularza zamówienia.
        </Typography>
      </Typography>
    ),
  },
  {
    header: "§7 Metody płatności",
    content: (
      <Typography sx={{ textAlign: "justify" }}>
        <Typography>
          1. Sprzedawca umożliwia płatność za zamówiony Towar w formie przedpłaty na rachunek
          bankowy.
        </Typography>
        <Typography>
          2. Płatność elektroniczna kartą kredytową (Visa, Visa Electron, MasterCard, Maestro) lub
          przelewem internetowym bankowości elektronicznej za pośrednictwem serwisu płatności
          internetowych Przelewy24.
        </Typography>
        <Typography>
          3. Sprzedawca dokumentuje sprzedaż usługi zgodnie z żądaniem Klienta.
        </Typography>
      </Typography>
    ),
  },
  {
    header: "§8 Rękojmia",
    content: (
      <Typography sx={{ textAlign: "justify" }}>
        <Typography>
          1. W przypadku roszczeń dotyczących usług Sprzedawca odpowiada za zgodność usługi z umową,
          zgodnie z obowiązującymi przepisami prawa.
        </Typography>
        <Typography>
          2. Sprzedawca odpowiada niezwłocznie na zgłoszenie Konsumenta jednak nie później niż w
          terminie do 14 dni kalendarzowych od dnia jego otrzymania. Nierozpatrzenie zgłoszenia w
          zakreślonym terminie jest równoznaczne z jego uwzględnieniem przez Sprzedawcę i uznaniem
          go za uzasadnione.
        </Typography>
        <Typography>
          3. W przypadku stwierdzenia niezgodności usługi z umową, Klient ma prawo do zgłoszenia
          reklamacji. Reklamacje należy składać drogą elektroniczną na adres mailowy Sprzedawcy lub
          w formie pisemnej na adres pocztowy Sprzedawcy. Jeśli konsument ma trudności i nie wie,
          jak skonstruować zgłoszenie o wadach usługi, zgłoszenie może przesłać dla przykładu na
          formularzu stanowiącym załącznik nr 2 do niniejszego Regulaminu, co stanowi tylko
          ułatwienie dla procesu reklamacji, nie stanowi żadnego wymogu korzystania z w/w wzorca dla
          skuteczności reklamacji.
        </Typography>
        <Typography>
          4. Sprzedawca odpowiada za niezgodność usługi z umową, w przypadku jej stwierdzenia przed
          upływem dwóch lat od wykonania usługi.
        </Typography>
        <Typography>
          5. Sprzedawca pokrywa koszty związane z usunięciem wad usługi lub jej ponownym wykonaniem.
        </Typography>
      </Typography>
    ),
  },
  {
    header: "§9 Odstąpienie",
    content: (
      <Typography sx={{ textAlign: "justify" }}>
        <Typography>
          1. Zgodnie z przepisami prawa Klientowi będącemu Konsumentem w myśl art. 27 ustawy z dnia
          30 maja 2014 r. (Dz.U. z 2014 r. poz. 827 z późn. zm.) o prawach Konsumenta, przysługuje
          prawo do odstąpienia od umowy zawartej na odległość bez podawania przyczyny.
        </Typography>
        <Typography>
          2. Zgodnie z art. 38 pkt. 13 ustawy o prawach konsumenta – „o dostarczanie treści
          cyfrowych, które nie są zapisane na nośniku materialnym, jeżeli spełnianie świadczenia
          rozpoczęło się za wyraźną zgodą konsumenta przed upływem terminu do odstąpienia od umowy i
          po poinformowaniu go przez przedsiębiorcę o utracie prawa odstąpienia od umowy.” – w
          takiej sytuacji prawo odstąpienia nie przysługuje.
        </Typography>
        <Typography>
          3. Prawo do odstąpienia od umowy przysługuje w terminie 14 dni kalendarzowych od momentu
          zawarcia umowy.
        </Typography>
        <Typography>
          4. Gdy Klient będący Konsumentem odstąpi od umowy, umowa jest uważana za niezawartą, a
          Konsument jest zwolniony wówczas z wszelkich zobowiązań. To co strony świadczyły sobie
          nawzajem podlega zwrotowi w stanie niezmienionym, chyba że zmiana była konieczna w
          granicach zwykłego zarządu. Zwrot powinien nastąpić niezwłocznie, nie później niż w
          terminie czternastu dni.
        </Typography>
        <Typography>
          5. Klient będący Konsumentem może odstąpić od umowy, składając oświadczenie na formularzu
          stanowiącym załącznik nr 1 do niniejszego Regulaminu, przesyłając je drogą elektroniczną
          lub na adres pocztowy Sprzedawcy według wyboru Klienta. Załącznik nr 1 stanowi tylko pomoc
          w odstąpieniu od umowy, nie jest wzorem koniecznym do skorzystania z prawa do odstąpienia
          od umowy. Klient może, ale nie musi z niego korzystać. Dla skutecznego odstąpienia
          wystarczy przesłanie oświadczenia na piśmie na adres Sprzedawcy.
        </Typography>
        <Typography>
          6. Do zachowania terminu określonego w pkt. 2 wystarczy wysłanie oświadczenia Klienta o
          odstąpieniu od umowy przed jego upływem.
        </Typography>
        <Typography>
          7. Sprzedawca niezwłocznie potwierdzi Klientowi otrzymanie oświadczenia o odstąpieniu od
          umowy i stosownie poinformuje Klienta o dalszym postępowaniu, w tym o sposobie zwrotu
          kosztów oraz w razie pytań udzieli na nie odpowiedzi.
        </Typography>
        <Typography>
          8. Sprzedawca niezwłocznie, w terminie nie dłuższym niż 14 dni kalendarzowych od dnia
          otrzymania oświadczenia Klienta o odstąpieniu od umowy, zwróci Klientowi wszelkie
          otrzymane od niego płatności, w tym koszty związane z realizacją usługi. Sprzedawca
          dokonuje zwrotu płatności przy użyciu takiego samego sposobu płatności, jakiego użył
          Klient, chyba że Klient wyraźnie zgodził się na inny sposób zwrotu płatności, który nie
          wiąże się dla niego z żadnymi kosztami.
        </Typography>
        <Typography>
          9. Klient będący Konsumentem ponosi wyłącznie bezpośrednie koszty odstąpienia od umowy.
        </Typography>
        <Typography>
          10. Prawo do odstąpienia od umowy nie przysługuje Klientowi w odniesieniu do umów
          określonych w art. 38 ustawy z dnia 30 maja 2014 r. o prawach Konsumenta m. in. w
          sytuacji:{" "}
          <Typography sx={{ ml: 3 }}>
            • O świadczenie usług, jeżeli przedsiębiorca wykonał w pełni usługę za wyraźną zgodą
            Konsumenta, który został poinformowany przed rozpoczęciem świadczenia, że po spełnieniu
            świadczenia przez przedsiębiorcę utraci prawo odstąpienia od umowy;{" "}
          </Typography>
          <Typography sx={{ ml: 3 }}>
            • W której przedmiotem świadczenia jest usługa z elementami cyfrowymi, która po jej
            spełnieniu nie może zostać wycofana.
          </Typography>
        </Typography>
      </Typography>
    ),
  },
  {
    header: "§10 Postępowanie reklamacyjne",
    content: (
      <Typography sx={{ textAlign: "justify" }}>
        <Typography>
          1. Dla prawidłowego złożenia reklamacji Klient powinien podać swoje dane takie jak: imię i
          nazwisko lub nazwę firmy, adres zamieszkania lub adres siedziby firmy oraz adres poczty
          elektronicznej, przedmiot reklamacji, w miarę możliwości numer zamówienia wraz ze
          wskazaniem okresu czasu, którego dotyczy reklamacja oraz okoliczności uzasadniające
          złożenie reklamacji (opis na czym ona polega) ewentualnie jakich cech usługa zamawiana nie
          posiada, a według zapewnień Sprzedawcy lub według sposobu przedstawienia go Klientowi
          miała posiadać.
        </Typography>
        <Typography>
          2. Jeżeli Klientem jest Konsument, w wypadku pierwszej reklamacji klient może liczyć na
          ponowne wykonanie usługi albo zwrot kosztów. Dla usługi cyfrowej konsument będzie mógł
          żądać również usunięcia wad usług cyfrowych, a jeżeli usunięcie wady będzie nieskuteczne,
          może żądać obniżenia ceny lub odstąpić od umowy. Przy ocenie nadmierności kosztów
          uwzględnia się wartość usługi wolnej od wad, rodzaj i znaczenie stwierdzonej wady, a także
          bierze się pod uwagę niedogodności, na jakie narażałby Klienta inny sposób zaspokojenia.
        </Typography>
        <Typography>
          3. Jeżeli przepisy odrębne nie stanowią inaczej, przedsiębiorca jest obowiązany udzielić
          odpowiedzi na reklamację konsumenta w terminie 14 dni od dnia jej otrzymania. Jeżeli
          przedsiębiorca nie udzielił odpowiedzi na reklamację w terminie, o którym mowa wyżej,
          uważa się, że uznał reklamację. Odpowiedź na reklamację przedsiębiorca przekazuje
          konsumentowi na papierze lub innym trwałym nośniku (np. pamięci USB lub płycie CD/DVD,
          odpowiadając na reklamację.)
        </Typography>
        <Typography>
          4. W przypadku nierozpatrzenia zgłoszenia w zakreślonym terminie, należy uznać je za
          uwzględnione przez Sprzedawcę. Roszczenie dotyczące odstąpienia od umowy, w przypadku jego
          nierozpatrzenia w terminie, nie jest równoznaczne z uznaniem złożonej reklamacji.
        </Typography>
      </Typography>
    ),
  },
  {
    header: "§11 Odpowiedzialność",
    content: (
      <Typography sx={{ textAlign: "justify" }}>
        <Typography>
          1. Zamieszczając ewentualne treści oraz udostępniając je, Klient dobrowolnie je
          rozpowszechnia. Sprzedawca nie jest dostawcą treści i w żaden sposób nie utożsamia się z
          nimi, jest jedynie podmiotem, który udostępnia zasoby teleinformatyczne. Klient oświadcza,
          że:
          <Typography sx={{ ml: 3 }}>
            • Jest uprawniony do korzystania i udostępniania zamieszczanych przez siebie treści
            autorskich praw majątkowych, praw własności przemysłowej lub praw pokrewnych;
          </Typography>
          <Typography sx={{ ml: 3 }}>
            • Umieszczenie oraz udostępnienie w ramach usług, danych osobowych, wizerunku,
            informacji dotyczących innych osób niż Klient odbyło się w sposób zgodny z prawem,
            dobrowolny oraz za zgodą właścicieli treści, których one dotyczą;
          </Typography>
          <Typography sx={{ ml: 3 }}>
            • Akceptuje wgląd do opublikowanych przez siebie informacji, danych, obrazów i innych
            treści przez pozostałych Klient oraz Sprzedawcę, zezwala Sprzedawcy nieodpłatnie na ich
            wykorzystanie;
          </Typography>
          <Typography sx={{ ml: 3 }}>
            • Wyraża zgodę na dokonywanie opracowań, modyfikacji i interpretacji utworów w
            rozumieniu Ustawy o prawie autorskim i prawach pokrewnych.
          </Typography>
          <Typography>2. Klient nie jest uprawniony do:</Typography>
          <Typography sx={{ ml: 3 }}>
            • Zamieszczania danych osobowych osób trzecich, rozpowszechniania wizerunku bez
            wymaganego zezwolenia lub zgody osoby trzeciej której dane te dotyczą;
          </Typography>
          <Typography sx={{ ml: 3 }}>
            • Zamieszczania treści o charakterze reklamowym i lub promocyjnym, niezgodny z celem
            działalności serwisu.
          </Typography>
        </Typography>
        <Typography>
          3. W przypadku otrzymania powiadomienia przez osobę trzecią, uprawnioną bądź organ władzy
          Państwowej Sprzedawca zastrzega sobie prawo do modyfikowania lub usuwania treści
          zamieszczanych przez Klient, w sytuacji stwierdzenia, że mogą one stanowić naruszenie
          niniejszego Regulaminu lub obowiązujących przepisów prawa. Sprzedawca nie kontroluje na
          bieżąco zamieszczanych treści.
        </Typography>
      </Typography>
    ),
  },
  {
    header: "§12 Pozasądowe sposoby rozpatrywania reklamacji i dochodzenia roszczeń",
    content: (
      <Typography sx={{ textAlign: "justify" }}>
        <Typography>
          1. Informacje o pozasądowych sposobach rozpatrywania reklamacji i dochodzenia roszczeń, a
          także zasady dostępu do tych procedur udostępniane są w siedzibach oraz na stronach
          internetowych powiatowych (miejskich) rzeczników Konsumentów, organizacji społecznych, do
          których zadań statutowych należy ochrona Konsumentów, Wojewódzkich Inspektoratów Inspekcji
          Handlowej oraz pod następującymi adresami Urzędu Ochrony Konkurencji i Konsumentów:
          www.uokik.gov.pl/spory_konsumenckie.php, www.uokik.gov.pl/wazne_adresy.php,
          www.uokik.gov.pl/sprawy_indywidualne.php
        </Typography>
        <Typography>
          2. Konsument posiada między innymi następujące możliwości skorzystania z pozasądowych
          sposobów rozpatrywania reklamacji i dochodzenia swoich roszczeń:
          <Typography sx={{ ml: 3 }}>
            • zwrócenie się do Wojewódzkiego Inspektora Inspekcji Handlowej z wnioskiem o wszczęcie
            postępowania mediacyjnego w sprawie polubownego zakończenia sporu.
          </Typography>
          <Typography sx={{ ml: 3 }}>
            • zwrócenie się do stałego polubownego Sądu Konsumenckiego działającego przy Wojewódzkim
            Inspektorze Inspekcji Handlowej z wnioskiem o rozstrzygnięcie sporu wynikłego z zawartej
            umowy, adres www.uokik.gov.pl/wazne_adresy.php.
          </Typography>
          <Typography sx={{ ml: 3 }}>
            • zwrócenie się o bezpłatną pomoc prawną m.in. do Federacji Konsumentów - adres strony
            internetowej: www.federacjakonsumentow.org.pl.
          </Typography>
        </Typography>
        <Typography>
          3. W rozwiązywaniu sporów transgranicznych pomaga Sieć Europejskich Centrów Konsumenckich.
          Adresy tych instytucji dostępne są na stronie internetowej Europejskiego Centrum
          Konsumenckiego www.konsument.gov.pl.
        </Typography>
        <Typography>
          4. Konsument może również skorzystać z platformy internetowego systemu rozstrzygania
          sporów (platforma ODR), zgodnie z rozporządzeniem Parlamentu Europejskiego i Rady (UE) Nr
          524/2013 z dnia 21 maja 2013 r. w sprawie internetowego systemu rozstrzygania sporów
          Konsumenckich oraz zmiany rozporządzenia (WE) nr 2006/2004 i dyrektywy 2009/22/WE
          (rozporządzenie w sprawie ODR w sporach konsumenckich). ODR (online dispute resolution)
          dostępnej pod adresem elektronicznym: http://ec.europa.eu/consumers/odr/ Europejska
          platforma ODR stanowi jeden wspólny punkt dostępu dla konsumentów i przedsiębiorców,
          umożliwiający pozasądowe rozstrzyganie sporów dotyczących zobowiązań umownych,
          wynikających z zawartej internetowej umowy sprzedaży: https://webgate.ec.europa.eu/
          odr/main/index.cfm?event=main.home.show&lng=PL
        </Typography>
        <Typography>
          5. Skorzystanie z pozasądowych sposobów rozpatrywania reklamacji i dochodzenia roszczeń ma
          charakter dobrowolny i może mieć miejsce tylko, gdy obie strony sporu tj. Sprzedawca i
          Klient wyrażą na to zgodę.
        </Typography>
      </Typography>
    ),
  },
  {
    header: "§13 Postanowienia dotyczące przedsiębiorców",
    content: (
      <Typography sx={{ textAlign: "justify" }}>
        <Typography>
          1. Regulację i postanowienia w niniejszym paragrafie 13 dotyczą tylko Klientów i
          Usługobiorców nie będących konsumentami (zakup o charakterze zawodowym).
        </Typography>
        <Typography>
          2. Sprzedawca zastrzega sobie prawo odstąpienia od umowy sprzedaży zawartej z klientem
          niebędącym konsumentem w terminie 14 dni kalendarzowych od dnia jej zawarcia. Odstąpienie
          od umowy sprzedaży może nastąpić bez podania przyczyny i nie może rodzić z tego tytułu po
          stronie klienta niebędącego konsumentem żadnych roszczeń w stosunku do sprzedawcy.
        </Typography>
        <Typography>
          3. W wypadku klientów będących usługobiorcami i nie będących jednocześnie konsumentami
          usługodawca może wypowiedzieć umowę o świadczenie Usługi Elektronicznej ze skutkiem
          natychmiastowym nawet bez wskazywania przyczyn, pod warunkiem, że wysłał klientowi
          stosowne oświadczenie.
        </Typography>
        <Typography>
          4. Sprzedawca ma prawo ograniczyć dostępne sposoby płatności do kilku bądź do jednego, za
          poszczególne bądź wszystkie towary. Sprzedawca może wymagać dokonania przedpłaty w całości
          lub części, niezależnie od wybranego sposobu płatności oraz faktu zawarcia umowy
          sprzedaży.
        </Typography>
        <Typography>
          5. Niebezpieczeństwo przypadkowej utraty lub uszkodzenia produktu przechodzi na kupującego
          z chwilą wydania przez sprzedawcę zamawianego produktu przewoźnikowi. Z chwilą wydania
          przewoźnikowi zamawianego produktu przechodzą na klienta niebędącego konsumentem także
          wszystkie korzyści i ciężary z towarem związane. Sprzedawca w takim wypadku nie ponosi
          odpowiedzialności za utratę, ubytek, uszkodzenie od momentu przyjęcia go przez przewoźnika
          aż do wydania go klientowi.
        </Typography>
        <Typography>
          6. Klient nie będący konsumentem obowiązany jest zbadać przesyłkę w czasie i w sposób
          przyjęty przy przesyłkach tego rodzaju. Jeżeli stwierdzi, że nastąpił ubytek lub
          uszkodzenie produktu w czasie jego transportowania, obowiązany jest dokonać wszelkich
          czynności niezbędnych i potrzebnych do ustalenia odpowiedzialności przewoźnika.
        </Typography>
        <Typography>
          7. Sprzedawca informuje, że zgodnie z art. 558 § 1 Kodeksu Cywilnego odpowiedzialność z
          tytułu rękojmi za produkt wobec klienta nie będącego konsumentem zostaje wyłączona.
        </Typography>
        <Typography>
          8. Odpowiedzialność sprzedawcy jest ograniczona w ramach pojedynczego roszczenia, jak i za
          wszystkie roszczenia w sumie, do wysokości zapłaconej. Sprzedawca ponosi odpowiedzialność
          tylko za typowe szkody przewidywalne w momencie zawarcia umowy i nie ponosi
          odpowiedzialności z tytułu utraconych korzyści.
        </Typography>
        <Typography>
          9. Wszelkie spory między serwisem internetowym a klientem niebędącym konsumentem zostają
          poddane sądowi właściwemu ze względu na siedzibę sprzedawcy.
        </Typography>
      </Typography>
    ),
  },
  {
    header: "§14 Postanowienia końcowe",
    content: (
      <Typography sx={{ textAlign: "justify" }}>
        <Typography>
          1. Serwis internetowy honoruje wszelkie prawa Klientów przewidziane w przepisach
          obowiązującego prawa.
        </Typography>
        <Typography>
          2. Jeśli obowiązujące prawo przyznaje Klientom będącym konsumentami korzystniejsze
          obowiązkowe i wymagane prawem uregulowania niż te, które są zawarte w niniejszym
          Regulaminie, odpowiednie postanowienia Regulaminu są bezpośrednio zastępowane przez
          konkretne normy obowiązującego prawa i tym samym są wiążące dla w/w właściciela.
        </Typography>
        <Typography>
          3. Wszelkie treści zamieszczone na stronie Serwisu internetowego (wliczając w to grafikę,
          teksty, układ stron i logotypy) korzystają z ochrony przewidzianej dla praw autorskich i
          są wyłączną własnością Sprzedawcy. Wykorzystywanie tych treści bez pisemnej zgody
          Sprzedawcy skutkuje odpowiedzialnością cywilną oraz karną.
        </Typography>
        <Typography>
          4. Właściciel Serwisu jako administrator danych osobowych, informują Pana/ Panią, iż:
          <Typography sx={{ ml: 3 }}>
            • Podanie danych jest zawsze dobrowolne, ale niezbędne do realizacji zamówienia;
          </Typography>
          <Typography sx={{ ml: 3 }}>
            • Osoba podająca swoje dane osobowe ma nieograniczone prawo dostępu do wszystkich treści
            swoich danych i ich sprostowania, usunięcia (prawo do bycia zapomnianym), ograniczenia
            przetwarzania, prawo do przenoszenia danych, prawo do cofnięcia zgody w dowolnym
            momencie bez wpływu na zgodność z prawem przetwarzania, dane mogą być udostępnione
            jednak właściwym organom państwa w sytuacji, gdy odpowiedni przepis tego będzie wymagał.
          </Typography>
          <Typography sx={{ ml: 3 }}>
            • Podstawą przetwarzania danych osobowych będzie art. 6 ust. 1 pkt a) oraz treść
            ogólnego rozporządzenia o ochronie danych.;
          </Typography>
          <Typography sx={{ ml: 3 }}>
            • Dane osobowe będą przechowywane i przetwarzane przez okres niezbędny do zakończenia
            przetwarzania i realizacji zamówienia, lecz nie dłużej niż przez okres 3 lat (2 lata
            okres to okres reklamacji i 1 rok na ewentualnie inne roszczenia i sytuacje wyjątkowe).
          </Typography>
          <Typography sx={{ ml: 3 }}>
            • Osoba udostępniająca swoje dane osobowe ma prawo wniesienia skargi do UODO, gdy uzna,
            że przetwarzanie danych osobowych dotyczących realizacji zamówienia narusza przepisy
            ogólnego rozporządzenia o ochronie danych osobowych z dnia 27 kwietnia 2016 r.;
          </Typography>
        </Typography>
        <Typography>
          5. Państwa dane będą przetwarzane w sposób zautomatyzowany w tym również w formie
          profilowania.
        </Typography>
        <Typography>
          6. Zmieniony Regulamin wiąże Klientów, jeżeli zostały zachowane wymagania określone w art.
          384 Kodeksu cywilnego (tj. Klient został prawidłowo powiadomiony o zmianach).
        </Typography>
        <Typography>
          7. Sprzedawca zastrzega sobie prawo do dokonywania zmian Regulaminu z ważnych przyczyn to
          jest:
          <Typography sx={{ ml: 3 }}>• Zmiany przepisów prawa;</Typography>
          <Typography sx={{ ml: 3 }}>• Zmiany sposobów płatności i dostaw;</Typography>
          <Typography sx={{ ml: 3 }}>• Zmiana kursu walut,</Typography>
          <Typography sx={{ ml: 3 }}>
            • Zmiany sposobu świadczenia usług drogą elektroniczną objętym regulaminem,
          </Typography>
          <Typography sx={{ ml: 3 }}>
            • Zmiany danych Sprzedawcy, w tym adresu poczty elektronicznej, numeru telefonu.
          </Typography>
        </Typography>
        <Typography>
          8. Zmiany regulaminu nie mają wpływu na złożone i realizowane już zamówienia, do nich
          zastosowanie ma regulamin obowiązującym w chwili złożenia zamówienia. Sprzedawca o
          zamierzonej zmianie informuje na stronie serwisu co najmniej na 30 dni wcześniej. W
          przypadku braku akceptacji zmienionego regulaminu Usługobiorcy mogą w terminie 30 dni od
          dnia otrzymania wiadomości wypowiedzieć umowę ze skutkiem natychmiastowym.
        </Typography>
        <Typography>
          9. Spory powstałe w wyniku świadczenia usług na podstawie niniejszego Regulaminu zostaną
          poddane pod rozstrzygnięcie Sądowi Powszechnemu według wyboru Klienta będącego
          jednocześnie konsumentem, zgodnie z właściwymi przepisami prawa polskiego.
        </Typography>
        <Typography>10. Załączniki do Regulaminu stanowią jego integralną część.</Typography>
        <Typography>
          11. Umowa o świadczenie usług zawierana jest w języku polskim, o treści zgodnej z
          Regulaminem.
        </Typography>

        <Typography>
          12. Klienci w/w serwisu mogą uzyskać dostęp do niniejszego Regulaminu w każdym czasie za
          pośrednictwem odsyłacza zamieszczonego na stronie głównej serwisu oraz pobrać go i
          sporządzić jego wydruk, komercyjne wykorzystanie podlega jednak ochronie Kancelarii
          Prawnej LEGATO.
        </Typography>
        <Typography>13. Regulamin wchodzi w życie z dniem 1 września 2024.</Typography>
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
