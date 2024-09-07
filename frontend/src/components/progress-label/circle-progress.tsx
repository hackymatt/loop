import { Box, Typography, CircularProgress, CircularProgressProps } from "@mui/material";

export function CircularProgressWithLabel(props: CircularProgressProps & { value: number }) {
  const { value, size } = props;
  return (
    <Box sx={{ position: "relative", display: "inline-flex" }}>
      <CircularProgress variant="determinate" {...props} />
      <Box
        sx={{
          top: 0,
          left: 0,
          bottom: 0,
          right: 0,
          position: "absolute",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
        }}
      >
        <Typography
          variant="caption"
          component="div"
          sx={{ color: "text.secondary", fontSize: Number(size) / 3.5 }}
        >{`${Math.round(value)}%`}</Typography>
      </Box>
    </Box>
  );
}
