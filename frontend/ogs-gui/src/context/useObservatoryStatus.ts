import {
    useContext,
} from "react";

import {
    ObservatoryStatusContext,
} from "./observatoryStatusContext";


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