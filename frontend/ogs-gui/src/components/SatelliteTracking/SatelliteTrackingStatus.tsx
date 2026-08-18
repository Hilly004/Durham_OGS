import { useEffect, useState } from "react";

import StatusCard from "../Common/DashboardStatusCard";
import { getSatelliteTrackingStatus } from "../../api/satellite";


interface TrackingStatus {
    tracking: boolean;
    azimuth?: number;
    altitude?: number;
    ra?: number;
    dec?: number;
}


export default function SatelliteTrackingStatusWidget() {

    const [status, setStatus] =
        useState<TrackingStatus | null>(null);

    const [error, setError] =
        useState<string | null>(null);


    useEffect(() => {

        async function updateStatus() {

            try {

                const result = await getSatelliteTrackingStatus();

                setStatus(result.data);
                setError(null);

            } catch (error) {

                if (error instanceof Error) {
                    setError(error.message);
                } else {
                    setError(
                        "Unable to retrieve tracking status"
                    );
                }

            }

        }


        updateStatus();

        const interval = setInterval(
            updateStatus,
            2000
        );


        return () => {
            clearInterval(interval);
        };

    }, []);


    return (
        <StatusCard
            title="Tracking Status"
            status={
                status?.tracking
                    ? "connected"
                    : "disconnected"
            }
        >

            <div className="space-y-4">

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

                    <span className="text-sm text-slate-400">
                        Tracking
                    </span>

                    <div className="flex items-center gap-2">

                        <span
                            className={`
                                h-2.5
                                w-2.5
                                rounded-full

                                ${
                                    status?.tracking
                                        ? "bg-green-500"
                                        : "bg-slate-600"
                                }
                            `}
                        />

                        <span
                            className={
                                status?.tracking
                                    ? "text-sm font-medium text-green-400"
                                    : "text-sm font-medium text-slate-400"
                            }
                        >
                            {status?.tracking
                                ? "Active"
                                : "Inactive"}
                        </span>

                    </div>

                </div>


                {/* Coordinates */}

                <div className="grid grid-cols-2 gap-3">

                    <StatusValue
                        label="Azimuth"
                        value={
                            status?.azimuth !== undefined
                                ? `${status.azimuth.toFixed(2)}°`
                                : "—"
                        }
                    />

                    <StatusValue
                        label="Altitude"
                        value={
                            status?.altitude !== undefined
                                ? `${status.altitude.toFixed(2)}°`
                                : "—"
                        }
                    />

                    <StatusValue
                        label="RA"
                        value={
                            status?.ra !== undefined
                                ? status.ra.toFixed(4)
                                : "—"
                        }
                    />

                    <StatusValue
                        label="DEC"
                        value={
                            status?.dec !== undefined
                                ? `${status.dec.toFixed(4)}°`
                                : "—"
                        }
                    />

                </div>


                {/* Error */}

                {error && (
                    <div
                        className="
                            rounded-lg
                            border
                            border-red-500/20
                            bg-red-500/10
                            px-3
                            py-2
                            text-sm
                            text-red-300
                        "
                    >
                        {error}
                    </div>
                )}

            </div>

        </StatusCard>
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