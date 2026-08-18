type DashboardStatusCardProps = {
    title: string;
    connected: boolean;
    children: React.ReactNode;
};

export default function DashboardStatusCard({
    title,
    connected,
    children,
}: DashboardStatusCardProps) {
    return (
        <div
            className="
                flex
                h-full
                w-full
                flex-col
                overflow-hidden
                rounded-xl
                border
                border-slate-800
                bg-slate-900
            "
        >
            <div
                className="
                    flex
                    shrink-0
                    items-center
                    justify-between
                    border-b
                    border-slate-800
                    px-4
                    py-3
                "
            >
                <h2 className="text-sm font-semibold text-slate-100">
                    {title}
                </h2>

                <div className="flex items-center gap-2">
                    <span
                        className={`
                            h-2
                            w-2
                            rounded-full
                            ${
                                connected
                                    ? "bg-green-500"
                                    : "bg-red-500"
                            }
                        `}
                    />

                    <span className="text-xs text-slate-400">
                        {connected ? "Connected" : "Disconnected"}
                    </span>
                </div>
            </div>

            <div className="min-h-0 flex-1 p-4">
                {children}
            </div>
        </div>
    );
}