import { useApiQuery } from "../../hooks/useApi";
import { Loader } from "../../components/Loader";

export default function RetryProbe() {
  const q = useApiQuery<{ ok: boolean }>(["retry-probe"], "/__test/500-then-200");
  if (q.isLoading) return <Loader />;
  return <div data-testid="retry-result">{q.data?.ok ? "OK" : "KO"}</div>;
}
