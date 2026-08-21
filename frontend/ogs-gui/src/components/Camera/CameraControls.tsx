import {
    useState,
} from "react";

import {
    Camera,
    CircleStop,
    Play,
} from "lucide-react";

import {
    startCameraStream,
    stopCameraStream,
} from "../../api/camera";


interface CameraControlsProps {
    connected: boolean;
}


export default function CameraControls({
    connected,
}: CameraControlsProps) {

    const [loading, setLoading] =
        useState(false);

    const [streaming, setStreaming] =
        useState(false);


    async function handleStartStream() {

        if (!connected) {
            return;
        }

        setLoading(true);

        try {

            await startCameraStream();

            setStreaming(true);

        } catch (error) {

            console.error(
                "Unable to start camera stream:",
                error
            );

        } finally {

            setLoading(false);

        }
    }


    async function handleStopStream() {

        if (!connected) {
            return;
        }

        setLoading(true);

        try {

            await stopCameraStream();

            setStreaming(false);

        } catch (error) {

            console.error(
                "Unable to stop camera stream:",
                error
            );

        } finally {

            setLoading(false);

        }
    }


    function handleCapture() {

        if (
            !connected ||
            streaming
        ) {
            return;
        }

        /*
         * For now this can trigger the
         * single-frame endpoint/display.
         *
         * Later this can call a dedicated
         * save/capture API.
         */
        const image =
            new Image();

        image.src =
            `/api/camera/frame?v=${Date.now()}`;
    }


    return (
        <div
            className="
                flex
                h-full
                flex-col
                gap-4
                rounded-lg
                border
                border-slate-800
                bg-slate-950/40
                p-4
            "
        >

            <h2
                className="
                    text-sm
                    font-semibold
                    text-slate-200
                "
            >
                Camera Controls
            </h2>


            <button
                type="button"
                onClick={handleCapture}
                disabled={
                    loading ||
                    !connected ||
                    streaming
                }
                className="
                    flex
                    items-center
                    justify-center
                    gap-2
                    rounded-lg
                    bg-slate-800
                    px-3
                    py-2
                    text-sm
                    font-medium
                    text-slate-200
                    hover:bg-slate-700
                    disabled:cursor-not-allowed
                    disabled:opacity-40
                "
            >

                <Camera size={16} />

                Capture

            </button>


            {!streaming ? (

                <button
                    type="button"
                    onClick={handleStartStream}
                    disabled={
                        loading ||
                        !connected
                    }
                    className="
                        flex
                        items-center
                        justify-center
                        gap-2
                        rounded-lg
                        bg-violet-600
                        px-3
                        py-2
                        text-sm
                        font-medium
                        text-white
                        hover:bg-violet-500
                        disabled:cursor-not-allowed
                        disabled:opacity-40
                    "
                >

                    <Play size={16} />

                    Live View

                </button>

            ) : (

                <button
                    type="button"
                    onClick={handleStopStream}
                    disabled={loading}
                    className="
                        flex
                        items-center
                        justify-center
                        gap-2
                        rounded-lg
                        bg-red-600
                        px-3
                        py-2
                        text-sm
                        font-medium
                        text-white
                        hover:bg-red-500
                        disabled:cursor-not-allowed
                        disabled:opacity-40
                    "
                >

                    <CircleStop size={16} />

                    Stop Live View

                </button>

            )}

        </div>
    );
}