import {
    useEffect,
    useState,
} from "react";

import {
    getDomeStatus,
} from "../../api/dome";

import type {
    DomeStatusData,
} from "../../api/dome";

import DashboardStatusCard
    from "../Common/DashboardStatusCard";

import DashboardStatusRow
    from "../Common/DashboardStatusRow";


export default function DomeStatusWidget() {

    const [status, setStatus] =
        useState<DomeStatusData | null>(null);


    useEffect(() => {

        async function update() {

            try {

                const domeStatus =
                    await getDomeStatus();

                setStatus(domeStatus);

            } catch (error) {

                console.error(
                    "Unable to retrieve dome status:",
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


    const domeState =
        !status?.connected
            ? "--"
            : status.fault
                ? "Fault"
                : status.moving
                    ? "Moving"
                    : status.isOpen
                        ? "Open"
                        : "Closed";


    return (
        <DashboardStatusCard
            title="Dome"
            connected={
                status?.connected ?? false
            }
        >

            <div className="space-y-1">

                <DashboardStatusRow
                    label="State"
                    value={domeState}
                    valueClassName={
                        status?.fault
                            ? "text-red-400"
                            : status?.moving
                                ? "text-amber-400"
                                : "text-slate-300"
                    }
                />

                <DashboardStatusRow
                    label="Open"
                    value={
                        status?.connected
                            ? status.isOpen
                                ? "Yes"
                                : "No"
                            : "--"
                    }
                />

                <DashboardStatusRow
                    label="Moving"
                    value={
                        status?.connected
                            ? status.moving
                                ? "Yes"
                                : "No"
                            : "--"
                    }
                    valueClassName={
                        status?.moving
                            ? "text-amber-400"
                            : "text-slate-300"
                    }
                />

                <DashboardStatusRow
                    label="Fault"
                    value={
                        status?.connected
                            ? status.fault
                                ? "Detected"
                                : "None"
                            : "--"
                    }
                    valueClassName={
                        status?.fault
                            ? "text-red-400"
                            : "text-slate-300"
                    }
                />

            </div>

        </DashboardStatusCard>
    );
}