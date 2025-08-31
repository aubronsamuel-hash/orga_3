import { useEffect, useState } from "react";
import { Dialog } from "../components/ui/dialog";
import { Input } from "../components/ui/input";

export function Shortcuts() {
  const [commandOpen, setCommandOpen] = useState(false);
  const [helpOpen, setHelpOpen] = useState(false);

  useEffect(() => {
    const handler = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === "k") {
        e.preventDefault();
        setCommandOpen(true);
      }
      if (e.key === "?") {
        e.preventDefault();
        setHelpOpen(true);
      }
      if (e.key === "Escape") {
        setCommandOpen(false);
        setHelpOpen(false);
      }
    };
    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, []);

  return (
    <>
      <Dialog open={commandOpen} onClose={() => setCommandOpen(false)}>
        <div className="space-y-2">
          <h2 className="text-lg font-medium">Command Menu</h2>
          <Input aria-label="Search" placeholder="Type a command" />
        </div>
      </Dialog>
      <Dialog open={helpOpen} onClose={() => setHelpOpen(false)}>
        <h2 className="mb-2 text-lg font-medium">Keyboard Shortcuts</h2>
        <ul className="list-disc pl-4 text-sm">
          <li>
            <kbd>Ctrl</kbd>/<kbd>Cmd</kbd> + <kbd>K</kbd> - Open command menu
          </li>
          <li>
            <kbd>?</kbd> - Show help
          </li>
        </ul>
      </Dialog>
    </>
  );
}
