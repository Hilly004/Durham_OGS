import StatusCard from "../Common/StatusCard";

export default function ActivityLog() {

    return (
        <StatusCard
            title="Activity"
            status="safe"
        >

            <div className="h-full flex flex-col">

                <h2 className="text-lg font-bold mb-3">
                Activity
                </h2>

                <div className="
                    flex-1
                    overflow-y-auto
                    space-y-2
                ">

                {/* log entries */}

                </div>

            </div>

        </StatusCard>
    );
}