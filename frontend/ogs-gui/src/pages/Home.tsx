import MountStatusWidget from "../components/Mount/MountStatus";
import DomeStatusWidget from "../components/Dome/DomeStatus";
import WeatherStatusWidget from "../components/Weather/WeatherStatus";
import CameraWidget from "../components/Camera/CameraWidget";
import ActivityLog from "../components/Activity/ActivityWidget";

export default function Home() {
    return (
        <div className="w-full h-full p-4">

            {/* Header */}

            <div className="
                flex
                items-center
                justify-between
                mb-4
            ">

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
                        Observatory Safe
                    </span>

                </div>

            </div>


            {/* Main dashboard */}

            <div className="
                grid
                grid-cols-4
                grid-rows-[1fr_auto]
                gap-4
                h-[calc(100vh-100px)]
            ">


                {/* LEFT SIDE */}

                <div className="
                    col-span-2
                    grid
                    grid-rows-[1fr_auto]
                    gap-4
                    min-h-0
                ">


                    {/* Mount */}

                    <MountStatusWidget />


                    {/* Dome + Weather */}

                    <div className="
                        grid
                        grid-cols-2
                        gap-4
                    ">

                        <DomeStatusWidget />

                        <WeatherStatusWidget />

                    </div>

                </div>


                {/* RIGHT SIDE */}

                <div className="
                    col-span-2
                    grid
                    grid-rows-[1fr_200px]
                    gap-4
                    min-h-0
                ">


                    {/* Camera */}

                    <div className="min-h-0">
                        <CameraWidget />
                    </div>


                    {/* Activity */}

                    <div className="
                        min-h-0
                        overflow-hidden
                    ">
                        <ActivityLog />
                    </div>

                </div>

            </div>

        </div>
    );
}