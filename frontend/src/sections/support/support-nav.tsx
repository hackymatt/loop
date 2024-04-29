import Box from "@mui/material/Box";
import Tabs from "@mui/material/Tabs";
import { Button } from "@mui/material";
import Drawer from "@mui/material/Drawer";
import { styled } from "@mui/material/styles";
import Typography from "@mui/material/Typography";
import Tab, { tabClasses } from "@mui/material/Tab";
import Stack, { StackProps } from "@mui/material/Stack";
import CardActionArea from "@mui/material/CardActionArea";

import { paths } from "src/routes/paths";
import { RouterLink } from "src/routes/components";

import { useResponsive } from "src/hooks/use-responsive";

import Image from "src/components/image";
import Iconify from "src/components/iconify";
import Scrollbar from "src/components/scrollbar";

// ----------------------------------------------------------------------

interface ContactButtonStyleProps extends StackProps {
  href: string;
  children?: React.ReactNode;
}

const StyledButton = styled((props: ContactButtonStyleProps) => (
  <CardActionArea sx={{ borderRadius: 1 }}>
    <Button component={RouterLink} href={props.href} color="inherit" fullWidth>
      <Stack direction="row" alignItems="center" spacing={2} {...props} width={1} />
    </Button>
  </CardActionArea>
))(({ theme }) => ({
  ...theme.typography.subtitle2,
  padding: theme.spacing(2),
  borderRadius: theme.shape.borderRadius,
  border: `solid 1px ${theme.palette.divider}`,
}));

// ----------------------------------------------------------------------

type Props = {
  data: {
    title: string;
    icon: string;
  }[];
  open: boolean;
  onClose: VoidFunction;
  topic: string;
  onChangeTopic: (event: React.SyntheticEvent, newValue: string) => void;
};

export default function SupportNav({ topic, data, onChangeTopic, open, onClose }: Props) {
  const mdUp = useResponsive("up", "md");

  const renderContent = (
    <Scrollbar
      sx={{
        py: { xs: 3, md: 0 },
      }}
    >
      <Tabs
        value={topic}
        onChange={onChangeTopic}
        orientation="vertical"
        sx={{
          pl: { xs: 2.5, md: 0 },
        }}
      >
        {data.map((item) => (
          <Tab
            key={item.title}
            value={item.title}
            label={item.title}
            icon={
              <Image
                disabledEffect
                alt={item.icon}
                src={item.icon}
                sx={{ width: 28, height: 28, mr: `20px !important` }}
              />
            }
            sx={{
              height: 56,
              typography: "body2",
              justifyContent: "flex-start",
              [`& .${tabClasses.selected}`]: {
                typography: "subtitle2",
              },
            }}
          />
        ))}
      </Tabs>

      <Box
        sx={{
          mt: { xs: 2.5, md: 5 },
          pl: { xs: 2.5, md: 0 },
          pr: { xs: 2.5, md: 5 },
        }}
      >
        <Typography variant="h4" paragraph>
          Nadal potrzebujesz pomocy?
        </Typography>

        <Stack spacing={2}>
          <StyledButton href={paths.contact}>
            <Iconify icon="carbon:email" width={24} />
            <Typography variant="subtitle2">Kontakt</Typography>
          </StyledButton>
        </Stack>
      </Box>
    </Scrollbar>
  );

  return mdUp ? (
    <Drawer
      variant="permanent"
      PaperProps={{
        sx: {
          width: 280,
          position: "unset",
          bgcolor: "background.default",
        },
      }}
    >
      {renderContent}
    </Drawer>
  ) : (
    <Drawer
      open={open}
      onClose={onClose}
      PaperProps={{
        sx: { width: 280 },
      }}
    >
      {renderContent}
    </Drawer>
  );
}
