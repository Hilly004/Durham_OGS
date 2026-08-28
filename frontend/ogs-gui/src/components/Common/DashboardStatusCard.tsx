import type {
    ReactNode,
} from "react";

import Card from "./Card";
import StatusIndicator from "./StatusIndicator";


interface DashboardStatusCardProps {
    title: string;
    connected: boolean;
    children: ReactNode;
}


export default function DashboardStatusCard({
    title,
    connected,
    children,
}: DashboardStatusCardProps) {

    return (
        <Card
            className="
                flex
                h-full
                w-full
                flex-col
                overflow-hidden
            "
        >

            <div
                className="
                    flex
                    items-center
                    justify-between
                    border-b
                    border-slate-800
                    px-4
                    py-3
                "
            >

                <h2
                    className="
                        text-sm
                        font-semibold
                        text-slate-100
                    "
                >
                    {title}
                </h2>

                <StatusIndicator
                    active={connected}
                />

            </div>

            <div
                className="
                    min-h-0
                    flex-1
                    p-4
                "
            >
                {children}
            </div>

        </Card>
    );
}