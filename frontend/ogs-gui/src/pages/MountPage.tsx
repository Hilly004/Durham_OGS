import MountControls from "../components/Mount/MountControls";
import MountStatus from "../components/Mount/MountStatus";


export default function Mount() {
    return (
        <div className="w-full h-full p-4">

            {/* Header */}

            <div className="
                flex
                items-center
                justify-between
                mb-4
            ">

                <div>
                    <h1 className="
                        text-xl
                        font-semibold
                        text-slate-100
                    ">
                        Mount
                    </h1>

                    <p className="
                        text-sm
                        text-slate-400
                    ">
                        Telescope mount control and status
                    </p>
                </div>


                {/* Connection status */}

                <div className="
                    flex
                    items-center
                    gap-2
                    px-3
                    py-2
                    rounded-lg
                    bg-slate-800
                    border
                    border-slate-700
                ">

                    <span className="
                        w-2.5
                        h-2.5
                        rounded-full
                        bg-green-500
                    "/>

                    <span className="
                        text-sm
                        text-green-400
                        font-medium
                    ">
                        Connected
                    </span>

                </div>

            </div>


            {/* Main content */}

            <div className="
                grid
                grid-cols-2
                gap-4
                h-[calc(100vh-100px)]
            ">

                {/* Mount status */}

                <div className="min-h-0">
                    <MountStatus />
                </div>


                {/* Mount controls */}

                <div className="min-h-0">
                    <MountControls />
                </div>

            </div>

        </div>
    );
}