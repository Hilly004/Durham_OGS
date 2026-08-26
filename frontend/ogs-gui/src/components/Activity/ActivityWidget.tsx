import {
    useCallback,
    useEffect,
    useRef,
    useState,
} from "react";

import {
    Activity,
    ChevronDown,
    ChevronUp,
    Download,
    Trash2,
} from "lucide-react";

import {
    clearActivity,
    getActivity,
} from "../../api/activity";

import type {
    ActivityEntry,
} from "../../api/activity";


interface ActivityLogProps {
    expanded: boolean;
    onToggleExpanded: () => void;
}


export default function ActivityLog({
    expanded,
    onToggleExpanded,
}: ActivityLogProps) {

    const [entries, setEntries] =
        useState<ActivityEntry[]>([]);

    const [error, setError] =
        useState<string | null>(null);

    const [connected, setConnected] =
        useState(false);

    const logContainerRef =
        useRef<HTMLDivElement | null>(null);


    const updateActivity = useCallback(
        async () => {

            try {

                const activity =
                    await getActivity(100);

                setEntries(activity);

                setConnected(true);
                setError(null);

            } catch (error) {

                setConnected(false);

                if (error instanceof Error) {
                    setError(error.message);
                } else {
                    setError(
                        "Unable to retrieve activity"
                    );
                }

            }

        },
        []
    );


    useEffect(() => {

        const initialTimer =
            window.setTimeout(
                () => {
                    void updateActivity();
                },
                0
            );


        const interval =
            window.setInterval(
                () => {
                    void updateActivity();
                },
                3000
            );


        return () => {

            window.clearTimeout(
                initialTimer
            );

            window.clearInterval(
                interval
            );

        };

    }, [updateActivity]);


    /*
     * Scroll to newest message whenever
     * the activity list changes.
     */
    useEffect(() => {

        if (!expanded) {
            return;
        }

        const container =
            logContainerRef.current;

        if (!container) {
            return;
        }

        container.scrollTop =
            container.scrollHeight;

    }, [entries, expanded]);


    async function handleClear() {

        try {

            await clearActivity();

            setEntries([]);
            setError(null);

        } catch (error) {

            console.error(
                "Unable to clear activity:",
                error
            );

        }
    }


    function handleExportCSV() {

        if (entries.length === 0) {
            return;
        }


        const header = [
            "Timestamp",
            "Level",
            "Source",
            "Message",
        ];


        const rows = entries.map(
            (entry) => [
                entry.timestamp,
                entry.level,
                entry.source,
                entry.message,
            ]
        );


        const csv = [
            header,
            ...rows,
        ]
            .map(
                (row) =>
                    row
                        .map(
                            (value) =>
                                escapeCSV(
                                    String(value)
                                )
                        )
                        .join(",")
            )
            .join("\n");


        const blob =
            new Blob(
                [csv],
                {
                    type:
                        "text/csv;charset=utf-8;",
                }
            );


        const url =
            URL.createObjectURL(blob);


        const link =
            document.createElement("a");

        link.href = url;

        link.download =
            `observatory-activity-${createFilenameTimestamp()}.csv`;

        document.body.appendChild(link);

        link.click();

        document.body.removeChild(link);

        URL.revokeObjectURL(url);
    }


    return (
        <div
            className="
                flex
                h-full
                flex-col
                overflow-hidden
                bg-slate-950
            "
        >

            {/* Header */}
            <div
                className="
                    flex
                    h-9
                    shrink-0
                    items-center
                    justify-between
                    border-b
                    border-slate-800
                    px-4
                "
            >

                {/* Left */}
                <div className="flex items-center gap-3">

                    <Activity
                        size={15}
                        className="text-violet-400"
                    />


                    <span
                        className="
                            text-xs
                            font-semibold
                            uppercase
                            tracking-widest
                            text-slate-400
                        "
                    >
                        Activity
                    </span>


                    {/* Live Status */}
                    <div
                        className="
                            flex
                            items-center
                            gap-1.5
                        "
                    >

                        <span
                            className={`
                                h-1.5
                                w-1.5
                                rounded-full

                                ${
                                    connected
                                        ? "bg-green-500"
                                        : "bg-red-500"
                                }
                            `}
                        />

                        <span
                            className="
                                text-[10px]
                                font-medium
                                text-slate-500
                            "
                        >
                            {connected
                                ? "LIVE"
                                : "OFFLINE"}
                        </span>

                    </div>

                </div>


                {/* Right */}
                <div className="flex items-center gap-2">

                    {/* Event Count */}
                    <span
                        className="
                            mr-2
                            text-xs
                            text-slate-600
                        "
                    >
                        {entries.length}
                        {" "}
                        {entries.length === 1
                            ? "event"
                            : "events"}
                    </span>


                    {/* Expand / Collapse */}
                    <button
                        type="button"
                        onClick={
                            onToggleExpanded
                        }
                        title={
                            expanded
                                ? "Collapse activity log"
                                : "Expand activity log"
                        }
                        className="
                            rounded-md
                            p-1
                            text-slate-600
                            transition-colors
                            hover:bg-slate-900
                            hover:text-violet-300
                        "
                    >

                        {expanded ? (
                            <ChevronDown
                                size={18}
                            />
                        ) : (
                            <ChevronUp
                                size={18}
                            />
                        )}

                    </button>


                    {/* Export CSV */}
                    <button
                        type="button"
                        onClick={
                            handleExportCSV
                        }
                        disabled={
                            entries.length === 0
                        }
                        title="Export activity to CSV"
                        className="
                            rounded-md
                            p-1
                            text-slate-600
                            transition-colors
                            hover:bg-slate-900
                            hover:text-violet-300
                            disabled:cursor-not-allowed
                            disabled:opacity-30
                        "
                    >
                        <Download size={18} />
                    </button>


                    {/* Clear */}
                    <button
                        type="button"
                        onClick={handleClear}
                        disabled={
                            entries.length === 0
                        }
                        title="Clear activity log"
                        className="
                            rounded-md
                            p-1
                            text-slate-600
                            transition-colors
                            hover:bg-slate-900
                            hover:text-slate-300
                            disabled:cursor-not-allowed
                            disabled:opacity-30
                        "
                    >
                        <Trash2 size={18} />
                    </button>

                </div>

            </div>


            {/* Only render contents when expanded */}
            {expanded && (
                <>

                    {/* API Error */}
                    {error && (

                        <div
                            className="
                                shrink-0
                                border-b
                                border-slate-800
                                px-4
                                py-1.5
                                text-xs
                                text-slate-500
                            "
                        >
                            Activity service unavailable
                        </div>

                    )}


                    {/* Log */}
                    <div
                        ref={
                            logContainerRef
                        }
                        className="
                            min-h-0
                            flex-1
                            overflow-y-auto
                            px-3
                            py-2
                        "
                    >

                        {entries.length === 0 ? (

                            <div
                                className="
                                    flex
                                    h-full
                                    items-center
                                    justify-center
                                "
                            >

                                <div className="text-center">

                                    <Activity
                                        size={20}
                                        className="
                                            mx-auto
                                            mb-2
                                            text-slate-700
                                        "
                                    />

                                    <p
                                        className="
                                            text-xs
                                            text-slate-600
                                        "
                                    >
                                        No activity recorded
                                    </p>

                                </div>

                            </div>

                        ) : (

                            <div className="space-y-0.5">

                                {entries.map(
                                    (entry) => (

                                        <ActivityRow
                                            key={
                                                `${entry.timestamp}-${entry.id}`
                                            }
                                            entry={
                                                entry
                                            }
                                        />

                                    )
                                )}

                            </div>

                        )}

                    </div>

                </>
            )}

        </div>
    );
}


function ActivityRow({
    entry,
}: {
    entry: ActivityEntry;
}) {

    return (
        <div
            className="
                grid
                grid-cols-[75px_90px_1fr]
                items-center
                gap-2
                rounded-md
                px-2
                py-1.5
                text-xs
                transition-colors
                hover:bg-slate-900
            "
        >

            {/* Time */}
            <span
                className="
                    font-mono
                    text-[11px]
                    text-slate-600
                "
            >
                {formatTime(
                    entry.timestamp
                )}
            </span>


            {/* Source */}
            <div
                className="
                    flex
                    items-center
                    gap-2
                "
            >

                <span
                    className={`
                        h-1.5
                        w-1.5
                        shrink-0
                        rounded-full

                        ${getSourceDotColour(
                            entry.source
                        )}
                    `}
                />

                <span
                    className={`
                        truncate
                        font-medium

                        ${getSourceColour(
                            entry.source
                        )}
                    `}
                >
                    {entry.source}
                </span>

            </div>


            {/* Message */}
            <span
                title={entry.message}
                className={`
                    truncate

                    ${getLevelColour(
                        entry.level
                    )}
                `}
            >
                {entry.message}
            </span>

        </div>
    );
}


function formatTime(
    timestamp: string
) {

    const date =
        new Date(timestamp);

    if (
        Number.isNaN(
            date.getTime()
        )
    ) {
        return "--:--:--";
    }

    return date.toLocaleTimeString(
        [],
        {
            hour: "2-digit",
            minute: "2-digit",
            second: "2-digit",
            hour12: false,
        }
    );
}


function createFilenameTimestamp() {

    const now =
        new Date();

    return now
        .toISOString()
        .replaceAll(":", "-")
        .replace(/\.\d{3}Z$/, "");
}


function escapeCSV(
    value: string
) {

    const escaped =
        value.replaceAll(
            '"',
            '""'
        );

    return `"${escaped}"`;
}


function getLevelColour(
    level: ActivityEntry["level"]
) {

    switch (level) {

        case "success":
            return "text-green-400";

        case "warning":
            return "text-amber-400";

        case "error":
            return "text-red-400";

        default:
            return "text-slate-300";
    }
}


function getSourceColour(
    source: string
) {

    switch (
        source.toUpperCase()
    ) {

        case "MOUNT":
            return "text-violet-400";

        case "DOME":
            return "text-violet-300";

        case "WEATHER":
            return "text-sky-400";

        case "CAMERA":
            return "text-indigo-400";

        case "TRACKING":
            return "text-fuchsia-400";

        case "SYSTEM":
            return "text-slate-400";

        default:
            return "text-slate-500";
    }
}


function getSourceDotColour(
    source: string
) {

    switch (
        source.toUpperCase()
    ) {

        case "MOUNT":
            return "bg-violet-400";

        case "DOME":
            return "bg-violet-300";

        case "WEATHER":
            return "bg-sky-400";

        case "CAMERA":
            return "bg-indigo-400";

        case "TRACKING":
            return "bg-fuchsia-400";

        case "SYSTEM":
            return "bg-slate-500";

        default:
            return "bg-slate-600";
    }
}