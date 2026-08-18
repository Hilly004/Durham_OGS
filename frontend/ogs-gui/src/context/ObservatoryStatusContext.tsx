import {
    createContext,
    useCallback,
    useContext,
    useEffect,
    useState,
    type ReactNode,
} from "react";

import {
    getMountStatus,
} from "../api/mount";

import {
    getDomeStatus,
} from "../api/dome";

import {
    getWeatherStatus,
} from "../api/weather";

import type {
    MountStatusData,
} from "../api/mount";

import type {
    DomeStatusData,
} from "../api/dome";

import type {
    WeatherStatusData,
} from "../api/weather";


export type ObservatoryState =
    | "nominal"
    | "degraded"
    | "unsafe"
    | "offline";


interface ObservatoryStatusContextValue {

    mountStatus:
        MountStatusData | null;

    domeStatus:
        DomeStatusData | null;

    weatherStatus:
        WeatherStatusData | null;

    observatoryState:
        ObservatoryState;

    refresh:
        () => Promise<void>;
}


const ObservatoryStatusContext =
    createContext<
        ObservatoryStatusContextValue | undefined
    >(undefined);


export function ObservatoryStatusProvider({
    children,
}: {
    children: ReactNode;
}) {

    const [mountStatus, setMountStatus] =
        useState<MountStatusData | null>(null);

    const [domeStatus, setDomeStatus] =
        useState<DomeStatusData | null>(null);

    const [weatherStatus, setWeatherStatus] =
        useState<WeatherStatusData | null>(null);


    const refresh =
        useCallback(async () => {

            const results =
                await Promise.allSettled([
                    getMountStatus(),
                    getDomeStatus(),
                    getWeatherStatus(),
                ]);


            const [
                mountResult,
                domeResult,
                weatherResult,
            ] = results;


            setMountStatus(
                mountResult.status === "fulfilled"
                    ? mountResult.value
                    : null
            );


            setDomeStatus(
                domeResult.status === "fulfilled"
                    ? domeResult.value
                    : null
            );


            setWeatherStatus(
                weatherResult.status === "fulfilled"
                    ? weatherResult.value
                    : null
            );

        }, []);


    useEffect(() => {

        refresh();

        const interval = setInterval(
            refresh,
            3000
        );

        return () => {
            clearInterval(interval);
        };

    }, [refresh]);


    const observatoryState =
        calculateObservatoryState(
            mountStatus,
            domeStatus,
            weatherStatus
        );


    return (
        <ObservatoryStatusContext.Provider
            value={{
                mountStatus,
                domeStatus,
                weatherStatus,
                observatoryState,
                refresh,
            }}
        >
            {children}
        </ObservatoryStatusContext.Provider>
    );
}


export function useObservatoryStatus() {

    const context =
        useContext(
            ObservatoryStatusContext
        );


    if (!context) {
        throw new Error(
            "useObservatoryStatus must be used inside ObservatoryStatusProvider"
        );
    }


    return context;
}


function calculateObservatoryState(
    mount: MountStatusData | null,
    dome: DomeStatusData | null,
    weather: WeatherStatusData | null
): ObservatoryState {

    const mountConnected =
        mount?.connected ?? false;

    const domeConnected =
        dome?.connected ?? false;

    const weatherConnected =
        weather?.connected ?? false;


    const anyConnected =
        mountConnected ||
        domeConnected ||
        weatherConnected;


    if (!anyConnected) {
        return "offline";
    }


    if (
        weather?.safe === false ||
        dome?.fault === true
    ) {
        return "unsafe";
    }


    if (
        !mountConnected ||
        !domeConnected ||
        !weatherConnected
    ) {
        return "degraded";
    }


    return "nominal";
}