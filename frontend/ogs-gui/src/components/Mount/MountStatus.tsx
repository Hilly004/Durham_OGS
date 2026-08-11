import { useEffect, useState } from "react";

import {
    getMountStatus,
    getMountPosition,
    getMountPosition_rd,
    connectMount,
    disconnectMount,
} from "../../api/mount";

import type {
    MountStatusData,
    MountPosition,
    MountPosition_rd,
} from "../../api/mount";

import StatusCard from "../Common/StatusCard";


export default function MountStatusWidget() {

    const [status, setStatus] =
        useState<MountStatusData | null>(null);

    const [position, setPosition] =
        useState<MountPosition | null>(null);

    const [position_rd, setPosition_rd] =
        useState<MountPosition_rd | null>(null);


    // --------------------------------------------------
    // Update mount information
    // --------------------------------------------------

    useEffect(() => {

        const update = async () => {

            try {

                const mountStatus =
                    await getMountStatus();

                setStatus(mountStatus);


                if (mountStatus.connected) {

                    const mountPosition =
                        await getMountPosition();

                    setPosition(mountPosition);


                    const mountPosition_rd =
                        await getMountPosition_rd();

                    setPosition_rd(mountPosition_rd);

                } else {

                    setPosition(null);
                    setPosition_rd(null);

                }

            } catch (error) {

                console.error(error);

            }

        };


        update();

        const timer =
            setInterval(update, 5000);

        return () =>
            clearInterval(timer);

    }, []);


    // --------------------------------------------------
    // Connect
    // --------------------------------------------------

    async function handleConnect() {

        try {

            await connectMount();

        } catch (error) {

            console.error(error);

        }

    }


    // --------------------------------------------------
    // Disconnect
    // --------------------------------------------------

    async function handleDisconnect() {

        try {

            await disconnectMount();

        } catch (error) {

            console.error(error);

        }

    }


    // --------------------------------------------------
    // No status
    // --------------------------------------------------

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


    // --------------------------------------------------
    // Mount card
    // --------------------------------------------------

    return (

        <StatusCard
            title="Mount"
            status={
                status.connected
                    ? "connected"
                    : "disconnected"
            }
        >

            {/* Alt/Az */}

            <div className="
                grid
                grid-cols-2
                gap-4
            ">

                <div>

                    <p className="
                        text-slate-400
                        text-sm
                    ">
                        Altitude
                    </p>

                    <p className="
                        text-xl
                        font-semibold
                    ">
                        {position?.alt ?? "--"}°
                    </p>

                </div>


                <div>

                    <p className="
                        text-slate-400
                        text-sm
                    ">
                        Azimuth
                    </p>

                    <p className="
                        text-xl
                        font-semibold
                    ">
                        {position?.az ?? "--"}°
                    </p>

                </div>

            </div>


            {/* RA/Dec */}

            <div className="
                grid
                grid-cols-2
                gap-4
                mt-4
            ">

                <div>

                    <p className="
                        text-slate-400
                        text-sm
                    ">
                        Right Ascension
                    </p>

                    <p className="
                        text-xl
                        font-semibold
                    ">
                        {position_rd?.ra ?? "--"}
                    </p>

                </div>


                <div>

                    <p className="
                        text-slate-400
                        text-sm
                    ">
                        Declination
                    </p>

                    <p className="
                        text-xl
                        font-semibold
                    ">
                        {position_rd?.dec ?? "--"}°
                    </p>

                </div>

            </div>


            {/* Connection */}

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
}ß