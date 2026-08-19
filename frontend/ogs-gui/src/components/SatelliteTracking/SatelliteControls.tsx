import {
    useEffect,
    useMemo,
    useState,
} from "react";

import {
    Search,
    Trash2,
    Square,
    ChevronDown,
} from "lucide-react";

import DashboardStatusCard
    from "../Common/DashboardStatusCard";

import {
    slewToSatellite,
    predictSatellitePass,
    getCurrentJulianDate,
    listSatellites,
    stopSatelliteTracking,
    deleteSatellite,
    deleteAllSatellites,
} from "../../api/satellite";

import type {
    SatelliteRecord,
} from "../../api/satellite";


export default function SatelliteControls() {

    const [
        satellites,
        setSatellites,
    ] = useState<
        SatelliteRecord[]
    >([]);


    const [
        search,
        setSearch,
    ] = useState("");


    const [
        searchOpen,
        setSearchOpen,
    ] = useState(false);


    const [
        selectedSatellite,
        setSelectedSatellite,
    ] = useState<
        SatelliteRecord | null
    >(null);


    const [
        predictionMinutes,
        setPredictionMinutes,
    ] = useState(60);


    const [
        action,
        setAction,
    ] = useState<
        string | null
    >(null);


    const [
        message,
        setMessage,
    ] = useState<
        string | null
    >(null);


    const [
        passStart,
        setPassStart,
    ] = useState<
        number | null
    >(null);


    const [
        passEnd,
        setPassEnd,
    ] = useState<
        number | null
    >(null);


    /*
     * Load stored satellites.
     */
    useEffect(() => {

        async function load() {

            try {

                const result =
                    await listSatellites();


                setSatellites(
                    result
                );


            } catch (error) {

                console.error(
                    "Unable to load satellites:",
                    error
                );


                setMessage(
                    "Unable to load stored satellites."
                );
            }
        }


        load();

    }, []);


    /*
     * Filter satellites based on
     * the text typed into the selector.
     */
    const filteredSatellites =
        useMemo(() => {

            const query =
                search
                    .trim()
                    .toLowerCase();


            if (!query) {

                return satellites;
            }


            /*
             * If the selected satellite's
             * name is currently in the field,
             * show all satellites when the
             * selector is reopened.
             */
            if (
                selectedSatellite
                &&
                query ===
                selectedSatellite.name
                    .toLowerCase()
            ) {

                return satellites;
            }


            return satellites.filter(
                satellite =>
                    satellite.name
                        .toLowerCase()
                        .includes(query)
            );

        }, [
            satellites,
            search,
            selectedSatellite,
        ]);


    /*
     * Select a satellite from the
     * search results.
     */
    function selectSatellite(
        satellite:
            SatelliteRecord
    ) {

        setSelectedSatellite(
            satellite
        );


        setSearch(
            satellite.name
        );


        setSearchOpen(
            false
        );


        setMessage(null);
        setPassStart(null);
        setPassEnd(null);
    }


    /*
     * Clear the currently selected
     * satellite.
     */
    function clearSelection() {

        setSelectedSatellite(
            null
        );


        setSearch("");


        setSearchOpen(
            true
        );


        setMessage(null);
        setPassStart(null);
        setPassEnd(null);
    }


    /*
     * Slew / track selected satellite.
     */
    async function handleSlew() {

        if (!selectedSatellite) {

            setMessage(
                "Select a satellite first."
            );

            return;
        }


        setAction("slew");
        setMessage(null);


        try {

            const result =
                await slewToSatellite(
                    selectedSatellite.id
                );


            setMessage(
                result.data.message
            );


        } catch (error) {

            if (
                error instanceof Error
            ) {

                setMessage(
                    error.message
                );

            } else {

                setMessage(
                    "Failed to slew to satellite."
                );
            }


        } finally {

            setAction(null);
        }
    }


    /*
     * Predict satellite pass.
     */
    async function handlePrediction() {

        if (!selectedSatellite) {

            setMessage(
                "Select a satellite first."
            );

            return;
        }


        if (
            predictionMinutes < 1
            ||
            predictionMinutes > 1440
        ) {

            setMessage(
                "Prediction window must be between 1 and 1440 minutes."
            );

            return;
        }


        setAction("predict");
        setMessage(null);


        try {

            const result =
                await predictSatellitePass(
                    selectedSatellite.id,
                    getCurrentJulianDate(),
                    predictionMinutes
                );


            if (!result.data.found) {

                setPassStart(null);
                setPassEnd(null);


                setMessage(
                    "No pass found in the selected time window."
                );

                return;
            }


            setPassStart(
                result.data.start_jd
            );


            setPassEnd(
                result.data.end_jd
            );


            setMessage(
                "Satellite pass found."
            );


        } catch (error) {

            if (
                error instanceof Error
            ) {

                setMessage(
                    error.message
                );

            } else {

                setMessage(
                    "Failed to predict satellite pass."
                );
            }


        } finally {

            setAction(null);
        }
    }


    /*
     * Stop satellite tracking.
     */
    async function handleStopTracking() {

        setAction("stop");
        setMessage(null);


        try {

            const result =
                await stopSatelliteTracking();


            setMessage(
                result.data.message
            );


        } catch (error) {

            if (
                error instanceof Error
            ) {

                setMessage(
                    error.message
                );

            } else {

                setMessage(
                    "Failed to stop satellite tracking."
                );
            }


        } finally {

            setAction(null);
        }
    }


    /*
     * Delete selected satellite.
     */
    async function handleDeleteSatellite() {

        if (!selectedSatellite) {

            setMessage(
                "Select a satellite first."
            );

            return;
        }


        const satelliteName =
            selectedSatellite.name;


        const satelliteId =
            selectedSatellite.id;


        const confirmed =
            window.confirm(
                `Are you sure you want to delete "${satelliteName}"?\n\nThis action cannot be undone.`
            );


        if (!confirmed) {
            return;
        }


        setAction("delete");
        setMessage(null);


        try {

            await deleteSatellite(
                satelliteId
            );


            setSatellites(
                current =>
                    current.filter(
                        satellite =>
                            satellite.id !==
                            satelliteId
                    )
            );


            setSelectedSatellite(
                null
            );


            setSearch("");


            setSearchOpen(
                false
            );


            setPassStart(null);
            setPassEnd(null);


            setMessage(
                `Satellite deleted: ${satelliteName}`
            );


        } catch (error) {

            if (
                error instanceof Error
            ) {

                setMessage(
                    error.message
                );

            } else {

                setMessage(
                    "Failed to delete satellite."
                );
            }


        } finally {

            setAction(null);
        }
    }


    /*
     * Delete every stored satellite.
     */
    async function handleDeleteAllSatellites() {

        if (satellites.length === 0) {

            setMessage(
                "There are no satellites to delete."
            );

            return;
        }


        const confirmed =
            window.confirm(
                `Are you sure you want to delete all ${satellites.length} stored satellites?\n\nThis action cannot be undone.`
            );


        if (!confirmed) {
            return;
        }


        setAction("delete-all");
        setMessage(null);


        try {

            const result =
                await deleteAllSatellites();


            setSatellites([]);

            setSelectedSatellite(
                null
            );

            setSearch("");

            setSearchOpen(
                false
            );

            setPassStart(null);
            setPassEnd(null);


            setMessage(
                result.message
            );


        } catch (error) {

            if (
                error instanceof Error
            ) {

                setMessage(
                    error.message
                );

            } else {

                setMessage(
                    "Failed to delete satellites."
                );
            }


        } finally {

            setAction(null);
        }
    }


    const loading =
        action !== null;


    return (
        <DashboardStatusCard
            title="Satellite Controls"
            connected={true}
        >

            <div
                className="
                    space-y-5
                "
            >

                {/* Satellite Selector */}

                <div>

                    <label
                        htmlFor="satellite-search"
                        className="
                            mb-2
                            block
                            text-xs
                            font-medium
                            uppercase
                            tracking-wide
                            text-slate-500
                        "
                    >
                        Satellite
                    </label>


                    <div
                        className="
                            relative
                        "
                    >

                        {/* Combined Search / Dropdown */}

                        <div
                            className="
                                relative
                            "
                        >

                            <Search
                                size={16}

                                className="
                                    pointer-events-none
                                    absolute
                                    left-3
                                    top-1/2
                                    -translate-y-1/2
                                    text-slate-500
                                "
                            />


                            <input
                                id="satellite-search"

                                type="text"

                                value={
                                    search
                                }

                                onFocus={() => {

                                    setSearchOpen(
                                        true
                                    );

                                }}

                                onChange={(
                                    event
                                ) => {

                                    setSearch(
                                        event.target.value
                                    );


                                    /*
                                     * Typing changes the
                                     * selection, so clear the
                                     * previous selected object.
                                     */
                                    setSelectedSatellite(
                                        null
                                    );


                                    setSearchOpen(
                                        true
                                    );


                                    setPassStart(null);
                                    setPassEnd(null);
                                    setMessage(null);
                                }}

                                placeholder={
                                    satellites.length === 0
                                        ? "No satellites stored"
                                        : "Search or select satellite..."
                                }

                                autoComplete="off"

                                disabled={
                                    loading
                                    ||
                                    satellites.length === 0
                                }

                                className="
                                    w-full
                                    rounded-lg
                                    border
                                    border-slate-700
                                    bg-slate-800
                                    py-2.5
                                    pl-10
                                    pr-10
                                    text-sm
                                    text-slate-100
                                    outline-none
                                    transition
                                    placeholder:text-slate-600
                                    focus:border-violet-500
                                    focus:ring-2
                                    focus:ring-violet-500/20
                                    disabled:cursor-not-allowed
                                    disabled:opacity-50
                                "
                            />


                            <button
                                type="button"

                                aria-label={
                                    searchOpen
                                        ? "Close satellite list"
                                        : "Open satellite list"
                                }

                                disabled={
                                    loading
                                    ||
                                    satellites.length === 0
                                }

                                onClick={() => {

                                    setSearchOpen(
                                        current =>
                                            !current
                                    );

                                }}

                                className="
                                    absolute
                                    right-2
                                    top-1/2
                                    flex
                                    -translate-y-1/2
                                    items-center
                                    justify-center
                                    rounded
                                    p-1
                                    text-slate-500
                                    transition
                                    hover:bg-slate-700
                                    hover:text-slate-200
                                    disabled:cursor-not-allowed
                                "
                            >

                                <ChevronDown
                                    size={17}

                                    className={
                                        searchOpen
                                            ? "rotate-180 transition-transform"
                                            : "transition-transform"
                                    }
                                />

                            </button>

                        </div>


                        {/* Search Results */}

                        {
                            searchOpen
                            &&
                            satellites.length > 0
                            &&
                            (

                                <div
                                    className="
                                        absolute
                                        z-50
                                        mt-1
                                        max-h-60
                                        w-full
                                        overflow-y-auto
                                        rounded-lg
                                        border
                                        border-slate-700
                                        bg-slate-900
                                        shadow-xl
                                    "
                                >

                                    {
                                        filteredSatellites
                                            .length > 0
                                            ? (

                                                filteredSatellites
                                                    .map(
                                                        satellite => (

                                                            <button
                                                                key={
                                                                    satellite.id
                                                                }

                                                                type="button"

                                                                onMouseDown={(
                                                                    event
                                                                ) => {

                                                                    /*
                                                                     * Prevent input
                                                                     * from losing focus
                                                                     * before click.
                                                                     */
                                                                    event
                                                                        .preventDefault();

                                                                }}

                                                                onClick={() => {

                                                                    selectSatellite(
                                                                        satellite
                                                                    );

                                                                }}

                                                                className="
                                                                    block
                                                                    w-full
                                                                    border-b
                                                                    border-slate-800
                                                                    px-3
                                                                    py-2.5
                                                                    text-left
                                                                    text-sm
                                                                    text-slate-200
                                                                    transition
                                                                    last:border-b-0
                                                                    hover:bg-violet-500/10
                                                                    hover:text-violet-300
                                                                "
                                                            >

                                                                {
                                                                    satellite.name
                                                                }

                                                            </button>

                                                        )
                                                    )

                                            )
                                            : (

                                                <div
                                                    className="
                                                        px-3
                                                        py-3
                                                        text-sm
                                                        text-slate-500
                                                    "
                                                >
                                                    No matching satellites
                                                </div>

                                            )
                                    }

                                </div>

                            )
                        }

                    </div>


                    {/* Satellite count */}

                    {
                        satellites.length > 0
                        &&
                        (

                            <p
                                className="
                                    mt-2
                                    text-xs
                                    text-slate-500
                                "
                            >

                                {
                                    selectedSatellite
                                        ? `${satellites.length} stored satellites`
                                        : search.trim()
                                            ? `${filteredSatellites.length} of ${satellites.length} satellites shown`
                                            : `${satellites.length} stored satellites`
                                }

                            </p>

                        )
                    }


                    {/* Delete Controls */}

                    <div
                        className="
                            mt-3
                            grid
                            grid-cols-2
                            gap-3
                        "
                    >

                        <button
                            type="button"

                            onClick={
                                handleDeleteSatellite
                            }

                            disabled={
                                loading
                                ||
                                !selectedSatellite
                            }

                            className="
                                flex
                                items-center
                                justify-center
                                gap-2
                                rounded-lg
                                border
                                border-red-500/30
                                bg-red-500/10
                                px-3
                                py-2
                                text-sm
                                font-medium
                                text-red-300
                                transition
                                hover:bg-red-500/20
                                disabled:cursor-not-allowed
                                disabled:opacity-50
                            "
                        >

                            <Trash2
                                size={15}
                            />

                            {
                                action === "delete"
                                    ? "Deleting..."
                                    : "Delete Selected"
                            }

                        </button>


                        <button
                            type="button"

                            onClick={
                                handleDeleteAllSatellites
                            }

                            disabled={
                                loading
                                ||
                                satellites.length === 0
                            }

                            className="
                                flex
                                items-center
                                justify-center
                                gap-2
                                rounded-lg
                                border
                                border-red-500/40
                                bg-red-500/15
                                px-3
                                py-2
                                text-sm
                                font-medium
                                text-red-300
                                transition
                                hover:bg-red-500/25
                                disabled:cursor-not-allowed
                                disabled:opacity-50
                            "
                        >

                            <Trash2
                                size={15}
                            />

                            {
                                action === "delete-all"
                                    ? "Deleting..."
                                    : "Delete All"
                            }

                        </button>

                    </div>

                </div>


                {/* Selected Satellite */}

                {
                    selectedSatellite
                    &&
                    (

                        <div
                            className="
                                flex
                                items-center
                                justify-between
                                rounded-lg
                                border
                                border-violet-500/20
                                bg-violet-500/10
                                px-3
                                py-2
                            "
                        >

                            <div>

                                <p
                                    className="
                                        text-xs
                                        text-slate-500
                                    "
                                >
                                    Selected
                                </p>


                                <p
                                    className="
                                        text-sm
                                        font-medium
                                        text-violet-300
                                    "
                                >

                                    {
                                        selectedSatellite.name
                                    }

                                </p>

                            </div>


                            <button
                                type="button"

                                onClick={
                                    clearSelection
                                }

                                disabled={
                                    loading
                                }

                                className="
                                    text-xs
                                    text-slate-500
                                    transition
                                    hover:text-slate-200
                                    disabled:cursor-not-allowed
                                    disabled:opacity-50
                                "
                            >
                                Change
                            </button>

                        </div>

                    )
                }


                {/* Prediction */}

                <div>

                    <label
                        htmlFor="prediction-minutes"
                        className="
                            mb-2
                            block
                            text-xs
                            font-medium
                            uppercase
                            tracking-wide
                            text-slate-500
                        "
                    >
                        Prediction Window
                    </label>


                    <div
                        className="
                            flex
                            items-center
                            gap-3
                        "
                    >

                        <input
                            id="prediction-minutes"

                            type="number"

                            min="1"
                            max="1440"

                            value={
                                predictionMinutes
                            }

                            onChange={(
                                event
                            ) => {

                                setPredictionMinutes(
                                    Number(
                                        event
                                            .target
                                            .value
                                    )
                                );

                            }}

                            disabled={
                                loading
                            }

                            className="
                                flex-1
                                rounded-lg
                                border
                                border-slate-700
                                bg-slate-800
                                px-3
                                py-2
                                text-slate-100
                                outline-none
                                focus:border-violet-500
                                focus:ring-2
                                focus:ring-violet-500/20
                                disabled:cursor-not-allowed
                                disabled:opacity-50
                            "
                        />


                        <span
                            className="
                                text-sm
                                text-slate-500
                            "
                        >
                            minutes
                        </span>

                    </div>

                </div>


                {/* Main Actions */}

                <div
                    className="
                        grid
                        grid-cols-2
                        gap-3
                    "
                >

                    <button
                        type="button"

                        onClick={
                            handlePrediction
                        }

                        disabled={
                            loading
                            ||
                            !selectedSatellite
                        }

                        className="
                            rounded-lg
                            border
                            border-violet-500/30
                            bg-violet-500/10
                            px-4
                            py-2.5
                            text-sm
                            font-medium
                            text-violet-300
                            transition
                            hover:bg-violet-500/20
                            disabled:cursor-not-allowed
                            disabled:opacity-50
                        "
                    >

                        {
                            action === "predict"
                                ? "Predicting..."
                                : "Predict Pass"
                        }

                    </button>


                    <button
                        type="button"

                        onClick={
                            handleSlew
                        }

                        disabled={
                            loading
                            ||
                            !selectedSatellite
                        }

                        className="
                            rounded-lg
                            bg-violet-600
                            px-4
                            py-2.5
                            text-sm
                            font-medium
                            text-white
                            transition
                            hover:bg-violet-500
                            disabled:cursor-not-allowed
                            disabled:opacity-50
                        "
                    >

                        {
                            action === "slew"
                                ? "Starting..."
                                : "Track Satellite"
                        }

                    </button>

                </div>


                {/* Stop Tracking */}

                <button
                    type="button"

                    onClick={
                        handleStopTracking
                    }

                    disabled={
                        loading
                    }

                    className="
                        flex
                        w-full
                        items-center
                        justify-center
                        gap-2
                        rounded-lg
                        border
                        border-red-500/30
                        bg-red-500/10
                        px-4
                        py-2.5
                        text-sm
                        font-medium
                        text-red-300
                        transition
                        hover:bg-red-500/20
                        disabled:cursor-not-allowed
                        disabled:opacity-50
                    "
                >

                    <Square
                        size={14}
                    />


                    {
                        action === "stop"
                            ? "Stopping..."
                            : "Stop Tracking"
                    }

                </button>


                {/* Pass Result */}

                {
                    (
                        passStart !== null
                        ||
                        passEnd !== null
                    )
                    &&
                    (

                        <div
                            className="
                                rounded-lg
                                border
                                border-slate-700
                                bg-slate-800/50
                                p-4
                            "
                        >

                            <p
                                className="
                                    mb-3
                                    text-xs
                                    font-medium
                                    uppercase
                                    tracking-wide
                                    text-slate-500
                                "
                            >
                                Predicted Pass
                            </p>


                            <div
                                className="
                                    grid
                                    grid-cols-2
                                    gap-4
                                    text-sm
                                "
                            >

                                <div>

                                    <p
                                        className="
                                            text-slate-500
                                        "
                                    >
                                        Start JD
                                    </p>


                                    <p
                                        className="
                                            mt-1
                                            font-mono
                                            text-slate-200
                                        "
                                    >

                                        {
                                            passStart
                                                ?.toFixed(
                                                    6
                                                )
                                        }

                                    </p>

                                </div>


                                <div>

                                    <p
                                        className="
                                            text-slate-500
                                        "
                                    >
                                        End JD
                                    </p>


                                    <p
                                        className="
                                            mt-1
                                            font-mono
                                            text-slate-200
                                        "
                                    >

                                        {
                                            passEnd
                                                ?.toFixed(
                                                    6
                                                )
                                        }

                                    </p>

                                </div>

                            </div>

                        </div>

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

        </DashboardStatusCard>
    );
}