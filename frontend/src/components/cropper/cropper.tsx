import { useRef, useState } from "react";
import AvatarEditor from "react-avatar-editor";

import { Box, Modal, Stack, Slider, Button, Typography } from "@mui/material";

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
    <Modal
      sx={{
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
      }}
      open={open}
    >
      <Box
        sx={{
          position: "absolute",
          top: "50%",
          left: "50%",
          transform: "translate(-50%, -50%)",
          boxShadow: 24,
          bgcolor: "common.white",
          p: 6,
          borderRadius: "4px",
        }}
      >
        <Stack
          spacing={0.5}
          sx={{
            width: "300px",
            height: "300px",
            display: "flex",
            flexFlow: "column",
            justifyContent: "center",
            alignItems: "center",
            p: 2,
          }}
        >
          <Typography variant="h6" component="h2">
            Dopasuj zdjęcie
          </Typography>
          <AvatarEditor
            ref={cropRef}
            image={image}
            style={{ width: "100%", height: "100%" }}
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

          <Stack direction="row" spacing={1} sx={{ p: 2 }}>
            <Button color="inherit" size="small" variant="contained" onClick={onClose}>
              Anuluj
            </Button>
            <Button color="primary" size="small" variant="contained" onClick={handleSave}>
              Zapisz
            </Button>
          </Stack>
        </Stack>
      </Box>
    </Modal>
  );
};
