import axios from "axios";
import https from "https";

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

export const Api = createAxiosInstance(process.env.API_URL ?? "");
