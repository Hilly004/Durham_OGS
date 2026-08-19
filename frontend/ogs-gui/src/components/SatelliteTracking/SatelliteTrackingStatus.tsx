import {
    useEffect,
    useState,
} from "react";

import {
    getSatelliteTrackingStatus,
} from "../../api/satellite";

import {
    getMountPosition,
    getMountPosition_rd,
} from "../../api/mount";

import DashboardStatusCard
    from "../Common/DashboardStatusCard";


interface TrackingStatus {

    status:
        | "slewing"
        | "waiting"
        | "catching"
        | "tracking"
        | "ended"
        | "idle";

    tracking: boolean;

    satelliteId:
        number | null;

    satelliteName:
        string | null;

    azimuth:
        number | null;

    altitude:
        number | null;

    ra:
        number | null;

    dec:
        number | null;
}


export default function SatelliteTrackingStatusWidget() {

    const [status, setStatus] =
        useState<TrackingStatus | null>(
            null
        );


    useEffect(() => {

        async function updateStatus() {

            try {

                /*
                 * Get tracking state and
                 * current mount coordinates
                 * simultaneously.
                 */
                const [
                    trackingResult,
                    altAzResult,
                    raDecResult,
                ] = await Promise.allSettled([
                    getSatelliteTrackingStatus(),
                    getMountPosition(),
                    getMountPosition_rd(),
                ]);


                if (
                    trackingResult.status !==
                    "fulfilled"
                ) {
                    return;
                }


                const tracking =
                    trackingResult.value.data;


                const altAz =
                    altAzResult.status ===
                    "fulfilled"
                        ? altAzResult.value
                        : null;


                const raDec =
                    raDecResult.status ===
                    "fulfilled"
                        ? raDecResult.value
                        : null;


                setStatus({
                    status:
                        tracking.status,

                    tracking:
                        tracking.tracking,

                    satelliteId:
                        tracking.satellite_id,

                    satelliteName:
                        tracking.satellite_name,

                    altitude:
                        altAz?.alt ?? null,

                    azimuth:
                        altAz?.az ?? null,

                    ra:
                        raDec?.ra ?? null,

                    dec:
                        raDec?.dec ?? null,
                });


            } catch (error) {

                console.error(
                    "Unable to retrieve satellite tracking status:",
                    error
                );

            }
        }


        updateStatus();


        const interval =
            setInterval(
                updateStatus,
                1000
            );


        return () => {
            clearInterval(
                interval
            );
        };

    }, []);


    const active =
        status?.status === "tracking" ||
        status?.status === "slewing" ||
        status?.status === "waiting" ||
        status?.status === "catching";


    return (
        <DashboardStatusCard
            title="Tracking Status"
            connected={active}
        >

            <div className="space-y-4">

                {/* Satellite */}
                <div
                    className="
                        rounded-lg
                        border
                        border-slate-800
                        bg-slate-950/50
                        p-4
                    "
                >

                    <p
                        className="
                            text-xs
                            uppercase
                            tracking-wide
                            text-slate-500
                        "
                    >
                        Satellite
                    </p>

                    <p
                        className="
                            mt-1
                            text-base
                            font-medium
                            text-slate-100
                        "
                    >
                        {
                            status?.satelliteName
                            ?? "No satellite selected"
                        }
                    </p>

                </div>

                {/* Two line element */}
                <div
                    className="
                        rounded-lg
                        border
                        border-slate-800
                        bg-slate-950/50
                        p-4
                    "
                >

                    <p
                        className="
                            text-xs
                            uppercase
                            tracking-wide
                            text-slate-500
                        "
                    >
                        TLE
                    </p>

                    <p
                        className="
                            mt-1
                            text-base
                            font-medium
                            text-slate-100
                        "
                    >
                        {
                            status?.satelliteName
                            ?? "No satellite selected"
                        }
                    </p>

                </div>


                {/* Tracking State */}
                <div
                    className="
                        flex
                        items-center
                        justify-between
                        rounded-lg
                        border
                        border-slate-800
                        bg-slate-950/50
                        p-4
                    "
                >

                    <span
                        className="
                            text-sm
                            text-slate-400
                        "
                    >
                        State
                    </span>


                    <div
                        className="
                            flex
                            items-center
                            gap-2
                        "
                    >

                        <span
                            className={`
                                h-2.5
                                w-2.5
                                rounded-full

                                ${
                                    active
                                        ? "bg-green-500"
                                        : "bg-slate-600"
                                }
                            `}
                        />


                        <span
                            className={
                                active
                                    ? "text-sm font-medium text-green-400"
                                    : "text-sm font-medium text-slate-400"
                            }
                        >
                            {
                                formatTrackingState(
                                    status?.status
                                )
                            }
                        </span>

                    </div>

                </div>


                {/* Alt / Az */}
                <div>

                    <p
                        className="
                            mb-2
                            text-[10px]
                            font-semibold
                            uppercase
                            tracking-widest
                            text-slate-500
                        "
                    >
                        Alt / Az
                    </p>


                    <div
                        className="
                            grid
                            grid-cols-2
                            gap-3
                        "
                    >

                        <StatusValue
                            label="Altitude"
                            value={
                                status?.altitude !==
                                null &&
                                status?.altitude !==
                                undefined
                                    ? `${status.altitude.toFixed(2)}°`
                                    : "—"
                            }
                        />


                        <StatusValue
                            label="Azimuth"
                            value={
                                status?.azimuth !==
                                null &&
                                status?.azimuth !==
                                undefined
                                    ? `${status.azimuth.toFixed(2)}°`
                                    : "—"
                            }
                        />

                    </div>

                </div>


                {/* RA / DEC */}
                <div>

                    <p
                        className="
                            mb-2
                            text-[10px]
                            font-semibold
                            uppercase
                            tracking-widest
                            text-slate-500
                        "
                    >
                        RA / DEC
                    </p>


                    <div
                        className="
                            grid
                            grid-cols-2
                            gap-3
                        "
                    >

                        <StatusValue
                            label="RA"
                            value={
                                status?.ra !== null &&
                                status?.ra !== undefined
                                    ? `${status.ra.toFixed(4)} h`
                                    : "—"
                            }
                        />


                        <StatusValue
                            label="DEC"
                            value={
                                status?.dec !== null &&
                                status?.dec !== undefined
                                    ? `${status.dec.toFixed(4)}°`
                                    : "—"
                            }
                        />

                    </div>

                </div>

            </div>

        </DashboardStatusCard>
    );
}


function StatusValue({
    label,
    value,
}: {
    label: string;
    value: string;
}) {

    return (
        <div
            className="
                rounded-lg
                border
                border-slate-800
                bg-slate-950/50
                p-3
            "
        >

            <p
                className="
                    text-xs
                    uppercase
                    tracking-wide
                    text-slate-500
                "
            >
                {label}
            </p>


            <p
                className="
                    mt-1
                    font-mono
                    text-sm
                    text-slate-200
                "
            >
                {value}
            </p>

        </div>
    );
}


function formatTrackingState(
    state:
        TrackingStatus["status"]
        | undefined
) {

    switch (state) {

        case "slewing":
            return "Slewing";

        case "waiting":
            return "Waiting";

        case "catching":
            return "Catching";

        case "tracking":
            return "Tracking";

        case "ended":
            return "Ended";

        default:
            return "Idle";
    }
}