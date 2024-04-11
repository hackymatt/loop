import { Controller, useController, useFormContext } from "react-hook-form";
import {
  Droppable,
  Draggable,
  DropResult,
  DragDropContext,
  DroppableProvided,
  DraggableProvided,
  ResponderProvided,
} from "@hello-pangea/dnd";

import { Chip } from "@mui/material";
import TextField from "@mui/material/TextField";
import Autocomplete, { AutocompleteProps } from "@mui/material/Autocomplete";

import { countries } from "src/assets/data";

// ----------------------------------------------------------------------

interface Props<
  T,
  Multiple extends boolean | undefined,
  DisableClearable extends boolean | undefined,
  FreeSolo extends boolean | undefined,
> extends AutocompleteProps<T, Multiple, DisableClearable, FreeSolo> {
  name: string;
  label?: string;
  placeholder?: string;
  hiddenLabel?: boolean;
  helperText?: React.ReactNode;
}

export default function RHFAutocompleteDnd<
  T,
  Multiple extends boolean | undefined,
  DisableClearable extends boolean | undefined,
  FreeSolo extends boolean | undefined,
>({
  name,
  label,
  helperText,
  hiddenLabel,
  placeholder,
  ...other
}: Omit<Props<T, Multiple, DisableClearable, FreeSolo>, "renderInput">) {
  const { control, setValue } = useFormContext();

  const { multiple } = other;

  const {
    field: { value: currentValue },
  } = useController({ name, control });

  const handleDragEnd = (result: DropResult, provided?: ResponderProvided) => {
    if (!result.destination) {
      return;
    }

    if (result.destination.index === result.source.index) {
      return;
    }

    const temp = [...currentValue];
    const oldValue = temp[result.destination!.index];
    const newValue = temp[result.source.index];
    temp[result.destination!.index] = newValue;
    temp[result.source.index] = oldValue;

    setValue(name, temp);
  };

  return (
    <Controller
      name={name}
      control={control}
      render={({ field, fieldState: { error } }) => (
        <Autocomplete
          {...field}
          id={`autocomplete-${name}`}
          autoHighlight={!multiple}
          disableCloseOnSelect={multiple}
          onChange={(event, newValue) => setValue(name, newValue, { shouldValidate: true })}
          noOptionsText="Brak opcji"
          renderInput={(params) => (
            <TextField
              {...params}
              label={label}
              placeholder={placeholder}
              error={!!error}
              helperText={error ? error?.message : helperText}
              inputProps={{
                ...params.inputProps,
                autoComplete: "new-password",
              }}
            />
          )}
          renderTags={(selected, getTagProps, ownerState) => (
            <DragDropContext onDragEnd={handleDragEnd}>
              <Droppable droppableId="droppable">
                {(droppableProvided: DroppableProvided) => (
                  <div {...droppableProvided.droppableProps} ref={droppableProvided.innerRef}>
                    {selected.map((item, index) => {
                      const tagLabel = ownerState.getOptionLabel(item);
                      return (
                        <Draggable key={tagLabel} draggableId={tagLabel} index={index}>
                          {(draggableProvided: DraggableProvided) => (
                            <Chip
                              ref={draggableProvided.innerRef}
                              {...draggableProvided.draggableProps}
                              {...draggableProvided.dragHandleProps}
                              {...getTagProps({ index })}
                              key={tagLabel}
                              label={tagLabel}
                              size="small"
                              variant="soft"
                            />
                          )}
                        </Draggable>
                      );
                    })}
                    {droppableProvided.placeholder}
                  </div>
                )}
              </Droppable>
            </DragDropContext>
          )}
          {...other}
        />
      )}
    />
  );
}

// ----------------------------------------------------------------------

export function getCountry(inputValue: string) {
  const option = countries.filter((country) => country.label === inputValue)[0];

  return {
    ...option,
  };
}
