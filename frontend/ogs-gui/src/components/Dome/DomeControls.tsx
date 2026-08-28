import {
    useState,
} from "react";

import {
    ArrowDown,
    ArrowUp,
    DoorOpen,
} from "lucide-react";

import {
    closeDome,
    closeDomeOne,
    closeDomeTwo,
    openDome,
    openDomeOne,
    openDomeTwo,
} from "../../api/dome";

import Card
    from "../Common/Card";


interface DomeControlsProps {
    connected: boolean;
}


export default function DomeControls({
    connected,
}: DomeControlsProps) {

    const [
        loading,
        setLoading,
    ] = useState(false);

    const [
        action,
        setAction,
    ] = useState<string | null>(
        null
    );


    async function runCommand(
        name: string,
        command: () => Promise<void>
    ) {

        if (
            !connected
            ||
            loading
        ) {
            return;
        }


        setLoading(true);
        setAction(name);


        try {

            await command();

        } catch (error) {

            console.error(
                `Dome command failed: ${name}`,
                error
            );

        } finally {

            setLoading(false);
            setAction(null);

        }
    }


    const controlButton = `
        flex
        w-full
        items-center
        justify-center
        gap-2
        rounded-lg
        border
        border-slate-700
        bg-slate-800
        px-4
        py-2.5
        text-sm
        font-medium
        text-slate-200
        transition
        hover:border-violet-500/40
        hover:bg-violet-500/10
        hover:text-violet-300
        disabled:cursor-not-allowed
        disabled:opacity-40
    `;


    return (
        <Card
            className="
                flex
                h-full
                w-full
                flex-col
                overflow-hidden
            "
        >

            {/* Header */}
            <div
                className="
                    flex
                    shrink-0
                    items-center
                    justify-between
                    border-b
                    border-slate-800
                    px-5
                    py-3
                "
            >

                <div>

                    <h2
                        className="
                            text-sm
                            font-semibold
                            text-slate-100
                        "
                    >
                        Dome Controls
                    </h2>

                    <p
                        className="
                            mt-0.5
                            text-xs
                            text-slate-500
                        "
                    >
                        Enclosure and shutter positioning
                    </p>

                </div>


                <div
                    className="
                        flex
                        items-center
                        gap-2
                    "
                >

                    <span
                        className={`
                            h-2
                            w-2
                            rounded-full
                            ${
                                connected
                                    ? "bg-green-500"
                                    : "bg-slate-600"
                            }
                        `}
                    />

                    <span
                        className="
                            text-xs
                            text-slate-500
                        "
                    >
                        {connected
                            ? "Ready"
                            : "Unavailable"}
                    </span>

                </div>

            </div>


            {/* Content */}
            <div
                className="
                    min-h-0
                    flex-1
                    overflow-y-auto
                    p-5
                "
            >

                <div className="space-y-6">

                    {/* Whole Dome */}
                    <section>

                        <div
                            className="
                                mb-3
                                flex
                                items-center
                                gap-2
                            "
                        >

                            <DoorOpen
                                size={15}
                                className="
                                    text-violet-400
                                "
                            />

                            <p
                                className="
                                    text-xs
                                    font-semibold
                                    uppercase
                                    tracking-wider
                                    text-slate-500
                                "
                            >
                                Whole Dome
                            </p>

                        </div>


                        <div
                            className="
                                grid
                                grid-cols-2
                                gap-3
                            "
                        >

                            <button
                                type="button"
                                onClick={() =>
                                    void runCommand(
                                        "open",
                                        openDome
                                    )
                                }
                                disabled={
                                    !connected
                                    ||
                                    loading
                                }
                                className={
                                    controlButton
                                }
                            >

                                <ArrowUp
                                    size={16}
                                />

                                {action === "open"
                                    ? "Opening..."
                                    : "Open Dome"}

                            </button>


                            <button
                                type="button"
                                onClick={() =>
                                    void runCommand(
                                        "close",
                                        closeDome
                                    )
                                }
                                disabled={
                                    !connected
                                    ||
                                    loading
                                }
                                className={
                                    controlButton
                                }
                            >

                                <ArrowDown
                                    size={16}
                                />

                                {action === "close"
                                    ? "Closing..."
                                    : "Close Dome"}

                            </button>

                        </div>

                    </section>


                    {/* Individual Shutters */}
                    <section
                        className="
                            border-t
                            border-slate-800
                            pt-5
                        "
                    >

                        <div
                            className="
                                mb-3
                                flex
                                items-center
                                gap-2
                            "
                        >

                            <DoorOpen
                                size={15}
                                className="
                                    text-violet-400
                                "
                            />

                            <p
                                className="
                                    text-xs
                                    font-semibold
                                    uppercase
                                    tracking-wider
                                    text-slate-500
                                "
                            >
                                Individual Shutters
                            </p>

                        </div>


                        <div
                            className="
                                grid
                                grid-cols-2
                                gap-4
                            "
                        >

                            {/* Left shutter */}
                            <div
                                className="
                                    rounded-lg
                                    border
                                    border-slate-800
                                    bg-slate-950/40
                                    p-4
                                "
                            >

                                <p
                                    className="
                                        mb-3
                                        text-sm
                                        font-medium
                                        text-slate-300
                                    "
                                >
                                    Left Shutter
                                </p>


                                <div
                                    className="
                                        space-y-2
                                    "
                                >

                                    <button
                                        type="button"
                                        onClick={() =>
                                            void runCommand(
                                                "left-open",
                                                openDomeOne
                                            )
                                        }
                                        disabled={
                                            !connected
                                            ||
                                            loading
                                        }
                                        className={
                                            controlButton
                                        }
                                    >

                                        <ArrowUp
                                            size={16}
                                        />

                                        {action ===
                                        "left-open"
                                            ? "Opening..."
                                            : "Open"}

                                    </button>


                                    <button
                                        type="button"
                                        onClick={() =>
                                            void runCommand(
                                                "left-close",
                                                closeDomeOne
                                            )
                                        }
                                        disabled={
                                            !connected
                                            ||
                                            loading
                                        }
                                        className={
                                            controlButton
                                        }
                                    >

                                        <ArrowDown
                                            size={16}
                                        />

                                        {action ===
                                        "left-close"
                                            ? "Closing..."
                                            : "Close"}

                                    </button>

                                </div>

                            </div>


                            {/* Right shutter */}
                            <div
                                className="
                                    rounded-lg
                                    border
                                    border-slate-800
                                    bg-slate-950/40
                                    p-4
                                "
                            >

                                <p
                                    className="
                                        mb-3
                                        text-sm
                                        font-medium
                                        text-slate-300
                                    "
                                >
                                    Right Shutter
                                </p>


                                <div
                                    className="
                                        space-y-2
                                    "
                                >

                                    <button
                                        type="button"
                                        onClick={() =>
                                            void runCommand(
                                                "right-open",
                                                openDomeTwo
                                            )
                                        }
                                        disabled={
                                            !connected
                                            ||
                                            loading
                                        }
                                        className={
                                            controlButton
                                        }
                                    >

                                        <ArrowUp
                                            size={16}
                                        />

                                        {action ===
                                        "right-open"
                                            ? "Opening..."
                                            : "Open"}

                                    </button>


                                    <button
                                        type="button"
                                        onClick={() =>
                                            void runCommand(
                                                "right-close",
                                                closeDomeTwo
                                            )
                                        }
                                        disabled={
                                            !connected
                                            ||
                                            loading
                                        }
                                        className={
                                            controlButton
                                        }
                                    >

                                        <ArrowDown
                                            size={16}
                                        />

                                        {action ===
                                        "right-close"
                                            ? "Closing..."
                                            : "Close"}

                                    </button>

                                </div>

                            </div>

                        </div>

                    </section>


                    {/* Disconnected message */}
                    {!connected && (

                        <div
                            className="
                                rounded-lg
                                border
                                border-slate-800
                                bg-slate-900/50
                                px-3
                                py-3
                                text-center
                                text-xs
                                text-slate-500
                            "
                        >
                            Connect the dome to enable
                            controls.
                        </div>

                    )}

                </div>

            </div>

        </Card>
    );
}