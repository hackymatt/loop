import Box from "@mui/material/Box";
import { Link } from "@mui/material";
import Chip from "@mui/material/Chip";
import Stack from "@mui/material/Stack";
import { alpha } from "@mui/material/styles";
import Typography from "@mui/material/Typography";

import { paths } from "src/routes/paths";
import { RouterLink } from "src/routes/components";

import Iconify, { isIconExists } from "src/components/iconify";
import { CircularProgressWithLabel } from "src/components/progress-label/circle-progress";

import {
  ICourseTagProps,
  ICourseTopicProps,
  ICourseDetailsProps,
  ICourseCandidateProps,
  ICourseTechnologyDetailsProps,
} from "src/types/course";

import CourseDetailsModuleList from "./course-details-module-list";

// ----------------------------------------------------------------------

type Props = {
  course: ICourseDetailsProps;
};

export default function CourseDetailsSummary({ course }: Props) {
  const { progress, modules, overview, candidates, topics, technologies, tags } = course;

  return (
    <Stack spacing={5}>
      <Stack direction="row" spacing={1} alignItems="center">
        {progress !== null ? <CircularProgressWithLabel value={progress} size={40} /> : null}
        <Typography variant="h4">Program szkolenia</Typography>
      </Stack>

      {modules.length > 0 ? <CourseDetailsModuleList course={course} modules={modules} /> : null}

      <Box>
        <Typography component="h6" variant="h4" sx={{ mb: 2 }}>
          Dlaczego ten kurs?
        </Typography>
        <Typography sx={{ textAlign: "justify" }}>
          {overview?.split("\n").map((line, index) => (
            <Box key={index} component="span">
              {line}
              <br />
            </Box>
          )) ?? ""}
        </Typography>
      </Box>

      {candidates.length > 0 ? (
        <Stack spacing={3}>
          <Typography variant="h4">Dla kogo ten kurs?</Typography>

          <Stack spacing={1}>
            {candidates.map((candidate: ICourseCandidateProps) => (
              <Stack key={candidate.id} direction="row" alignItems="center" spacing={1.5}>
                <Box
                  sx={{
                    width: 20,
                    height: 20,
                    flexShrink: 0,
                    display: "flex",
                    borderRadius: "50%",
                    alignItems: "center",
                    justifyContent: "center",
                    bgcolor: (theme) => alpha(theme?.palette?.primary?.main, 0.08),
                  }}
                >
                  <Iconify
                    icon="carbon:checkmark"
                    sx={{ width: 16, height: 16, color: "primary.main" }}
                  />
                </Box>
                {candidate.name}
              </Stack>
            ))}
          </Stack>
        </Stack>
      ) : null}

      {topics.length > 0 ? (
        <Stack spacing={3}>
          <Typography variant="h4">Czego się nauczysz?</Typography>

          <Stack spacing={1}>
            {topics.map((topic: ICourseTopicProps) => (
              <Stack key={topic.id} direction="row" alignItems="center" spacing={1.5}>
                <Box
                  sx={{
                    width: 20,
                    height: 20,
                    flexShrink: 0,
                    display: "flex",
                    borderRadius: "50%",
                    alignItems: "center",
                    justifyContent: "center",
                    bgcolor: (theme) => alpha(theme?.palette?.primary?.main, 0.08),
                  }}
                >
                  <Iconify
                    icon="carbon:checkmark"
                    sx={{ width: 16, height: 16, color: "primary.main" }}
                  />
                </Box>
                {topic.name}
              </Stack>
            ))}
          </Stack>
        </Stack>
      ) : null}

      {technologies.length > 0 ? (
        <Stack spacing={3}>
          <Typography variant="h4">O technologiach w tym kursie</Typography>

          <Stack spacing={2}>
            {technologies.map((technology: ICourseTechnologyDetailsProps) => {
              const defaultIcon = `bxl:${technology.name.toLowerCase()}`;
              const icon = isIconExists(defaultIcon) ? defaultIcon : "carbon:code";
              return (
                <Stack key={technology.id} spacing={0}>
                  <Stack direction="row" alignItems="center" spacing={1.5}>
                    <Box
                      sx={{
                        width: 20,
                        height: 20,
                        flexShrink: 0,
                        display: "flex",
                        borderRadius: "50%",
                        alignItems: "center",
                        justifyContent: "center",
                        bgcolor: (theme) => alpha(theme?.palette?.primary?.main, 0.08),
                      }}
                    >
                      <Iconify icon={icon} sx={{ width: 16, height: 16, color: "primary.main" }} />
                    </Box>
                    {technology.name}
                  </Stack>
                  <Typography
                    variant="body2"
                    color="text.secondary"
                    ml={4}
                    sx={{ textAlign: "justify" }}
                  >
                    {technology.description?.split("\n").map((line, index) => (
                      <Box key={index} component="span">
                        {line}
                        <br />
                      </Box>
                    )) ?? ""}
                  </Typography>
                </Stack>
              );
            })}
          </Stack>
        </Stack>
      ) : null}

      {tags.length > 0 ? (
        <Box display="flex" alignItems="center" flexWrap="wrap">
          <Typography variant="subtitle2" sx={{ mr: 1 }}>
            Tagi
          </Typography>

          <Box gap={1} display="flex" flexWrap="wrap">
            {tags.map((tag: ICourseTagProps) => (
              <Link
                component={RouterLink}
                key={tag.id}
                href={`${paths.courses}?tags_in=${tag.name}`}
              >
                <Chip key={tag.id} size="small" variant="soft" label={tag.name} />
              </Link>
            ))}
          </Box>
        </Box>
      ) : null}
    </Stack>
  );
}
