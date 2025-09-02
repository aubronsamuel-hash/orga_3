import React from "react";

type Props = {
  onClick: () => void;
  disabled?: boolean;
};

export default function CSVButton({ onClick, disabled }: Props) {
  return (
    <button
      onClick={onClick}
      disabled={disabled}
      className="px-3 py-2 rounded-2xl shadow border text-sm disabled:opacity-50"
      aria-label="Exporter CSV"
      title="Exporter CSV"
    >
      Export CSV
    </button>
  );
}
