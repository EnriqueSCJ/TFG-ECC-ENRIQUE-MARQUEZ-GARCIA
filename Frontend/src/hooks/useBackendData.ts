import { useEffect, useState, type DependencyList } from "react";
import { getBackendErrorMessage } from "../services/apiClient";

interface BackendDataState<T> {
  data: T | null;
  error: string | null;
  loading: boolean;
}

export function useBackendData<T>(
  load: () => Promise<T>,
  dependencies: DependencyList,
  enabled = true,
): BackendDataState<T> {
  const [state, setState] = useState<BackendDataState<T>>({
    data: null,
    error: null,
    loading: false,
  });

  useEffect(() => {
    let cancelled = false;

    if (!enabled) {
      setState({ data: null, error: null, loading: false });
      return () => {
        cancelled = true;
      };
    }

    setState((current) => ({ ...current, error: null, loading: true }));

    load()
      .then((data) => {
        if (!cancelled) {
          setState({ data, error: null, loading: false });
        }
      })
      .catch((error: unknown) => {
        if (!cancelled) {
          setState({ data: null, error: getBackendErrorMessage(error), loading: false });
        }
      });

    return () => {
      cancelled = true;
    };
  }, dependencies);

  return state;
}
