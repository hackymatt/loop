import { useState, useEffect, useCallback } from "react";

import Stack from "@mui/material/Stack";
import Drawer from "@mui/material/Drawer";
import TextField from "@mui/material/TextField";
import Typography from "@mui/material/Typography";
import InputAdornment from "@mui/material/InputAdornment";

import { useResponsive } from "src/hooks/use-responsive";
import { useQueryParams } from "src/hooks/use-query-params";

import Iconify from "src/components/iconify";

import { IQueryParams, IQueryParamValue } from "src/types/queryParams";

import FilterLevel from "./filter-level";
import FilterPrice from "./filter-price";
import FilterRating from "./filter-rating";
import FilterDuration from "./filter-duration";
import FilterCategories from "./filter-categories";

// ----------------------------------------------------------------------

type Props = {
  open: boolean;
  onClose: VoidFunction;
  onChange: (filters: IQueryParams) => void;
};

export default function Filters({ open, onClose, onChange }: Props) {
  const mdUp = useResponsive("up", "md");
  const { getQueryParam, setQueryParam, removeQueryParam } = useQueryParams();

  const [filters, setFilters] = useState<IQueryParams>({
    search: getQueryParam("search"),
    rating_from: getQueryParam("rating_from"),
    level_in: getQueryParam("level_in"),
    technology_in: getQueryParam("technology_in"),
    price_from: getQueryParam("price_from"),
    price_to: getQueryParam("price_to"),
    filters: getQueryParam("filters"),
  });

  useEffect(() => {
    if (filters) {
      onChange(filters);
    }
  }, [filters, onChange]);

  const handleChange = useCallback(
    (name: string, value: IQueryParamValue) => {
      console.log(value);
      if (value) {
        setFilters({
          ...filters,
          [name]: value,
        });
        setQueryParam(name, value);
      } else {
        setFilters({
          ...filters,
          [name]: null,
        });
        removeQueryParam(name);
      }
    },
    [filters, removeQueryParam, setQueryParam],
  );

  const renderContent = (
    <Stack
      spacing={2.5}
      sx={{
        flexShrink: 0,
        width: { xs: 1, md: 280 },
      }}
    >
      <TextField
        fullWidth
        hiddenLabel
        placeholder="Szukaj..."
        InputProps={{
          startAdornment: (
            <InputAdornment position="start">
              <Iconify icon="carbon:search" width={24} sx={{ color: "text.disabled" }} />
            </InputAdornment>
          ),
        }}
        value={filters?.search ?? ""}
        onChange={(event) => handleChange("search", event.target.value)}
      />

      <Block title="Ocena">
        <FilterRating
          filterRating={filters?.rating_from ?? null}
          onChangeRating={(value) => handleChange("rating_from", value)}
        />
      </Block>

      <Block title="Czas trwania">
        <FilterDuration
          filterDuration={filters?.filters ?? ""}
          onChangeDuration={(value) => handleChange("filters", value)}
        />
      </Block>

      <Block title="Technologia">
        <FilterCategories
          filterCategories={filters?.technology_in ?? ""}
          onChangeCategory={(value) => handleChange("technology_in", value)}
        />
      </Block>

      <Block title="Poziom">
        <FilterLevel
          filterLevel={filters?.level_in ?? ""}
          onChangeLevel={(value) => handleChange("level_in", value)}
        />
      </Block>

      <Block title="Cena">
        <FilterPrice
          filterPriceFrom={filters?.price_from ?? 0}
          filterPriceTo={filters?.price_to ?? 0}
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
  children: React.ReactNode;
};

function Block({ title, children }: BlockProps) {
  return (
    <Stack spacing={1.5}>
      <Typography variant="overline" sx={{ color: "text.disabled" }}>
        {title}
      </Typography>

      {children}
    </Stack>
  );
}
