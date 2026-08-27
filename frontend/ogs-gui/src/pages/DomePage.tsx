import {
    useState,
} from "react";

import DomeControls from "../components/Dome/DomeControls";
import DomeStatus from "../components/Dome/DomeStatus";

import {
    connectDome,
    disconnectDome,
} from "../api/dome";

import {
    useObservatoryStatus,
} from "../context/useObservatoryStatus";


export default function DomePage() {

    const {
        domeStatus: status,
        refresh,
    } =
        useObservatoryStatus();


    const [loading, setLoading] =
        useState(false);


    async function handleConnection() {

        setLoading(true);

        try {

            if (status?.connected) {
                await disconnectDome();
            } else {
                await connectDome();
            }

        } catch (error) {

            console.error(
                "Unable to change dome connection:",
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

                <div>

                    <h1
                        className="
                            text-xl
                            font-semibold
                            text-slate-100
                        "
                    >
                        Dome Control
                    </h1>

                    <p className="text-sm text-slate-400">
                        AstroHaven enclosure control and monitoring
                    </p>

                </div>


                <div className="flex items-center gap-3">

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

                <div
                    className="
                        col-span-5
                        min-h-0
                        overflow-hidden
                    "
                >
                    <DomeStatus />
                </div>


                <div
                    className="
                        col-span-7
                        min-h-0
                        overflow-hidden
                    "
                >
                    <DomeControls />
                </div>

            </div>

        </div>
    );
}