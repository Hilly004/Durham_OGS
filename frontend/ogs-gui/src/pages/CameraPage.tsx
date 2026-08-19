import {
    useState,
} from "react";

import CameraWidget
    from "../components/Camera/CameraWidget";

import type {
    CameraStatusData,
} from "../api/camera";


export default function CameraPage() {

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
                        Camera Control
                    </h1>

                    <p
                        className="
                            text-sm
                            text-slate-400
                        "
                    >

                        {status.camera
                            ? `${status.camera.name} · ${status.camera.serial}`
                            : "Imaging camera control and acquisition"}

                    </p>

                </div>


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
                                status.streaming
                                    ? "animate-pulse bg-red-500"
                                    : status.connected
                                        ? "bg-green-500"
                                        : "bg-red-500"
                            }
                        `}
                    />


                    <span
                        className="
                            text-sm
                            text-slate-300
                        "
                    >

                        {status.streaming
                            ? "Live"
                            : status.connected
                                ? "Connected"
                                : "Disconnected"}

                    </span>

                </div>

            </div>


            {/* Camera */}

            <div
                className="
                    min-h-0
                    flex-1
                    overflow-hidden
                "
            >

                <CameraWidget
                    onStatusChange={
                        setStatus
                    }
                />

            </div>

        </div>
    );
}