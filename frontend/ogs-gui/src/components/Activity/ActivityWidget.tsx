import StatusCard from "../Common/StatusCard";

export default function ActivityLog() {

    return (
        <StatusCard
            title="Activity"
            status="safe"
        >

            <div className="space-y-4">

                <div className="flex gap-4">

                    <span className="text-slate-500 text-sm">
                        14:42:31
                    </span>

                    <p className="text-slate-300">
                        Mount connected
                    </p>

                </div>


                <div className="flex gap-4">

                    <span className="text-slate-500 text-sm">
                        14:41:18
                    </span>

                    <p className="text-slate-300">
                        Weather conditions safe
                    </p>

                </div>


                <div className="flex gap-4">

                    <span className="text-slate-500 text-sm">
                        14:40:52
                    </span>

                    <p className="text-slate-300">
                        Dome position updated
                    </p>

                </div>


                <div className="flex gap-4">

                    <span className="text-slate-500 text-sm">
                        14:39:44
                    </span>

                    <p className="text-slate-300">
                        Observatory started
                    </p>

                </div>

            </div>

        </StatusCard>
    );
}