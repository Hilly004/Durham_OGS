import { useState } from "react";

import StatusCard from "../Common/DashboardStatusCard";

import {
    slewToSatellite,
    predictSatellitePass,
    getCurrentJulianDate,
} from "../../api/satellite";


export default function SatelliteControls() {

    const [satelliteId, setSatelliteId] =
        useState<number>(1);

    const [predictionMinutes, setPredictionMinutes] =
        useState<number>(60);

    const [loading, setLoading] =
        useState(false);

    const [message, setMessage] =
        useState<string | null>(null);

    const [passStart, setPassStart] =
        useState<number | null>(null);

    const [passEnd, setPassEnd] =
        useState<number | null>(null);


    async function handleSlew() {

        setLoading(true);
        setMessage(null);

        try {

            const result =
                await slewToSatellite(satelliteId);

            setMessage(
                result.data.message
            );

        } catch (error) {

            if (error instanceof Error) {
                setMessage(error.message);
            } else {
                setMessage(
                    "Failed to slew to satellite"
                );
            }

        } finally {
            setLoading(false);
        }
    }


    async function handlePrediction() {

        setLoading(true);
        setMessage(null);

        try {

            const result =
                await predictSatellitePass(
                    satelliteId,
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

            if (error instanceof Error) {
                setMessage(error.message);
            } else {
                setMessage(
                    "Failed to predict satellite pass"
                );
            }

        } finally {
            setLoading(false);
        }
    }


    return (
        <StatusCard
            title="Satellite Controls"
            status="connected"
        >

            <div className="space-y-5">


                {/* Satellite */}

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
                        Satellite ID
                    </label>

                    <input
                        type="number"
                        min="1"
                        value={satelliteId}
                        onChange={(event) =>
                            setSatelliteId(
                                Number(event.target.value)
                            )
                        }
                        className="
                            w-full
                            rounded-lg
                            border
                            border-slate-700
                            bg-slate-800
                            px-3
                            py-2
                            text-slate-100
                            outline-none
                            transition
                            focus:border-violet-500
                            focus:ring-2
                            focus:ring-violet-500/20
                        "
                    />

                </div>


                {/* Prediction Window */}

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

                    <div className="flex items-center gap-3">

                        <input
                            type="number"
                            min="1"
                            value={predictionMinutes}
                            onChange={(event) =>
                                setPredictionMinutes(
                                    Number(
                                        event.target.value
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

                        <span className="text-sm text-slate-500">
                            minutes
                        </span>

                    </div>

                </div>


                {/* Actions */}

                <div className="grid grid-cols-2 gap-3">

                    <button
                        onClick={handlePrediction}
                        disabled={loading}
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
                        Predict Pass
                    </button>


                    <button
                        onClick={handleSlew}
                        disabled={loading}
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
                        Slew to Satellite
                    </button>

                </div>


                {/* Pass Result */}

                {(passStart || passEnd) && (

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

                                <p className="text-slate-500">
                                    Start JD
                                </p>

                                <p
                                    className="
                                        mt-1
                                        font-mono
                                        text-slate-200
                                    "
                                >
                                    {passStart?.toFixed(6)}
                                </p>

                            </div>


                            <div>

                                <p className="text-slate-500">
                                    End JD
                                </p>

                                <p
                                    className="
                                        mt-1
                                        font-mono
                                        text-slate-200
                                    "
                                >
                                    {passEnd?.toFixed(6)}
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

        </StatusCard>
    );
}