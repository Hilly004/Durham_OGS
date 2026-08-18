import CameraWidget
    from "../components/Camera/CameraWidget";


export default function CameraPage() {

    return (
        <div
            className="
                flex
                h-full
                w-full
                flex-col
                gap-4
                overflow-hidden
                p-4
            "
        >

            {/* Header */}
            <div
                className="
                    flex
                    shrink-0
                    items-center
                    justify-between
                "
            >

                <div>

                    <h1
                        className="
                            text-xl
                            font-semibold
                            text-slate-100
                        "
                    >
                        Camera Control
                    </h1>

                    <p
                        className="
                            text-sm
                            text-slate-400
                        "
                    >
                        Imaging camera control and acquisition
                    </p>

                </div>


                <div
                    className="
                        flex
                        items-center
                        gap-2
                        rounded-lg
                        border
                        border-slate-800
                        bg-slate-900
                        px-3
                        py-2
                    "
                >

                    <span
                        className="
                            h-2.5
                            w-2.5
                            rounded-full
                            bg-red-500
                        "
                    />

                    <span
                        className="
                            text-sm
                            text-slate-300
                        "
                    >
                        Disconnected
                    </span>

                </div>

            </div>


            {/* Camera */}
            <div
                className="
                    min-h-0
                    flex-1
                    overflow-hidden
                "
            >
                <CameraWidget />
            </div>

        </div>
    );
}