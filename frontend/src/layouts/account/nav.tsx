"use client";

import { useRouter } from "next/navigation";
import { useState, useEffect, ChangeEvent } from "react";

import Link from "@mui/material/Link";
import Stack from "@mui/material/Stack";
import { LoadingButton } from "@mui/lab";
import Drawer from "@mui/material/Drawer";
import Avatar from "@mui/material/Avatar";
import Divider from "@mui/material/Divider";
import { alpha } from "@mui/material/styles";
import ListItemText from "@mui/material/ListItemText";
import ListItemIcon from "@mui/material/ListItemIcon";
import ListItemButton from "@mui/material/ListItemButton";

import { paths } from "src/routes/paths";
import { useActiveLink } from "src/routes/hooks";
import { RouterLink } from "src/routes/components";

import { useResponsive } from "src/hooks/use-responsive";

import { useUserDetails, useUpdateUserDetails } from "src/api/auth/details";

import Iconify from "src/components/iconify";
import { useUserContext } from "src/components/user";
import TextMaxLine from "src/components/text-max-line";
import { useToastContext } from "src/components/toast";
import { CropperModal } from "src/components/cropper/cropper";

// ----------------------------------------------------------------------

const navigations = [
  {
    title: "Dane osobowe",
    path: paths.account.personal,
    icon: <Iconify icon="carbon:user" />,
  },
  {
    title: "Zarządzaj hasłem",
    path: paths.account.password,
    icon: <Iconify icon="carbon:user" />,
  },
  {
    title: "Lekcje",
    path: paths.account.lessons,
    icon: <Iconify icon="carbon:document" />,
  },
];

// ----------------------------------------------------------------------

type Props = {
  open: boolean;
  onClose: VoidFunction;
};

export default function Nav({ open, onClose }: Props) {
  const { enqueueSnackbar } = useToastContext();

  const { push } = useRouter();

  const mdUp = useResponsive("up", "md");

  const { logoutUser, isLoggedIn } = useUserContext();

  const { data: userDetails } = useUserDetails();
  const { mutateAsync: updatePhoto, isLoading } = useUpdateUserDetails();

  const handleLogout = async () => {
    try {
      await logoutUser({});
      enqueueSnackbar("Wylogowano pomyślnie", { variant: "success" });
    } catch (error) {
      enqueueSnackbar("Wystąpił błąd", { variant: "error" });
    }
  };

  useEffect(() => {
    if (!isLoggedIn) {
      push(paths.login);
    }
  }, [isLoggedIn, push]);

  const genderAvatarUrl =
    userDetails?.gender === "Kobieta"
      ? "/assets/images/avatar/avatar_female.jpg"
      : "/assets/images/avatar/avatar_male.jpg";

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
      await updatePhoto({ ...userDetails, image: newPhoto ?? "" });
      enqueueSnackbar("Zapisano pomyślnie", { variant: "success" });
    } catch (error) {
      enqueueSnackbar("Wystąpił błąd", { variant: "error" });
    }
  };

  const handleImageChange = async (source: string) => {
    await handleSubmit(source);
  };

  const renderContent = (
    <Stack
      sx={{
        flexShrink: 0,
        borderRadius: 2,
        width: 1,
        ...(mdUp && {
          width: 280,
          border: (theme) => `solid 1px ${alpha(theme.palette.grey[500], 0.24)}`,
        }),
      }}
    >
      <Stack spacing={2} sx={{ p: 3, pb: 2 }}>
        <Stack spacing={2} direction="row" alignItems="center">
          <Avatar src={avatarUrl} sx={{ width: 64, height: 64 }} />
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
        </Stack>

        {userDetails && (
          <Stack spacing={0.5}>
            <TextMaxLine variant="subtitle1" line={1}>
              {`${userDetails.first_name} ${userDetails.last_name}`}
            </TextMaxLine>
            <TextMaxLine variant="body2" line={1} sx={{ color: "text.secondary" }}>
              {userDetails.email}
            </TextMaxLine>
          </Stack>
        )}
      </Stack>

      <Divider sx={{ borderStyle: "dashed" }} />

      <Stack sx={{ my: 1, px: 2 }}>
        {navigations.map((item) => (
          <NavItem key={item.title} item={item} />
        ))}
      </Stack>

      <Divider sx={{ borderStyle: "dashed" }} />

      <Stack sx={{ my: 1, px: 2 }}>
        <ListItemButton
          sx={{
            px: 1,
            height: 44,
            borderRadius: 1,
          }}
          onClick={handleLogout}
        >
          <ListItemIcon>
            <Iconify icon="carbon:logout" />
          </ListItemIcon>
          <ListItemText
            primary="Wyloguj"
            primaryTypographyProps={{
              typography: "body2",
            }}
          />
        </ListItemButton>
      </Stack>
    </Stack>
  );

  return (
    <>
      {mdUp ? (
        renderContent
      ) : (
        <Drawer
          open={open}
          onClose={onClose}
          PaperProps={{
            sx: {
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

type NavItemProps = {
  item: {
    title: string;
    path: string;
    icon: React.ReactNode;
  };
};

function NavItem({ item }: NavItemProps) {
  const active = useActiveLink(item.path);

  return (
    <Link
      component={RouterLink}
      key={item.title}
      href={item.path}
      color={active ? "primary" : "inherit"}
      underline="none"
    >
      <ListItemButton
        sx={{
          px: 1,
          height: 44,
          borderRadius: 1,
        }}
      >
        <ListItemIcon>{item.icon}</ListItemIcon>
        <ListItemText
          primary={item.title}
          primaryTypographyProps={{
            typography: "body2",
            ...(active && {
              typography: "subtitle2",
            }),
          }}
        />
      </ListItemButton>
    </Link>
  );
}
