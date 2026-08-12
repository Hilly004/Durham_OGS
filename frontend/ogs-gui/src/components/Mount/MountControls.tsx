import { useState } from "react";


export default function MountControls() {

    const [loading, setLoading] = useState(false);


    const park = async () => {

        setLoading(true);

        try {

            const response = await fetch(
                "/api/mount/slew_to_park",
                {
                    method: "POST",
                }
            );

            if (!response.ok) {
                throw new Error("Failed to park mount");
            }

        } catch (error) {

            console.error(error);

        } finally {

            setLoading(false);

        }
    };


    const unpark = async () => {

        setLoading(true);

        try {

            const response = await fetch(
                "/api/mount/unpark",
                {
                    method: "POST",
                }
            );

            if (!response.ok) {
                throw new Error("Failed to unpark mount");
            }

        } catch (error) {

            console.error(error);

        } finally {

            setLoading(false);

        }
    };


    const stop = async () => {

        try {

            const response = await fetch(
                "/api/mount/stop",
                {
                    method: "POST",
                }
            );

            if (!response.ok) {
                throw new Error("Failed to stop mount");
            }

        } catch (error) {

            console.error(error);

        }
    };


    return (
        <div className="
            bg-slate-800
            border
            border-slate-700
            rounded-lg
            p-4
            h-full
            flex
            flex-col
        ">

            <div className="mb-6">

                <h2 className="
                    text-lg
                    font-semibold
                    text-slate-100
                ">
                    Mount Controls
                </h2>

                <p className="
                    text-sm
                    text-slate-400
                ">
                    Telescope movement and tracking
                </p>

            </div>


            {/* Position */}

            <div>

                <p className="
                    text-xs
                    uppercase
                    tracking-wider
                    text-slate-500
                    mb-3
                ">
                    Position
                </p>


                <div className="
                    grid
                    grid-cols-2
                    gap-3
                ">

                    <button
                        onClick={park}
                        disabled={loading}
                        className="
                            px-4
                            py-3
                            rounded-lg
                            bg-slate-700
                            border
                            border-slate-600
                            text-sm
                            font-medium
                            text-slate-200
                            hover:bg-slate-600
                            disabled:opacity-50
                        "
                    >
                        Park
                    </button>


                    <button
                        onClick={unpark}
                        disabled={loading}
                        className="
                            px-4
                            py-3
                            rounded-lg
                            bg-slate-700
                            border
                            border-slate-600
                            text-sm
                            font-medium
                            text-slate-200
                            hover:bg-slate-600
                            disabled:opacity-50
                        "
                    >
                        Unpark
                    </button>

                </div>


                <button
                    onClick={stop}
                    className="
                        w-full
                        mt-3
                        px-4
                        py-3
                        rounded-lg
                        bg-red-900/40
                        border
                        border-red-800
                        text-sm
                        font-medium
                        text-red-400
                        hover:bg-red-900/60
                    "
                >
                    Stop
                </button>

            </div>

        </div>
    );
}