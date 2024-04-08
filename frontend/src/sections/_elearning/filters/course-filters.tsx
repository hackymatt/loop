import { useMemo, useCallback } from "react";

import Stack from "@mui/material/Stack";
import Drawer from "@mui/material/Drawer";
import Button from "@mui/material/Button";
import Typography from "@mui/material/Typography";

import { useResponsive } from "src/hooks/use-responsive";
import { useQueryParams } from "src/hooks/use-query-params";

import { useLecturers } from "src/api/lecturers/lecturers";
import { useTechnologies } from "src/api/technologies/technologies";

import { IQueryParamValue } from "src/types/query-params";
import { ICourseByCategoryProps } from "src/types/course";

import FilterLevel from "./filter-level";
import FilterPrice from "./filter-price";
import FilterRating from "./filter-rating";
import FilterSearch from "./filter-search";
import FilterDuration from "./filter-duration";
import FilterTeachers from "./filter-teachers";
import FilterCategories from "./filter-categories";

// ----------------------------------------------------------------------

const DURATION_OPTIONS = [
  { value: "(duration_to=60)", label: "0 - 1 godzin" },
  { value: "(duration_from=60)&(duration_to=180)", label: "1 - 3 godzin" },
  { value: "(duration_from=180)&(duration_to=360)", label: "3 - 6 godzin" },
  { value: "(duration_from=360)&(duration_to=1080)", label: "6 - 18 godzin" },
  { value: "(duration_from=1080)", label: "18+ godzin" },
];

const LEVEL_OPTIONS = [
  { value: "P", label: "Podstawowy" },
  { value: "Ś", label: "Średniozaawansowany" },
  { value: "Z", label: "Zaawansowany" },
  { value: "E", label: "Ekspert" },
];

const RATING_OPTIONS = ["4", "3", "2"];

// ----------------------------------------------------------------------

type Props = {
  open: boolean;
  onClose: VoidFunction;
};

export default function Filters({ open, onClose }: Props) {
  const mdUp = useResponsive("up", "md");
  const { setQueryParam, removeQueryParam, getQueryParams } = useQueryParams();

  const { data: technologies } = useTechnologies({ sort_by: "name" });
  const { data: teachers } = useLecturers({ sort_by: "full_name", page_size: -1 });

  const filters = useMemo(() => getQueryParams(), [getQueryParams]);

  const handleChange = useCallback(
    (name: string, value: IQueryParamValue) => {
      if (value) {
        setQueryParam(name, value);
      } else {
        removeQueryParam(name);
      }
    },
    [removeQueryParam, setQueryParam],
  );

  const renderContent = (
    <Stack
      spacing={1.5}
      sx={{
        flexShrink: 0,
        width: { xs: 1, md: 280 },
      }}
    >
      <FilterSearch
        value={filters?.search ?? ""}
        onChangeSearch={(value) => handleChange("search", value)}
      />

      <Block title="Ocena">
        <FilterRating
          value={filters?.rating_from ?? null}
          options={RATING_OPTIONS}
          onChangeRating={(value) => handleChange("rating_from", value)}
        />
      </Block>

      <Block title="Czas trwania">
        <FilterDuration
          value={filters?.filters ?? ""}
          options={DURATION_OPTIONS}
          onChangeDuration={(value) => handleChange("filters", value)}
        />
      </Block>

      <Block title="Technologia">
        <FilterCategories
          value={filters?.technology_in ?? ""}
          options={technologies?.map((technology: ICourseByCategoryProps) => technology.name)}
          onChangeCategory={(value) => handleChange("technology_in", value)}
        />
      </Block>

      <Block title="Poziom">
        <FilterLevel
          value={filters?.level_in ?? ""}
          options={LEVEL_OPTIONS}
          onChangeLevel={(value) => handleChange("level_in", value)}
        />
      </Block>

      <Block title="Instruktorzy">
        <FilterTeachers
          value={filters?.lecturer_in ?? ""}
          options={teachers}
          onChangeTeacher={(value) => handleChange("lecturer_in", value)}
        />
      </Block>

      <Block title="Cena">
        <FilterPrice
          valuePriceFrom={filters?.price_from ?? 0}
          valuePriceTo={filters?.price_to ?? 0}
          onChangeStartPrice={(value) => handleChange("price_from", value)}
          onChangeEndPrice={(value) => handleChange("price_to", value)}
        />
      </Block>
    </Stack>
  );

  return (
    <>
      {mdUp ? (
        renderContent
      ) : (
        <Drawer
          anchor="right"
          open={open}
          onClose={onClose}
          PaperProps={{
            sx: {
              pt: 5,
              px: 3,
              width: 280,
            },
          }}
        >
          {renderContent}
        </Drawer>
      )}
    </>
  );
}

// ----------------------------------------------------------------------

type BlockProps = {
  title: string;
  clear?: boolean;
  onClear?: VoidFunction;
  children: React.ReactNode;
};

function Block({ title, clear, onClear, children }: BlockProps) {
  return (
    <Stack spacing={0.5}>
      <Stack
        direction="row"
        justifyContent="space-between"
        alignItems="center"
        sx={{ minHeight: 30 }}
      >
        <Typography variant="overline" sx={{ color: "text.disabled" }}>
          {title}
        </Typography>
        {clear && (
          <Button variant="text" size="small" color="primary" onClick={onClear}>
            Wyczyść
          </Button>
        )}
      </Stack>

      {children}
    </Stack>
  );
}
