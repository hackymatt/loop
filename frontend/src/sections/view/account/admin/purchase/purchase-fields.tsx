import { useOthers } from "src/api/others/others";
import { usePayments } from "src/api/payment/payments";
import { useServices } from "src/api/services/services";

import { RHFTextField, RHFAutocompleteDnd } from "src/components/hook-form";

import { IPaymentProp } from "src/types/payment";
import { IServiceProp } from "src/types/service";
import { ITeamMemberProps } from "src/types/team";

export const usePurchaseFields = () => {
  const { data: availableServices, isLoading: isLoadingServices } = useServices({
    sort_by: "title",
    page_size: -1,
  });
  const { data: availableOthers, isLoading: isLoadingOthers } = useOthers({
    sort_by: "full_name",
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
        getOptionLabel={(option) => (option as ITeamMemberProps)?.name ?? ""}
        loading={isLoadingOthers}
        isOptionEqualToValue={(a, b) => a.id === b.id}
      />
    ),
    payment: (
      <RHFAutocompleteDnd
        key="payment"
        name="payment"
        label="Płatność"
        multiple
        options={availablePayments ?? []}
        getOptionLabel={(option) =>
          `${(option as IPaymentProp).sessionId} (${(option as IPaymentProp).amount} ${(option as IPaymentProp).currency})`
        }
        loading={isLoadingPayments}
        isOptionEqualToValue={(a, b) => a.sessionId === b.sessionId}
      />
    ),
  };
  return { fields };
};
