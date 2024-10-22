import { useMemo, useState, ChangeEvent } from "react";

import { Stack } from "@mui/system";
import { Avatar, Tooltip } from "@mui/material";
import LoadingButton from "@mui/lab/LoadingButton";

import { getGenderAvatar } from "src/utils/get-gender-avatar";

import { useUserDetails, useUpdateUserDetails } from "src/api/auth/details";

import Iconify from "src/components/iconify";
import { useToastContext } from "src/components/toast";
import { CropperModal } from "src/components/cropper/cropper";

import { IGender } from "src/types/testimonial";

// ----------------------------------------------------------------------

export default function AccountImage() {
  const { enqueueSnackbar } = useToastContext();

  const { data: userDetails } = useUserDetails();
  const { mutateAsync: updatePhoto, isLoading } = useUpdateUserDetails();

  const genderAvatarUrl = getGenderAvatar(userDetails?.gender);

  const avatarUrl = userDetails?.image || genderAvatarUrl;

  const [isCropperModalOpen, setIsCropperModalOpen] = useState<boolean>(false);
  const [image, setImage] = useState<string>();

  const handleImagePick = (e: ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { files } = e.target as HTMLInputElement;
    if (files && files.length > 0) {
      setImage(URL.createObjectURL(files[0]));
      setIsCropperModalOpen(true);
    }
  };

  const handleSubmit = async (newPhoto: string) => {
    try {
      await updatePhoto({
        ...userDetails,
        gender: (userDetails.gender as IGender) ?? "",
        image: newPhoto ?? "",
      });
      enqueueSnackbar("Zapisano pomyślnie", { variant: "success" });
    } catch (error) {
      enqueueSnackbar("Wystąpił błąd", { variant: "error" });
    }
  };

  const handleImageChange = async (source: string) => {
    await handleSubmit(source);
  };

  const isUploadDisabled = useMemo(
    () => userDetails?.first_name === "" || userDetails?.last_name === "",
    [userDetails?.first_name, userDetails?.last_name],
  );

  return (
    <Stack spacing={2} direction="row" alignItems="center">
      <Avatar src={avatarUrl} sx={{ width: 64, height: 64 }} />
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
          {userDetails?.image === null ? (
            <LoadingButton
              component="label"
              variant="text"
              size="small"
              color="primary"
              startIcon={<Iconify icon="carbon:add-large" />}
              loading={isLoading}
              disabled={isUploadDisabled}
            >
              Dodaj zdjęcie
              <input type="file" hidden onChange={handleImagePick} />
              <CropperModal
                open={isCropperModalOpen}
                image={image ?? ""}
                onImageChange={handleImageChange}
                onClose={() => setIsCropperModalOpen(false)}
              />
            </LoadingButton>
          ) : (
            <LoadingButton
              component="label"
              variant="text"
              size="small"
              color="error"
              startIcon={<Iconify icon="carbon:subtract-large" />}
              loading={isLoading}
              onClick={() => handleImageChange("")}
            >
              Usuń zdjęcie
            </LoadingButton>
          )}
        </Stack>
      </Tooltip>
    </Stack>
  );
}
