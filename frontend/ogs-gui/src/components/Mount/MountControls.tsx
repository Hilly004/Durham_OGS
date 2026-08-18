import {
    useRef,
    useState,
    type FormEvent,
} from "react";

import {
    ArrowDown,
    ArrowLeft,
    ArrowRight,
    ArrowUp,
    Crosshair,
    MapPin,
    Octagon,
    ParkingCircle,
    Play,
} from "lucide-react";

import {
    slewMount,
    startManualMove,
    stopManualMove,
} from "../../api/mount";

import type {
    ManualMoveDirection,
} from "../../api/mount";


interface MountControlsProps {
    connected: boolean;
}


export default function MountControls({
    connected,
}: MountControlsProps) {

    const [ra, setRa] =
        useState("");

    const [dec, setDec] =
        useState("");

    const [loading, setLoading] =
        useState(false);

    const [action, setAction] =
        useState<string | null>(null);

    const activeDirection =
        useRef<ManualMoveDirection | null>(
            null
        );


    async function handleSlew(
        event: FormEvent
    ) {

        event.preventDefault();

        if (!connected) {
            return;
        }


        const raValue =
            Number(ra);

        const decValue =
            Number(dec);


        if (
            !Number.isFinite(raValue) ||
            !Number.isFinite(decValue)
        ) {

            console.error(
                "Invalid RA / DEC coordinates"
            );

            return;
        }


        setLoading(true);
        setAction("slew");


        try {

            await slewMount(
                raValue,
                decValue
            );

        } catch (error) {

            console.error(
                "Failed to slew mount:",
                error
            );

        } finally {

            setLoading(false);
            setAction(null);

        }
    }


    async function handlePark() {

        if (!connected) {
            return;
        }


        setLoading(true);
        setAction("park");


        try {

            const response =
                await fetch(
                    "/api/mount/slew_to_park",
                    {
                        method: "POST",
                    }
                );


            if (!response.ok) {
                throw new Error(
                    "Failed to park mount"
                );
            }

        } catch (error) {

            console.error(
                "Failed to park mount:",
                error
            );

        } finally {

            setLoading(false);
            setAction(null);

        }
    }


    async function handleUnpark() {

        if (!connected) {
            return;
        }


        setLoading(true);
        setAction("unpark");


        try {

            const response =
                await fetch(
                    "/api/mount/unpark",
                    {
                        method: "POST",
                    }
                );


            if (!response.ok) {
                throw new Error(
                    "Failed to unpark mount"
                );
            }

        } catch (error) {

            console.error(
                "Failed to unpark mount:",
                error
            );

        } finally {

            setLoading(false);
            setAction(null);

        }
    }


    async function handleStop() {

        if (!connected) {
            return;
        }


        try {

            if (activeDirection.current) {

                await stopManualMove(
                    activeDirection.current
                );

                activeDirection.current =
                    null;
            }


            const response =
                await fetch(
                    "/api/mount/stop",
                    {
                        method: "POST",
                    }
                );


            if (!response.ok) {
                throw new Error(
                    "Failed to stop mount"
                );
            }

        } catch (error) {

            console.error(
                "Failed to stop mount:",
                error
            );

        }
    }


    async function handleMoveStart(
        direction: ManualMoveDirection
    ) {

        if (!connected) {
            return;
        }


        /*
         * Don't start the same direction twice.
         */
        if (
            activeDirection.current ===
            direction
        ) {
            return;
        }


        /*
         * Stop any currently active direction
         * before starting another.
         */
        if (activeDirection.current) {

            try {

                await stopManualMove(
                    activeDirection.current
                );

            } catch (error) {

                console.error(
                    "Unable to stop previous movement:",
                    error
                );
            }
        }


        activeDirection.current =
            direction;


        try {

            await startManualMove(
                direction
            );

        } catch (error) {

            console.error(
                `Failed to move mount ${direction}:`,
                error
            );

            activeDirection.current =
                null;
        }
    }


    async function handleMoveStop(
        direction: ManualMoveDirection
    ) {

        /*
         * Ignore duplicate release events.
         */
        if (
            activeDirection.current !==
            direction
        ) {
            return;
        }


        activeDirection.current =
            null;


        try {

            await stopManualMove(
                direction
            );

        } catch (error) {

            console.error(
                `Failed to stop mount ${direction}:`,
                error
            );

        }
    }


    function directionButton(
        direction: ManualMoveDirection,
        icon: React.ReactNode
    ) {

        return (
            <button
                type="button"

                onMouseDown={() =>
                    handleMoveStart(
                        direction
                    )
                }

                onMouseUp={() =>
                    handleMoveStop(
                        direction
                    )
                }

                onMouseLeave={() =>
                    handleMoveStop(
                        direction
                    )
                }

                onTouchStart={(event) => {

                    event.preventDefault();

                    handleMoveStart(
                        direction
                    );
                }}

                onTouchEnd={(event) => {

                    event.preventDefault();

                    handleMoveStop(
                        direction
                    );
                }}

                disabled={!connected}

                className="
                    flex
                    h-12
                    w-12
                    select-none
                    items-center
                    justify-center
                    rounded-lg
                    border
                    border-slate-700
                    bg-slate-800
                    text-slate-300
                    transition
                    hover:border-violet-500/40
                    hover:bg-violet-500/10
                    hover:text-violet-300
                    active:bg-violet-500/20
                    active:text-violet-200
                    disabled:cursor-not-allowed
                    disabled:opacity-40
                "
            >
                {icon}
            </button>
        );
    }


    return (
        <div
            className="
                flex
                h-full
                w-full
                flex-col
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
                    shrink-0
                    items-center
                    justify-between
                    border-b
                    border-slate-800
                    px-5
                    py-3
                "
            >

                <div>

                    <h2
                        className="
                            text-sm
                            font-semibold
                            text-slate-100
                        "
                    >
                        Mount Controls
                    </h2>

                    <p
                        className="
                            mt-0.5
                            text-xs
                            text-slate-500
                        "
                    >
                        Slewing and manual positioning
                    </p>

                </div>


                <div
                    className="
                        flex
                        items-center
                        gap-2
                    "
                >

                    <span
                        className={`
                            h-2
                            w-2
                            rounded-full
                            ${
                                connected
                                    ? "bg-green-500"
                                    : "bg-slate-600"
                            }
                        `}
                    />

                    <span
                        className="
                            text-xs
                            text-slate-500
                        "
                    >
                        {connected
                            ? "Ready"
                            : "Unavailable"}
                    </span>

                </div>

            </div>


            {/* Content */}
            <div
                className="
                    min-h-0
                    flex-1
                    overflow-y-auto
                    p-5
                "
            >

                <div className="space-y-6">

                    {/* Target Coordinates */}
                    <section>

                        <div
                            className="
                                mb-3
                                flex
                                items-center
                                gap-2
                            "
                        >

                            <Crosshair
                                size={15}
                                className="text-violet-400"
                            />

                            <p
                                className="
                                    text-xs
                                    font-semibold
                                    uppercase
                                    tracking-wider
                                    text-slate-500
                                "
                            >
                                Target Coordinates
                            </p>

                        </div>


                        <form
                            onSubmit={
                                handleSlew
                            }
                        >

                            <div
                                className="
                                    grid
                                    grid-cols-2
                                    gap-3
                                "
                            >

                                <div>

                                    <label
                                        className="
                                            mb-1.5
                                            block
                                            text-xs
                                            text-slate-500
                                        "
                                    >
                                        Right Ascension (decimal hours)
                                    </label>

                                    <input
                                        type="number"
                                        step="any"
                                        value={ra}
                                        onChange={(event) =>
                                            setRa(
                                                event
                                                    .target
                                                    .value
                                            )
                                        }
                                        disabled={
                                            !connected
                                        }
                                        placeholder="RA"
                                        className="
                                            w-full
                                            rounded-lg
                                            border
                                            border-slate-700
                                            bg-slate-950
                                            px-3
                                            py-2.5
                                            font-mono
                                            text-sm
                                            text-slate-200
                                            outline-none
                                            transition
                                            placeholder:text-slate-600
                                            focus:border-violet-500
                                            focus:ring-2
                                            focus:ring-violet-500/20
                                            disabled:cursor-not-allowed
                                            disabled:opacity-40
                                        "
                                    />

                                </div>


                                <div>

                                    <label
                                        className="
                                            mb-1.5
                                            block
                                            text-xs
                                            text-slate-500
                                        "
                                    >
                                        Declination (decimal degrees)
                                    </label>

                                    <input
                                        type="number"
                                        step="any"
                                        value={dec}
                                        onChange={(event) =>
                                            setDec(
                                                event
                                                    .target
                                                    .value
                                            )
                                        }
                                        disabled={
                                            !connected
                                        }
                                        placeholder="DEC"
                                        className="
                                            w-full
                                            rounded-lg
                                            border
                                            border-slate-700
                                            bg-slate-950
                                            px-3
                                            py-2.5
                                            font-mono
                                            text-sm
                                            text-slate-200
                                            outline-none
                                            transition
                                            placeholder:text-slate-600
                                            focus:border-violet-500
                                            focus:ring-2
                                            focus:ring-violet-500/20
                                            disabled:cursor-not-allowed
                                            disabled:opacity-40
                                        "
                                    />

                                </div>

                            </div>


                            <button
                                type="submit"
                                disabled={
                                    !connected ||
                                    loading ||
                                    !ra ||
                                    !dec
                                }
                                className="
                                    mt-3
                                    flex
                                    w-full
                                    items-center
                                    justify-center
                                    gap-2
                                    rounded-lg
                                    bg-violet-600
                                    px-4
                                    py-2.5
                                    text-sm
                                    font-medium
                                    text-white
                                    transition
                                    hover:bg-violet-500
                                    disabled:cursor-not-allowed
                                    disabled:opacity-40
                                "
                            >

                                <Play
                                    size={15}
                                />

                                {action === "slew"
                                    ? "Slewing..."
                                    : "Slew to Target"}

                            </button>

                        </form>

                    </section>


                    {/* Park / Unpark */}
                    <section
                        className="
                            border-t
                            border-slate-800
                            pt-5
                        "
                    >

                        <div
                            className="
                                mb-3
                                flex
                                items-center
                                gap-2
                            "
                        >

                            <MapPin
                                size={15}
                                className="text-violet-400"
                            />

                            <p
                                className="
                                    text-xs
                                    font-semibold
                                    uppercase
                                    tracking-wider
                                    text-slate-500
                                "
                            >
                                Position
                            </p>

                        </div>


                        <div
                            className="
                                grid
                                grid-cols-2
                                gap-3
                            "
                        >

                            <button
                                type="button"
                                onClick={
                                    handlePark
                                }
                                disabled={
                                    !connected ||
                                    loading
                                }
                                className="
                                    flex
                                    items-center
                                    justify-center
                                    gap-2
                                    rounded-lg
                                    border
                                    border-slate-700
                                    bg-slate-800
                                    px-4
                                    py-2.5
                                    text-sm
                                    font-medium
                                    text-slate-300
                                    transition
                                    hover:bg-slate-700
                                    hover:text-slate-100
                                    disabled:cursor-not-allowed
                                    disabled:opacity-40
                                "
                            >

                                <ParkingCircle
                                    size={15}
                                />

                                {action === "park"
                                    ? "Parking..."
                                    : "Park"}

                            </button>


                            <button
                                type="button"
                                onClick={
                                    handleUnpark
                                }
                                disabled={
                                    !connected ||
                                    loading
                                }
                                className="
                                    flex
                                    items-center
                                    justify-center
                                    gap-2
                                    rounded-lg
                                    border
                                    border-slate-700
                                    bg-slate-800
                                    px-4
                                    py-2.5
                                    text-sm
                                    font-medium
                                    text-slate-300
                                    transition
                                    hover:bg-slate-700
                                    hover:text-slate-100
                                    disabled:cursor-not-allowed
                                    disabled:opacity-40
                                "
                            >

                                <ParkingCircle
                                    size={15}
                                />

                                {action === "unpark"
                                    ? "Unparking..."
                                    : "Unpark"}

                            </button>

                        </div>

                    </section>


                    {/* Manual Movement */}
                    <section
                        className="
                            border-t
                            border-slate-800
                            pt-5
                        "
                    >

                        <div
                            className="
                                mb-4
                                flex
                                items-center
                                justify-between
                            "
                        >

                            <div>

                                <p
                                    className="
                                        text-xs
                                        font-semibold
                                        uppercase
                                        tracking-wider
                                        text-slate-500
                                    "
                                >
                                    Manual Movement
                                </p>

                                <p
                                    className="
                                        mt-1
                                        text-xs
                                        text-slate-600
                                    "
                                >
                                    Hold a direction to move
                                </p>

                            </div>

                        </div>


                        <div
                            className="
                                mx-auto
                                grid
                                w-fit
                                grid-cols-3
                                grid-rows-3
                                items-center
                                justify-items-center
                                gap-2
                            "
                        >

                            <div />

                            {directionButton(
                                "north",
                                <ArrowUp
                                    size={19}
                                />
                            )}

                            <div />


                            {directionButton(
                                "west",
                                <ArrowLeft
                                    size={19}
                                />
                            )}


                            <div
                                className="
                                    flex
                                    h-10
                                    w-10
                                    items-center
                                    justify-center
                                    rounded-full
                                    border
                                    border-slate-800
                                    bg-slate-950
                                    text-[9px]
                                    font-semibold
                                    uppercase
                                    tracking-wider
                                    text-slate-600
                                "
                            >
                                Move
                            </div>


                            {directionButton(
                                "east",
                                <ArrowRight
                                    size={19}
                                />
                            )}


                            <div />

                            {directionButton(
                                "south",
                                <ArrowDown
                                    size={19}
                                />
                            )}

                            <div />

                        </div>

                    </section>


                    {/* Stop */}
                    <section
                        className="
                            border-t
                            border-slate-800
                            pt-5
                        "
                    >

                        <button
                            type="button"
                            onClick={
                                handleStop
                            }
                            disabled={
                                !connected
                            }
                            className="
                                flex
                                w-full
                                items-center
                                justify-center
                                gap-2
                                rounded-lg
                                border
                                border-red-500/30
                                bg-red-500/10
                                px-4
                                py-3
                                text-sm
                                font-semibold
                                text-red-300
                                transition
                                hover:bg-red-500/20
                                disabled:cursor-not-allowed
                                disabled:opacity-40
                            "
                        >

                            <Octagon
                                size={16}
                            />

                            Stop Mount

                        </button>

                    </section>

                </div>

            </div>

        </div>
    );
}