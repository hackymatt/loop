import { Gender, IGender } from "src/types/testimonial";

export function getGenderAvatar(gender?: IGender) {
  switch (gender) {
    case Gender.FEMALE:
      return "/assets/images/avatar/avatar_female.jpg";
    case Gender.MALE:
      return "/assets/images/avatar/avatar_male.jpg";
    default:
      return "/assets/images/avatar/avatar_default.jpg";
  }
}
