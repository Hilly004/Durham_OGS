import {
    useRef,
    useState,
} from "react";

import {
    Outlet,
} from "react-router-dom";

import Sidebar from "./sidebar";
import ActivityLog from "../Activity/ActivityWidget";


const COLLAPSED_HEIGHT = 37;
const DEFAULT_EXPANDED_HEIGHT = 250;
const MIN_EXPANDED_HEIGHT = 140;


export default function Layout() {

    const [activityExpanded, setActivityExpanded] =
        useState(false);

    const [activityHeight, setActivityHeight] =
        useState(DEFAULT_EXPANDED_HEIGHT);

    const resizing = useRef(false);


    function handleResizeStart(
        event: React.MouseEvent<HTMLDivElement>
    ) {

        if (!activityExpanded) {
            return;
        }

        resizing.current = true;

        const startY = event.clientY;
        const startHeight = activityHeight;

        document.body.style.userSelect = "none";
        document.body.style.cursor = "ns-resize";


        function handleMouseMove(
            mouseEvent: MouseEvent
        ) {

            if (!resizing.current) {
                return;
            }

            /*
             * Moving upward decreases clientY,
             * so subtract the difference to
             * increase drawer height.
             */
            const difference =
                startY - mouseEvent.clientY;

            const maxHeight =
                window.innerHeight * 0.7;

            const newHeight = Math.min(
                Math.max(
                    startHeight + difference,
                    MIN_EXPANDED_HEIGHT
                ),
                maxHeight
            );

            setActivityHeight(newHeight);
        }


        function handleMouseUp() {

            resizing.current = false;

            document.body.style.userSelect = "";
            document.body.style.cursor = "";

            window.removeEventListener(
                "mousemove",
                handleMouseMove
            );

            window.removeEventListener(
                "mouseup",
                handleMouseUp
            );
        }


        window.addEventListener(
            "mousemove",
            handleMouseMove
        );

        window.addEventListener(
            "mouseup",
            handleMouseUp
        );
    }


    function toggleActivity() {

        setActivityExpanded(
            (current) => !current
        );
    }


    return (
        <div
            className="
                flex
                h-screen
                overflow-hidden
                bg-slate-950
            "
        >

            {/* Sidebar */}
            <Sidebar />


            {/* Main Application Area */}
            <div
                className="
                    flex
                    min-w-0
                    flex-1
                    flex-col
                "
            >

                {/* Current Page */}
                <main
                    className="
                        min-h-0
                        flex-1
                        overflow-hidden
                    "
                >
                    <Outlet />
                </main>


                {/* Activity Drawer */}
                <div
                    style={{
                        height: activityExpanded
                            ? activityHeight
                            : COLLAPSED_HEIGHT,
                    }}
                    className="
                        relative
                        shrink-0
                        border-t
                        border-slate-800
                        bg-slate-950
                    "
                >

                    {/* Drag Handle */}
                    {activityExpanded && (

                        <div
                            onMouseDown={
                                handleResizeStart
                            }
                            title="Drag to resize activity log"
                            className="
                                absolute
                                -top-1
                                left-0
                                right-0
                                z-20
                                h-2
                                cursor-ns-resize
                                group
                            "
                        >

                            <div
                                className="
                                    absolute
                                    left-1/2
                                    top-0
                                    h-1
                                    w-12
                                    -translate-x-1/2
                                    rounded-full
                                    bg-slate-700
                                    transition-colors
                                    group-hover:bg-violet-400
                                "
                            />

                        </div>

                    )}


                    <ActivityLog
                        expanded={activityExpanded}
                        onToggleExpanded={
                            toggleActivity
                        }
                    />

                </div>

            </div>

        </div>
    );
}