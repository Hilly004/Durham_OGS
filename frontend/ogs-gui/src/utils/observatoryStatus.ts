import type {
    ObservatoryState,
} from "../context/observatoryStatusContext";


export function getObservatoryStateStyle(
    state: ObservatoryState
) {

    switch (state) {

        case "ready":
            return {
                label: "NOMINAL",
                dot: "bg-green-500",
                text: "text-green-400",
            };

        case "partial":
            return {
                label: "DEGRADED",
                dot: "bg-amber-500",
                text: "text-amber-400",
            };

        case "unsafe":
            return {
                label: "UNSAFE",
                dot: "bg-red-500",
                text: "text-red-400",
            };

        case "offline":
            return {
                label: "OFFLINE",
                dot: "bg-slate-500",
                text: "text-slate-400",
            };
    }
}