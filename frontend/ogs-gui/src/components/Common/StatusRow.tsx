import type {
    ReactNode,
} from "react";


interface StatusRowProps {
    label: string;
    value: ReactNode;
    valueClassName?: string;
    className?: string;
}

export default function StatusRow({
    label,
    value,
    valueClassName = "text-slate-300",
    className = "",
}: StatusRowProps) {

    return (
        <div
            className={`
                flex
                items-center
                justify-between
                py-1.3
                ${className}
            `}
        >

            <span className="text-sm text-slate-500">
                {label}
            </span>

            <span
                className={`
                    text-sm
                    font-medium
                    ${valueClassName}
                `}
            >
                {value}
            </span>

        </div>
    );
}