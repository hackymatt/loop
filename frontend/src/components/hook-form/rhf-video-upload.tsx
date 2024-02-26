import { useRef, useState, ChangeEvent } from "react";
import { Controller, useFormContext } from "react-hook-form";

import { Stack } from "@mui/system";
import LoadingButton from "@mui/lab/LoadingButton";
import FormHelperText from "@mui/material/FormHelperText";
import FormControlLabel, { FormControlLabelProps } from "@mui/material/FormControlLabel";

import { urlToBlob } from "src/utils/blob-to-base64";

import Player from "../player";
import Iconify from "../iconify";

// ----------------------------------------------------------------------

interface Props extends Omit<FormControlLabelProps, "control"> {
  name: string;
  helperText?: React.ReactNode;
}

export default function RHFVideoUpload({ name, helperText, ...other }: Props) {
  const { control } = useFormContext();

  return (
    <Controller
      name={name}
      control={control}
      render={({ field, fieldState: { error } }) => (
        <div>
          <FormControlLabel control={<VideoInput {...field} />} {...other} />

          {(!!error || helperText) && (
            <FormHelperText error={!!error}>{error ? error?.message : helperText}</FormHelperText>
          )}
        </div>
      )}
    />
  );
}

function VideoInput({ value, onChange }: { value: string; onChange: (file: string) => void }) {
  const videoRef = useRef(null);
  const [source, setSource] = useState<string>(value);

  const handleFilePick = async (e: ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { files } = e.target as HTMLInputElement;
    if (files && files.length > 0) {
      const url = URL.createObjectURL(files[0]);
      setSource(url);
      const base64Image = await urlToBlob(url);
      onChange(base64Image as string);
    }
  };

  return (
    <Stack
      direction="column"
      alignItems="center"
      sx={{
        typography: "caption",
        cursor: "pointer",
        "&:hover": { opacity: 0.72 },
      }}
    >
      {source === "" ? (
        <LoadingButton
          component="label"
          variant="text"
          size="small"
          color="primary"
          startIcon={<Iconify icon="carbon:add-large" />}
        >
          Dodaj film
          <input ref={videoRef} hidden type="file" onChange={handleFilePick} accept=".mp4" />
        </LoadingButton>
      ) : (
        <LoadingButton
          component="label"
          variant="text"
          size="small"
          color="error"
          startIcon={<Iconify icon="carbon:subtract-large" />}
          onClick={() => setSource("")}
        >
          Usuń film
        </LoadingButton>
      )}
      {source && <Player controls url={source} />}
    </Stack>
  );
}
