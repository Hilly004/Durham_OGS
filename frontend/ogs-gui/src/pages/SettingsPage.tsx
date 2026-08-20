import {
    useEffect,
    useState,
} from "react";

import {
    Save,
} from "lucide-react";

import {
    getSettings,
    saveSettings,
} from "../api/settings";

import type {
    ObservatorySettings,
} from "../api/settings";

import ObservatorySettingsSection
    from "../components/Settings/ObservatorySettings";

import ConnectionSettings
    from "../components/Settings/ConnectionSettings";

import SafetySettings
    from "../components/Settings/SafetySettings";

import MountSetupSettings
    from "../components/Settings/MountSetupSettings";

import MountAlignmentSettings
    from "../components/Settings/MountAlignmentSettings";

import SystemSettings
    from "../components/Settings/SystemSettings";


type Tab =
    | "general"
    | "connections"
    | "safety"
    | "mount"
    | "alignment"
    | "system";


export default function SettingsPage() {

    const [
        settings,
        setSettings,
    ] = useState<
        ObservatorySettings | null
    >(null);


    const [
        tab,
        setTab,
    ] = useState<Tab>(
        "general"
    );


    const [
        loading,
        setLoading,
    ] = useState(true);


    const [
        saving,
        setSaving,
    ] = useState(false);


    const [
        message,
        setMessage,
    ] = useState<
        string | null
    >(null);


    /*
     * Load saved settings.
     */
    useEffect(() => {

        async function loadSettings() {

            try {

                const result =
                    await getSettings();


                setSettings(
                    result
                );


            } catch (error) {

                setMessage(
                    error instanceof Error
                        ? error.message
                        : "Unable to load settings"
                );


            } finally {

                setLoading(
                    false
                );
            }
        }


        void loadSettings();

    }, []);


    /*
     * Update one setting locally.
     */
    function change(
        key:
            keyof ObservatorySettings,

        value:
            string
            | number
            | boolean
    ) {

        setSettings(
            current => {

                if (!current) {
                    return current;
                }


                return {
                    ...current,
                    [key]: value,
                };
            }
        );


        setMessage(null);
    }


    /*
     * Save all persistent settings.
     */
    async function save() {

        if (!settings) {
            return;
        }


        setSaving(true);
        setMessage(null);


        try {

            const {
                id: _id,
                ...payload
            } = settings;


            const result =
                await saveSettings(
                    payload
                );


            setSettings(
                result
            );


            setMessage(
                "Settings saved."
            );


        } catch (error) {

            setMessage(
                error instanceof Error
                    ? error.message
                    : "Unable to save settings"
            );


        } finally {

            setSaving(false);
        }
    }


    /*
     * Loading state.
     */
    if (loading) {

        return (

            <div
                className="
                    flex
                    h-full
                    items-center
                    justify-center
                    p-6
                    text-slate-400
                "
            >
                Loading settings...
            </div>
        );
    }


    /*
     * Failed to load settings.
     */
    if (!settings) {

        return (

            <div
                className="
                    h-full
                    overflow-y-auto
                    p-6
                    text-red-300
                "
            >
                {
                    message
                    ??
                    "Settings unavailable"
                }
            </div>
        );
    }


    const tabs:
        Array<[Tab, string]> =
    [
        [
            "general",
            "General",
        ],

        [
            "connections",
            "Connections",
        ],

        [
            "safety",
            "Safety",
        ],

        [
            "mount",
            "Mount Setup",
        ],

        [
            "alignment",
            "Alignment",
        ],

        [
            "system",
            "System",
        ],
    ];


    return (

        /*
         * Main scrolling container.
         *
         * h-full:
         * Uses the available dashboard height.
         *
         * overflow-y-auto:
         * Enables vertical scrolling when
         * settings content is taller than
         * the available area.
         */
        <div
            className="
                h-full
                min-h-0
                overflow-y-auto
                overscroll-contain
            "
        >

            {/*
             * Inner content container.
             *
             * pb-12 gives the final section
             * breathing room at the bottom.
             */}
            <div
                className="
                    space-y-5
                    p-6
                    pb-12
                "
            >

                {/* Page Header */}

                <div
                    className="
                        flex
                        flex-wrap
                        items-center
                        justify-between
                        gap-3
                    "
                >

                    <div>

                        <h1
                            className="
                                text-2xl
                                font-semibold
                                text-slate-100
                            "
                        >
                            Settings
                        </h1>


                        <p
                            className="
                                mt-1
                                text-sm
                                text-slate-500
                            "
                        >
                            Configure the observatory,
                            hardware connections,
                            safety and mount alignment.
                        </p>

                    </div>


                    <button
                        type="button"

                        onClick={
                            save
                        }

                        disabled={
                            saving
                        }

                        className="
                            flex
                            items-center
                            gap-2
                            rounded-lg
                            bg-violet-600
                            px-4
                            py-2
                            text-sm
                            font-medium
                            text-white
                            transition
                            hover:bg-violet-500
                            disabled:cursor-not-allowed
                            disabled:opacity-50
                        "
                    >

                        <Save
                            size={16}
                        />


                        {
                            saving
                                ? "Saving..."
                                : "Save Settings"
                        }

                    </button>

                </div>


                {/* Tabs */}

                <div
                    className="
                        flex
                        flex-wrap
                        gap-2
                        border-b
                        border-slate-800
                        pb-3
                    "
                >

                    {
                        tabs.map(
                            ([
                                value,
                                label,
                            ]) => (

                                <button
                                    key={
                                        value
                                    }

                                    type="button"

                                    onClick={
                                        () =>
                                            setTab(
                                                value
                                            )
                                    }

                                    className={
                                        `
                                            rounded-lg
                                            px-3
                                            py-2
                                            text-sm
                                            transition
                                            ${
                                                tab === value
                                                    ? `
                                                        bg-violet-500/15
                                                        text-violet-300
                                                    `
                                                    : `
                                                        text-slate-400
                                                        hover:bg-slate-800
                                                        hover:text-slate-200
                                                    `
                                            }
                                        `
                                    }
                                >
                                    {label}
                                </button>

                            )
                        )
                    }

                </div>


                {/* General */}

                {
                    tab === "general"
                    &&
                    (

                        <ObservatorySettingsSection
                            settings={
                                settings
                            }

                            onChange={
                                change
                            }
                        />

                    )
                }


                {/* Connections */}

                {
                    tab === "connections"
                    &&
                    (

                        <ConnectionSettings
                            settings={
                                settings
                            }

                            onChange={
                                change
                            }
                        />

                    )
                }


                {/* Safety */}

                {
                    tab === "safety"
                    &&
                    (

                        <SafetySettings
                            settings={
                                settings
                            }

                            onChange={
                                change
                            }
                        />

                    )
                }


                {/* Mount Setup */}

                {
                    tab === "mount"
                    &&
                    (

                        <MountSetupSettings
                            settings={
                                settings
                            }
                        />

                    )
                }


                {/* Alignment */}

                {
                    tab === "alignment"
                    &&
                    (

                        <MountAlignmentSettings />

                    )
                }


                {/* System */}

                {
                    tab === "system"
                    &&
                    (

                        <SystemSettings
                            settings={
                                settings
                            }

                            onChange={
                                change
                            }
                        />

                    )
                }


                {/* Feedback */}

                {
                    message
                    &&
                    (

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

                    )
                }

            </div>

        </div>
    );
}