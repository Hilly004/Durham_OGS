import {
    useState
} from "react";

import {
    Plus
} from "lucide-react";

import SatelliteTrackingStatusWidget
    from "../components/SatelliteTracking/SatelliteTrackingStatus";

import SatelliteControls
    from "../components/SatelliteTracking/SatelliteControls";

import TLEUpload
    from "../components/SatelliteTracking/TLEUpload";


export default function SatellitePage() {

    const [showTLEUpload, setShowTLEUpload] =
        useState(false);


    return (
        <div className="flex h-full w-full flex-col gap-4 overflow-hidden p-4">

            {/* Header */}
            <div className="flex shrink-0 items-center justify-between">

                <div>
                    <h1 className="text-xl font-semibold text-slate-100">
                        Satellite Tracking
                    </h1>

                    <p className="text-sm text-slate-400">
                        Manage TLEs, predict passes and control satellite tracking
                    </p>
                </div>


                <div className="flex items-center gap-3">

                    <button
                        onClick={() => setShowTLEUpload(true)}
                        className="
                            flex
                            items-center
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
                        "
                    >
                        <Plus size={16} />

                        Add TLE
                    </button>


                    <div
                        className="
                            flex
                            items-center
                            gap-2
                            rounded-lg
                            border
                            border-violet-500/20
                            bg-violet-500/10
                            px-3
                            py-2
                        "
                    >
                        <span className="h-2.5 w-2.5 rounded-full bg-violet-400" />

                        <span className="text-sm font-medium text-violet-300">
                            Tracking System
                        </span>
                    </div>

                </div>

            </div>


            {/* Main Content */}
            <div className="grid min-h-0 flex-1 grid-cols-12 gap-4">

                <div className="col-span-5 min-h-0 overflow-hidden">
                    <SatelliteTrackingStatusWidget />
                </div>

                <div className="col-span-7 min-h-0 overflow-hidden">
                    <SatelliteControls />
                </div>

            </div>


            {/* TLE Modal */}
            {showTLEUpload && (

                <div
                    className="
                        fixed
                        inset-0
                        z-50
                        flex
                        items-center
                        justify-center
                        bg-black/60
                        p-4
                        backdrop-blur-sm
                    "
                    onClick={() => setShowTLEUpload(false)}
                >

                    <div
                        className="
                            w-full
                            max-w-3xl
                        "
                        onClick={(event) => event.stopPropagation()}
                    >
                        <TLEUpload
                            onClose={() => setShowTLEUpload(false)}
                        />
                    </div>

                </div>

            )}

        </div>
    );
}