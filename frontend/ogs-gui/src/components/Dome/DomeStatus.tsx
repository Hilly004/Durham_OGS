import { useEffect, useState } from "react";

import {
    getDomeStatus,
    connectDome,
    disconnectDome,
} from "../../api/dome";

import type { DomeStatusData } from "../../api/dome";

export default function DomeStatus() {

    const [status, setStatus] = useState<DomeStatusData | null>(null);

    useEffect(() => {

        const update = () => {
            getDomeStatus()
                .then(setStatus)
                .catch(console.error);
        };

        update();

        const timer = setInterval(update, 1000);

        return () => clearInterval(timer);

    }, []);

    async function handleConnect() {
        await connectDome();
    }

    async function handleDisconnect() {
        await disconnectDome();
    }

    if (!status) {
        return (
            <div className="bg-slate-800 rounded-xl p-6 border border-slate-700">
                <h2 className="text-xl font-bold mb-4">
                    Dome Status
                </h2>

                <p className="text-red-400">
                    Not connected
                </p>

                <button
                    onClick={handleConnect}
                    className="mt-4 px-4 py-2 rounded bg-blue-600 hover:bg-blue-700 text-white"
                >
                    Connect
                </button>
            </div>
        );
    }

    return (
        <div className="bg-slate-800 rounded-xl p-6 border border-slate-700">

            <h2 className="text-xl font-bold mb-4">
                Dome Status
            </h2>

            <p>
                Connected: {status.connected ? "Yes" : "No"}
            </p>

            <p>
                Open: {status.isOpen ? "Yes" : "No"}
            </p>

            <button
                onClick={
                    status.connected
                        ? handleDisconnect
                        : handleConnect
                }
            >
                {status.connected ? "Disconnect" : "Connect"}
            </button>

        </div>
    );
}