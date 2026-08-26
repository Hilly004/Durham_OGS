import {
    useState,
} from "react";

import DashboardStatusCard
    from "../Common/DashboardStatusCard";

import DashboardStatusRow
    from "../Common/DashboardStatusRow";

import {
    useObservatoryStatus,
} from "../../context/ObservatoryStatusContext";


type CoordinateMode =
    | "altaz"
    | "radec";


export default function MountStatusWidget() {

    const {
        mountStatus: status,
        mountPosition: position,
        mountPositionRd: positionRd,
    } =
        useObservatoryStatus();


    const [mode, setMode] =
        useState<CoordinateMode>("altaz");


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
                        RA / Dec
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
                                label="Right Ascension"
                                value={
                                    positionRd
                                        ? formatNumber(positionRd.ra)
                                        : "--"
                                }
                            />

                            <DashboardStatusRow
                                label="Declination"
                                value={
                                    positionRd
                                        ? `${formatNumber(positionRd.dec)}°`
                                        : "--"
                                }
                            />
                        </>
                    )}

                </div>

                <DashboardStatusRow
                    label="Movement"
                    value={
                        status?.movement_status
                        ?? "--"
                    }
                />

                <DashboardStatusRow
                    label="Tracking"
                    value={
                        status?.tracking_status
                        ?? "--"
                    }
                />

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