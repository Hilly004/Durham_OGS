import { useEffect, useState } from "react";

import {
    getDomeStatus,
    connectDome,
    disconnectDome,
} from "../../api/dome";

import type { DomeStatusData } from "../../api/dome";

import StatusCard from "../Common/StatusCard";


export default function DomeStatusWidget() {

    const [status, setStatus] =
        useState<DomeStatusData | null>(null);


    useEffect(() => {

        const update = () => {

            getDomeStatus()
                .then(setStatus)
                .catch(console.error);

        };

        update();

        const timer = setInterval(update, 5000);

        return () => clearInterval(timer);

    }, []);


    async function handleConnect() {

        try {
            await connectDome();
        } catch (error) {
            console.error(error);
        }

    }


    async function handleDisconnect() {

        try {
            await disconnectDome();
        } catch (error) {
            console.error(error);
        }

    }


    if (!status) {

        return (
            <StatusCard
                title="Dome"
                status="error"
            >

                <p className="text-red-400">
                    Unable to read dome status
                </p>

                <button
                    onClick={handleConnect}
                    className="
                        mt-4
                        w-full
                        px-4
                        py-2
                        rounded-lg
                        bg-blue-600
                        hover:bg-blue-700
                        transition
                    "
                >
                    Connect
                </button>

            </StatusCard>
        );
    }


    return (
    <StatusCard
        title="Dome"
        status={
            status.connected
                ? "connected"
                : "disconnected"
        }
    >

        <div className="text-2xl font-semibold">
            Open
        </div>


        {/* Connection button */}

        <button
            onClick={
                status.connected
                    ? handleDisconnect
                    : handleConnect
            }

            className="
                w-full
                mt-6
                px-4
                py-2
                rounded-lg
                bg-slate-700
                hover:bg-slate-600
                text-white
                transition
            "
        >
            {status.connected
                ? "Disconnect"
                : "Connect"}
        </button>

    </StatusCard>
);
}