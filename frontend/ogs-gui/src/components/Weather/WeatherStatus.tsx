import { useEffect, useState } from "react";

import {
    connectWeather,
    disconnectWeather,
    getWeatherStatus,
} from "../../api/weather";

import type {
    WeatherStatusData,
} from "../../api/weather";

import StatusCard from "../Common/StatusCard";


export default function WeatherStatusWidget() {

    const [status, setStatus] = useState<WeatherStatusData>({
    connected: false,
    safe: false,
    state: "unknown",
    reason: null
});

    // --------------------------------------------------
    // Update weather information
    // --------------------------------------------------

    useEffect(() => {

        const update = async () => {

            try {

                const weatherStatus =
                    await getWeatherStatus();

                setStatus(weatherStatus);


            } catch (error) {

                console.error(error);

            }

        };


        update();

        const timer =
            setInterval(update, 100000);

        return () =>
            clearInterval(timer);

    }, []);


    // --------------------------------------------------
    // Connect
    // --------------------------------------------------

    async function handleConnect() {

    try {

        await connectWeather();

        const weatherStatus =
            await getWeatherStatus();

        setStatus(weatherStatus);

    } catch (error) {

        console.error(error);

    }
    }


    // --------------------------------------------------
    // Disconnect
    // --------------------------------------------------

    async function handleDisconnect() {

    try {

        await disconnectWeather();

        const weatherStatus =
            await getWeatherStatus();

        setStatus(weatherStatus);

    } catch (error) {

        console.error(error);

    }
    }

    // --------------------------------------------------
    // Weather card
    // --------------------------------------------------

    return (
    <StatusCard
        title="Weather"
        status={
            status.state === "safe"
                ? "safe"
                : status.state === "unsafe"
                    ? "error"
                    : "warning"
}
    >

        <div className="flex items-center justify-between">

            <span className="text-sm text-slate-400">
                Connection
            </span>

            <span className="text-sm">
                {status.connected
                    ? "Connected"
                    : "Disconnected"}
            </span>

        </div>


        <div className="mt-4">

            {status.reason && (
                <p className="text-xs text-slate-400 mt-1">
                    {status.reason}
                </p>
            )}

        </div>


        <div className="mt-4">

            {status.connected ? (

                <button
                    onClick={handleDisconnect}
                    className="
                        w-full
                        px-4
                        py-2
                        rounded-lg
                        bg-red-600
                        hover:bg-red-700
                        transition
                    "
                >
                    Disconnect
                </button>

            ) : (

                <button
                    onClick={handleConnect}
                    className="
                        w-full
                        px-4
                        py-2
                        rounded-lg
                        bg-blue-600
                        hover:bg-blue-700
                        transition
                    "
                >
                    Connect
                </button>

            )}

        </div>

    </StatusCard>
);
}