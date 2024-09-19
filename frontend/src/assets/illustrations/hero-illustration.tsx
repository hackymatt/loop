import { memo } from "react";
import { m } from "framer-motion";

import Box, { BoxProps } from "@mui/material/Box";

import Image from "src/components/image";

import Shape from "./pattern/shape";
import Pattern02 from "./pattern/pattern-02";
import Pattern01 from "./pattern/pattern-01";

// ----------------------------------------------------------------------

const varUp = {
  animate: { y: [-8, 8, -8], x: [-4, 4, -4] },
  transition: { duration: 8, repeat: Infinity },
};

const varDown = {
  animate: { y: [8, -8, 8], x: [4, -4, 4] },
  transition: { duration: 8, repeat: Infinity },
};

const varLeft = {
  animate: { x: [8, -8, 8], y: [4, -4, 4] },
  transition: { duration: 7, repeat: Infinity },
};

const varRight = {
  animate: { x: [8, -8, 8], y: [4, -4, 4] },
  transition: { duration: 7, repeat: Infinity },
};

// ----------------------------------------------------------------------

function HeroIllustration({ sx, ...other }: BoxProps) {
  return (
    <Box
      sx={{
        width: 670,
        height: 670,
        display: "flex",
        alignItems: "center",
        position: "relative",
        justifyContent: "center",
        ...sx,
      }}
      {...other}
    >
      <Box sx={{ position: "absolute", right: 18, bottom: 28, zIndex: 8 }}>
        <Image
          visibleByDefault
          disabledEffect
          alt="teacher"
          src="/assets/images/general/teacher-hero.webp"
          sx={{ width: 546, height: 650 }}
        />
      </Box>

      <Box
        {...varRight}
        component={m.div}
        sx={{ position: "absolute", left: 18, top: 220, zIndex: 8 }}
      >
        <Image
          visibleByDefault
          disabledEffect
          alt="pencil icon"
          src="/assets/icons/ic_pencil.png"
          sx={{ width: 60, height: 77 }}
        />
      </Box>

      <Box
        {...varUp}
        component={m.div}
        sx={{ zIndex: 9, left: 120, bottom: 168, position: "absolute" }}
      >
        <Image
          visibleByDefault
          disabledEffect
          alt="python"
          src="/assets/icons/platforms/ic_python.svg"
          sx={{ width: 56, height: 56 }}
        />
      </Box>

      {/* Icon */}

      <Box
        {...varLeft}
        component={m.div}
        sx={{ top: 80, right: 42, zIndex: 8, position: "absolute" }}
      >
        <Image
          visibleByDefault
          disabledEffect
          alt="vba"
          src="/assets/icons/platforms/ic_vba.svg"
          sx={{ height: 66 }}
        />
      </Box>

      <Box
        {...varLeft}
        component={m.div}
        sx={{ top: 120, left: 120, zIndex: 8, position: "absolute" }}
      >
        <Image
          visibleByDefault
          disabledEffect
          alt="java"
          src="/assets/icons/platforms/ic_java.svg"
          sx={{ height: 56 }}
        />
      </Box>

      <Box {...varRight} component={m.div} sx={{ zIndex: 8, bottom: 160, position: "absolute" }}>
        <Image
          visibleByDefault
          disabledEffect
          alt="js"
          src="/assets/icons/platforms/ic_js.svg"
          sx={{ width: 56, height: 56 }}
        />
      </Box>

      <Box
        {...varUp}
        component={m.div}
        sx={{ zIndex: 8, bottom: 240, right: 90, position: "absolute" }}
      >
        <Image
          visibleByDefault
          disabledEffect
          alt="c++"
          src="/assets/icons/platforms/ic_c++.svg"
          sx={{ width: 56, height: 56 }}
        />
      </Box>

      <Box
        {...varUp}
        component={m.div}
        sx={{ zIndex: 8, top: 210, right: 0, position: "absolute" }}
      >
        <Image
          visibleByDefault
          disabledEffect
          alt="c++"
          src="/assets/icons/platforms/ic_git.svg"
          sx={{ height: 46 }}
        />
      </Box>

      <Box {...varDown} component={m.div} sx={{ zIndex: 8, left: 150, position: "absolute" }}>
        <Image
          visibleByDefault
          disabledEffect
          alt="ts"
          src="/assets/icons/platforms/ic_ts.svg"
          sx={{ width: 56, height: 56 }}
        />
      </Box>

      <Pattern01 sx={{ left: 0, top: 0 }} />
      <Pattern02 sx={{ top: 0, left: 0, opacity: 0.24, transform: "scale(1.2)" }} />
      <Shape sx={{ position: "absolute", right: 32, bottom: 32 }} />
    </Box>
  );
}

export default memo(HeroIllustration);
