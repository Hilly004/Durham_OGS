import {
    useCallback,
    useEffect,
    useRef,
    useState,
    type ReactNode,
} from "react";

import {
    getMountStatus,
    getMountPosition,
    getMountPosition_rd,
} from "../api/mount";

import type {
    MountStatusData,
    MountPosition,
    MountPosition_rd,
} from "../api/mount";

import {
    getDomeStatus,
} from "../api/dome";

import type {
    DomeStatusData,
} from "../api/dome";

import {
    getWeatherStatus,
} from "../api/weather";

import type {
    WeatherStatusData,
} from "../api/weather";

import {
    getCameraStatus,
} from "../api/camera";

import type {
    CameraStatusData,
} from "../api/camera";

import {
    ObservatoryStatusContext,
} from "./observatoryStatusContext";

import type {
    ObservatoryState,
} from "./observatoryStatusContext";


interface Props {
    children: ReactNode;
}


const POLL_INTERVAL_MS =
    2000;


function calculateObservatoryState(
    mountStatus: MountStatusData | null,
    domeStatus: DomeStatusData | null,
    weatherStatus: WeatherStatusData | null,
    cameraStatus: CameraStatusData | null
): ObservatoryState {

    const mountConnected =
        mountStatus?.connected
        ?? false;

    const domeConnected =
        domeStatus?.connected
        ?? false;

    const weatherConnected =
        weatherStatus?.connected
        ?? false;

    const cameraConnected =
        cameraStatus?.connected
        ?? false;


    const anyConnected =
        mountConnected
        ||
        domeConnected
        ||
        weatherConnected
        ||
        cameraConnected;


    if (!anyConnected) {

        return "offline";

    }


    if (
        weatherConnected
        &&
        weatherStatus?.safe === false
    ) {

        return "unsafe";

    }


    if (
        mountConnected
        &&
        domeConnected
        &&
        weatherConnected
        &&
        cameraConnected
    ) {

        return "ready";

    }


    return "partial";
}


export function ObservatoryStatusProvider({
    children,
}: Props) {

    const [
        mountStatus,
        setMountStatus,
    ] =
        useState<
            MountStatusData | null
        >(null);


    const [
        mountPosition,
        setMountPosition,
    ] =
        useState<
            MountPosition | null
        >(null);


    const [
        mountPositionRd,
        setMountPositionRd,
    ] =
        useState<
            MountPosition_rd | null
        >(null);


    const [
        domeStatus,
        setDomeStatus,
    ] =
        useState<
            DomeStatusData | null
        >(null);


    const [
        weatherStatus,
        setWeatherStatus,
    ] =
        useState<
            WeatherStatusData | null
        >(null);


    const [
        cameraStatus,
        setCameraStatus,
    ] =
        useState<
            CameraStatusData | null
        >(null);


    const [
        refreshing,
        setRefreshing,
    ] =
        useState(false);


    const [
        lastUpdated,
        setLastUpdated,
    ] =
        useState<Date | null>(
            null
        );


    const refreshInProgress =
        useRef(false);


    const refresh =
        useCallback(
            async () => {

                if (
                    refreshInProgress.current
                ) {

                    return;

                }


                refreshInProgress.current =
                    true;

                setRefreshing(true);


                try {

                    const [
                        mountResult,
                        domeResult,
                        weatherResult,
                        cameraResult,
                    ] =
                        await Promise.allSettled([
                            getMountStatus(),
                            getDomeStatus(),
                            getWeatherStatus(),
                            getCameraStatus(),
                        ]);


                    let currentMountStatus:
                        MountStatusData | null =
                            null;


                    if (
                        mountResult.status
                        ===
                        "fulfilled"
                    ) {

                        currentMountStatus =
                            mountResult.value;

                        setMountStatus(
                            mountResult.value
                        );

                    }


                    if (
                        domeResult.status
                        ===
                        "fulfilled"
                    ) {

                        setDomeStatus(
                            domeResult.value
                        );

                    }


                    if (
                        weatherResult.status
                        ===
                        "fulfilled"
                    ) {

                        setWeatherStatus(
                            weatherResult.value
                        );

                    }


                    if (
                        cameraResult.status
                        ===
                        "fulfilled"
                    ) {

                        setCameraStatus(
                            cameraResult.value
                        );

                    }


                    if (
                        currentMountStatus
                        ?.
                        connected
                    ) {

                        const [
                            altAzResult,
                            raDecResult,
                        ] =
                            await Promise.allSettled([
                                getMountPosition(),
                                getMountPosition_rd(),
                            ]);


                        if (
                            altAzResult.status
                            ===
                            "fulfilled"
                        ) {

                            setMountPosition(
                                altAzResult.value
                            );

                        }


                        if (
                            raDecResult.status
                            ===
                            "fulfilled"
                        ) {

                            setMountPositionRd(
                                raDecResult.value
                            );

                        }

                    } else if (
                        currentMountStatus
                        &&
                        !currentMountStatus.connected
                    ) {

                        setMountPosition(
                            null
                        );

                        setMountPositionRd(
                            null
                        );

                    }


                    setLastUpdated(
                        new Date()
                    );

                } finally {

                    refreshInProgress.current =
                        false;

                    setRefreshing(false);

                }

            },
            []
        );


    useEffect(() => {

        let cancelled =
            false;

        let timeout:
            ReturnType<
                typeof setTimeout
            >
            |
            undefined;


        async function poll() {

            await refresh();


            if (cancelled) {

                return;

            }


            timeout =
                setTimeout(
                    poll,
                    POLL_INTERVAL_MS
                );

        }


        void poll();


        return () => {

            cancelled =
                true;


            if (
                timeout
                !==
                undefined
            ) {

                clearTimeout(
                    timeout
                );

            }

        };

    }, [refresh]);


    const observatoryState =
        calculateObservatoryState(
            mountStatus,
            domeStatus,
            weatherStatus,
            cameraStatus
        );


    return (

        <ObservatoryStatusContext.Provider
            value={{
                mountStatus,
                mountPosition,
                mountPositionRd,
                domeStatus,
                weatherStatus,
                cameraStatus,
                observatoryState,
                refreshing,
                lastUpdated,
                refresh,
            }}
        >
            {children}
        </ObservatoryStatusContext.Provider>

    );
}