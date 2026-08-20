import {
    useCallback,
    useEffect,
    useRef,
    useState,
} from "react";

import {
    Camera,
    CircleStop,
    Play,
    Plug,
    PlugZap,
    RefreshCw,
} from "lucide-react";

import StatusCard
    from "../Common/DashboardStatusCard";

import {
    connectCamera,
    disconnectCamera,
    getCameraStatus,
    setCameraExposure,
    setCameraGain,
    startCameraStream,
    stopCameraStream,
} from "../../api/camera";

import type {
    CameraStatusData,
} from "../../api/camera";


interface CameraWidgetProps {
    onStatusChange?: (
        status: CameraStatusData
    ) => void;
}


export default function CameraWidget({
    onStatusChange,
}: CameraWidgetProps) {

    const [
        status,
        setStatus,
    ] = useState<CameraStatusData>({
        connected: false,
        streaming: false,
        camera: null,
        exposure: null,
        gain: null,
        frame_count: 0,
    });


    const [
        exposure,
        setExposure,
    ] = useState("");


    const [
        gain,
        setGain,
    ] = useState("");


    const [
        loading,
        setLoading,
    ] = useState(false);


    const [
        error,
        setError,
    ] = useState<string | null>(
        null
    );


    /*
     * Used to force the browser to request
     * the newest frame.
     */
    const [
        frameVersion,
        setFrameVersion,
    ] = useState(0);


    /*
     * Prevent overlapping image refresh timers.
     */
    const frameTimer =
        useRef<number | null>(
            null
        );


    const refreshStatus =
        useCallback(async () => {

            try {

                const currentStatus =
                    await getCameraStatus();

                setStatus(
                    currentStatus
                );

                onStatusChange?.(
                    currentStatus
                );


                /*
                 * Don't overwrite a field while
                 * the user is typing unless its
                 * current value is blank.
                 */
                if (
                    currentStatus.exposure !==
                        null
                ) {

                    setExposure(
                        String(
                            currentStatus.exposure
                        )
                    );
                }


                if (
                    currentStatus.gain !==
                        null
                ) {

                    setGain(
                        String(
                            currentStatus.gain
                        )
                    );
                }


                setError(null);

            } catch (err) {

                console.error(
                    "Unable to get camera status:",
                    err
                );

            }

        }, [onStatusChange]);


    /*
     * Poll camera state.
     */
    useEffect(() => {

        refreshStatus();

        const timer =
            window.setInterval(
                refreshStatus,
                2000
            );


        return () => {
            window.clearInterval(
                timer
            );
        };

    }, [refreshStatus]);


    /*
     * Refresh image while streaming.
     *
     * 200 ms = about 5 browser updates
     * per second.
     *
     * The camera itself can continue
     * acquiring faster than this.
     */
    useEffect(() => {

        if (
            !status.connected ||
            !status.streaming
        ) {

            if (
                frameTimer.current !== null
            ) {

                window.clearInterval(
                    frameTimer.current
                );

                frameTimer.current = null;
            }

            return;
        }


        frameTimer.current =
            window.setInterval(
                () => {

                    setFrameVersion(
                        current =>
                            current + 1
                    );

                },
                200
            );


        return () => {

            if (
                frameTimer.current !== null
            ) {

                window.clearInterval(
                    frameTimer.current
                );

                frameTimer.current =
                    null;
            }

        };

    }, [
        status.connected,
        status.streaming,
    ]);


    async function handleConnect() {

        if (loading) {
            return;
        }


        setLoading(true);
        setError(null);


        try {

            await connectCamera();

            await refreshStatus();

            /*
             * Retrieve the first still image
             * after connection.
             */
            setFrameVersion(
                current =>
                    current + 1
            );

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


    async function handleDisconnect() {

        if (loading) {
            return;
        }


        setLoading(true);
        setError(null);


        try {

            /*
             * The backend should stop the
             * stream during disconnect too,
             * but explicitly stopping it here
             * gives the UI cleaner state.
             */
            if (status.streaming) {

                try {
                    await stopCameraStream();
                } catch {
                    // Disconnect anyway
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


    async function handleStartStream() {

        if (
            loading ||
            !status.connected
        ) {
            return;
        }


        setLoading(true);
        setError(null);


        try {

            await startCameraStream();

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


    async function handleStopStream() {

        if (
            loading ||
            !status.connected
        ) {
            return;
        }


        setLoading(true);
        setError(null);


        try {

            await stopCameraStream();

            await refreshStatus();

            /*
             * Refresh once more after stopping
             * so the final acquired frame stays
             * visible.
             */
            setFrameVersion(
                current =>
                    current + 1
            );

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


    async function handleExposure() {

        if (!status.connected) {
            return;
        }


        const value =
            Number(exposure);


        if (
            !Number.isFinite(value) ||
            value <= 0
        ) {

            setError(
                "Exposure must be a valid positive number."
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


    async function handleGain() {

        if (!status.connected) {
            return;
        }


        const value =
            Number(gain);


        if (!Number.isFinite(value)) {

            setError(
                "Gain must be a valid number."
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


    function handleSingleFrame() {

        if (
            !status.connected ||
            status.streaming
        ) {
            return;
        }


        setFrameVersion(
            current =>
                current + 1
        );
    }


    /*
     * Query parameter prevents browser caching.
     */
    const frameUrl =
        `/api/camera/frame?v=${frameVersion}`;


    return (
        <StatusCard
            title="Allied Vision Camera"
            connected={status.connected}
        >

            <div
                className="
                    grid
                    h-full
                    min-h-0
                    grid-cols-1
                    gap-4
                    xl:grid-cols-[minmax(0,1fr)_300px]
                "
            >

                {/* =====================================================
                    Camera image
                ===================================================== */}

                <div
                    className="
                        flex
                        min-h-0
                        flex-col
                    "
                >

                    <div
                        className="
                            relative
                            flex
                            h-[600px]
                            w-[800px]
                            items-center
                            justify-center
                            overflow-hidden
                            rounded-lg
                            border
                            border-slate-800
                            bg-black
                        "
                    >

                        {status.connected ? (

                            <img
                                key={frameVersion}
                                src={frameUrl}
                                alt="Mako camera feed"

                                className="
                                    max-h-full
                                    max-w-full
                                    object-contain
                                "

                                onError={(event) => {

                                    /*
                                     * Hide broken image icon while
                                     * waiting for first stream frame.
                                     */
                                    event.currentTarget.style.visibility =
                                        "hidden";

                                }}

                                onLoad={(event) => {

                                    event.currentTarget.style.visibility =
                                        "visible";

                                }}
                            />

                        ) : (

                            <div
                                className="
                                    text-center
                                "
                            >

                                <Camera
                                    size={48}
                                    className="
                                        mx-auto
                                        mb-3
                                        text-slate-700
                                    "
                                />

                                <p
                                    className="
                                        text-sm
                                        text-slate-400
                                    "
                                >
                                    No camera feed
                                </p>

                                <p
                                    className="
                                        mt-1
                                        text-xs
                                        text-slate-600
                                    "
                                >
                                    Camera not connected
                                </p>

                            </div>

                        )}


                        {status.streaming && (

                            <div
                                className="
                                    absolute
                                    left-3
                                    top-3
                                    flex
                                    items-center
                                    gap-2
                                    rounded-md
                                    bg-slate-950/80
                                    px-2.5
                                    py-1.5
                                    backdrop-blur
                                "
                            >

                                <span
                                    className="
                                        h-2
                                        w-2
                                        animate-pulse
                                        rounded-full
                                        bg-red-500
                                    "
                                />

                                <span
                                    className="
                                        text-xs
                                        font-medium
                                        text-slate-200
                                    "
                                >
                                    LIVE
                                </span>

                            </div>

                        )}

                    </div>


                    <div
                        className="
                            mt-3
                            flex
                            items-center
                            justify-between
                            gap-3
                            text-xs
                            text-slate-500
                        "
                    >

                        <span>
                            {status.streaming
                                ? "Live acquisition"
                                : status.connected
                                    ? "Single frame mode"
                                    : "Offline"}
                        </span>

                        <span>
                            Frames: {
                                status.frame_count
                            }
                        </span>

                    </div>

                </div>


                {/* =====================================================
                    Controls
                ===================================================== */}

                <div
                    className="
                        flex
                        min-h-0
                        flex-col
                        gap-4
                        overflow-y-auto
                    "
                >

                    {/* Connection */}

                    <div
                        className="
                            rounded-lg
                            border
                            border-slate-800
                            bg-slate-950/40
                            p-4
                        "
                    >

                        <h3
                            className="
                                mb-3
                                text-sm
                                font-semibold
                                text-slate-200
                            "
                        >
                            Connection
                        </h3>


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
                                    handleConnect
                                }

                                disabled={
                                    loading ||
                                    status.connected
                                }

                                className="
                                    flex
                                    items-center
                                    justify-center
                                    gap-2
                                    rounded-lg
                                    bg-emerald-600
                                    px-3
                                    py-2
                                    text-sm
                                    font-medium
                                    text-white
                                    transition
                                    hover:bg-emerald-500
                                    disabled:cursor-not-allowed
                                    disabled:opacity-40
                                "
                            >

                                <PlugZap
                                    size={16}
                                />

                                Connect

                            </button>


                            <button
                                type="button"
                                onClick={
                                    handleDisconnect
                                }

                                disabled={
                                    loading ||
                                    !status.connected
                                }

                                className="
                                    flex
                                    items-center
                                    justify-center
                                    gap-2
                                    rounded-lg
                                    bg-slate-800
                                    px-3
                                    py-2
                                    text-sm
                                    font-medium
                                    text-slate-200
                                    transition
                                    hover:bg-slate-700
                                    disabled:cursor-not-allowed
                                    disabled:opacity-40
                                "
                            >

                                <Plug
                                    size={16}
                                />

                                Disconnect

                            </button>

                        </div>

                    </div>


                    {/* Live view */}

                    <div
                        className="
                            rounded-lg
                            border
                            border-slate-800
                            bg-slate-950/40
                            p-4
                        "
                    >

                        <h3
                            className="
                                mb-3
                                text-sm
                                font-semibold
                                text-slate-200
                            "
                        >
                            Acquisition
                        </h3>


                        <div
                            className="
                                grid
                                grid-cols-2
                                gap-2
                            "
                        >

                            {!status.streaming ? (

                                <button
                                    type="button"

                                    onClick={
                                        handleStartStream
                                    }

                                    disabled={
                                        loading ||
                                        !status.connected
                                    }

                                    className="
                                        flex
                                        items-center
                                        justify-center
                                        gap-2
                                        rounded-lg
                                        bg-violet-600
                                        px-3
                                        py-2
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
                                        py-2
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

                                    Stop

                                </button>

                            )}


                            <button
                                type="button"

                                onClick={
                                    handleSingleFrame
                                }

                                disabled={
                                    loading ||
                                    !status.connected ||
                                    status.streaming
                                }

                                className="
                                    flex
                                    items-center
                                    justify-center
                                    gap-2
                                    rounded-lg
                                    bg-slate-800
                                    px-3
                                    py-2
                                    text-sm
                                    font-medium
                                    text-slate-200
                                    transition
                                    hover:bg-slate-700
                                    disabled:cursor-not-allowed
                                    disabled:opacity-40
                                "
                            >

                                <RefreshCw
                                    size={16}
                                />

                                Capture

                            </button>

                        </div>

                    </div>


                    {/* Exposure */}

                    <div
                        className="
                            rounded-lg
                            border
                            border-slate-800
                            bg-slate-950/40
                            p-4
                        "
                    >

                        <label
                            className="
                                mb-2
                                block
                                text-xs
                                font-medium
                                uppercase
                                tracking-wide
                                text-slate-500
                            "
                        >
                            Exposure
                        </label>


                        <div
                            className="
                                flex
                                gap-2
                            "
                        >

                            <div
                                className="
                                    relative
                                    flex-1
                                "
                            >

                                <input
                                    type="number"

                                    value={exposure}

                                    onChange={
                                        event =>
                                            setExposure(
                                                event.target.value
                                            )
                                    }

                                    disabled={
                                        !status.connected
                                    }

                                    className="
                                        w-full
                                        rounded-lg
                                        border
                                        border-slate-700
                                        bg-slate-950
                                        px-3
                                        py-2
                                        pr-10
                                        text-sm
                                        text-slate-200
                                        outline-none
                                        focus:border-violet-500
                                        disabled:opacity-50
                                    "
                                />

                                <span
                                    className="
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

                                onClick={
                                    handleExposure
                                }

                                disabled={
                                    loading ||
                                    !status.connected
                                }

                                className="
                                    rounded-lg
                                    bg-slate-800
                                    px-3
                                    py-2
                                    text-sm
                                    text-slate-200
                                    hover:bg-slate-700
                                    disabled:opacity-40
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
                            border
                            border-slate-800
                            bg-slate-950/40
                            p-4
                        "
                    >

                        <label
                            className="
                                mb-2
                                block
                                text-xs
                                font-medium
                                uppercase
                                tracking-wide
                                text-slate-500
                            "
                        >
                            Gain
                        </label>


                        <div
                            className="
                                flex
                                gap-2
                            "
                        >

                            <div
                                className="
                                    relative
                                    flex-1
                                "
                            >

                                <input
                                    type="number"

                                    step="0.1"

                                    value={gain}

                                    onChange={
                                        event =>
                                            setGain(
                                                event.target.value
                                            )
                                    }

                                    disabled={
                                        !status.connected
                                    }

                                    className="
                                        w-full
                                        rounded-lg
                                        border
                                        border-slate-700
                                        bg-slate-950
                                        px-3
                                        py-2
                                        pr-10
                                        text-sm
                                        text-slate-200
                                        outline-none
                                        focus:border-violet-500
                                        disabled:opacity-50
                                    "
                                />

                                <span
                                    className="
                                        absolute
                                        right-3
                                        top-1/2
                                        -translate-y-1/2
                                        text-xs
                                        text-slate-500
                                    "
                                >
                                    dB
                                </span>

                            </div>


                            <button
                                type="button"

                                onClick={
                                    handleGain
                                }

                                disabled={
                                    loading ||
                                    !status.connected
                                }

                                className="
                                    rounded-lg
                                    bg-slate-800
                                    px-3
                                    py-2
                                    text-sm
                                    text-slate-200
                                    hover:bg-slate-700
                                    disabled:opacity-40
                                "
                            >
                                Set
                            </button>

                        </div>

                    </div>


                    {/* Camera information */}

                    <div
                        className="
                            rounded-lg
                            border
                            border-slate-800
                            bg-slate-950/40
                            p-4
                        "
                    >

                        <h3
                            className="
                                mb-3
                                text-sm
                                font-semibold
                                text-slate-200
                            "
                        >
                            Camera
                        </h3>


                        <div
                            className="
                                space-y-2
                                text-xs
                            "
                        >

                            <InfoRow
                                label="Model"
                                value={
                                    status.camera
                                        ?.model ??
                                    "—"
                                }
                            />

                            <InfoRow
                                label="Serial"
                                value={
                                    status.camera
                                        ?.serial ??
                                    "—"
                                }
                            />

                            <InfoRow
                                label="Device ID"
                                value={
                                    status.camera
                                        ?.id ??
                                    "—"
                                }
                            />

                        </div>

                    </div>


                    {error && (

                        <div
                            className="
                                rounded-lg
                                border
                                border-red-900/60
                                bg-red-950/40
                                px-3
                                py-2
                                text-xs
                                text-red-300
                            "
                        >
                            {error}
                        </div>

                    )}

                </div>

            </div>

        </StatusCard>
    );
}


function InfoRow({
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
                items-start
                justify-between
                gap-4
            "
        >

            <span
                className="
                    text-slate-500
                "
            >
                {label}
            </span>

            <span
                className="
                    break-all
                    text-right
                    text-slate-300
                "
            >
                {value}
            </span>

        </div>
    );
}