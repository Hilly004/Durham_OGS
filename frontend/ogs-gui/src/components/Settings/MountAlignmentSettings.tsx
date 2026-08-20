import {
    useEffect,
    useMemo,
    useState,
} from "react";

import {
    ArrowDown,
    ArrowLeft,
    ArrowRight,
    ArrowUp,
    Crosshair,
    Trash2,
} from "lucide-react";

import {
    addAlignmentPoint,
    deleteAlignmentModel,
    deleteAlignmentPoint,
    deleteSavedModel,
    getAlignment,
    getSavedModels,
    loadModel,
    nudgeAlignmentMount,
    saveModel,
    slewToAlignmentTarget,
} from "../../api/mount_setup";

import type {
    AlignmentData,
} from "../../api/mount_setup";


type AlignmentStep =
    | "target"
    | "centering"
    | "ready";


function parseRa(
    value: string
): number | null {

    const text =
        value.trim();


    if (!text) {
        return null;
    }


    /*
     * Decimal hours.
     */
    if (!text.includes(":")) {

        const result =
            Number(text);


        if (
            Number.isFinite(
                result
            )
            &&
            result >= 0
            &&
            result < 24
        ) {

            return result;
        }


        return null;
    }


    /*
     * HH:MM or HH:MM:SS
     */
    const parts =
        text.split(":");


    if (
        parts.length < 2
        ||
        parts.length > 3
    ) {

        return null;
    }


    const hours =
        Number(parts[0]);

    const minutes =
        Number(parts[1]);

    const seconds =
        parts.length === 3
            ? Number(parts[2])
            : 0;


    if (
        !Number.isFinite(hours)
        ||
        !Number.isFinite(minutes)
        ||
        !Number.isFinite(seconds)
    ) {

        return null;
    }


    if (
        hours < 0
        ||
        hours >= 24
        ||
        minutes < 0
        ||
        minutes >= 60
        ||
        seconds < 0
        ||
        seconds >= 60
    ) {

        return null;
    }


    return (
        hours
        +
        minutes / 60
        +
        seconds / 3600
    );
}


function parseDec(
    value: string
): number | null {

    const text =
        value
            .trim()
            .replace("°", "")
            .replace("*", ":");


    if (!text) {
        return null;
    }


    /*
     * Decimal degrees.
     */
    if (!text.includes(":")) {

        const result =
            Number(text);


        if (
            Number.isFinite(
                result
            )
            &&
            result >= -90
            &&
            result <= 90
        ) {

            return result;
        }


        return null;
    }


    const negative =
        text.startsWith("-");


    const clean =
        text.replace(
            /^[+-]/,
            ""
        );


    const parts =
        clean.split(":");


    if (
        parts.length < 2
        ||
        parts.length > 3
    ) {

        return null;
    }


    const degrees =
        Number(parts[0]);

    const minutes =
        Number(parts[1]);

    const seconds =
        parts.length === 3
            ? Number(parts[2])
            : 0;


    if (
        !Number.isFinite(degrees)
        ||
        !Number.isFinite(minutes)
        ||
        !Number.isFinite(seconds)
    ) {

        return null;
    }


    if (
        degrees < 0
        ||
        degrees > 90
        ||
        minutes < 0
        ||
        minutes >= 60
        ||
        seconds < 0
        ||
        seconds >= 60
    ) {

        return null;
    }


    let result =
        (
            degrees
            +
            minutes / 60
            +
            seconds / 3600
        );


    if (negative) {

        result *= -1;
    }


    if (
        result < -90
        ||
        result > 90
    ) {

        return null;
    }


    return result;
}


function errorQuality(
    error: number
) {

    if (error < 30) {

        return {
            label: "Good",

            className:
                "text-emerald-300",
        };
    }


    if (error <= 60) {

        return {
            label: "Review",

            className:
                "text-amber-300",
        };
    }


    return {
        label: "Poor",

        className:
            "text-red-300",
    };
}


export default function
MountAlignmentSettings() {

    const [
        alignment,
        setAlignment,
    ] = useState<
        AlignmentData | null
    >(null);


    const [
        models,
        setModels,
    ] = useState<
        string[]
    >([]);


    const [
        modelName,
        setModelName,
    ] = useState("");


    const [
        starName,
        setStarName,
    ] = useState("");


    const [
        ra,
        setRa,
    ] = useState("");


    const [
        dec,
        setDec,
    ] = useState("");


    const [
        step,
        setStep,
    ] = useState<
        AlignmentStep
    >("target");


    const [
        nudgeSize,
        setNudgeSize,
    ] = useState(30);


    const [
        busy,
        setBusy,
    ] = useState(false);


    const [
        message,
        setMessage,
    ] = useState<
        string | null
    >(null);


    const parsedRa =
        useMemo(
            () =>
                parseRa(ra),
            [ra]
        );


    const parsedDec =
        useMemo(
            () =>
                parseDec(dec),
            [dec]
        );


    const targetValid =
        (
            parsedRa !== null
            &&
            parsedDec !== null
        );


    async function refresh() {

        try {

            const alignmentResult =
                await getAlignment();


            setAlignment(
                alignmentResult.data
            );


            const modelResult =
                await getSavedModels();


            setModels(
                modelResult.data
                ??
                []
            );


        } catch (error) {

            setMessage(
                error instanceof Error
                    ? error.message
                    : (
                        "Unable to load alignment information."
                    )
            );
        }
    }


    useEffect(() => {

        void refresh();

    }, []);


    async function runAction(
        action:
            () => Promise<unknown>,

        successMessage: string
    ) {

        setBusy(true);
        setMessage(null);


        try {

            await action();


            setMessage(
                successMessage
            );


            await refresh();


        } catch (error) {

            setMessage(
                error instanceof Error
                    ? error.message
                    : (
                        "Alignment command failed."
                    )
            );


        } finally {

            setBusy(false);
        }
    }


    async function handleSlew() {

        if (
            parsedRa === null
            ||
            parsedDec === null
        ) {

            setMessage(
                (
                    "Enter a valid RA and Dec first."
                )
            );

            return;
        }


        setBusy(true);
        setMessage(null);


        try {

            await slewToAlignmentTarget(
                starName.trim()
                    ||
                    "Alignment star",

                parsedRa,
                parsedDec
            );


            setStep(
                "centering"
            );


            setMessage(
                (
                    "Slew started. Centre the target using the nudge controls."
                )
            );


        } catch (error) {

            setMessage(
                error instanceof Error
                    ? error.message
                    : (
                        "Unable to slew to alignment target."
                    )
            );


        } finally {

            setBusy(false);
        }
    }


    async function handleNudge(
        direction:
            | "north"
            | "south"
            | "east"
            | "west"
    ) {

        setBusy(true);
        setMessage(null);


        try {

            await nudgeAlignmentMount(
                direction,
                nudgeSize
            );


            setMessage(
                (
                    `Nudged ${direction} `
                    +
                    `${nudgeSize} arcsec.`
                )
            );


        } catch (error) {

            setMessage(
                error instanceof Error
                    ? error.message
                    : "Nudge failed."
            );


        } finally {

            setBusy(false);
        }
    }


    async function handleAddPoint() {

        if (
            parsedRa === null
            ||
            parsedDec === null
        ) {

            setMessage(
                (
                    "Alignment target coordinates are invalid."
                )
            );

            return;
        }


        const confirmed =
            window.confirm(
                (
                    "Is the alignment target accurately centred in the camera/telescope?"
                )
            );


        if (!confirmed) {
            return;
        }


        setBusy(true);
        setMessage(null);


        try {

            await addAlignmentPoint(
                starName.trim()
                    ||
                    "Alignment star",

                parsedRa,
                parsedDec
            );


            setMessage(
                (
                    "Alignment point added"
                    +
                    (
                        starName.trim()
                            ? `: ${starName.trim()}`
                            : "."
                    )
                )
            );


            setStarName("");
            setRa("");
            setDec("");


            setStep(
                "target"
            );


            await refresh();


        } catch (error) {

            setMessage(
                error instanceof Error
                    ? error.message
                    : (
                        "Unable to add alignment point."
                    )
            );


        } finally {

            setBusy(false);
        }
    }


    const inputClass =
        `
            mt-1
            w-full
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
        `;


    const buttonClass =
        `
            rounded-lg
            border
            border-violet-500/30
            bg-violet-500/10
            px-3
            py-2
            text-sm
            font-medium
            text-violet-300
            transition
            hover:bg-violet-500/20
            disabled:cursor-not-allowed
            disabled:opacity-50
        `;


    const nudgeButtonClass =
        `
            flex
            h-11
            w-11
            items-center
            justify-center
            rounded-lg
            border
            border-slate-700
            bg-slate-800
            text-slate-200
            transition
            hover:border-violet-500/40
            hover:bg-violet-500/10
            hover:text-violet-300
            disabled:cursor-not-allowed
            disabled:opacity-50
        `;


    return (

        <section
            className="
                space-y-6
                rounded-xl
                border
                border-slate-800
                bg-slate-900/40
                p-5
            "
        >

            <div>

                <h2
                    className="
                        text-lg
                        font-semibold
                        text-slate-100
                    "
                >
                    Mount Alignment
                </h2>


                <p
                    className="
                        mt-1
                        text-sm
                        text-slate-500
                    "
                >
                    Slew to a known target,
                    centre it accurately,
                    then add it to the
                    TenMicron pointing model.
                </p>

            </div>


            {/* Current model */}

            <div>

                <h3
                    className="
                        mb-3
                        font-medium
                        text-slate-200
                    "
                >
                    Current Model
                </h3>


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
                            Alignment Points
                        </div>


                        <div
                            className="
                                mt-1
                                text-xl
                                text-slate-100
                            "
                        >
                            {
                                alignment
                                    ?.star_count
                                ??
                                0
                            }
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
                            Expected RMS
                        </div>


                        <div
                            className="
                                mt-1
                                text-sm
                                text-slate-100
                            "
                        >
                            {
                                alignment
                                    ?.model
                                    ?.expected_rms_arcsec
                                != null
                                    ? (
                                        `${alignment.model.expected_rms_arcsec.toFixed(1)}"`
                                    )
                                    : "—"
                            }
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
                            Polar Error
                        </div>


                        <div
                            className="
                                mt-1
                                text-sm
                                text-slate-100
                            "
                        >
                            {
                                alignment
                                    ?.model
                                    ?.polar_error
                                != null
                                    ? (
                                        `${alignment.model.polar_error.toFixed(4)}°`
                                    )
                                    : "—"
                            }
                        </div>

                    </div>

                </div>


                {
                    alignment?.model
                    &&
                    (

                        <div
                            className="
                                mt-3
                                grid
                                gap-3
                                md:grid-cols-3
                            "
                        >

                            <div
                                className="
                                    rounded-lg
                                    border
                                    border-slate-800
                                    p-3
                                "
                            >
                                <p
                                    className="
                                        text-xs
                                        text-slate-500
                                    "
                                >
                                    Model Terms
                                </p>

                                <p
                                    className="
                                        mt-1
                                        text-sm
                                        text-slate-200
                                    "
                                >
                                    {
                                        alignment
                                            .model
                                            .terms
                                        ??
                                        "—"
                                    }
                                </p>
                            </div>


                            <div
                                className="
                                    rounded-lg
                                    border
                                    border-slate-800
                                    p-3
                                "
                            >
                                <p
                                    className="
                                        text-xs
                                        text-slate-500
                                    "
                                >
                                    Orthogonality Error
                                </p>

                                <p
                                    className="
                                        mt-1
                                        text-sm
                                        text-slate-200
                                    "
                                >
                                    {
                                        alignment
                                            .model
                                            .orthogonality_error
                                        != null
                                            ? `${alignment.model.orthogonality_error.toFixed(4)}°`
                                            : "—"
                                    }
                                </p>
                            </div>


                            <div
                                className="
                                    rounded-lg
                                    border
                                    border-slate-800
                                    p-3
                                "
                            >
                                <p
                                    className="
                                        text-xs
                                        text-slate-500
                                    "
                                >
                                    Position Angle
                                </p>

                                <p
                                    className="
                                        mt-1
                                        text-sm
                                        text-slate-200
                                    "
                                >
                                    {
                                        alignment
                                            .model
                                            .position_angle
                                        != null
                                            ? `${alignment.model.position_angle.toFixed(2)}°`
                                            : "—"
                                    }
                                </p>
                            </div>

                        </div>

                    )
                }

            </div>


            {/* Guided workflow */}

            <div
                className="
                    rounded-xl
                    border
                    border-slate-800
                    p-4
                "
            >

                <h3
                    className="
                        mb-1
                        font-medium
                        text-slate-200
                    "
                >
                    Add Alignment Point
                </h3>


                <p
                    className="
                        mb-5
                        text-sm
                        text-slate-500
                    "
                >
                    Complete the steps in order.
                </p>


                {/* Step 1 */}

                <div
                    className="
                        border-b
                        border-slate-800
                        pb-5
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

                        <span
                            className="
                                flex
                                h-6
                                w-6
                                items-center
                                justify-center
                                rounded-full
                                bg-violet-500/15
                                text-xs
                                text-violet-300
                            "
                        >
                            1
                        </span>

                        <span
                            className="
                                font-medium
                                text-slate-200
                            "
                        >
                            Select Target
                        </span>

                    </div>


                    <div
                        className="
                            grid
                            gap-3
                            md:grid-cols-3
                        "
                    >

                        <label
                            className="
                                text-sm
                                text-slate-300
                            "
                        >
                            Star name

                            <input
                                className={
                                    inputClass
                                }

                                value={
                                    starName
                                }

                                onChange={(
                                    event
                                ) => {

                                    setStarName(
                                        event
                                            .target
                                            .value
                                    );

                                    setStep(
                                        "target"
                                    );
                                }}

                                placeholder="e.g. Vega"
                            />

                        </label>


                        <label
                            className="
                                text-sm
                                text-slate-300
                            "
                        >
                            Right Ascension

                            <input
                                className={
                                    inputClass
                                }

                                value={
                                    ra
                                }

                                onChange={(
                                    event
                                ) => {

                                    setRa(
                                        event
                                            .target
                                            .value
                                    );

                                    setStep(
                                        "target"
                                    );
                                }}

                                placeholder="18:36:56 or 18.6156"
                            />

                        </label>


                        <label
                            className="
                                text-sm
                                text-slate-300
                            "
                        >
                            Declination

                            <input
                                className={
                                    inputClass
                                }

                                value={
                                    dec
                                }

                                onChange={(
                                    event
                                ) => {

                                    setDec(
                                        event
                                            .target
                                            .value
                                    );

                                    setStep(
                                        "target"
                                    );
                                }}

                                placeholder="+38:47:01 or 38.7836"
                            />

                        </label>

                    </div>


                    {
                        (
                            ra.trim()
                            ||
                            dec.trim()
                        )
                        &&
                        !targetValid
                        &&
                        (

                            <p
                                className="
                                    mt-2
                                    text-sm
                                    text-red-300
                                "
                            >
                                Enter valid RA and
                                Dec coordinates.
                            </p>

                        )
                    }


                    <button
                        type="button"

                        className={
                            `${buttonClass} mt-4`
                        }

                        disabled={
                            busy
                            ||
                            !targetValid
                        }

                        onClick={
                            handleSlew
                        }
                    >

                        <span
                            className="
                                flex
                                items-center
                                gap-2
                            "
                        >
                            <Crosshair
                                size={16}
                            />

                            Slew to Target
                        </span>

                    </button>

                </div>


                {/* Step 2 */}

                <div
                    className="
                        border-b
                        border-slate-800
                        py-5
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

                        <span
                            className="
                                flex
                                h-6
                                w-6
                                items-center
                                justify-center
                                rounded-full
                                bg-violet-500/15
                                text-xs
                                text-violet-300
                            "
                        >
                            2
                        </span>

                        <span
                            className="
                                font-medium
                                text-slate-200
                            "
                        >
                            Centre Target
                        </span>

                    </div>


                    {
                        step === "target"
                            ? (

                                <p
                                    className="
                                        text-sm
                                        text-slate-500
                                    "
                                >
                                    Slew to the alignment
                                    target first.
                                </p>

                            )
                            : (

                                <>

                                    <p
                                        className="
                                            mb-4
                                            text-sm
                                            text-slate-500
                                        "
                                    >
                                        Use the controls until
                                        the target is accurately
                                        centred.
                                    </p>


                                    <div
                                        className="
                                            flex
                                            flex-col
                                            items-center
                                            gap-2
                                        "
                                    >

                                        <button
                                            type="button"

                                            className={
                                                nudgeButtonClass
                                            }

                                            disabled={
                                                busy
                                            }

                                            onClick={
                                                () =>
                                                    handleNudge(
                                                        "north"
                                                    )
                                            }
                                        >
                                            <ArrowUp
                                                size={18}
                                            />
                                        </button>


                                        <div
                                            className="
                                                flex
                                                items-center
                                                gap-2
                                            "
                                        >

                                            <button
                                                type="button"

                                                className={
                                                    nudgeButtonClass
                                                }

                                                disabled={
                                                    busy
                                                }

                                                onClick={
                                                    () =>
                                                        handleNudge(
                                                            "west"
                                                        )
                                                }
                                            >
                                                <ArrowLeft
                                                    size={18}
                                                />
                                            </button>


                                            <div
                                                className="
                                                    flex
                                                    h-11
                                                    w-11
                                                    items-center
                                                    justify-center
                                                    text-violet-300
                                                "
                                            >
                                                <Crosshair
                                                    size={20}
                                                />
                                            </div>


                                            <button
                                                type="button"

                                                className={
                                                    nudgeButtonClass
                                                }

                                                disabled={
                                                    busy
                                                }

                                                onClick={
                                                    () =>
                                                        handleNudge(
                                                            "east"
                                                        )
                                                }
                                            >
                                                <ArrowRight
                                                    size={18}
                                                />
                                            </button>

                                        </div>


                                        <button
                                            type="button"

                                            className={
                                                nudgeButtonClass
                                            }

                                            disabled={
                                                busy
                                            }

                                            onClick={
                                                () =>
                                                    handleNudge(
                                                        "south"
                                                    )
                                            }
                                        >
                                            <ArrowDown
                                                size={18}
                                            />
                                        </button>

                                    </div>


                                    <div
                                        className="
                                            mx-auto
                                            mt-4
                                            max-w-xs
                                        "
                                    >

                                        <label
                                            className="
                                                text-sm
                                                text-slate-300
                                            "
                                        >
                                            Nudge size

                                            <select
                                                className={
                                                    inputClass
                                                }

                                                value={
                                                    nudgeSize
                                                }

                                                onChange={(
                                                    event
                                                ) =>
                                                    setNudgeSize(
                                                        Number(
                                                            event
                                                                .target
                                                                .value
                                                        )
                                                    )
                                                }
                                            >
                                                <option value={5}>
                                                    5 arcsec
                                                </option>

                                                <option value={15}>
                                                    15 arcsec
                                                </option>

                                                <option value={30}>
                                                    30 arcsec
                                                </option>

                                                <option value={60}>
                                                    60 arcsec
                                                </option>

                                                <option value={120}>
                                                    120 arcsec
                                                </option>
                                            </select>

                                        </label>

                                    </div>


                                    {
                                        step === "centering"
                                        &&
                                        (

                                            <button
                                                type="button"

                                                className={
                                                    `${buttonClass} mt-4`
                                                }

                                                disabled={
                                                    busy
                                                }

                                                onClick={() => {

                                                    setStep(
                                                        "ready"
                                                    );

                                                    setMessage(
                                                        (
                                                            "Target marked as centred. "
                                                            +
                                                            "You can now add "
                                                            +
                                                            "the alignment point."
                                                        )
                                                    );
                                                }}
                                            >
                                                Target is Centred
                                            </button>

                                        )
                                    }

                                </>

                            )
                    }

                </div>


                {/* Step 3 */}

                <div
                    className="
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

                        <span
                            className="
                                flex
                                h-6
                                w-6
                                items-center
                                justify-center
                                rounded-full
                                bg-violet-500/15
                                text-xs
                                text-violet-300
                            "
                        >
                            3
                        </span>

                        <span
                            className="
                                font-medium
                                text-slate-200
                            "
                        >
                            Add Point
                        </span>

                    </div>


                    {
                        step === "ready"
                            ? (

                                <div
                                    className="
                                        rounded-lg
                                        border
                                        border-violet-500/20
                                        bg-violet-500/10
                                        p-3
                                    "
                                >

                                    <p
                                        className="
                                            text-sm
                                            text-slate-300
                                        "
                                    >
                                        Target
                                    </p>


                                    <p
                                        className="
                                            mt-1
                                            font-medium
                                            text-violet-300
                                        "
                                    >
                                        {
                                            starName.trim()
                                            ||
                                            "Alignment star"
                                        }
                                    </p>


                                    <p
                                        className="
                                            mt-2
                                            text-sm
                                            text-slate-400
                                        "
                                    >
                                        RA {ra}
                                        {" · "}
                                        Dec {dec}
                                    </p>


                                    <button
                                        type="button"

                                        className={
                                            `${buttonClass} mt-4`
                                        }

                                        disabled={
                                            busy
                                        }

                                        onClick={
                                            handleAddPoint
                                        }
                                    >
                                        Add Alignment Point
                                    </button>

                                </div>

                            )
                            : (

                                <p
                                    className="
                                        text-sm
                                        text-slate-500
                                    "
                                >
                                    Confirm that the target
                                    is centred before adding
                                    it to the model.
                                </p>

                            )
                    }

                </div>

            </div>


            {/* Alignment points */}

            <div>

                <h3
                    className="
                        mb-3
                        font-medium
                        text-slate-200
                    "
                >
                    Alignment Points
                </h3>


                <div
                    className="
                        space-y-2
                    "
                >

                    {
                        alignment
                            ?.stars
                            ?.map(
                                star => {

                                    const quality =
                                        errorQuality(
                                            star.error_arcsec
                                        );


                                    return (

                                        <div
                                            key={
                                                star.index
                                            }

                                            className="
                                                grid
                                                gap-2
                                                rounded-lg
                                                bg-slate-800/50
                                                px-3
                                                py-2
                                                text-sm
                                                md:grid-cols-[40px_1fr_1fr_90px_80px_auto]
                                                md:items-center
                                            "
                                        >

                                            <span
                                                className="
                                                    text-slate-500
                                                "
                                            >
                                                #{star.index}
                                            </span>


                                            <span
                                                className="
                                                    text-slate-200
                                                "
                                            >
                                                HA {
                                                    star.hour_angle
                                                }
                                            </span>


                                            <span
                                                className="
                                                    text-slate-200
                                                "
                                            >
                                                {
                                                    star.declination
                                                }
                                            </span>


                                            <span
                                                className="
                                                    font-mono
                                                    text-slate-300
                                                "
                                            >
                                                {
                                                    star
                                                        .error_arcsec
                                                        .toFixed(1)
                                                }
                                                &quot;
                                            </span>


                                            <span
                                                className={
                                                    quality.className
                                                }
                                            >
                                                {
                                                    quality.label
                                                }
                                            </span>


                                            <button
                                                type="button"

                                                className="
                                                    text-left
                                                    text-red-300
                                                    transition
                                                    hover:text-red-200
                                                    disabled:opacity-50
                                                    md:text-right
                                                "

                                                disabled={
                                                    busy
                                                }

                                                onClick={() => {

                                                    if (
                                                        window.confirm(
                                                            (
                                                                "Delete alignment "
                                                                +
                                                                `point ${star.index}?`
                                                            )
                                                        )
                                                    ) {

                                                        void runAction(
                                                            () =>
                                                                deleteAlignmentPoint(
                                                                    star.index
                                                                ),

                                                            "Alignment point deleted."
                                                        );
                                                    }
                                                }}
                                            >
                                                Delete
                                            </button>

                                        </div>

                                    );
                                }
                            )
                    }


                    {
                        !alignment
                            ?.stars
                            ?.length
                        &&
                        (

                            <p
                                className="
                                    text-sm
                                    text-slate-500
                                "
                            >
                                No alignment points stored.
                            </p>

                        )
                    }

                </div>

            </div>


            {/* Saved models */}

            <div>

                <h3
                    className="
                        mb-3
                        font-medium
                        text-slate-200
                    "
                >
                    Saved Models
                </h3>


                <div
                    className="
                        mb-3
                        flex
                        gap-2
                    "
                >

                    <input
                        className={
                            inputClass
                        }

                        maxLength={15}

                        value={
                            modelName
                        }

                        onChange={(
                            event
                        ) =>
                            setModelName(
                                event
                                    .target
                                    .value
                            )
                        }

                        placeholder="Model name"
                    />


                    <button
                        type="button"

                        className={
                            buttonClass
                        }

                        disabled={
                            busy
                            ||
                            !modelName.trim()
                            ||
                            !alignment?.star_count
                        }

                        onClick={() => {

                            void runAction(
                                () =>
                                    saveModel(
                                        modelName.trim()
                                    ),

                                "Alignment model saved."
                            );
                        }}
                    >
                        Save Current
                    </button>

                </div>


                <div
                    className="
                        space-y-2
                    "
                >

                    {
                        models.map(
                            model => (

                                <div
                                    key={
                                        model
                                    }

                                    className="
                                        flex
                                        items-center
                                        justify-between
                                        rounded-lg
                                        bg-slate-800/50
                                        px-3
                                        py-2
                                    "
                                >

                                    <span
                                        className="
                                            text-sm
                                            text-slate-200
                                        "
                                    >
                                        {model}
                                    </span>


                                    <div
                                        className="
                                            flex
                                            gap-2
                                        "
                                    >

                                        <button
                                            type="button"

                                            className={
                                                buttonClass
                                            }

                                            disabled={
                                                busy
                                            }

                                            onClick={() => {

                                                if (
                                                    window.confirm(
                                                        (
                                                            "Load alignment "
                                                            +
                                                            `model "${model}"?`
                                                        )
                                                    )
                                                ) {

                                                    void runAction(
                                                        () =>
                                                            loadModel(
                                                                model
                                                            ),

                                                        "Alignment model loaded."
                                                    );
                                                }
                                            }}
                                        >
                                            Load
                                        </button>


                                        <button
                                            type="button"

                                            className="
                                                text-sm
                                                text-red-300
                                                hover:text-red-200
                                                disabled:opacity-50
                                            "

                                            disabled={
                                                busy
                                            }

                                            onClick={() => {

                                                if (
                                                    window.confirm(
                                                        (
                                                            "Delete saved "
                                                            +
                                                            `model "${model}"?`
                                                        )
                                                    )
                                                ) {

                                                    void runAction(
                                                        () =>
                                                            deleteSavedModel(
                                                                model
                                                            ),

                                                        "Saved model deleted."
                                                    );
                                                }
                                            }}
                                        >
                                            Delete
                                        </button>

                                    </div>

                                </div>

                            )
                        )
                    }

                </div>

            </div>


            {/* Danger Zone */}

            <div
                className="
                    rounded-xl
                    border
                    border-red-500/20
                    bg-red-500/5
                    p-4
                "
            >

                <h3
                    className="
                        font-medium
                        text-red-300
                    "
                >
                    Danger Zone
                </h3>


                <p
                    className="
                        mt-1
                        text-sm
                        text-slate-500
                    "
                >
                    This removes every alignment
                    point from the currently
                    active model.
                </p>


                <button
                    type="button"

                    className="
                        mt-3
                        flex
                        items-center
                        gap-2
                        rounded-lg
                        border
                        border-red-500/30
                        bg-red-500/10
                        px-3
                        py-2
                        text-sm
                        text-red-300
                        hover:bg-red-500/20
                        disabled:opacity-50
                    "

                    disabled={
                        busy
                        ||
                        !alignment?.star_count
                    }

                    onClick={() => {

                        if (
                            window.confirm(
                                (
                                    "Delete the active "
                                    +
                                    "alignment model and "
                                    +
                                    "all alignment points?"
                                    +
                                    "\n\n"
                                    +
                                    "This cannot be undone."
                                )
                            )
                        ) {

                            void runAction(
                                deleteAlignmentModel,
                                "Alignment model deleted."
                            );
                        }
                    }}
                >

                    <Trash2
                        size={15}
                    />

                    Delete Active Model

                </button>

            </div>


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

        </section>
    );
}