import { useRef, useState } from "react";
import AvatarEditor from "react-avatar-editor";

import { Stack, Slider, Button, Dialog, DialogActions, DialogContent } from "@mui/material";

import { blobToBase64 } from "src/utils/blob-to-base64";

type Props = {
  open: boolean;
  image: string;
  onImageChange: (source: string) => void;
  onClose: VoidFunction;
};

// Modal
export const CropperModal = ({ open, image, onImageChange, onClose }: Props) => {
  const [slideValue, setSlideValue] = useState<number>(10);
  const cropRef = useRef<InstanceType<typeof AvatarEditor>>(null);

  // handle save
  const handleSave = async () => {
    if (cropRef && cropRef.current) {
      const dataUrl = cropRef.current.getImage().toDataURL();
      const result = await fetch(dataUrl);
      const blob = await result.blob();
      const base64Image = await blobToBase64(blob);
      onImageChange(base64Image as string);
      onClose();
    }
  };

  const handleChange = (event: Event, newValue: number | number[]) => {
    setSlideValue(newValue as number);
  };

  return (
    <Dialog maxWidth="sm" onClose={onClose} open={open}>
      <DialogContent
        sx={{
          p: 1,
          display: "flex",
          flexFlow: "column",
          justifyContent: "center",
          alignItems: "center",
        }}
      >
        <Stack spacing={2.5}>
          <AvatarEditor
            ref={cropRef}
            image={image}
            border={0}
            borderRadius={150}
            scale={slideValue / 10}
            rotate={0}
          />

          <Slider
            min={5}
            max={20}
            sx={{
              margin: "0 auto",
              width: "90%",
            }}
            size="medium"
            defaultValue={slideValue}
            value={slideValue}
            onChange={handleChange}
          />
        </Stack>
      </DialogContent>

      <DialogActions>
        <Button variant="outlined" onClick={onClose} color="inherit">
          Anuluj
        </Button>

        <Button color="inherit" type="submit" variant="contained" onClick={handleSave}>
          Zapisz
        </Button>
      </DialogActions>
    </Dialog>
  );
};
