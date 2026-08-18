import {
    useEffect,
    useMemo,
    useState,
} from "react";

import {
    Search,
    Satellite,
    Square,
} from "lucide-react";

import DashboardStatusCard
    from "../Common/DashboardStatusCard";

import {
    slewToSatellite,
    predictSatellitePass,
    getCurrentJulianDate,
    listSatellites,
    stopSatelliteTracking,
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
            }
        }


        load();

    }, []);


    /*
     * Search satellites by name.
     */
    const filteredSatellites =
        useMemo(() => {

            const query =
                search
                    .trim()
                    .toLowerCase();


            if (!query) {

                return satellites
                    .slice(0, 8);
            }


            return satellites
                .filter(
                    satellite =>
                        satellite.name
                            .toLowerCase()
                            .includes(query)
                )
                .slice(0, 8);

        }, [
            satellites,
            search,
        ]);


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

        setMessage(null);
        setPassStart(null);
        setPassEnd(null);
    }


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
                    "Failed to slew to satellite"
                );
            }


        } finally {

            setAction(null);
        }
    }


    async function
    handlePrediction() {

        if (!selectedSatellite) {

            setMessage(
                "Select a satellite first."
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
                    (
                        "No pass found in the selected time window."
                    )
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
                    "Failed to predict satellite pass"
                );
            }


        } finally {

            setAction(null);
        }
    }


    async function
    handleStopTracking() {

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
                    "Failed to stop satellite tracking"
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

                {/* Satellite Search */}

                <div>

                    <label
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

                        <Search
                            size={16}
                            className="
                                absolute
                                left-3
                                top-1/2
                                -translate-y-1/2
                                text-slate-500
                            "
                        />


                        <input
                            type="text"

                            value={
                                search
                            }

                            onChange={(
                                event
                            ) => {

                                setSearch(
                                    event
                                        .target
                                        .value
                                );

                                /*
                                 * If user starts
                                 * editing again,
                                 * clear selection.
                                 */
                                if (
                                    selectedSatellite
                                    &&
                                    event
                                        .target
                                        .value
                                    !==
                                    selectedSatellite
                                        .name
                                ) {

                                    setSelectedSatellite(
                                        null
                                    );
                                }
                            }}

                            placeholder="
                                Search stored satellites...
                            "

                            className="
                                w-full
                                rounded-lg
                                border
                                border-slate-700
                                bg-slate-800
                                py-2.5
                                pl-10
                                pr-3
                                text-sm
                                text-slate-100
                                outline-none
                                transition
                                placeholder:text-slate-600
                                focus:border-violet-500
                                focus:ring-2
                                focus:ring-violet-500/20
                            "
                        />

                    </div>


                    {/* Search Results */}

                    {!selectedSatellite && (

                        <div
                            className="
                                mt-2
                                overflow-hidden
                                rounded-lg
                                border
                                border-slate-800
                                bg-slate-950/70
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

                                                        onClick={() =>
                                                            selectSatellite(
                                                                satellite
                                                            )
                                                        }

                                                        className="
                                                            flex
                                                            w-full
                                                            items-center
                                                            justify-between
                                                            border-b
                                                            border-slate-800
                                                            px-3
                                                            py-2.5
                                                            text-left
                                                            transition
                                                            last:border-b-0
                                                            hover:bg-violet-500/10
                                                        "
                                                    >

                                                        <div
                                                            className="
                                                                flex
                                                                items-center
                                                                gap-2
                                                            "
                                                        >

                                                            <Satellite
                                                                size={15}
                                                                className="
                                                                    text-violet-400
                                                                "
                                                            />


                                                            <span
                                                                className="
                                                                    text-sm
                                                                    text-slate-300
                                                                "
                                                            >
                                                                {
                                                                    satellite
                                                                        .name
                                                                }
                                                            </span>

                                                        </div>


                                                        <span
                                                            className="
                                                                font-mono
                                                                text-xs
                                                                text-slate-600
                                                            "
                                                        >
                                                            ID {
                                                                satellite.id
                                                            }
                                                        </span>

                                                    </button>
                                                )
                                            )

                                    ) : (

                                        <div
                                            className="
                                                px-3
                                                py-3
                                                text-sm
                                                text-slate-500
                                            "
                                        >
                                            No matching satellites.
                                        </div>

                                    )
                            }

                        </div>

                    )}


                    {/* Selected */}

                    {selectedSatellite && (

                        <div
                            className="
                                mt-2
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
                                        selectedSatellite
                                            .name
                                    }
                                </p>

                            </div>


                            <button
                                type="button"

                                onClick={() => {

                                    setSelectedSatellite(
                                        null
                                    );

                                    setSearch("");
                                }}

                                className="
                                    text-xs
                                    text-slate-500
                                    transition
                                    hover:text-slate-200
                                "
                            >
                                Change
                            </button>

                        </div>

                    )}

                </div>


                {/* Prediction */}

                <div>

                    <label
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
                            type="number"
                            min="1"
                            max="1440"

                            value={
                                predictionMinutes
                            }

                            onChange={(
                                event
                            ) =>
                                setPredictionMinutes(
                                    Number(
                                        event
                                            .target
                                            .value
                                    )
                                )
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
                            action ===
                            "predict"
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
                            action ===
                            "slew"
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

                {(
                    passStart !== null
                    ||
                    passEnd !== null
                ) && (

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

                )}


                {/* Feedback */}

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

            </div>

        </DashboardStatusCard>
    );
}