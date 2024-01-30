import { useMemo, useCallback } from "react";

import Stack from "@mui/material/Stack";
import Drawer from "@mui/material/Drawer";
import Button from "@mui/material/Button";
import Typography from "@mui/material/Typography";

import { useResponsive } from "src/hooks/use-responsive";
import { useQueryParams } from "src/hooks/use-query-params";

import { IQueryParamValue } from "src/types/queryParams";

import FilterRating from "./filter-rating";
import FilterSearch from "./filter-search";

// ----------------------------------------------------------------------

type Props = {
  open: boolean;
  onClose: VoidFunction;
};

export default function Filters({ open, onClose }: Props) {
  const mdUp = useResponsive("up", "md");
  const { setQueryParam, removeQueryParam, getQueryParams } = useQueryParams();

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
      spacing={2.5}
      sx={{
        flexShrink: 0,
        width: { xs: 1, md: 280 },
      }}
    >
      <FilterSearch
        filterSearch={filters?.search ?? ""}
        onChangeSearch={(value) => handleChange("search", value)}
      />

      <Block
        title="Ocena"
        clear={!!filters?.rating_from}
        onClear={() => handleChange("rating_from", null)}
      >
        <FilterRating
          filterRating={filters?.rating_from ?? null}
          onChangeRating={(value) => handleChange("rating_from", value)}
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
