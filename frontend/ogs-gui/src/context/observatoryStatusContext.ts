import {
    createContext,
} from "react";

import type {
    MountStatusData,
    MountPosition,
    MountPosition_rd,
} from "../api/mount";

import type {
    DomeStatusData,
} from "../api/dome";

import type {
    WeatherStatusData,
} from "../api/weather";

import type {
    CameraStatusData,
} from "../api/camera";


export type ObservatoryState =
    | "offline"
    | "unsafe"
    | "ready"
    | "partial";


export interface ObservatoryStatusContextValue {

    mountStatus:
        MountStatusData | null;

    mountPosition:
        MountPosition | null;

    mountPositionRd:
        MountPosition_rd | null;

    domeStatus:
        DomeStatusData | null;

    weatherStatus:
        WeatherStatusData | null;

    cameraStatus:
        CameraStatusData | null;

    observatoryState:
        ObservatoryState;

    refreshing:
        boolean;

    lastUpdated:
        Date | null;

    refresh:
        () => Promise<void>;

}


export const ObservatoryStatusContext =
    createContext<
        ObservatoryStatusContextValue | null
    >(null);