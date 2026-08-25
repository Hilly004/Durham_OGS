import {
    useCallback,
    useEffect,
    useState,
} from "react";

import {
    Camera,
    CircleStop,
    Play,
    Plug,
    PlugZap,
} from "lucide-react";

import {
    connectCamera,
    disconnectCamera,
    getCameraLiveUrl,
    getCameraStatus,
    setCameraExposure,
    setCameraGain,
    startCameraStream,
    stopCameraStream,
} from "../../api/camera";

import type {
    CameraStatusData,
} from "../../api/camera";


export default function CameraWidget() {

    const [status, setStatus] =
        useState<CameraStatusData>({
            connected: false,
            streaming: false,
            camera: null,
            exposure: null,
            gain: null,
            gain_unit: null,
            frame_rate: null,
            frame_count: 0,
        });


    const [streaming, setStreaming] =
        useState(false);


    const [loading, setLoading] =
        useState(false);


    const [error, setError] =
        useState<string | null>(
            null
        );


    const [exposure, setExposure] =
        useState("");


    const [gain, setGain] =
        useState("");


    const [streamKey, setStreamKey] =
        useState(0);


    // =========================================================
    // Status
    // =========================================================

    const refreshStatus =
        useCallback(
            async () => {

                try {

                    const result =
                        await getCameraStatus();


                    setStatus(result);


                    setStreaming(
                        result.streaming
                    );


                    if (
                        result.exposure !== null
                        &&
                        document.activeElement?.id
                        !==
                        "camera-exposure"
                    ) {

                        setExposure(
                            String(
                                Math.round(
                                    result.exposure
                                )
                            )
                        );

                    }


                    if (
                        result.gain !== null
                        &&
                        document.activeElement?.id
                        !==
                        "camera-gain"
                    ) {

                        setGain(
                            String(
                                Math.round(
                                    result.gain
                                )
                            )
                        );

                    }

                } catch (err) {

                    console.error(
                        "Unable to get camera status:",
                        err
                    );

                }

            },
            []
        );


    useEffect(() => {

        refreshStatus();


        const interval =
            window.setInterval(
                refreshStatus,
                3000
            );


        return () => {

            window.clearInterval(
                interval
            );

        };

    }, [
        refreshStatus,
    ]);


    // =========================================================
    // Connect
    // =========================================================

    async function handleConnect() {

        if (
            loading
            ||
            status.connected
        ) {
            return;
        }


        setLoading(true);
        setError(null);


        try {

            await connectCamera();

            await refreshStatus();

        } catch (err) {

            const message =
                err instanceof Error
                    ? err.message
                    : "Unable to connect camera";


            setError(message);

        } finally {

            setLoading(false);

        }

    }


    // =========================================================
    // Disconnect
    // =========================================================

    async function handleDisconnect() {

        if (
            loading
            ||
            !status.connected
        ) {
            return;
        }


        setLoading(true);
        setError(null);


        try {

            //
            // Remove the MJPEG image first.
            //
            setStreaming(false);


            if (status.streaming) {

                try {

                    await stopCameraStream();

                } catch (err) {

                    console.warn(
                        (
                            "Unable to stop stream "
                            + "before disconnect:"
                        ),
                        err
                    );

                }

            }


            await disconnectCamera();

            await refreshStatus();

        } catch (err) {

            const message =
                err instanceof Error
                    ? err.message
                    : "Unable to disconnect camera";


            setError(message);

        } finally {

            setLoading(false);

        }

    }


    // =========================================================
    // Start live view
    // =========================================================

    async function handleStartStream() {

        if (
            loading
            ||
            !status.connected
            ||
            streaming
        ) {
            return;
        }


        setLoading(true);
        setError(null);


        try {

            //
            // Start the ZWO SDK video capture
            // on the backend.
            //
            await startCameraStream();


            //
            // Incrementing the key makes React create
            // a completely new <img>, and therefore
            // a new MJPEG HTTP connection.
            //
            setStreamKey(
                previous =>
                    previous + 1
            );


            setStreaming(true);


            await refreshStatus();

        } catch (err) {

            const message =
                err instanceof Error
                    ? err.message
                    : "Unable to start live view";


            setError(message);

        } finally {

            setLoading(false);

        }

    }


    // =========================================================
    // Stop live view
    // =========================================================

    async function handleStopStream() {

        if (
            loading
            ||
            !streaming
        ) {
            return;
        }


        setLoading(true);
        setError(null);


        try {

            //
            // Removing the <img> closes the browser's
            // MJPEG HTTP connection immediately.
            //
            setStreaming(false);


            await stopCameraStream();

            await refreshStatus();

        } catch (err) {

            const message =
                err instanceof Error
                    ? err.message
                    : "Unable to stop live view";


            setError(message);

        } finally {

            setLoading(false);

        }

    }


    // =========================================================
    // Exposure
    // =========================================================

    async function handleExposure() {

        if (
            loading
            ||
            !status.connected
        ) {
            return;
        }


        const value =
            Number(exposure);


        if (
            !Number.isFinite(value)
            ||
            value <= 0
        ) {

            setError(
                (
                    "Exposure must be a "
                    + "positive number."
                )
            );

            return;

        }


        setLoading(true);
        setError(null);


        try {

            await setCameraExposure(
                value
            );

            await refreshStatus();

        } catch (err) {

            const message =
                err instanceof Error
                    ? err.message
                    : "Unable to set exposure";


            setError(message);

        } finally {

            setLoading(false);

        }

    }


    // =========================================================
    // Gain
    // =========================================================

    async function handleGain() {

        if (
            loading
            ||
            !status.connected
        ) {
            return;
        }


        const value =
            Number(gain);


        if (
            !Number.isFinite(value)
            ||
            value < 0
        ) {

            setError(
                (
                    "Gain must be a valid "
                    + "non-negative number."
                )
            );

            return;

        }


        setLoading(true);
        setError(null);


        try {

            await setCameraGain(
                value
            );

            await refreshStatus();

        } catch (err) {

            const message =
                err instanceof Error
                    ? err.message
                    : "Unable to set gain";


            setError(message);

        } finally {

            setLoading(false);

        }

    }


    // =========================================================
    // Live view error
    // =========================================================

    function handleStreamError() {

        //
        // Do not continuously recreate the stream here.
        // If FastAPI closes /live because the camera
        // stops, simply remove the image and show an error.
        //
        setStreaming(false);

        setError(
            (
                "Live view connection closed. "
                + "Check the camera and try again."
            )
        );

    }


    // =========================================================
    // Render
    // =========================================================

    return (

        <div
            className="
                flex h-full
                min-h-0 flex-col
                rounded-xl
                border border-slate-800
                bg-slate-950
                p-4
            "
        >

            {/* ==================================================
                Header
            ================================================== */}

            <div
                className="
                    mb-4 flex
                    flex-wrap items-center
                    justify-between gap-3
                "
            >

                <div>

                    <div
                        className="
                            flex items-center
                            gap-2
                        "
                    >

                        <Camera
                            size={20}
                            className="text-slate-300"
                        />

                        <h2
                            className="
                                font-semibold
                                text-slate-100
                            "
                        >
                            ZWO Camera
                        </h2>

                    </div>


                    <div
                        className="
                            mt-1 text-xs
                            text-slate-500
                        "
                    >

                        {
                            status.camera
                                ? (
                                    status.camera.model
                                )
                                : (
                                    "No camera connected"
                                )
                        }

                    </div>

                </div>


                <div
                    className="
                        flex flex-wrap
                        items-center gap-2
                    "
                >

                    {!status.connected ? (

                        <button
                            type="button"
                            disabled={loading}
                            onClick={
                                handleConnect
                            }
                            className="
                                inline-flex
                                min-h-10
                                items-center
                                gap-2
                                rounded-lg
                                border
                                border-slate-700
                                bg-slate-900
                                px-3 py-2
                                text-sm
                                text-slate-200
                                transition
                                hover:bg-slate-800
                                disabled:cursor-not-allowed
                                disabled:opacity-50
                            "
                        >

                            <Plug
                                size={16}
                            />

                            Connect

                        </button>

                    ) : (

                        <button
                            type="button"
                            disabled={loading}
                            onClick={
                                handleDisconnect
                            }
                            className="
                                inline-flex
                                min-h-10
                                items-center
                                gap-2
                                rounded-lg
                                border
                                border-slate-700
                                bg-slate-900
                                px-3 py-2
                                text-sm
                                text-slate-200
                                transition
                                hover:bg-slate-800
                                disabled:cursor-not-allowed
                                disabled:opacity-50
                            "
                        >

                            <PlugZap
                                size={16}
                            />

                            Disconnect

                        </button>

                    )}


                    {!streaming ? (

                        <button
                            type="button"
                            disabled={
                                loading
                                ||
                                !status.connected
                            }
                            onClick={
                                handleStartStream
                            }
                            className="
                                inline-flex
                                min-h-10
                                items-center
                                gap-2
                                rounded-lg
                                border
                                border-slate-700
                                bg-slate-900
                                px-3 py-2
                                text-sm
                                text-slate-200
                                transition
                                hover:bg-slate-800
                                disabled:cursor-not-allowed
                                disabled:opacity-50
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
                            disabled={loading}
                            onClick={
                                handleStopStream
                            }
                            className="
                                inline-flex
                                min-h-10
                                items-center
                                gap-2
                                rounded-lg
                                border
                                border-slate-700
                                bg-slate-900
                                px-3 py-2
                                text-sm
                                text-slate-200
                                transition
                                hover:bg-slate-800
                                disabled:cursor-not-allowed
                                disabled:opacity-50
                            "
                        >

                            <CircleStop
                                size={16}
                            />

                            Stop

                        </button>

                    )}

                </div>

            </div>


            {/* ==================================================
                Camera image
            ================================================== */}

            <div
                className="
                    relative
                    flex min-h-[300px]
                    flex-1
                    items-center
                    justify-center
                    overflow-hidden
                    rounded-lg
                    border border-slate-800
                    bg-black
                "
            >

                {streaming ? (

                    <img
                        key={streamKey}

                        src={
                            getCameraLiveUrl()
                        }

                        alt="ZWO live view"

                        onError={
                            handleStreamError
                        }

                        className="
                            block
                            h-full
                            max-h-full
                            w-full
                            object-contain
                        "
                    />

                ) : (

                    <div
                        className="
                            flex flex-col
                            items-center
                            justify-center
                            gap-2
                            text-center
                            text-slate-500
                        "
                    >

                        <Camera
                            size={36}
                        />

                        <span
                            className="
                                text-sm
                            "
                        >

                            {
                                status.connected
                                    ? (
                                        "Press Live View"
                                    )
                                    : (
                                        "Connect camera to start"
                                    )
                            }

                        </span>

                    </div>

                )}


                {streaming && (

                    <div
                        className="
                            absolute
                            left-3 top-3
                            rounded-md
                            bg-black/60
                            px-2 py-1
                            text-xs
                            text-white
                        "
                    >
                        LIVE
                    </div>

                )}

            </div>


            {/* ==================================================
                Camera status
            ================================================== */}

            <div
                className="
                    mt-4 grid
                    gap-2
                    text-sm
                    sm:grid-cols-2
                    lg:grid-cols-4
                "
            >

                <StatusItem
                    label="Connection"
                    value={
                        status.connected
                            ? "Connected"
                            : "Disconnected"
                    }
                />


                <StatusItem
                    label="Exposure"
                    value={
                        status.exposure !== null
                            ? (
                                `${
                                    Math.round(
                                        status.exposure
                                    )
                                } µs`
                            )
                            : "--"
                    }
                />


                <StatusItem
                    label="Gain"
                    value={
                        status.gain !== null
                            ? (
                                `${
                                    Math.round(
                                        status.gain
                                    )
                                }${
                                    status.gain_unit
                                        ? (
                                            ` ${
                                                status.gain_unit
                                            }`
                                        )
                                        : ""
                                }`
                            )
                            : "--"
                    }
                />


                <StatusItem
                    label="Frame rate"
                    value={
                        status.frame_rate !== null
                        &&
                        status.frame_rate !== undefined
                            ? (
                                `${
                                    status.frame_rate
                                    .toFixed(1)
                                } FPS`
                            )
                            : "--"
                    }
                />

            </div>


            {/* ==================================================
                Camera controls
            ================================================== */}

            <div
                className="
                    mt-4 grid
                    gap-4
                    lg:grid-cols-2
                "
            >

                {/* Exposure */}

                <div
                    className="
                        rounded-lg
                        border border-slate-800
                        bg-slate-900/50
                        p-3
                    "
                >

                    <label
                        htmlFor="camera-exposure"
                        className="
                            mb-2 block
                            text-sm font-medium
                            text-slate-300
                        "
                    >
                        Exposure (µs)
                    </label>


                    <div
                        className="
                            flex gap-2
                        "
                    >

                        <input
                            id="camera-exposure"

                            type="number"

                            min="1"

                            step="1"

                            disabled={
                                !status.connected
                                ||
                                loading
                            }

                            value={
                                exposure
                            }

                            onChange={
                                event =>
                                    setExposure(
                                        event.target.value
                                    )
                            }

                            onKeyDown={
                                event => {

                                    if (
                                        event.key
                                        ===
                                        "Enter"
                                    ) {

                                        handleExposure();

                                    }

                                }
                            }

                            className="
                                min-w-0
                                flex-1
                                rounded-lg
                                border
                                border-slate-700
                                bg-slate-950
                                px-3 py-2
                                text-slate-100
                                outline-none
                                focus:border-slate-500
                                disabled:opacity-50
                            "
                        />


                        <button
                            type="button"

                            disabled={
                                !status.connected
                                ||
                                loading
                            }

                            onClick={
                                handleExposure
                            }

                            className="
                                rounded-lg
                                border
                                border-slate-700
                                bg-slate-800
                                px-4 py-2
                                text-sm
                                text-slate-100
                                hover:bg-slate-700
                                disabled:cursor-not-allowed
                                disabled:opacity-50
                            "
                        >
                            Set
                        </button>

                    </div>

                </div>


                {/* Gain */}

                <div
                    className="
                        rounded-lg
                        border border-slate-800
                        bg-slate-900/50
                        p-3
                    "
                >

                    <label
                        htmlFor="camera-gain"
                        className="
                            mb-2 block
                            text-sm font-medium
                            text-slate-300
                        "
                    >
                        Gain (ASI)
                    </label>


                    <div
                        className="
                            flex gap-2
                        "
                    >

                        <input
                            id="camera-gain"

                            type="number"

                            min="0"

                            step="1"

                            disabled={
                                !status.connected
                                ||
                                loading
                            }

                            value={
                                gain
                            }

                            onChange={
                                event =>
                                    setGain(
                                        event.target.value
                                    )
                            }

                            onKeyDown={
                                event => {

                                    if (
                                        event.key
                                        ===
                                        "Enter"
                                    ) {

                                        handleGain();

                                    }

                                }
                            }

                            className="
                                min-w-0
                                flex-1
                                rounded-lg
                                border
                                border-slate-700
                                bg-slate-950
                                px-3 py-2
                                text-slate-100
                                outline-none
                                focus:border-slate-500
                                disabled:opacity-50
                            "
                        />


                        <button
                            type="button"

                            disabled={
                                !status.connected
                                ||
                                loading
                            }

                            onClick={
                                handleGain
                            }

                            className="
                                rounded-lg
                                border
                                border-slate-700
                                bg-slate-800
                                px-4 py-2
                                text-sm
                                text-slate-100
                                hover:bg-slate-700
                                disabled:cursor-not-allowed
                                disabled:opacity-50
                            "
                        >
                            Set
                        </button>

                    </div>

                </div>

            </div>


            {/* ==================================================
                Error
            ================================================== */}

            {error && (

                <div
                    className="
                        mt-4
                        rounded-lg
                        border
                        border-red-900/60
                        bg-red-950/40
                        px-3 py-2
                        text-sm
                        text-red-300
                    "
                >
                    {error}
                </div>

            )}

        </div>

    );

}


/* =============================================================
   Status item
============================================================= */

interface StatusItemProps {
    label: string;
    value: string;
}


function StatusItem({
    label,
    value,
}: StatusItemProps) {

    return (

        <div
            className="
                rounded-lg
                border border-slate-800
                bg-slate-900/40
                px-3 py-2
            "
        >

            <div
                className="
                    text-xs
                    text-slate-500
                "
            >
                {label}
            </div>


            <div
                className="
                    mt-1
                    truncate
                    text-slate-200
                "
            >
                {value}
            </div>

        </div>

    );

}