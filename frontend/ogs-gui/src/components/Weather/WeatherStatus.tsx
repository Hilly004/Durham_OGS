import {
    useObservatoryStatus,
} from "../../context/useObservatoryStatus";

import DashboardStatusCard
    from "../Common/DashboardStatusCard";

import DashboardStatusRow
    from "../Common/DashboardStatusRow";


export default function WeatherStatusWidget() {

    const {
        weatherStatus: status,
    } =
        useObservatoryStatus();


    const conditions =
        !status
            ? "Unknown"
            : status.state.toUpperCase();


    const override =
        status?.override === true
            ? "Force Safe"
            : status?.override === false
                ? "Force Unsafe"
                : "Auto";


    return (
        <DashboardStatusCard
            title="Weather"
            connected={
                status?.connected ?? false
            }
        >

            <div className="space-y-1">

                <DashboardStatusRow
                    label="Conditions"
                    value={conditions}
                    valueClassName={
                        status?.state === "safe"
                            ? "text-green-400"
                            : status?.state === "unsafe"
                                ? "text-red-400"
                                : "text-slate-400"
                    }
                />


                <DashboardStatusRow
                    label="Actual"
                    value={
                        status
                            ? status.actualSafe
                                ? "SAFE"
                                : "UNSAFE"
                            : "--"
                    }
                    valueClassName={
                        status?.actualSafe
                            ? "text-green-400"
                            : "text-red-400"
                    }
                />


                <DashboardStatusRow
                    label="Override"
                    value={override}
                    valueClassName={
                        status?.override !== null &&
                        status?.override !== undefined
                            ? "text-amber-400"
                            : "text-slate-300"
                    }
                />


                <DashboardStatusRow
                    label="Reason"
                    value={
                        status?.reason ??
                        "No restrictions"
                    }
                />

            </div>

        </DashboardStatusCard>
    );
}