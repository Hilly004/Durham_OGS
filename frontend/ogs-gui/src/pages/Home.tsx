import {
    useEffect,
    useState,
} from "react";

import MountStatusWidget
    from "../components/Mount/MountStatus";

import DomeStatusWidget
    from "../components/Dome/DomeStatus";

import WeatherStatusWidget
    from "../components/Weather/WeatherStatus";

import CameraWidget
    from "../components/Camera/CameraWidget";

import {
    useObservatoryStatus,
} from "../context/ObservatoryStatusContext";

import {
    getObservatoryStateStyle,
} from "../utils/observatoryStatus";


export default function Home() {

    const [time, setTime] =
        useState(new Date());

    const {
        observatoryState,
    } = useObservatoryStatus();

    const observatoryStyle =
        getObservatoryStateStyle(
            observatoryState
        );


    /*
     * Dashboard clock
     */
    useEffect(() => {

        const interval = setInterval(
            () => {
                setTime(new Date());
            },
            1000
        );

        return () => {
            clearInterval(interval);
        };

    }, []);


    return (
        <div
            className="
                flex
                h-full
                w-full
                flex-col
                gap-3
                overflow-hidden
                p-4
            "
        >

            {/* Observatory Status Bar */}
            <div
                className="
                    flex
                    shrink-0
                    items-center
                    justify-between
                    rounded-xl
                    border
                    border-slate-800
                    bg-slate-900
                    px-5
                    py-3
                "
            >

                {/* Left */}
                <div
                    className="
                        flex
                        items-center
                        gap-4
                    "
                >

                    <h1
                        className="
                            text-lg
                            font-semibold
                            text-slate-100
                        "
                    >
                        Observatory
                    </h1>


                    <div
                        className="
                            h-5
                            w-px
                            bg-slate-700
                        "
                    />


                    {/* Overall Observatory State */}
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
                                ${observatoryStyle.dot}
                            `}
                        />

                        <span
                            className={`
                                text-sm
                                font-medium
                                ${observatoryStyle.text}
                            `}
                        >
                            {observatoryStyle.label}
                        </span>

                    </div>

                </div>


                {/* Right */}
                <div
                    className="
                        flex
                        items-center
                        gap-6
                    "
                >

                    <span
                        className="
                            text-sm
                            text-slate-500
                        "
                    >
                        Durham Optical Ground Station
                    </span>


                    <span
                        className="
                            font-mono
                            text-sm
                            text-slate-300
                        "
                    >
                        {time.toLocaleTimeString(
                            [],
                            {
                                hour: "2-digit",
                                minute: "2-digit",
                                second: "2-digit",
                                hour12: false,
                            }
                        )}
                    </span>

                </div>

            </div>


            {/* Dashboard */}
            <div
                className="
                    grid
                    min-h-0
                    flex-1
                    grid-cols-12
                    grid-rows-[210px_minmax(0,1fr)]
                    gap-3
                "
            >

                {/* Mount */}
                <div
                    className="
                        col-span-4
                        min-h-0
                        overflow-hidden
                    "
                >
                    <MountStatusWidget />
                </div>


                {/* Dome */}
                <div
                    className="
                        col-span-4
                        min-h-0
                        overflow-hidden
                    "
                >
                    <DomeStatusWidget />
                </div>


                {/* Weather */}
                <div
                    className="
                        col-span-4
                        min-h-0
                        overflow-hidden
                    "
                >
                    <WeatherStatusWidget />
                </div>


                {/* Camera */}
                <div
                    className="
                        col-span-8
                        min-h-0
                        overflow-hidden
                    "
                >
                    <CameraWidget />
                </div>


                {/* Target Tracking */}
                <div
                    className="
                        col-span-4
                        min-h-0
                        overflow-hidden
                        rounded-xl
                        border
                        border-slate-800
                        bg-slate-900
                    "
                >

                    {/* Header */}
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
                            Target Tracking
                        </h2>


                        <div
                            className="
                                flex
                                items-center
                                gap-2
                            "
                        >

                            <span
                                className="
                                    h-2
                                    w-2
                                    rounded-full
                                    bg-slate-600
                                "
                            />

                            <span
                                className="
                                    text-xs
                                    text-slate-500
                                "
                            >
                                Idle
                            </span>

                        </div>

                    </div>


                    {/* Content */}
                    <div
                        className="
                            space-y-1
                            p-4
                        "
                    >

                        <DashboardRow
                            label="Target"
                            value="None selected"
                        />

                        <DashboardRow
                            label="Tracking"
                            value="Inactive"
                        />

                        <DashboardRow
                            label="Next Pass"
                            value="--"
                        />

                    </div>

                </div>

            </div>

        </div>
    );
}


function DashboardRow({
    label,
    value,
}: {
    label: string;
    value: string;
}) {

    return (
        <div
            className="
                flex
                items-center
                justify-between
                py-1.5
            "
        >

            <span
                className="
                    text-sm
                    text-slate-500
                "
            >
                {label}
            </span>


            <span
                className="
                    text-sm
                    font-medium
                    text-slate-300
                "
            >
                {value}
            </span>

        </div>
    );
}