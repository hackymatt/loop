import Box from "@mui/material/Box";
import { Stack } from "@mui/system";
import { Button } from "@mui/material";
import Container from "@mui/material/Container";
import Typography from "@mui/material/Typography";

import { paths } from "src/routes/paths";

import { ITeamMemberProps } from "src/types/team";

import TeamItem from "./team-item";

// ----------------------------------------------------------------------

type Props = {
  members: ITeamMemberProps[];
};

export default function TeamAbout({ members }: Props) {
  const TEAM_MEMBER_SLOTS: number = 4 as const;
  return (
    <Container sx={{ py: { xs: 8, md: 15 } }}>
      <Typography
        variant="h2"
        sx={{
          textAlign: "center",
          mb: { xs: 4, md: 5 },
        }}
      >
        Nasi instruktorzy
      </Typography>

      <Box
        sx={{
          columnGap: 3,
          display: "grid",
          rowGap: { xs: 4, md: 5 },
          py: { xs: 4, md: 5 },
          gridTemplateColumns: {
            xs: "repeat(1, 1fr)",
            sm: "repeat(2, 1fr)",
            md: "repeat(4, 1fr)",
          },
        }}
      >
        {members.map((member) => (
          <TeamItem key={member.id} member={member} />
        ))}
      </Box>

      {members.length > TEAM_MEMBER_SLOTS && (
        <Stack alignItems="center">
          <Button variant="outlined" size="large" color="inherit" href={paths.teachers}>
            Zobacz wszystkich instruktorów
          </Button>
        </Stack>
      )}
    </Container>
  );
}
