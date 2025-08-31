import { useApiMutation } from "../../hooks/useApi";
import { queryClient } from "../../lib/queryClient";

type Profile = { id: string; display_name: string };

export function useUpdateProfile() {
  return useApiMutation<Profile, Partial<Profile>, { prev?: Profile }>("/v1/me/profile", {
    onMutate: async (patch) => {
      await queryClient.cancelQueries({ queryKey: ["me"] });
      const prev = queryClient.getQueryData<Profile>(["me"]);
      if (prev) {
        queryClient.setQueryData<Profile>(["me"], { ...prev, ...patch });
      }
      return { prev };
    },
    onError: (_err, _patch, ctx) => {
      if (ctx?.prev) queryClient.setQueryData(["me"], ctx.prev);
    },
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: ["me"] });
    },
  });
}
