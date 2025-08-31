// useApi.ts - helpers generiques useQuery/useMutation
import { useMutation, useQuery, UseQueryOptions, UseMutationOptions } from "@tanstack/react-query";
import { http } from "../lib/http";

export function useApiQuery<TData = unknown>(
  key: readonly unknown[],
  url: string,
  options?: Omit<UseQueryOptions<TData>, "queryKey" | "queryFn">
) {
  return useQuery<TData>({
    queryKey: key,
    queryFn: () => http<TData>(url),
    ...options,
  });
}

export function useApiMutation<TOut = unknown, TBody = unknown, TCtx = unknown>(
  url: string,
  options?: Omit<UseMutationOptions<TOut, unknown, TBody, TCtx>, "mutationFn">
) {
  return useMutation<TOut, unknown, TBody, TCtx>({
    mutationFn: (body: TBody) =>
      http<TOut>(url, {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify(body),
      }),
    ...options,
  });
}
