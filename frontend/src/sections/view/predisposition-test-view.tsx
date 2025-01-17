"use client";

import { useMemo, useState, useCallback } from "react";

import Container from "@mui/material/Container";
import Typography from "@mui/material/Typography";
import {
  Box,
  Radio,
  Paper,
  Stack,
  Button,
  RadioGroup,
  MobileStepper,
  FormControlLabel,
} from "@mui/material";

import { useResponsive } from "src/hooks/use-responsive";

import Image from "src/components/image";

import { NewsletterEmail } from "../newsletter/newsletter";
// ----------------------------------------------------------------------

const QUESTIONS = [
  "Czy lubisz rozwiązywać problemy i łamigłówki?",
  "Czy potrafisz skoncentrować się na jednym zadaniu przez dłuższy czas, nie tracąc motywacji?",
  "Czy dobrze radzisz sobie z matematyką lub logicznym myśleniem?",
  "Czy łatwo uczysz się nowych technologii i narzędzi?",
  "Czy czujesz się komfortowo, pracując samodzielnie nad projektem przez długi czas?",
  "Czy masz cierpliwość do analizowania i poprawiania błędów w kodzie (debugging)?",
  "Czy potrafisz myśleć logicznie i dzielić duże problemy na mniejsze, łatwiejsze do rozwiązania części?",
  "Czy jesteś otwarty na ciągłe uczenie się i rozwijanie swoich umiejętności?",
  "Czy potrafisz współpracować z innymi nad rozwiązaniem problemu?",
  "Czy potrafisz zachować spokój, gdy napotykasz na trudności lub gdy coś nie działa tak, jak powinno?",
  "Czy masz dobrą pamięć i potrafisz zapamiętywać szczegóły, które mogą być istotne przy rozwiązywaniu problemów?",
  "Czy jesteś cierpliwy w sytuacjach, gdy potrzebujesz przejść przez wiele kroków, aby osiągnąć cel?",
  "Czy potrafisz samodzielnie szukać informacji, gdy napotykasz na problem, który jest dla Ciebie nowy?",
  "Czy umiesz zarządzać swoim czasem, aby skutecznie pracować nad kilkoma zadaniami jednocześnie?",
  "Czy czujesz satysfakcję, gdy uda Ci się znaleźć rozwiązanie problemu po długim czasie poszukiwań?",
  "Czy dobrze znosisz krytykę lub sugestie innych osób na temat Twojej pracy?",
  "Czy często zadajesz pytania, aby lepiej zrozumieć problem lub zadanie, nad którym pracujesz?",
  "Czy lubisz analizować dane i wyciągać wnioski na ich podstawie?",
  "Czy uważasz, że potrafisz jasno wyrażać swoje myśli, zarówno w mowie, jak i w piśmie, gdy tłumaczysz komuś rozwiązanie problemu?",
  "Czy potrafisz radzić sobie z frustracją, gdy nie udaje Ci się osiągnąć zamierzonego efektu od razu?",
];

const OPTIONS = [
  "Zdecydowanie nie",
  "Raczej nie",
  "Nie mam zdania",
  "Raczej tak",
  "Zdecydowanie tak",
];

const RESULTS = [
  {
    score: 80,
    title: "Masz naturalne predyspozycje do programowania!",
    subtitle:
      "Twoje umiejętności logicznego myślenia, cierpliwość i chęć rozwoju sprawiają, że jesteś świetnym kandydatem na programistę. Kontynuuj rozwój, a osiągniesz w tej dziedzinie naprawdę dużo!",
    image: "/assets/icons/winners.svg",
  },
  {
    score: 60,
    title: "Masz solidne podstawy, aby zostać programistą!",
    subtitle:
      "Twoje umiejętności są na dobrym poziomie, a chęć rozwoju i gotowość do nauki pomogą Ci doskonalić się w tej dziedzinie. Kontynuuj naukę, a sukces w programowaniu będzie w Twoim zasięgu!",
    image: "/assets/icons/code_thinking.svg",
  },
  {
    score: 40,
    title: "Masz potencjał, ale przed Tobą jeszcze dużo nauki.",
    subtitle:
      "Twoje umiejętności mogą się rozwinąć, ale potrzebujesz więcej pracy nad niektórymi aspektami programowania. Z odpowiednią motywacją i determinacją możesz osiągnąć sukces!",
    image: "/assets/icons/online_learning.svg",
  },
  {
    score: 20,
    title: "Początki bywają trudne, ale nie zniechęcaj się!",
    subtitle:
      "Masz jeszcze sporo do nauki, ale każdy programista kiedyś zaczynał. Jeśli jesteś gotów na wyzwanie i nie boisz się pracy nad sobą, programowanie może stać się Twoją nową pasją!",
    image: "/assets/icons/showing_support.svg",
  },
];

// ----------------------------------------------------------------------

export default function PredispositionTestView() {
  const mdUp = useResponsive("up", "md");

  const [activeStep, setActiveStep] = useState(0);
  const [values, setValues] = useState<number[]>(Array(QUESTIONS.length).fill(3));

  const steps = useMemo(() => [...QUESTIONS, "Newsletter", "Wyniki"], []);

  const maxSteps = steps.length;

  const score = useMemo(() => values.reduce((acc, curr) => acc + curr, 0), [values]);
  const result = useMemo(() => RESULTS.find((r) => score >= r.score), [score]);

  const handleChange = useCallback((event: React.ChangeEvent<HTMLInputElement>, index: number) => {
    const selectedValue = event.target.value;
    const scoreValue = OPTIONS.indexOf(selectedValue) + 1;
    setValues((prevArray: number[]) => {
      const newArray = [...prevArray];
      newArray[index] = scoreValue;
      return newArray;
    });
  }, []);

  const handleNext = useCallback(() => {
    setActiveStep((prevActiveStep) => prevActiveStep + 1);
  }, []);

  const handleBack = useCallback(() => {
    setActiveStep((prevActiveStep) => prevActiveStep - 1);
  }, []);

  const isDisabled = useCallback(() => {
    if (activeStep === maxSteps - 1) {
      return true;
    }

    if (activeStep === maxSteps - 2) {
      return true;
    }

    return false;
  }, [activeStep, maxSteps]);

  const renderStepContent = () => {
    if (activeStep === QUESTIONS.length) {
      return (
        <Stack direction="column" spacing={2} alignItems="center">
          <Typography variant="body2">
            Aby zobaczyć wyniki zapisz się do naszego newslettera.
          </Typography>
          <Box maxWidth={400}>
            <NewsletterEmail
              buttonLabel="Pokaż wyniki"
              showSnackbar={false}
              onSuccess={() => setActiveStep((prevActiveStep) => prevActiveStep + 1)}
              onFailure={() => setActiveStep((prevActiveStep) => prevActiveStep + 1)}
            />
          </Box>
        </Stack>
      );
    }

    if (activeStep + 1 > QUESTIONS.length) {
      return (
        <Stack direction={{ xs: "column", md: "row" }} spacing={4}>
          <Stack maxWidth={500}>
            <Stack direction="row" alignItems="center" spacing={0.5}>
              <Typography variant="h5" fontWeight="regular">
                Twój wynik to{" "}
              </Typography>
              <Typography variant="h5">{score}</Typography>
              <Typography variant="h5" fontWeight="regular">
                {" "}
                punktów.
              </Typography>
            </Stack>
            <Typography variant="h5" fontWeight="bold" pt={2}>
              {result?.title}
            </Typography>
            <Typography variant="h6" fontWeight="regular">
              {result?.subtitle}
            </Typography>
          </Stack>
          <Image alt={result?.title} src={result?.image} sx={{ borderRadius: 2, height: 300 }} />
        </Stack>
      );
    }

    return (
      <RadioGroup
        row={mdUp}
        sx={{ p: 2 }}
        value={OPTIONS[values[activeStep] - 1]}
        onChange={(event) => handleChange(event, activeStep)}
      >
        {OPTIONS.map((option) => (
          <FormControlLabel
            key={`${option}=${activeStep}`}
            control={<Radio />}
            label={option}
            value={option}
            labelPlacement={!mdUp ? "end" : "top"}
          />
        ))}
      </RadioGroup>
    );
  };

  return (
    <Container>
      <Typography variant="h3" sx={{ py: { xs: 3, md: 8 } }}>
        Test predyspozycji
      </Typography>

      <Typography variant="body1">
        Odpowiedz na poniższe pytania, aby sprawdzić, czy masz naturalne predyspozycje, które pomogą
        Ci w nauce programowania.
      </Typography>
      <Typography variant="body1">
        Każde pytanie oceniaj w skali od 1 (zdecydowanie nie) do 5 (zdecydowanie tak).
      </Typography>

      <Box sx={{ flexGrow: 1, py: 4 }}>
        <Paper
          square
          elevation={0}
          sx={{
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            height: 50,
            pl: 2,
            bgcolor: "background.paper",
          }}
        >
          <Typography fontWeight="bold">{steps[activeStep]}</Typography>
        </Paper>
        <Box
          sx={{
            width: "100%",
            pt: 4,
            pb: 4,
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            bgcolor: "background.default",
          }}
        >
          {renderStepContent()}
        </Box>
        {activeStep < maxSteps - 1 && (
          <MobileStepper
            variant="progress"
            steps={maxSteps}
            position="static"
            activeStep={activeStep}
            nextButton={
              <Button size="small" onClick={handleNext} disabled={isDisabled()}>
                Dalej
              </Button>
            }
            backButton={
              <Button size="small" onClick={handleBack} disabled={activeStep === 0}>
                Wstecz
              </Button>
            }
          />
        )}
      </Box>
    </Container>
  );
}
