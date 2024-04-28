import axios from "axios";
import https from "https";

import { API_URL } from "src/config-global";

export const createAxiosInstance = (endpoint: string) => {
  if (endpoint.startsWith("https")) {
    const httpsAgent = new https.Agent({
      rejectUnauthorized: false,
    });
    return axios.create({ baseURL: endpoint, httpsAgent });
  }
  return axios.create({
    baseURL: endpoint,
    withCredentials: true,
  });
};

export const Api = createAxiosInstance(API_URL);
