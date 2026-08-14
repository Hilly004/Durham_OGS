import { useEffect, useState } from "react";

import MountStatusWidget from "../components/Mount/MountStatus";
import DomeStatusWidget from "../components/Dome/DomeStatus";
import WeatherStatusWidget from "../components/Weather/WeatherStatus";
import CameraWidget from "../components/Camera/CameraWidget";
import ActivityLog from "../components/Activity/ActivityWidget";

import { getObservatorySafety } from "../api/observatory";


export default function Home() {

    const [safetyStatus, setSafetyStatus] =
        useState<{
            safe: boolean 
            reason: string | null;
        } | null>(null);


    useEffect(() => {

        async function updateSafety() {
            try {
                const data = await getObservatorySafety();

                setSafetyStatus(data);

            } catch (error) {

                console.error(
                    "Failed to fetch observatory safety:",
                    error
                );

                setSafetyStatus(null);
            }
        }


        updateSafety();


        const timer = setInterval(
            updateSafety,
            5000
        );


        return () => clearInterval(timer);

    }, []);


    return (
        <div className="w-full h-full">

            <div
                className="
                    grid
                    grid-cols-4
                    grid-rows-[auto_1fr]
                    gap-4
                    h-full
                "
            >

                {/* ------------------------------------------------ */}
                {/* Observatory Safety */}
                {/* ------------------------------------------------ */}

                <div
                    className="
                        col-span-4
                        bg-slate-900
                        border
                        border-slate-800
                        rounded-xl
                        px-5
                        py-3
                        flex
                        items-center
                        justify-between
                    "
                >

                    <div>
                        <h1 className="text-xl font-semibold">
                            Optical Ground Station
                        </h1>

                        <p className="text-sm text-slate-400">
                            Durham Observatory
                        </p>
                    </div>


                    <div className="text-right">

                        <p className="text-xs text-slate-400">
                            Observatory Status
                        </p>

                        <div
                            className={
                                safetyStatus === null
                                    ? "font-semibold text-slate-400"
                                    : safetyStatus.safe
                                        ? "font-semibold text-green-400"
                                        : "font-semibold text-red-400"
                            }
                        >
                            {safetyStatus === null
                                ? "Safety status unavailable"
                                : safetyStatus.safe
                                    ? "Observatory Safe"
                                    : "Observatory Unsafe"}


                            {safetyStatus !== null &&
                                !safetyStatus.safe &&
                                safetyStatus.reason && (
                                    <p className="text-xs text-slate-400 mt-1">
                                        {safetyStatus.reason}
                                    </p>
                                )}
                        </div>

                    </div>

                </div>


                {/* ------------------------------------------------ */}
                {/* Left column */}
                {/* ------------------------------------------------ */}

                <div className="col-span-1 flex flex-col gap-4">

                    <MountStatusWidget />

                    <DomeStatusWidget />

                    <WeatherStatusWidget />

                </div>


                {/* ------------------------------------------------ */}
                {/* Camera + Activity */}
                {/* ------------------------------------------------ */}

                <div className="col-span-3 flex flex-col gap-4 min-h-0">

                    <div className="flex-[3] min-h-0">
                        <CameraWidget />
                    </div>


                    <div className="flex-[1] min-h-0">
                        <ActivityLog />
                    </div>

                </div>

            </div>

        </div>
    );
}