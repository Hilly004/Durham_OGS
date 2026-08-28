import {
    useEffect,
    useState,
} from "react";

import {
    Camera,
} from "lucide-react";

import StatusCard
    from "../Common/DashboardStatusCard";

import {
    useObservatoryStatus,
} from "../../context/useObservatoryStatus";


export default function HomeCameraWidget() {

    const {
        cameraStatus,
    } =
        useObservatoryStatus();


    const status =
        cameraStatus ?? {
            connected: false,
            streaming: false,
            camera: null,
            exposure: null,
            gain: null,
            frame_count: 0,
        };


    const [
        frameVersion,
        setFrameVersion,
    ] = useState(0);


    const [
        streamVersion,
        setStreamVersion,
    ] = useState(0);


    /*
     * Refresh displayed image while
     * live acquisition is running.
     *
     * A unique streamVersion prevents
     * the browser reusing frames from
     * an earlier camera session.
     *
     * 200 ms = approximately 5 FPS
     * on the dashboard.
     */
    useEffect(() => {

        if (
            !status.connected
            ||
            !status.streaming
        ) {

            setFrameVersion(0);

            return;
        }


        setStreamVersion(
            Date.now()
        );

        setFrameVersion(0);


        const timer =
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

            window.clearInterval(
                timer
            );

        };

    }, [
        status.connected,
        status.streaming,
    ]);


    const frameUrl =
        (
            "/api/camera/frame"
            +
            `?session=${streamVersion}`
            +
            `&frame=${frameVersion}`
        );


    return (
        <StatusCard
            title="Camera"
            connected={status.connected}
        >

            <div
                className="
                    flex
                    h-full
                    min-h-0
                    flex-col
                    gap-3
                "
            >

                {/* Camera image */}

                <div
                    className="
                        relative
                        flex
                        h-[600px]
                        items-center
                        justify-center
                        overflow-hidden
                        rounded-lg
                        border
                        border-slate-700
                        bg-black
                    "
                >

                    {
                        status.connected
                        &&
                        status.streaming
                            ? (

                                <img
                                    key={
                                        `${streamVersion}-${frameVersion}`
                                    }

                                    src={
                                        frameUrl
                                    }

                                    alt="Camera live view"

                                    className="
                                        h-full
                                        w-full
                                        object-contain
                                    "
                                />

                            )
                            : (

                                <div
                                    className="
                                        text-center
                                    "
                                >

                                    <Camera
                                        size={42}

                                        className="
                                            mx-auto
                                            mb-2
                                            text-slate-700
                                        "
                                    />

                                    <p
                                        className="
                                            text-sm
                                            text-slate-400
                                        "
                                    >
                                        {
                                            status.connected
                                                ? "Live view not running"
                                                : "Camera not connected"
                                        }
                                    </p>

                                </div>

                            )
                    }


                    {/* Live indicator */}

                    {
                        status.connected
                        &&
                        status.streaming
                        &&
                        (

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

                        )
                    }

                </div>


                {/* Status */}

                <div
                    className="
                        flex
                        shrink-0
                        items-center
                        justify-between
                        gap-4
                    "
                >

                </div>

            </div>

        </StatusCard>
    );
}