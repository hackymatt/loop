import { useRef, useState } from "react";
import AvatarEditor from "react-avatar-editor";

import { Box, Modal, Slider, Button, Stack } from "@mui/material";

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
      <Stack
        spacing={0.5}
        sx={{
          width: "300px",
          height: "300px",
          display: "flex",
          flexFlow: "column",
          justifyContent: "center",
          alignItems: "center",
        }}
      >
        <AvatarEditor
          ref={cropRef}
          image={image}
          style={{ width: "100%", height: "100%" }}
          border={50}
          borderRadius={150}
          color={[0, 0, 0, 0.72]}
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

        <Stack direction="row" spacing={1}>
          <Button color="inherit" size="small" variant="contained" onClick={onClose}>
            Anuluj
          </Button>
          <Button color="primary" size="small" variant="contained" onClick={handleSave}>
            Zapisz
          </Button>
        </Stack>
      </Stack>
    </Modal>
  );
};
