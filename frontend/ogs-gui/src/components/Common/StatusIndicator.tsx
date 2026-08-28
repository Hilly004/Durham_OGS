interface StatusIndicatorProps {
    active: boolean;
    activeLabel?: string;
    inactiveLabel?: string;
    className?: string;
}


export default function StatusIndicator({
    active,
    activeLabel = "Connected",
    inactiveLabel = "Disconnected",
    className = "",
}: StatusIndicatorProps) {

    return (
        <div
            className={`
                flex
                items-center
                gap-2
                text-sm
                ${className}
            `}
        >

            <span
                className={`
                    h-2
                    w-2
                    rounded-full
                    ${
                        active
                            ? "bg-emerald-400"
                            : "bg-slate-500"
                    }
                `}
            />

            <span
                className={
                    active
                        ? "text-slate-200"
                        : "text-slate-400"
                }
            >
                {
                    active
                        ? activeLabel
                        : inactiveLabel
                }
            </span>

        </div>
    );
}