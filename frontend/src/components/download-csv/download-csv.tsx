import { CSVDownload } from "react-csv";
import { useState, useEffect } from "react";

import { LoadingButton } from "@mui/lab";

import Iconify from "../iconify";

export default function DownloadCSVButton({
  queryHook,
  disabled = false,
}: {
  queryHook: any;
  disabled?: boolean;
}) {
  const [enabled, setEnabled] = useState<boolean>(false);
  const [initiateDownload, setInitiateDownload] = useState<boolean>(false);

  const { data, isLoading } = queryHook({ page_size: -1 }, enabled);

  useEffect(() => {
    if (enabled && data?.length) {
      setInitiateDownload(true);
    }
  }, [data?.length, enabled]);

  useEffect(() => {
    if (initiateDownload) {
      setEnabled(false);
      setInitiateDownload(false);
    }
  }, [initiateDownload]);

  return (
    <>
      {initiateDownload && <CSVDownload data={data} target="_blank" rel="noopener" />}
      <LoadingButton
        component="label"
        variant="contained"
        size="small"
        color="secondary"
        loading={enabled ? isLoading : false}
        onClick={() => setEnabled(true)}
        disabled={disabled}
      >
        <Iconify icon="carbon:download" />
      </LoadingButton>
    </>
  );
}
