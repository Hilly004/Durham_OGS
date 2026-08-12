interface StatusCardProps {
    title: string;
    status: "connected" | "disconnected" | "safe" | "warning" | "error";
    children: React.ReactNode;
}

export default function StatusCard({
    title,
    status,
    children,
}: StatusCardProps) {

    const statusConfig = {
        connected: {
            label: "Connected",
            colour: "text-green-400",
        },

        disconnected: {
            label: "Disconnected",
            colour: "text-red-400",
        },

        safe: {
            label: "Safe",
            colour: "text-green-400",
        },

        warning: {
            label: "Warning",
            colour: "text-yellow-400",
        },

        error: {
            label: "Error",
            colour: "text-red-400",
        },
    };

    const currentStatus = statusConfig[status];

    return (
        <div className="
            h-full
            bg-slate-900
            rounded-xl
            p-6
            shadow-lg
            border-3
            border-slate-700
        ">

            <div className="
                flex
                items-center
                justify-between
                mb-6
            ">

                <h2 className="text-xl font-semibold text-red-500">
                    {title}
                </h2>

                <span className={currentStatus.colour}>
                    {currentStatus.label}
                </span>

            </div>

            {children}

        </div>
    );
}