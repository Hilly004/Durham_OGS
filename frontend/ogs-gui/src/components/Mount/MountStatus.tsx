import { useEffect, useState } from "react";

import {
    getMountStatus,
    connectMount,
    disconnectMount,
} from "../../api/mount";

import type { MountStatusData } from "../../api/mount";

import StatusCard from "../Common/StatusCard";


export default function MountStatusWidget() {

    const [status, setStatus] =
        useState<MountStatusData | null>(null);


    useEffect(() => {

        const update = () => {

            getMountStatus()
                .then(setStatus)
                .catch(console.error);

        };

        update();

        const timer = setInterval(update, 5000);

        return () => clearInterval(timer);

    }, []);


    async function handleConnect() {

        try {
            await connectMount();
        } catch (error) {
            console.error(error);
        }

    }


    async function handleDisconnect() {

        try {
            await disconnectMount();
        } catch (error) {
            console.error(error);
        }

    }


    if (!status) {

        return (
            <StatusCard
                title="Mount"
                status="error"
            >

                <p className="text-red-400">
                    Unable to read mount status
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
        title="Mount"
        status={
            status.connected
                ? "connected"
                : "disconnected"
        }
    >

        <div className="
            grid
            grid-cols-2
            gap-4
        ">

            <div>
                <p className="text-slate-400 text-sm">
                    Altitude
                </p>

                <p className="text-2xl font-semibold">
                    {status.alt}°
                </p>
            </div>

            <div>
                <p className="text-slate-400 text-sm">
                    Azimuth
                </p>

                <p className="text-2xl font-semibold">
                    {status.az}°
                </p>
            </div>

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