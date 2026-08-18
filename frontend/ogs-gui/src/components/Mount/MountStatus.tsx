import {
    useEffect,
    useState,
} from "react";

import {
    getMountStatus,
    getMountPosition,
    getMountPosition_rd,
} from "../../api/mount";

import type {
    MountStatusData,
    MountPosition,
    MountPosition_rd,
} from "../../api/mount";

import DashboardStatusCard
    from "../Common/DashboardStatusCard";

import DashboardStatusRow
    from "../Common/DashboardStatusRow";


type CoordinateMode =
    | "altaz"
    | "radec";


export default function MountStatusWidget() {

    const [status, setStatus] =
        useState<MountStatusData | null>(null);

    const [position, setPosition] =
        useState<MountPosition | null>(null);

    const [positionRd, setPositionRd] =
        useState<MountPosition_rd | null>(null);

    const [mode, setMode] =
        useState<CoordinateMode>("altaz");


    useEffect(() => {

        async function update() {

            try {

                const mountStatus =
                    await getMountStatus();

                setStatus(mountStatus);


                if (!mountStatus.connected) {

                    setPosition(null);
                    setPositionRd(null);

                    return;
                }


                const [
                    altAz,
                    raDec,
                ] = await Promise.all([
                    getMountPosition(),
                    getMountPosition_rd(),
                ]);


                setPosition(altAz);
                setPositionRd(raDec);

            } catch (error) {

                console.error(
                    "Unable to retrieve mount status:",
                    error
                );

                setStatus(null);
                setPosition(null);
                setPositionRd(null);

            }

        }


        update();

        const interval = setInterval(
            update,
            3000
        );


        return () => {
            clearInterval(interval);
        };

    }, []);


    return (
        <DashboardStatusCard
            title="Mount"
            connected={
                status?.connected ?? false
            }
        >

            <div className="flex h-full flex-col">

                {/* Coordinate Toggle */}
                <div
                    className="
                        mb-3
                        grid
                        grid-cols-2
                        rounded-lg
                        bg-slate-950/60
                        p-1
                    "
                >

                    <button
                        type="button"
                        onClick={() =>
                            setMode("altaz")
                        }
                        className={`
                            rounded-md
                            px-2
                            py-1.5
                            text-xs
                            font-medium
                            transition

                            ${
                                mode === "altaz"
                                    ? "bg-violet-500/15 text-violet-300"
                                    : "text-slate-500 hover:text-slate-300"
                            }
                        `}
                    >
                        Alt / Az
                    </button>


                    <button
                        type="button"
                        onClick={() =>
                            setMode("radec")
                        }
                        className={`
                            rounded-md
                            px-2
                            py-1.5
                            text-xs
                            font-medium
                            transition

                            ${
                                mode === "radec"
                                    ? "bg-violet-500/15 text-violet-300"
                                    : "text-slate-500 hover:text-slate-300"
                            }
                        `}
                    >
                        RA / DEC
                    </button>

                </div>


                {/* Coordinate Values */}
                <div className="space-y-1">

                    {mode === "altaz" ? (
                        <>
                            <DashboardStatusRow
                                label="Altitude"
                                value={
                                    position
                                        ? `${formatNumber(position.alt)}°`
                                        : "--"
                                }
                            />

                            <DashboardStatusRow
                                label="Azimuth"
                                value={
                                    position
                                        ? `${formatNumber(position.az)}°`
                                        : "--"
                                }
                            />
                        </>
                    ) : (
                        <>
                            <DashboardStatusRow
                                label="RA"
                                value={
                                    positionRd
                                        ? formatNumber(positionRd.ra)
                                        : "--"
                                }
                            />

                            <DashboardStatusRow
                                label="DEC"
                                value={
                                    positionRd
                                        ? `${formatNumber(positionRd.dec)}°`
                                        : "--"
                                }
                            />
                        </>
                    )}

                </div>

            </div>

        </DashboardStatusCard>
    );
}


function formatNumber(
    value: number
) {
    return Number.isFinite(value)
        ? value.toFixed(2)
        : "--";
}