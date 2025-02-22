import { fDate } from "src/utils/format-time";

import { useUserDetails, useUpdateUserDetails } from "src/api/auth/details";

import UserImage from "src/components/user-image";
import { useToastContext } from "src/components/toast";

// ----------------------------------------------------------------------

export default function AccountImage() {
  const { enqueueSnackbar } = useToastContext();

  const { data: userDetails } = useUserDetails();
  const { mutateAsync: updatePhoto, isLoading } = useUpdateUserDetails();

  const handleSubmit = async (newPhoto: string) => {
    if (userDetails) {
      const {
        firstName,
        lastName,
        dob,
        gender,
        phoneNumber,
        streetAddress,
        zipCode,
        city,
        country,
        // eslint-disable-next-line @typescript-eslint/no-unused-vars
        image: _,
        ...rest
      } = userDetails;
      try {
        await updatePhoto({
          ...rest,
          first_name: firstName,
          last_name: lastName,
          dob: dob ? fDate(dob, "yyyy-MM-dd") : null,
          gender,
          phone_number: phoneNumber ?? null,
          street_address: streetAddress ?? null,
          zip_code: zipCode ?? null,
          city: city ?? null,
          country: country ?? null,
          image: newPhoto ?? "",
        });
        enqueueSnackbar("Zapisano pomyślnie", { variant: "success" });
      } catch (error) {
        enqueueSnackbar("Wystąpił błąd", { variant: "error" });
      }
    }
  };

  const handleImageChange = async (source: string) => {
    await handleSubmit(source);
  };

  return <UserImage userDetails={userDetails} loading={isLoading} onChange={handleImageChange} />;
}
