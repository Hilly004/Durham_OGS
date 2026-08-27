import {
    useEffect,
    useState,
} from "react";

import {
    ArrowDown,
    ArrowLeft,
    ArrowRight,
    ArrowUp,
    Crosshair,
} from "lucide-react";

import {
    correctSatelliteTrajectory,
    getSatelliteTrackingStatus,
} from "../../api/satellite";

import type {
    SatelliteCorrectionDirection,
} from "../../api/satellite";


const DURATION_OPTIONS = [
    50,
    100,
    250,
    500,
];


export default function TrajectoryAdjustment() {

    const [
        tracking,
        setTracking,
    ] = useState(false);


    const [
        durationMs,
        setDurationMs,
    ] = useState(100);


    const [
        activeDirection,
        setActiveDirection,
    ] = useState<
        SatelliteCorrectionDirection
        | null
    >(null);


    const [
        message,
        setMessage,
    ] = useState<
        string | null
    >(null);


    useEffect(() => {

        let cancelled =
            false;


        async function updateStatus() {

            try {

                const result =
                    await getSatelliteTrackingStatus();


                if (cancelled) {
                    return;
                }


                setTracking(
                    result.data.status
                    ===
                    "tracking"
                );

            } catch {

                if (!cancelled) {
                    setTracking(false);
                }
            }
        }


        void updateStatus();


        const interval =
            window.setInterval(
                () => {
                    void updateStatus();
                },
                1000
            );


        return () => {

            cancelled =
                true;

            window.clearInterval(
                interval
            );
        };

    }, []);


    async function handleCorrection(
        direction:
            SatelliteCorrectionDirection
    ) {

        if (!tracking) {

            setMessage(
                (
                    "Corrections are only available "
                    +
                    "while actively tracking a satellite."
                )
            );

            return;
        }


        if (activeDirection !== null) {
            return;
        }


        setActiveDirection(
            direction
        );

        setMessage(null);


        try {

            const result =
                await correctSatelliteTrajectory(
                    direction,
                    durationMs
                );


            setMessage(
                result.data.message
            );

        } catch (error) {

            if (error instanceof Error) {

                setMessage(
                    error.message
                );

            } else {

                setMessage(
                    "Satellite correction failed."
                );
            }

        } finally {

            setActiveDirection(
                null
            );
        }
    }


    const disabled =
        !tracking
        ||
        activeDirection !== null;


    function directionButtonClass(
        direction:
            SatelliteCorrectionDirection
    ) {

        return `
            flex
            h-12
            w-12
            items-center
            justify-center
            rounded-lg
            border
            transition

            ${
                disabled
                    ? `
                        cursor-not-allowed
                        border-slate-800
                        bg-slate-950
                        text-slate-600
                    `
                    : `
                        border-violet-500/30
                        bg-violet-500/10
                        text-violet-300
                        hover:border-violet-400/50
                        hover:bg-violet-500/20
                    `
            }

            ${
                activeDirection === direction
                    ? `
                        border-violet-400
                        bg-violet-500/30
                    `
                    : ""
            }
        `;
    }


    return (
        <div
            className="
                rounded-xl
                border
                border-slate-800
                bg-slate-900
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
                <div
                    className="
                        flex
                        items-center
                        gap-2
                    "
                >
                    <Crosshair
                        size={16}
                        className={
                            tracking
                                ? "text-violet-400"
                                : "text-slate-500"
                        }
                    />

                    <h2
                        className="
                            text-sm
                            font-semibold
                            text-slate-100
                        "
                    >
                        Trajectory Adjustment
                    </h2>
                </div>


                <span
                    className={
                        tracking
                            ? `
                                text-xs
                                font-medium
                                text-green-400
                            `
                            : `
                                text-xs
                                font-medium
                                text-slate-500
                            `
                    }
                >
                    {
                        tracking
                            ? "READY"
                            : "NOT TRACKING"
                    }
                </span>
            </div>


            <div
                className="
                    space-y-5
                    p-4
                "
            >
                <div>
                    <p
                        className="
                            mb-2
                            text-xs
                            font-medium
                            uppercase
                            tracking-wide
                            text-slate-500
                        "
                    >
                        Correction duration
                    </p>


                    <div
                        className="
                            grid
                            grid-cols-4
                            gap-2
                        "
                    >
                        {DURATION_OPTIONS.map(
                            value => (
                                <button
                                    key={value}
                                    type="button"
                                    disabled={
                                        activeDirection
                                        !==
                                        null
                                    }
                                    onClick={() =>
                                        setDurationMs(
                                            value
                                        )
                                    }
                                    className={`
                                        rounded-lg
                                        border
                                        px-2
                                        py-2
                                        text-xs
                                        font-medium
                                        transition

                                        ${
                                            durationMs
                                            ===
                                            value
                                                ? `
                                                    border-violet-400
                                                    bg-violet-500/20
                                                    text-violet-300
                                                `
                                                : `
                                                    border-slate-700
                                                    bg-slate-800
                                                    text-slate-400
                                                    hover:border-slate-600
                                                `
                                        }
                                    `}
                                >
                                    {value} ms
                                </button>
                            )
                        )}
                    </div>
                </div>


                <div
                    className="
                        flex
                        justify-center
                    "
                >
                    <div
                        className="
                            grid
                            grid-cols-3
                            grid-rows-3
                            gap-2
                        "
                    >
                        <div />

                        <button
                            type="button"
                            title="Correct north"
                            disabled={disabled}
                            onClick={() =>
                                void handleCorrection(
                                    "north"
                                )
                            }
                            className={
                                directionButtonClass(
                                    "north"
                                )
                            }
                        >
                            <ArrowUp size={20} />
                        </button>

                        <div />


                        <button
                            type="button"
                            title="Correct west"
                            disabled={disabled}
                            onClick={() =>
                                void handleCorrection(
                                    "west"
                                )
                            }
                            className={
                                directionButtonClass(
                                    "west"
                                )
                            }
                        >
                            <ArrowLeft size={20} />
                        </button>


                        <div
                            className="
                                flex
                                h-12
                                w-12
                                items-center
                                justify-center
                                rounded-lg
                                border
                                border-slate-800
                                bg-slate-950
                                text-[11px]
                                font-medium
                                text-slate-500
                            "
                        >
                            {durationMs}
                        </div>


                        <button
                            type="button"
                            title="Correct east"
                            disabled={disabled}
                            onClick={() =>
                                void handleCorrection(
                                    "east"
                                )
                            }
                            className={
                                directionButtonClass(
                                    "east"
                                )
                            }
                        >
                            <ArrowRight size={20} />
                        </button>

                        <div />

                        <button
                            type="button"
                            title="Correct south"
                            disabled={disabled}
                            onClick={() =>
                                void handleCorrection(
                                    "south"
                                )
                            }
                            className={
                                directionButtonClass(
                                    "south"
                                )
                            }
                        >
                            <ArrowDown size={20} />
                        </button>

                        <div />
                    </div>
                </div>


                <p
                    className="
                        text-center
                        text-xs
                        leading-relaxed
                        text-slate-500
                    "
                >
                    Each press briefly applies the TenMicron
                    manual movement command, then stops that
                    direction while the satellite trajectory
                    remains active.
                </p>


                {message && (
                    <div
                        className="
                            rounded-lg
                            border
                            border-slate-800
                            bg-slate-950
                            px-3
                            py-2
                            text-xs
                            text-slate-300
                        "
                    >
                        {message}
                    </div>
                )}
            </div>
        </div>
    );
}
