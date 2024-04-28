import { CSVDownload } from "react-csv";
import { useState, useEffect } from "react";

import { LoadingButton } from "@mui/lab";

import Iconify from "../iconify";

export default function DownloadCSVButton({
  queryHook,
  filename,
}: {
  queryHook: any;
  filename: string;
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
      {initiateDownload && <CSVDownload data={data} filename={filename} target="_blank" />}
      <LoadingButton
        component="label"
        variant="contained"
        size="small"
        color="success"
        loading={enabled ? isLoading : false}
        onClick={() => setEnabled(true)}
      >
        <Iconify icon="carbon:download" />
      </LoadingButton>
    </>
  );
}
