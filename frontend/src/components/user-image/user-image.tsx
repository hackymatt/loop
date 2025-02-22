import { useMemo, useState, ChangeEvent } from "react";

import { Stack } from "@mui/system";
import { Avatar, Tooltip } from "@mui/material";
import LoadingButton from "@mui/lab/LoadingButton";

import { getGenderAvatar } from "src/utils/get-gender-avatar";

import { Gender } from "src/consts/gender";

import Iconify from "src/components/iconify";
import { CropperModal } from "src/components/cropper/cropper";

import { IUserProps } from "src/types/user";

// ----------------------------------------------------------------------

type Props = {
  userDetails?: IUserProps;
  loading?: boolean;
  buttonPosition?: "left" | "right";
  onChange: (image: string) => void;
};

export default function UserImage({
  userDetails,
  buttonPosition = "right",
  loading,
  onChange,
}: Props) {
  const genderAvatarUrl = getGenderAvatar(userDetails?.gender ?? Gender.Other);

  const isImage = useMemo(() => Boolean(userDetails?.image), [userDetails?.image]);

  const avatarUrl = useMemo(
    () => userDetails?.image ?? genderAvatarUrl,
    [genderAvatarUrl, userDetails?.image],
  );

  const [isCropperModalOpen, setIsCropperModalOpen] = useState<boolean>(false);
  const [image, setImage] = useState<string>();

  const handleImagePick = (e: ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { files } = e.target as HTMLInputElement;
    if (files && files.length > 0) {
      setImage(URL.createObjectURL(files[0]));
      setIsCropperModalOpen(true);
    }
  };

  const handleImageChange = async (source: string) => {
    onChange(source);
  };

  const isUploadDisabled = useMemo(
    () => userDetails?.firstName === "" || userDetails?.lastName === "",
    [userDetails?.firstName, userDetails?.lastName],
  );

  const button = (
    <Tooltip title={isUploadDisabled ? "Uzupełnij swoje dane osobowe" : ""}>
      <Stack
        direction="row"
        alignItems="center"
        sx={{
          typography: "caption",
          cursor: "pointer",
          "&:hover": { opacity: 0.72 },
        }}
      >
        {!isImage ? (
          <LoadingButton
            component="label"
            variant="text"
            size="small"
            color="primary"
            startIcon={<Iconify icon="carbon:add-large" />}
            loading={loading}
            disabled={isUploadDisabled}
          >
            Dodaj zdjęcie
            <input type="file" hidden onChange={handleImagePick} />
          </LoadingButton>
        ) : (
          <LoadingButton
            component="label"
            variant="text"
            size="small"
            color="error"
            startIcon={<Iconify icon="carbon:subtract-large" />}
            loading={loading}
            onClick={() => handleImageChange("")}
          >
            Usuń zdjęcie
          </LoadingButton>
        )}
      </Stack>
    </Tooltip>
  );

  return (
    <>
      <Stack spacing={2} direction="row" alignItems="center">
        {buttonPosition === "left" && button}
        <Avatar src={avatarUrl} sx={{ width: 64, height: 64 }} />
        {buttonPosition === "right" && button}
      </Stack>
      <CropperModal
        open={isCropperModalOpen}
        image={image ?? ""}
        onImageChange={handleImageChange}
        onClose={() => setIsCropperModalOpen(false)}
      />
    </>
  );
}
