import {
    useState,
} from "react";

import MountControls
    from "../components/Mount/MountControls";

import MountStatus
    from "../components/Mount/MountStatus";

import HomeCameraWidget
    from "../components/Camera/HomeCameraWidget";

import {
    connectMount,
    disconnectMount,
} from "../api/mount";

import {
    useObservatoryStatus,
} from "../context/useObservatoryStatus";


export default function MountPage() {

    const {
        mountStatus: status,
        refresh,
    } =
        useObservatoryStatus();


    const [loading, setLoading] =
        useState(false);


    async function handleConnection() {

        setLoading(true);

        try {

            if (status?.connected) {
                await disconnectMount();
            } else {
                await connectMount();
            }

        } catch (error) {

            console.error(
                "Unable to change mount connection:",
                error
            );

        } finally {

            /*
             * Ask the central status provider
             * to immediately refresh after a
             * connection change.
             */
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
                        Mount Control
                    </h1>

                    <p
                        className="
                            text-sm
                            text-slate-400
                        "
                    >
                        Telescope mount control and positioning
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

                {/* Status */}
                <div
                    className="
                        col-span-5
                        min-h-0
                        overflow-hidden
                    "
                >
                    <MountStatus />
                </div>


                {/* Controls */}
                <div
                    className="
                        col-span-7
                        row-span-2
                        min-h-0
                        overflow-hidden
                    "
                >

                    <MountControls
                        connected={
                            status?.connected
                            ?? false
                        }
                    />

                </div>


                {/* Camera */}
                <div
                    className="
                        col-span-5
                        min-h-0
                        overflow-hidden
                    "
                >
                    <HomeCameraWidget />
                </div>

            </div>

        </div>
    );
}