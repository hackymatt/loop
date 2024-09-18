import Grid from "@mui/material/Unstable_Grid2";
import Container from "@mui/material/Container";
import Box, { BoxProps } from "@mui/material/Box";
import Typography from "@mui/material/Typography";

import {
  Carousel,
  useCarousel,
  CarouselThumbs,
  CarouselArrowFloatButtons,
} from "src/components/carousel";

import { ITestimonialProps } from "src/types/testimonial";

import { TestimonialItemContent, TestimonialItemThumbnail } from "./testimonial-item";

// ----------------------------------------------------------------------

type Props = BoxProps & {
  testimonials: ITestimonialProps[];
};

export default function Testimonial({ testimonials, sx, ...other }: Props) {
  const carousel = useCarousel({
    loop: true,
    startIndex: 1,
    thumbs: {
      loop: true,
      slidesToShow: "auto",
    },
  });

  return (
    <Box
      component="section"
      sx={{
        bgcolor: "background.neutral",
        py: { xs: 10, md: 15 },
        ...sx,
      }}
      {...other}
    >
      <Container sx={{ position: "relative" }}>
        <CarouselArrowFloatButtons
          {...carousel.arrows}
          options={carousel.options}
          slotProps={{
            prevBtn: { sx: { left: 16 } },
            nextBtn: { sx: { right: 16 } },
          }}
          sx={{
            borderRadius: "50%",
            color: "text.primary",
            bgcolor: "transparent",
            display: { xs: "none", md: "flex" },
          }}
        />

        <Grid container spacing={3} justifyContent="center">
          <Grid xs={12} md={6}>
            <Typography variant="h2" sx={{ mb: 5, textAlign: "center" }}>
              Co mówią nasi uczniowie
            </Typography>

            <Carousel carousel={carousel}>
              {testimonials.map((testimonial) => (
                <TestimonialItemContent key={testimonial.id} testimonial={testimonial} />
              ))}
            </Carousel>

            <CarouselThumbs
              ref={carousel.thumbs.thumbsRef}
              options={carousel.options?.thumbs}
              slotProps={{ disableMask: true }}
              sx={{ width: { xs: 1, sm: 480 } }}
            >
              {testimonials.map((testimonial, index) => (
                <TestimonialItemThumbnail
                  key={testimonial.id}
                  testimonial={testimonial}
                  selected={index === carousel.thumbs.selectedIndex}
                  onClick={() => carousel.thumbs.onClickThumb(index)}
                />
              ))}
            </CarouselThumbs>

            {testimonials.map(
              (testimonial, index) =>
                index === carousel.thumbs.selectedIndex && (
                  <Box key={testimonial.id} sx={{ mt: 3, textAlign: "center" }}>
                    <Typography variant="h6" sx={{ mb: 0.5 }}>
                      {testimonial.name}
                    </Typography>
                  </Box>
                ),
            )}
          </Grid>
        </Grid>
      </Container>
    </Box>
  );
}
