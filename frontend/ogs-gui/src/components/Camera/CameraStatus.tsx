import {
    useObservatoryStatus,
} from "../../context/ObservatoryStatusContext";

import DashboardStatusCard
    from "../Common/DashboardStatusCard";

import DashboardStatusRow
    from "../Common/DashboardStatusRow";


export default function CameraStatus() {

    const {
        cameraStatus: status,
    } =
        useObservatoryStatus();


    return (
        <DashboardStatusCard
            title="Camera"
            connected={
                status?.connected ?? false
            }
        >

            <div className="space-y-1">

                <DashboardStatusRow
                    label="Model"
                    value={
                        status?.camera?.model
                        ?? "--"
                    }
                />

                <DashboardStatusRow
                    label="Serial"
                    value={
                        status?.camera?.serial
                        ?? "--"
                    }
                />

                <DashboardStatusRow
                    label="Device ID"
                    value={
                        status?.camera?.id
                        ?? "--"
                    }
                />

                <DashboardStatusRow
                    label="Mode"
                    value={
                        status?.streaming
                            ? "Live"
                            : "Idle"
                    }
                />

                <DashboardStatusRow
                    label="Exposure"
                    value={
                        status?.exposure !== null
                        && status?.exposure !== undefined
                            ? `${status.exposure.toFixed(0)} µs`
                            : "--"
                    }
                />

                <DashboardStatusRow
                    label="Gain"
                    value={
                        status?.gain !== null
                        && status?.gain !== undefined
                            ? `${status.gain.toFixed(1)} dB`
                            : "--"
                    }
                />

                <DashboardStatusRow
                    label="Frames"
                    value={
                        String(
                            status?.frame_count ?? 0
                        )
                    }
                />

            </div>

        </DashboardStatusCard>
    );
}