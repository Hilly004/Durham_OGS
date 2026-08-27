import {
    useState,
} from "react";

import CameraControls
    from "../components/Camera/CameraControls";

import CameraStatus
    from "../components/Camera/CameraStatus";

import HomeCameraWidget
    from "../components/Camera/HomeCameraWidget";

import {
    connectCamera,
    disconnectCamera,
} from "../api/camera";

import {
    useObservatoryStatus,
} from "../context/useObservatoryStatus";


export default function CameraPage() {

    const {
        cameraStatus: status,
        refresh,
    } =
        useObservatoryStatus();


    const [loading, setLoading] =
        useState(false);


    async function handleConnection() {

        setLoading(true);

        try {

            if (status?.connected) {
                await disconnectCamera();
            } else {
                await connectCamera();
            }

        } catch (error) {

            console.error(
                "Unable to change camera connection:",
                error
            );

        } finally {

            await refresh();

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

                {/* Title */}
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
                        Allied Vision camera control and acquisition
                    </p>

                </div>


                {/* Connection */}
                <div className="flex items-center gap-3">

                    <button
                        type="button"
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
                    gap-4
                "
            >

                {/* Camera feed */}
                <div
                    className="
                        col-span-7
                        row-span-2
                        min-h-0
                        overflow-hidden
                    "
                >
                    <HomeCameraWidget />
                </div>


                {/* Status */}
                <div
                    className="
                        col-span-5
                        min-h-0
                        overflow-hidden
                    "
                >
                    <CameraStatus />
                </div>


                {/* Controls */}
                <div
                    className="
                        col-span-5
                        min-h-0
                        overflow-hidden
                    "
                >
                    <CameraControls
                        connected={
                            status?.connected ?? false
                        }
                    />
                </div>

            </div>

        </div>
    );
}