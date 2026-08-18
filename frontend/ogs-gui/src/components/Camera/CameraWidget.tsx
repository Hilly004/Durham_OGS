import StatusCard from "../Common/DashboardStatusCard";

export default function CameraWidget() {

    return (
        <StatusCard
            title="Camera"
            status="disconnected"
        >

            {/* Camera feed placeholder */}

            <div className="
                aspect-video
                bg-slate-950
                rounded-lg
                border
                border-slate-700
                flex
                items-center
                justify-center
            ">

                <div className="text-center">

                    <p className="
                        text-slate-500
                        text-4xl
                        mb-2
                    ">
                        
                    </p>

                    <p className="text-slate-400">
                        No camera feed
                    </p>

                    <p className="text-slate-500 text-sm mt-1">
                        Camera not connected
                    </p>

                </div>

            </div>

        </StatusCard>
    );
}