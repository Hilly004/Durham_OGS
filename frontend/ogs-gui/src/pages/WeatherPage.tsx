import {
    useCallback,
    useEffect,
    useState,
} from "react";

import {
    CloudSun,
    RefreshCw,
} from "lucide-react";

import {
    connectWeather,
    disconnectWeather,
    getWeatherStatus,
    setWeatherOverride,
} from "../api/weather";

import type {
    WeatherOverrideMode,
    WeatherStatusData,
} from "../api/weather";


export default function WeatherPage() {

    const [status, setStatus] =
        useState<WeatherStatusData | null>(null);

    const [loading, setLoading] =
        useState(false);


    const updateStatus = useCallback(async () => {

        try {

            const result =
                await getWeatherStatus();

            setStatus(result);

        } catch (error) {

            console.error(
                "Unable to retrieve weather status:",
                error
            );

        }

    }, []);


    useEffect(() => {

        updateStatus();

        const interval = setInterval(
            updateStatus,
            3000
        );

        return () => {
            clearInterval(interval);
        };

    }, [updateStatus]);


    async function handleConnection() {
        setLoading(true);

        try {
            if (status?.connected) {
                await disconnectWeather();
            } else {
                await connectWeather();
            }

            // Do not manually change status.connected.
            // Ask the backend what the real state is.
            await updateStatus();

        } catch (error) {
            console.error(
                "Unable to change weather connection:",
                error
            );

            // Refresh even after failure so the UI reflects reality.
            await updateStatus();

        } finally {
            setLoading(false);
        }
    }

    async function handleOverride(
        mode: WeatherOverrideMode
    ) {

        setLoading(true);

        try {

            await setWeatherOverride(mode);

            await updateStatus();

        } catch (error) {

            console.error(
                "Unable to change weather override:",
                error
            );

        } finally {

            setLoading(false);

        }
    }


    return (
        <div
            className="
                flex
                h-full
                w-full
                flex-col
                gap-4
                overflow-hidden
                p-4
            "
        >

            {/* Header */}
            <div
                className="
                    flex
                    shrink-0
                    items-center
                    justify-between
                "
            >

                <div>

                    <h1
                        className="
                            text-xl
                            font-semibold
                            text-slate-100
                        "
                    >
                        Weather Station
                    </h1>

                    <p className="text-sm text-slate-400">
                        Environmental monitoring and observatory safety
                    </p>

                </div>


                <div className="flex items-center gap-3">

                    {/* Connect / Disconnect */}
                    <button
                        onClick={handleConnection}
                        disabled={loading}
                        className="
                            rounded-lg
                            border
                            border-violet-500/30
                            bg-violet-500/10
                            px-4
                            py-2
                            text-sm
                            font-medium
                            text-violet-300
                            transition
                            hover:bg-violet-500/20
                            disabled:cursor-not-allowed
                            disabled:opacity-50
                        "
                    >
                        {loading
                            ? "Working..."
                            : status?.connected
                                ? "Disconnect"
                                : "Connect"}
                    </button>


                    {/* Connection Status */}
                    <div
                        className="
                            flex
                            items-center
                            gap-2
                            rounded-lg
                            border
                            border-slate-800
                            bg-slate-900
                            px-3
                            py-2
                        "
                    >

                        <span
                            className={`
                                h-2.5
                                w-2.5
                                rounded-full

                                ${
                                    status?.connected
                                        ? "bg-green-500"
                                        : "bg-red-500"
                                }
                            `}
                        />

                        <span className="text-sm text-slate-300">
                            {status?.connected
                                ? "Connected"
                                : "Disconnected"}
                        </span>

                    </div>

                </div>

            </div>

            {/* Main Content */}
            <div
                className="
                    grid
                    min-h-0
                    flex-1
                    grid-cols-12
                    grid-rows-[1fr_auto]
                    gap-4
                "
            >

                {/* Conditions */}
                <div
                    className="
                        col-span-5
                        rounded-xl
                        border
                        border-slate-800
                        bg-slate-900
                        p-5
                    "
                >

                    <h2 className="mb-5 text-sm font-semibold text-slate-100">
                        Conditions
                    </h2>


                    <div className="space-y-4">

                        <StatusRow
                            label="Effective State"
                            value={
                                status?.state?.toUpperCase()
                                ?? "UNKNOWN"
                            }
                            state={
                                status?.safe
                                    ? "safe"
                                    : "unsafe"
                            }
                        />


                        <StatusRow
                            label="Actual Weather"
                            value={
                                status?.actualSafe
                                    ? "SAFE"
                                    : "UNSAFE"
                            }
                            state={
                                status?.actualSafe
                                    ? "safe"
                                    : "unsafe"
                            }
                        />


                        {status?.reason && (

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
                                        mb-1
                                        text-xs
                                        uppercase
                                        tracking-wide
                                        text-slate-500
                                    "
                                >
                                    Reason
                                </p>

                                <p className="text-sm text-slate-300">
                                    {status.reason}
                                </p>

                            </div>

                        )}


                        {/* Override warning is intentionally amber,
                            because this is an active test condition. */}
                        {status?.override !== null &&
                            status?.override !== undefined && (

                            <div
                                className="
                                    rounded-lg
                                    border
                                    border-amber-500/30
                                    bg-amber-500/10
                                    p-4
                                "
                            >

                                <div className="flex items-center gap-2">

                                    <span
                                        className="
                                            h-2
                                            w-2
                                            rounded-full
                                            bg-amber-400
                                        "
                                    />

                                    <p className="text-xs font-semibold text-amber-300">
                                        WEATHER OVERRIDE ACTIVE
                                    </p>

                                </div>

                                <p className="mt-2 text-sm text-amber-400/80">
                                    {status.override
                                        ? "Safety is being forced SAFE."
                                        : "Safety is being forced UNSAFE."}
                                </p>

                            </div>

                        )}

                    </div>

                </div>


                {/* Sensor Readings */}
                <div
                    className="
                        col-span-7
                        rounded-xl
                        border
                        border-slate-800
                        bg-slate-900
                        p-5
                    "
                >

                    <h2 className="mb-5 text-sm font-semibold text-slate-100">
                        Sensor Readings
                    </h2>


                    <div className="grid grid-cols-2 gap-3">

                        <Reading
                            label="Temperature"
                            value="--"
                            unit="°C"
                        />

                        <Reading
                            label="Humidity"
                            value="--"
                            unit="%"
                        />

                        <Reading
                            label="Wind Speed"
                            value="--"
                            unit="m/s"
                        />

                        <Reading
                            label="Rain"
                            value="--"
                        />

                        <Reading
                            label="Cloud"
                            value="--"
                        />

                        <Reading
                            label="Last Update"
                            value="--"
                        />

                    </div>

                </div>


                {/* Override Controls */}
                <div
                    className="
                        col-span-12
                        rounded-xl
                        border
                        border-slate-800
                        bg-slate-900
                        p-4
                    "
                >

                    <div
                        className="
                            flex
                            items-center
                            justify-between
                        "
                    >

                        <div>

                            <h2 className="text-sm font-semibold text-slate-100">
                                Weather Test Override
                            </h2>

                            <p className="mt-1 text-xs text-slate-500">
                                Override the effective weather state for observatory testing.
                            </p>

                        </div>


                        <div className="flex gap-2">

                            <OverrideButton
                                active={
                                    status?.override === null
                                }
                                label="Auto"
                                onClick={() =>
                                    handleOverride("auto")
                                }
                                variant="auto"
                                disabled={loading}
                            />

                            <OverrideButton
                                active={
                                    status?.override === true
                                }
                                label="Force Safe"
                                onClick={() =>
                                    handleOverride("safe")
                                }
                                variant="safe"
                                disabled={loading}
                            />

                            <OverrideButton
                                active={
                                    status?.override === false
                                }
                                label="Force Unsafe"
                                onClick={() =>
                                    handleOverride("unsafe")
                                }
                                variant="unsafe"
                                disabled={loading}
                            />

                        </div>

                    </div>

                </div>

            </div>

        </div>
    );
}


function StatusRow({
    label,
    value,
    state,
}: {
    label: string;
    value: string;
    state: "safe" | "unsafe";
}) {

    return (
        <div
            className="
                flex
                items-center
                justify-between
                rounded-lg
                border
                border-slate-800
                bg-slate-950/50
                px-4
                py-3
            "
        >

            <span className="text-sm text-slate-400">
                {label}
            </span>


            <div className="flex items-center gap-2">

                <span
                    className={`
                        h-2
                        w-2
                        rounded-full
                        ${
                            state === "safe"
                                ? "bg-green-500"
                                : "bg-red-500"
                        }
                    `}
                />

                <span
                    className={
                        state === "safe"
                            ? "text-sm font-medium text-green-400"
                            : "text-sm font-medium text-red-400"
                    }
                >
                    {value}
                </span>

            </div>

        </div>
    );
}


function Reading({
    label,
    value,
    unit,
}: {
    label: string;
    value: string;
    unit?: string;
}) {

    return (
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
                {label}
            </p>

            <p
                className="
                    mt-2
                    font-mono
                    text-lg
                    text-slate-200
                "
            >
                {value}

                {unit && (
                    <span className="ml-1 text-sm text-slate-500">
                        {unit}
                    </span>
                )}
            </p>

        </div>
    );
}


function OverrideButton({
    active,
    label,
    onClick,
    variant,
    disabled,
}: {
    active: boolean;
    label: string;
    onClick: () => void;
    variant: "auto" | "safe" | "unsafe";
    disabled: boolean;
}) {

    let classes =
        "border-slate-700 bg-slate-800 text-slate-400 hover:bg-slate-700";

    if (active && variant === "auto") {
        classes =
            "border-violet-500/40 bg-violet-500/15 text-violet-300";
    }

    if (active && variant === "safe") {
        classes =
            "border-amber-500/50 bg-amber-500/20 text-amber-200";
    }

    if (active && variant === "unsafe") {
        classes =
            "border-red-500/50 bg-red-500/20 text-red-200";
    }


    return (
        <button
            type="button"
            onClick={onClick}
            disabled={disabled}
            className={`
                rounded-lg
                border
                px-4
                py-2
                text-sm
                font-medium
                transition
                disabled:cursor-not-allowed
                disabled:opacity-50
                ${classes}
            `}
        >
            {label}
        </button>
    );
}