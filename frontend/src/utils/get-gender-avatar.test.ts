import { Gender } from "src/types/testimonial";

import { getGenderAvatar } from "./get-gender-avatar";

describe("getGenderAvatar", () => {
  // Returns female avatar path for Gender.FEMALE
  it("should return female avatar path when gender is Gender.FEMALE", () => {
    const result = getGenderAvatar(Gender.FEMALE);
    expect(result).toBe("/assets/images/avatar/avatar_female.jpg");
  });

  // Returns male avatar path for Gender.MALE
  it("should return male avatar path when gender is Gender.MALE", () => {
    const result = getGenderAvatar(Gender.MALE);
    expect(result).toBe("/assets/images/avatar/avatar_male.jpg");
  });

  // Returns default avatar path for Gender.OTHER
  it("should return default avatar path when gender is Gender.OTHER", () => {
    const result = getGenderAvatar(Gender.OTHER);
    expect(result).toBe("/assets/images/avatar/avatar_default.jpg");
  });
});
