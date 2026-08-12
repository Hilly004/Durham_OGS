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

    const [status, setStatus] =
        useState<WeatherStatusData | null>(null);

    // --------------------------------------------------
    // Update mount information
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
            setInterval(update, 1000);

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
    // No status
    // --------------------------------------------------

    if (!status) {

        return (
            <StatusCard
                title="Weather"
                status="error"
            >

                <p className="text-red-400">
                    Unable to read weather status
                </p>

                <button
                    onClick={handleConnect}
                    className="
                        mt-4
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

            </StatusCard>
        );
    }


    // --------------------------------------------------
    // Mount card
    // --------------------------------------------------

    return (

        <StatusCard
            title="Weather"
            status={
                status.connected
                    ? "connected"
                    : "disconnected"
            }
        >


            {/* Connection */}

            <button
                onClick={
                    status.connected
                        ? handleDisconnect
                        : handleConnect
                }
                className="
                    w-full
                    mt-6
                    px-4
                    py-2
                    rounded-lg
                    bg-slate-700
                    hover:bg-slate-600
                    text-white
                    transition
                "
            >

                {status.connected
                    ? "Disconnect"
                    : "Connect"}

            </button>

        </StatusCard>
    );
}