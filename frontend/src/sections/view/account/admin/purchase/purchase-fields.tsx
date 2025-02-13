import { useUsers } from "src/api/users/users";
import { useServices } from "src/api/services/services";
import { usePayments } from "src/api/payment/payments";

import { RHFTextField, RHFAutocompleteDnd } from "src/components/hook-form";

import { IPaymentProp } from "src/types/payment";
import { IServiceProp } from "src/types/service";
import { UserType, IUserDetailsProps } from "src/types/user";

export const usePurchaseFields = () => {
  const { data: availableServices, isLoading: isLoadingServices } = useServices({
    sort_by: "title",
    page_size: -1,
  });
  const { data: availableOthers, isLoading: isLoadingOthers } = useUsers({
    sort_by: "email",
    user_type: UserType.OTHER[0],
    active: "False",
    page_size: -1,
  });

  const { data: availablePayments, isLoading: isLoadingPayments } = usePayments({
    sort_by: "session_id",
    page_size: -1,
  });

  const fields: { [key: string]: JSX.Element } = {
    service: (
      <RHFAutocompleteDnd
        key="service"
        name="service"
        label="Usługa"
        multiple
        options={availableServices ?? []}
        getOptionLabel={(option) => (option as IServiceProp)?.title ?? ""}
        loading={isLoadingServices}
        isOptionEqualToValue={(a, b) => a.title === b.title}
      />
    ),
    price: (
      <RHFTextField
        key="price"
        name="price"
        label="Cena"
        type="number"
        InputProps={{
          inputProps: { min: 0, step: ".01" },
        }}
      />
    ),
    other: (
      <RHFAutocompleteDnd
        key="other"
        name="other"
        label="Użytkownik"
        multiple
        options={availableOthers ?? []}
        getOptionLabel={(option) => (option as IUserDetailsProps)?.email ?? ""}
        loading={isLoadingOthers}
        isOptionEqualToValue={(a, b) => a.email === b.email}
      />
    ),
    payment: (
      <RHFAutocompleteDnd
        key="payment"
        name="payment"
        label="Płatność"
        multiple
        options={availablePayments ?? []}
        getOptionLabel={(option) => (option as IPaymentProp)?.sessionId ?? ""}
        loading={isLoadingPayments}
        isOptionEqualToValue={(a, b) => a.sessionId === b.sessionId}
      />
    ),
  };
  return { fields };
};
