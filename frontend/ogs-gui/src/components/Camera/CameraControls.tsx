import {
    useEffect,
    useState,
} from "react";

import {
    Camera,
    CircleStop,
    Gauge,
    Play,
    RefreshCw,
    Timer,
} from "lucide-react";

import {
    captureCameraFrame,
    getCameraStatus,
    getCameraStreamStatus,
    setCameraExposure,
    setCameraFrameRate,
    setCameraGain,
    startCameraStream,
    stopCameraStream,
} from "../../api/camera";


interface CameraControlsProps {
    connected: boolean;
}


const EXPOSURE_PRESETS = [
    {
        label: "1 ms",
        value: 1000,
    },
    {
        label: "10 ms",
        value: 10000,
    },
    {
        label: "50 ms",
        value: 50000,
    },
    {
        label: "100 ms",
        value: 100000,
    },
];


const GAIN_PRESETS = [
    0,
    5,
    10,
    20,
];


const FRAME_RATE_PRESETS = [
    5,
    10,
    15,
    30,
];


export default function CameraControls({
    connected,
}: CameraControlsProps) {

    const [
        loading,
        setLoading,
    ] = useState(false);


    const [
        streaming,
        setStreaming,
    ] = useState(false);


    const [
        exposure,
        setExposure,
    ] = useState("");


    const [
        gain,
        setGain,
    ] = useState("");


    const [
        frameRate,
        setFrameRate,
    ] = useState("");


    const [
        gainUnit,
        setGainUnit,
    ] = useState<string | null>(
        null
    );


    const [
        message,
        setMessage,
    ] = useState<string | null>(
        null
    );


    const [
        error,
        setError,
    ] = useState<string | null>(
        null
    );


    async function refreshCameraValues() {

        if (!connected) {

            setExposure("");
            setGain("");
            setFrameRate("");
            setStreaming(false);
            setGainUnit(null);

            return;
        }


        try {

            const [
                status,
                streamStatus,
            ] =
                await Promise.all([
                    getCameraStatus(),
                    getCameraStreamStatus(),
                ]);


            setExposure(
                status.exposure !== null
                    ? String(
                        status.exposure
                    )
                    : ""
            );


            setGain(
                status.gain !== null
                    ? String(
                        status.gain
                    )
                    : ""
            );


            setFrameRate(
                status.frame_rate !== null
                &&
                status.frame_rate !== undefined
                    ? String(
                        Number(
                            status.frame_rate
                        ).toFixed(1)
                    )
                    : ""
            );


            setGainUnit(
                status.gain_unit
                ??
                null
            );


            setStreaming(
                streamStatus.streaming
            );


        } catch (refreshError) {

            console.error(
                "Unable to refresh camera controls:",
                refreshError
            );

        }
    }


    useEffect(() => {

        void refreshCameraValues();

    }, [connected]);


    function showError(
        value: unknown
    ) {

        setMessage(null);


        if (
            value
            instanceof Error
        ) {

            setError(
                value.message
            );

        } else {

            setError(
                "Camera operation failed"
            );

        }
    }


    function showSuccess(
        value: string
    ) {

        setError(null);
        setMessage(value);
    }


    async function handleExposure(
        value?: number
    ) {

        if (!connected) {
            return;
        }


        const exposureValue =
            value
            ??
            Number(exposure);


        if (
            !Number.isFinite(
                exposureValue
            )
            ||
            exposureValue <= 0
        ) {

            setError(
                "Enter a valid exposure"
            );

            return;
        }


        setLoading(true);

        setMessage(null);
        setError(null);


        try {

            await setCameraExposure(
                exposureValue
            );


            setExposure(
                String(
                    exposureValue
                )
            );


            showSuccess(
                `Exposure set to ${exposureValue} µs`
            );


            await refreshCameraValues();


        } catch (exposureError) {

            showError(
                exposureError
            );


        } finally {

            setLoading(false);

        }
    }


    async function handleStartStream() {

        if (!connected) {
            return;
        }


        setLoading(true);

        setMessage(null);
        setError(null);


        try {

            await startCameraStream();

            setStreaming(true);

            showSuccess(
                "Live view started"
            );


        } catch (streamError) {

            showError(
                streamError
            );


        } finally {

            setLoading(false);

        }
    }


    async function handleStopStream() {

        if (!connected) {
            return;
        }


        setLoading(true);

        setMessage(null);
        setError(null);


        try {

            await stopCameraStream();

            setStreaming(false);

            showSuccess(
                "Live view stopped"
            );


        } catch (streamError) {

            showError(
                streamError
            );


        } finally {

            setLoading(false);

        }
    }


    async function handleCapture() {

        if (
            !connected
            ||
            streaming
        ) {
            return;
        }


        setLoading(true);

        setMessage(null);
        setError(null);


        try {

            const blob =
                await captureCameraFrame();


            if (blob.size === 0) {

                throw new Error(
                    "Camera returned an empty image"
                );
            }


            const url =
                URL.createObjectURL(
                    blob
                );


            const link =
                document.createElement(
                    "a"
                );


            link.href = url;

            link.download =
                `camera_capture_${Date.now()}.jpg`;


            document.body.appendChild(
                link
            );


            link.click();


            document.body.removeChild(
                link
            );


            window.setTimeout(
                () => {

                    URL.revokeObjectURL(
                        url
                    );

                },
                1000
            );


            showSuccess(
                "Frame captured"
            );


        } catch (captureError) {

            showError(
                captureError
            );


        } finally {

            setLoading(false);

        }
    }


    async function handleGain(
        value?: number
    ) {

        if (!connected) {
            return;
        }


        const gainValue =
            value
            ??
            Number(gain);


        if (
            !Number.isFinite(
                gainValue
            )
        ) {

            setError(
                "Enter a valid gain value"
            );

            return;
        }


        setLoading(true);

        setMessage(null);
        setError(null);


        try {

            await setCameraGain(
                gainValue
            );


            setGain(
                String(
                    gainValue
                )
            );


            showSuccess(
                (
                    "Gain set to "
                    +
                    `${gainValue}`
                    +
                    (
                        gainUnit
                            ? ` ${gainUnit}`
                            : ""
                    )
                )
            );


            await refreshCameraValues();


        } catch (gainError) {

            showError(
                gainError
            );


        } finally {

            setLoading(false);

        }
    }


    async function handleFrameRate(
        value?: number
    ) {

        if (!connected) {
            return;
        }


        const fpsValue =
            value
            ??
            Number(frameRate);


        if (
            !Number.isFinite(
                fpsValue
            )
            ||
            fpsValue <= 0
        ) {

            setError(
                "Enter a valid frame rate"
            );

            return;
        }


        setLoading(true);

        setMessage(null);
        setError(null);


        try {

            await setCameraFrameRate(
                fpsValue
            );


            setFrameRate(
                String(
                    fpsValue
                )
            );


            showSuccess(
                (
                    "Frame rate set to "
                    +
                    `${fpsValue} FPS`
                )
            );


            await refreshCameraValues();


        } catch (frameRateError) {

            showError(
                frameRateError
            );


        } finally {

            setLoading(false);

        }
    }


    const controlsDisabled =
        loading
        ||
        !connected;


    return (

        <div
            className="
                flex
                h-full
                min-h-0
                flex-col
                rounded-lg
                border
                border-slate-800
                bg-slate-950/40
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

                <div>

                    <h2
                        className="
                            text-sm
                            font-semibold
                            text-slate-200
                        "
                    >
                        Camera Controls
                    </h2>


                    <p
                        className="
                            mt-0.5
                            text-xs
                            text-slate-500
                        "
                    >
                        Acquisition and live-view settings
                    </p>

                </div>


                <button
                    type="button"

                    title="Refresh camera settings"

                    onClick={() =>
                        void refreshCameraValues()
                    }

                    disabled={
                        controlsDisabled
                    }

                    className="
                        flex
                        h-8
                        w-8
                        items-center
                        justify-center
                        rounded-lg
                        border
                        border-slate-800
                        bg-slate-900
                        text-slate-400
                        transition
                        hover:border-slate-700
                        hover:text-slate-200
                        disabled:cursor-not-allowed
                        disabled:opacity-40
                    "
                >

                    <RefreshCw
                        size={15}
                        className={
                            loading
                                ? "animate-spin"
                                : ""
                        }
                    />

                </button>

            </div>


            <div
                className="
                    flex-1
                    space-y-5
                    overflow-y-auto
                    p-4
                "
            >

                {/* Exposure */}

                <section>

                    <div
                        className="
                            mb-2
                            flex
                            items-center
                            gap-2
                        "
                    >

                        <Timer
                            size={15}
                            className="
                                text-violet-400
                            "
                        />

                        <span
                            className="
                                text-xs
                                font-medium
                                uppercase
                                tracking-wide
                                text-slate-400
                            "
                        >
                            Exposure
                        </span>

                    </div>


                    <div
                        className="
                            flex
                            gap-2
                        "
                    >

                        <div
                            className="
                                relative
                                min-w-0
                                flex-1
                            "
                        >

                            <input
                                type="number"

                                min="1"

                                value={
                                    exposure
                                }

                                onChange={event =>
                                    setExposure(
                                        event.target.value
                                    )
                                }

                                onKeyDown={event => {

                                    if (
                                        event.key
                                        ===
                                        "Enter"
                                    ) {

                                        void handleExposure();

                                    }
                                }}

                                disabled={
                                    controlsDisabled
                                }

                                placeholder="Exposure"

                                className="
                                    w-full
                                    rounded-lg
                                    border
                                    border-slate-700
                                    bg-slate-900
                                    px-3
                                    py-2
                                    pr-10
                                    text-sm
                                    text-slate-200
                                    outline-none
                                    transition
                                    focus:border-violet-500
                                    disabled:cursor-not-allowed
                                    disabled:opacity-40
                                "
                            />


                            <span
                                className="
                                    pointer-events-none
                                    absolute
                                    right-3
                                    top-1/2
                                    -translate-y-1/2
                                    text-xs
                                    text-slate-500
                                "
                            >
                                µs
                            </span>

                        </div>


                        <button
                            type="button"

                            onClick={() =>
                                void handleExposure()
                            }

                            disabled={
                                controlsDisabled
                            }

                            className="
                                rounded-lg
                                bg-violet-600
                                px-4
                                py-2
                                text-xs
                                font-medium
                                text-white
                                transition
                                hover:bg-violet-500
                                disabled:cursor-not-allowed
                                disabled:opacity-40
                            "
                        >
                            Apply
                        </button>

                    </div>


                    <div
                        className="
                            mt-2
                            grid
                            grid-cols-4
                            gap-2
                        "
                    >

                        {
                            EXPOSURE_PRESETS.map(
                                preset => (

                                    <button
                                        key={
                                            preset.value
                                        }

                                        type="button"

                                        disabled={
                                            controlsDisabled
                                        }

                                        onClick={() =>
                                            void handleExposure(
                                                preset.value
                                            )
                                        }

                                        className="
                                            rounded-md
                                            border
                                            border-slate-800
                                            bg-slate-900
                                            px-2
                                            py-1.5
                                            text-xs
                                            text-slate-400
                                            transition
                                            hover:border-violet-500/40
                                            hover:text-violet-300
                                            disabled:cursor-not-allowed
                                            disabled:opacity-40
                                        "
                                    >
                                        {
                                            preset.label
                                        }
                                    </button>

                                )
                            )
                        }

                    </div>

                </section>


                {/* Gain */}

                <section>

                    <div
                        className="
                            mb-2
                            flex
                            items-center
                            gap-2
                        "
                    >

                        <Gauge
                            size={15}
                            className="
                                text-violet-400
                            "
                        />

                        <span
                            className="
                                text-xs
                                font-medium
                                uppercase
                                tracking-wide
                                text-slate-400
                            "
                        >
                            Gain
                        </span>

                    </div>


                    <div
                        className="
                            flex
                            gap-2
                        "
                    >

                        <div
                            className="
                                relative
                                min-w-0
                                flex-1
                            "
                        >

                            <input
                                type="number"

                                step="0.1"

                                value={
                                    gain
                                }

                                onChange={event =>
                                    setGain(
                                        event.target.value
                                    )
                                }

                                onKeyDown={event => {

                                    if (
                                        event.key
                                        ===
                                        "Enter"
                                    ) {

                                        void handleGain();

                                    }
                                }}

                                disabled={
                                    controlsDisabled
                                }

                                placeholder="Gain"

                                className="
                                    w-full
                                    rounded-lg
                                    border
                                    border-slate-700
                                    bg-slate-900
                                    px-3
                                    py-2
                                    pr-12
                                    text-sm
                                    text-slate-200
                                    outline-none
                                    transition
                                    focus:border-violet-500
                                    disabled:cursor-not-allowed
                                    disabled:opacity-40
                                "
                            />


                            {gainUnit && (

                                <span
                                    className="
                                        pointer-events-none
                                        absolute
                                        right-3
                                        top-1/2
                                        -translate-y-1/2
                                        text-xs
                                        text-slate-500
                                    "
                                >
                                    {gainUnit}
                                </span>

                            )}

                        </div>


                        <button
                            type="button"

                            onClick={() =>
                                void handleGain()
                            }

                            disabled={
                                controlsDisabled
                            }

                            className="
                                rounded-lg
                                bg-violet-600
                                px-4
                                py-2
                                text-xs
                                font-medium
                                text-white
                                transition
                                hover:bg-violet-500
                                disabled:cursor-not-allowed
                                disabled:opacity-40
                            "
                        >
                            Apply
                        </button>

                    </div>


                    <div
                        className="
                            mt-2
                            grid
                            grid-cols-4
                            gap-2
                        "
                    >

                        {
                            GAIN_PRESETS.map(
                                value => (

                                    <button
                                        key={
                                            value
                                        }

                                        type="button"

                                        disabled={
                                            controlsDisabled
                                        }

                                        onClick={() =>
                                            void handleGain(
                                                value
                                            )
                                        }

                                        className="
                                            rounded-md
                                            border
                                            border-slate-800
                                            bg-slate-900
                                            px-2
                                            py-1.5
                                            text-xs
                                            text-slate-400
                                            transition
                                            hover:border-violet-500/40
                                            hover:text-violet-300
                                            disabled:cursor-not-allowed
                                            disabled:opacity-40
                                        "
                                    >
                                        {value}
                                    </button>

                                )
                            )
                        }

                    </div>

                </section>


                {/* Frame rate */}

                <section>

                    <div
                        className="
                            mb-2
                            flex
                            items-center
                            gap-2
                        "
                    >

                        <Gauge
                            size={15}
                            className="
                                text-violet-400
                            "
                        />

                        <span
                            className="
                                text-xs
                                font-medium
                                uppercase
                                tracking-wide
                                text-slate-400
                            "
                        >
                            Frame Rate
                        </span>

                    </div>


                    <div
                        className="
                            flex
                            gap-2
                        "
                    >

                        <div
                            className="
                                relative
                                min-w-0
                                flex-1
                            "
                        >

                            <input
                                type="number"

                                min="0.1"

                                step="0.1"

                                value={
                                    frameRate
                                }

                                onChange={event =>
                                    setFrameRate(
                                        event.target.value
                                    )
                                }

                                onKeyDown={event => {

                                    if (
                                        event.key
                                        ===
                                        "Enter"
                                    ) {

                                        void handleFrameRate();

                                    }
                                }}

                                disabled={
                                    controlsDisabled
                                }

                                placeholder="FPS"

                                className="
                                    w-full
                                    rounded-lg
                                    border
                                    border-slate-700
                                    bg-slate-900
                                    px-3
                                    py-2
                                    pr-12
                                    text-sm
                                    text-slate-200
                                    outline-none
                                    transition
                                    focus:border-violet-500
                                    disabled:cursor-not-allowed
                                    disabled:opacity-40
                                "
                            />


                            <span
                                className="
                                    pointer-events-none
                                    absolute
                                    right-3
                                    top-1/2
                                    -translate-y-1/2
                                    text-xs
                                    text-slate-500
                                "
                            >
                                FPS
                            </span>

                        </div>


                        <button
                            type="button"

                            onClick={() =>
                                void handleFrameRate()
                            }

                            disabled={
                                controlsDisabled
                            }

                            className="
                                rounded-lg
                                bg-violet-600
                                px-4
                                py-2
                                text-xs
                                font-medium
                                text-white
                                transition
                                hover:bg-violet-500
                                disabled:cursor-not-allowed
                                disabled:opacity-40
                            "
                        >
                            Apply
                        </button>

                    </div>


                    <div
                        className="
                            mt-2
                            grid
                            grid-cols-4
                            gap-2
                        "
                    >

                        {
                            FRAME_RATE_PRESETS.map(
                                value => (

                                    <button
                                        key={
                                            value
                                        }

                                        type="button"

                                        disabled={
                                            controlsDisabled
                                        }

                                        onClick={() =>
                                            void handleFrameRate(
                                                value
                                            )
                                        }

                                        className="
                                            rounded-md
                                            border
                                            border-slate-800
                                            bg-slate-900
                                            px-2
                                            py-1.5
                                            text-xs
                                            text-slate-400
                                            transition
                                            hover:border-violet-500/40
                                            hover:text-violet-300
                                            disabled:cursor-not-allowed
                                            disabled:opacity-40
                                        "
                                    >
                                        {value}
                                    </button>

                                )
                            )
                        }

                    </div>


                    <p
                        className="
                            mt-2
                            text-[11px]
                            leading-relaxed
                            text-slate-600
                        "
                    >
                        Some cameras determine frame rate
                        automatically from exposure and do
                        not support a direct FPS setting.
                    </p>

                </section>


                {/* Capture / streaming */}

                <section
                    className="
                        border-t
                        border-slate-800
                        pt-4
                    "
                >

                    <div
                        className="
                            grid
                            grid-cols-2
                            gap-2
                        "
                    >

                        <button
                            type="button"

                            onClick={
                                handleCapture
                            }

                            disabled={
                                loading
                                ||
                                !connected
                                ||
                                streaming
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
                                px-3
                                py-2.5
                                text-sm
                                font-medium
                                text-slate-200
                                transition
                                hover:bg-slate-700
                                disabled:cursor-not-allowed
                                disabled:opacity-40
                            "
                        >

                            <Camera
                                size={16}
                            />

                            Capture

                        </button>


                        {!streaming ? (

                            <button
                                type="button"

                                onClick={
                                    handleStartStream
                                }

                                disabled={
                                    loading
                                    ||
                                    !connected
                                }

                                className="
                                    flex
                                    items-center
                                    justify-center
                                    gap-2
                                    rounded-lg
                                    bg-violet-600
                                    px-3
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
                                    size={16}
                                />

                                Live View

                            </button>

                        ) : (

                            <button
                                type="button"

                                onClick={
                                    handleStopStream
                                }

                                disabled={
                                    loading
                                }

                                className="
                                    flex
                                    items-center
                                    justify-center
                                    gap-2
                                    rounded-lg
                                    bg-red-600
                                    px-3
                                    py-2.5
                                    text-sm
                                    font-medium
                                    text-white
                                    transition
                                    hover:bg-red-500
                                    disabled:cursor-not-allowed
                                    disabled:opacity-40
                                "
                            >

                                <CircleStop
                                    size={16}
                                />

                                Stop Live

                            </button>

                        )}

                    </div>

                </section>


                {/* Feedback */}

                {message && (

                    <div
                        className="
                            rounded-lg
                            border
                            border-emerald-500/20
                            bg-emerald-500/10
                            px-3
                            py-2
                            text-xs
                            text-emerald-300
                        "
                    >
                        {message}
                    </div>

                )}


                {error && (

                    <div
                        className="
                            rounded-lg
                            border
                            border-red-500/20
                            bg-red-500/10
                            px-3
                            py-2
                            text-xs
                            text-red-300
                        "
                    >
                        {error}
                    </div>

                )}


                {!connected && (

                    <div
                        className="
                            rounded-lg
                            border
                            border-slate-800
                            bg-slate-900/50
                            px-3
                            py-3
                            text-center
                            text-xs
                            text-slate-500
                        "
                    >
                        Connect a camera to enable controls.
                    </div>

                )}

            </div>

        </div>
    );
}