import {
    useEffect,
    useState,
} from "react";

import {
    getHomeStatus,
    getMountInfo,
    getMountTime,
    seekHome,
    seekHomeAlign,
    setMountSite,
    syncMountTime,
} from "../../api/mount_setup";

import type {
    MountInformation,
    MountTimeData,
} from "../../api/mount_setup";

import type {
    ObservatorySettings,
} from "../../api/settings";


interface Props {
    settings: ObservatorySettings;
}


export default function MountSetupSettings({
    settings,
}: Props) {

    const [
        info,
        setInfo,
    ] =
        useState<MountInformation | null>(
            null
        );

    const [
        time,
        setTime,
    ] =
        useState<MountTimeData | null>(
            null
        );

    const [
        home,
        setHome,
    ] =
        useState<string | null>(
            null
        );

    const [
        message,
        setMessage,
    ] =
        useState<string | null>(
            null
        );

    const [
        busy,
        setBusy,
    ] =
        useState(false);


    async function refresh() {

        try {

            const [
                infoResponse,
                timeResponse,
            ] =
                await Promise.all([
                    getMountInfo(),
                    getMountTime(),
                ]);


            setInfo(
                infoResponse.data
            );

            setTime(
                timeResponse.data
            );


            const homeResponse =
                await getHomeStatus();


            setHome(
                String(
                    homeResponse.data
                )
            );

        } catch (error) {

            setMessage(
                error instanceof Error
                    ? error.message
                    : "Unable to read mount setup"
            );

        }

    }


    useEffect(() => {

        const timer =
            window.setTimeout(
                () => {
                    void refresh();
                },
                0
            );


        return () => {

            window.clearTimeout(
                timer
            );

        };

    }, []);


    async function act(
        fn: () => Promise<unknown>,
        success: string
    ) {

        setBusy(true);

        setMessage(null);


        try {

            await fn();

            setMessage(
                success
            );

            await refresh();

        } catch (error) {

            setMessage(
                error instanceof Error
                    ? error.message
                    : "Mount command failed"
            );

        } finally {

            setBusy(false);

        }

    }


    const button =
        "rounded-lg border border-violet-500/30 bg-violet-500/10 px-4 py-2 text-sm text-violet-300 hover:bg-violet-500/20 disabled:opacity-50";


    return (

        <section
            className="
                space-y-5
                rounded-xl
                border
                border-slate-800
                bg-slate-900/40
                p-5
            "
        >

            <h2
                className="
                    text-lg
                    font-semibold
                    text-slate-100
                "
            >
                Mount Setup
            </h2>


            <div
                className="
                    grid
                    gap-3
                    md:grid-cols-3
                "
            >

                <div
                    className="
                        rounded-lg
                        bg-slate-800/60
                        p-3
                    "
                >

                    <div
                        className="
                            text-xs
                            text-slate-500
                        "
                    >
                        Product
                    </div>

                    <div
                        className="
                            mt-1
                            text-sm
                            text-slate-200
                        "
                    >
                        {info?.product ?? "—"}
                    </div>

                </div>


                <div
                    className="
                        rounded-lg
                        bg-slate-800/60
                        p-3
                    "
                >

                    <div
                        className="
                            text-xs
                            text-slate-500
                        "
                    >
                        Firmware
                    </div>

                    <div
                        className="
                            mt-1
                            text-sm
                            text-slate-200
                        "
                    >
                        {info?.firmware ?? "—"}
                    </div>

                </div>


                <div
                    className="
                        rounded-lg
                        bg-slate-800/60
                        p-3
                    "
                >

                    <div
                        className="
                            text-xs
                            text-slate-500
                        "
                    >
                        Home status
                    </div>

                    <div
                        className="
                            mt-1
                            text-sm
                            text-slate-200
                        "
                    >
                        {home ?? "—"}
                    </div>

                </div>

            </div>


            <div>

                <h3
                    className="
                        mb-2
                        font-medium
                        text-slate-200
                    "
                >
                    Site configuration
                </h3>

                <p
                    className="
                        mb-3
                        text-sm
                        text-slate-500
                    "
                >
                    Push the Observatory values above
                    into the TenMicron mount.
                </p>

                <button
                    className={button}
                    disabled={busy}
                    onClick={() => {

                        void act(
                            () =>
                                setMountSite(
                                    settings.latitude,
                                    settings.longitude,
                                    settings.elevation_m
                                ),
                            "Mount site configuration updated"
                        );

                    }}
                >
                    Apply Site to Mount
                </button>

            </div>


            <div>

                <h3
                    className="
                        mb-2
                        font-medium
                        text-slate-200
                    "
                >
                    Clock
                </h3>

                <div
                    className="
                        mb-3
                        grid
                        gap-2
                        text-sm
                        md:grid-cols-2
                    "
                >

                    <div>
                        Mount UTC:{" "}
                        <span
                            className="
                                text-slate-300
                            "
                        >
                            {time?.mount_utc ?? "—"}
                        </span>
                    </div>

                    <div>
                        Computer UTC:{" "}
                        <span
                            className="
                                text-slate-300
                            "
                        >
                            {time?.computer_utc ?? "—"}
                        </span>
                    </div>

                </div>


                <button
                    className={button}
                    disabled={busy}
                    onClick={() => {

                        if (
                            window.confirm(
                                "Set the mount UTC clock to the computer UTC time?"
                            )
                        ) {

                            void act(
                                syncMountTime,
                                "Mount UTC clock synchronised"
                            );

                        }

                    }}
                >
                    Sync Mount Clock
                </button>

            </div>


            <div>

                <h3
                    className="
                        mb-2
                        font-medium
                        text-slate-200
                    "
                >
                    Home
                </h3>

                <div
                    className="
                        flex
                        flex-wrap
                        gap-3
                    "
                >

                    <button
                        className={button}
                        disabled={busy}
                        onClick={() => {

                            if (
                                window.confirm(
                                    "Start the mount home search?"
                                )
                            ) {

                                void act(
                                    seekHome,
                                    "Home search started"
                                );

                            }

                        }}
                    >
                        Find Home
                    </button>


                    <button
                        className={button}
                        disabled={busy}
                        onClick={() => {

                            if (
                                window.confirm(
                                    "Start home search and apply stored home alignment?"
                                )
                            ) {

                                void act(
                                    seekHomeAlign,
                                    "Home search/alignment started"
                                );

                            }

                        }}
                    >
                        Find Home + Align
                    </button>

                </div>

            </div>


            {message && (

                <div
                    className="
                        rounded-lg
                        border
                        border-slate-700
                        bg-slate-800
                        px-3
                        py-2
                        text-sm
                        text-slate-300
                    "
                >
                    {message}
                </div>

            )}

        </section>

    );

}