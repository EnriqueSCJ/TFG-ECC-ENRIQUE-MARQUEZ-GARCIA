import axios, { AxiosError } from "axios";
import { ApiErrorPayload } from "../types/ecc";

const apiBaseUrl = import.meta.env.VITE_API_BASE_URL ?? "/api";

export class BackendApiError extends Error {
  readonly status?: number;
  readonly details?: unknown;

  constructor(message: string, status?: number, details?: unknown) {
    super(message);
    this.name = "BackendApiError";
    this.status = status;
    this.details = details;
  }
}

export const apiClient = axios.create({
  baseURL: apiBaseUrl,
  timeout: 12000,
  headers: {
    "Content-Type": "application/json",
  },
});

apiClient.interceptors.response.use(
  (response) => response,
  (error: AxiosError<ApiErrorPayload>) => {
    const payload = error.response?.data;
    const message =
      (typeof payload?.detail === "string" ? payload.detail : undefined) ??
      payload?.error ??
      payload?.message ??
      error.message ??
      "Error inesperado al comunicarse con el backend Python.";

    return Promise.reject(
      new BackendApiError(message, error.response?.status, payload ?? error.toJSON()),
    );
  },
);

export function getBackendErrorMessage(error: unknown): string {
  if (error instanceof BackendApiError) {
    return error.status ? `[${error.status}] ${error.message}` : error.message;
  }

  if (error instanceof Error) {
    return error.message;
  }

  return "Error desconocido.";
}
