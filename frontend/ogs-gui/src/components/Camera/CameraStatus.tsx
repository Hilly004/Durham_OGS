import {
    useEffect,
    useState,
} from "react";

import {
    getCameraStatus,
} from "../../api/camera";

import type {
    CameraStatusData,
} from "../../api/camera";

import DashboardStatusCard
    from "../Common/DashboardStatusCard";

import DashboardStatusRow
    from "../Common/DashboardStatusRow";


export default function CameraStatus() {

    const [status, setStatus] =
        useState<CameraStatusData | null>(
            null
        );


    useEffect(() => {

        async function update() {

            try {

                const result =
                    await getCameraStatus();

                setStatus(result);

            } catch (error) {

                console.error(
                    "Unable to retrieve camera status:",
                    error
                );

                setStatus(null);

            }

        }


        update();

        const interval = setInterval(
            update,
            3000
        );


        return () => {
            clearInterval(interval);
        };

    }, []);


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