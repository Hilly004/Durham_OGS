import {
    LayoutDashboard,
    Telescope,
    Warehouse,
    Camera,
    CloudSun,
    Satellite,
    Settings,
} from "lucide-react";

import {
    NavLink,
} from "react-router-dom";

import {
    useObservatoryStatus,
} from "../../context/ObservatoryStatusContext";

import {
    getObservatoryStateStyle,
} from "../../utils/observatoryStatus";


const navItems = [
    {
        name: "Dashboard",
        path: "/",
        icon: LayoutDashboard,
    },
    {
        name: "Mount",
        path: "/mount",
        icon: Telescope,
    },
    {
        name: "Dome",
        path: "/dome",
        icon: Warehouse,
    },
    {
        name: "Camera",
        path: "/camera",
        icon: Camera,
    },
    {
        name: "Weather",
        path: "/weather",
        icon: CloudSun,
    },
    {
        name: "Tracking",
        path: "/tracking",
        icon: Satellite,
    },
];


export default function Sidebar() {

    const {
        observatoryState,
    } = useObservatoryStatus();


    const observatoryStyle =
        getObservatoryStateStyle(
            observatoryState
        );


    return (
        <aside
            className="
                flex
                h-screen
                w-48
                shrink-0
                flex-col
                border-r
                border-slate-800
                bg-slate-950
                px-3
                py-4
            "
        >

            {/* Logo / Title */}
            <div className="mb-6 px-3">

                <div className="flex items-center gap-3">

                    <div
                        className="
                            flex
                            h-10
                            w-10
                            items-center
                            justify-center
                            rounded-xl
                            bg-violet-500/10
                            text-sm
                            font-bold
                            text-violet-300
                            ring-1
                            ring-violet-500/20
                        "
                    >
                        OGS
                    </div>


                    <div>

                        <h1
                            className="
                                text-sm
                                font-semibold
                                text-slate-100
                            "
                        >
                            Durham OGS
                        </h1>

                        <p
                            className="
                                text-xs
                                text-slate-500
                            "
                        >
                            Ground Station Control
                        </p>

                    </div>

                </div>

            </div>


            {/* Navigation */}
            <nav className="flex-1">

                <p
                    className="
                        mb-2
                        px-3
                        text-[10px]
                        font-semibold
                        uppercase
                        tracking-widest
                        text-slate-600
                    "
                >
                    Observatory
                </p>


                <div className="space-y-1">

                    {navItems.map((item) => {

                        const Icon =
                            item.icon;


                        return (
                            <NavLink
                                key={item.path}
                                to={item.path}
                                end={item.path === "/"}
                                className={({ isActive }) =>
                                    `
                                        group
                                        relative
                                        flex
                                        items-center
                                        gap-3
                                        rounded-lg
                                        px-3
                                        py-2.5
                                        text-sm
                                        font-medium
                                        transition-all

                                        ${
                                            isActive
                                                ? `
                                                    bg-violet-500/10
                                                    text-slate-100
                                                `
                                                : `
                                                    text-slate-400
                                                    hover:bg-slate-900
                                                    hover:text-slate-100
                                                `
                                        }
                                    `
                                }
                            >

                                {({ isActive }) => (
                                    <>

                                        {/* Active indicator */}
                                        {isActive && (

                                            <span
                                                className="
                                                    absolute
                                                    left-0
                                                    top-2
                                                    bottom-2
                                                    w-0.5
                                                    rounded-full
                                                    bg-violet-400
                                                "
                                            />

                                        )}


                                        {/* Icon */}
                                        <Icon
                                            size={18}
                                            className={
                                                isActive
                                                    ? "text-violet-400"
                                                    : `
                                                        text-slate-500
                                                        transition-colors
                                                        group-hover:text-violet-300
                                                    `
                                            }
                                        />


                                        {/* Label */}
                                        <span>
                                            {item.name}
                                        </span>


                                        {/* Active dot */}
                                        {isActive && (

                                            <span
                                                className="
                                                    ml-auto
                                                    h-1.5
                                                    w-1.5
                                                    rounded-full
                                                    bg-violet-400
                                                "
                                            />

                                        )}

                                    </>
                                )}

                            </NavLink>
                        );
                    })}

                </div>

            </nav>


            {/* Observatory State */}
            <div
                className="
                    mb-3
                    rounded-xl
                    border
                    border-slate-800
                    bg-slate-900
                    p-3
                "
            >

                <div
                    className="
                        flex
                        items-center
                        justify-between
                    "
                >

                    <span
                        className="
                            text-xs
                            text-slate-500
                        "
                    >
                        Observatory
                    </span>


                    <div
                        className="
                            flex
                            items-center
                            gap-1.5
                        "
                    >

                        <span
                            className={`
                                h-2
                                w-2
                                rounded-full
                                ${observatoryStyle.dot}
                            `}
                        />

                        <span
                            className={`
                                text-xs
                                font-medium
                                ${observatoryStyle.text}
                            `}
                        >
                            {observatoryStyle.label}
                        </span>

                    </div>

                </div>


                <p
                    className="
                        mt-2
                        text-xs
                        text-slate-500
                    "
                >
                    {getObservatoryDescription(
                        observatoryState
                    )}
                </p>

            </div>


            {/* Settings */}
            <NavLink
                to="/settings"
                className={({ isActive }) =>
                    `
                        group
                        flex
                        items-center
                        gap-3
                        rounded-lg
                        px-3
                        py-2.5
                        text-sm
                        font-medium
                        transition-all

                        ${
                            isActive
                                ? `
                                    bg-violet-500/10
                                    text-slate-100
                                `
                                : `
                                    text-slate-400
                                    hover:bg-slate-900
                                    hover:text-slate-100
                                `
                        }
                    `
                }
            >

                {({ isActive }) => (
                    <>

                        <Settings
                            size={18}
                            className={
                                isActive
                                    ? "text-violet-400"
                                    : `
                                        text-slate-500
                                        transition-colors
                                        group-hover:text-violet-300
                                    `
                            }
                        />

                        <span>
                            Settings
                        </span>

                    </>
                )}

            </NavLink>

        </aside>
    );
}


function getObservatoryDescription(
    state:
        | "nominal"
        | "degraded"
        | "unsafe"
        | "offline"
) {

    switch (state) {

        case "nominal":
            return "All monitored systems operational";

        case "degraded":
            return "One or more systems unavailable";

        case "unsafe":
            return "Observatory operation restricted";

        case "offline":
            return "Observatory systems offline";

    }
}