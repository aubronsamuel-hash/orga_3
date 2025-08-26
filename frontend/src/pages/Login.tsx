import { useState } from "react";
import { useForm } from "react-hook-form";
import { z } from "zod";
import { zodResolver } from "@hookform/resolvers/zod";
import { useAuth } from "../auth";
import { useLocation, useNavigate } from "react-router-dom";

const Schema = z.object({
  email: z.string().email(),
  password: z.string().min(6)
});
type Form = z.infer<typeof Schema>;

export function Login() {
  const { login } = useAuth();
  const nav = useNavigate();
  const loc = useLocation();
  const [error, setError] = useState<string | null>(null);
  const { register, handleSubmit, formState: { errors, isSubmitting } } = useForm<Form>({
    resolver: zodResolver(Schema),
    defaultValues: { email: "sam@example.com", password: "secret" }
  });

  const onSubmit = handleSubmit(async (values) => {
    setError(null);
    try {
      await login(values.email, values.password);
      const to = (loc.state as { from?: { pathname: string } } | undefined)?.from?.pathname || "/app";
      nav(to, { replace: true });
    } catch (e) {
      setError("Identifiants invalides");
    }
  });

  return (
    <section className="max-w-sm">
      <h1 className="text-xl font-semibold mb-2">Login</h1>
      <form onSubmit={onSubmit} className="space-y-3">
        <div>
          <label className="block text-sm">Email</label>
          <input className="border px-3 py-2 w-full" {...register("email")} />
          {errors.email && <p className="text-red-600 text-sm">Email invalide</p>}
        </div>
        <div>
          <label className="block text-sm">Mot de passe</label>
          <input type="password" className="border px-3 py-2 w-full" {...register("password")} />
          {errors.password && <p className="text-red-600 text-sm">Mot de passe invalide</p>}
        </div>
        {error && <p className="text-red-700 text-sm">{error}</p>}
        <button disabled={isSubmitting} className="px-3 py-2 rounded border">
          {isSubmitting ? "..." : "Se connecter"}
        </button>
      </form>
    </section>
  );
}
