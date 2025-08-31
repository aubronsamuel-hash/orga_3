import React from "react";
import { useUi } from "../state/ui";

export class ErrorBoundary extends React.Component<React.PropsWithChildren, { error?: Error }> {
  constructor(props: React.PropsWithChildren) {
    super(props);
    this.state = { error: undefined };
  }
  static getDerivedStateFromError(error: Error) { return { error }; }
  componentDidCatch(error: Error) {
    // toast global
    useUi.getState().pushToast({ kind: "error", text: "Une erreur est survenue" });
    console.error(error);
  }
  render() {
    if (this.state.error) {
      return (
        <div role="alert" className="p-4 text-sm border rounded">
          Oups. Erreur detectee. <button onClick={()=>location.reload()}>Recharger</button>
        </div>
      );
    }
    return this.props.children;
  }
}
