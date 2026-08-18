import { useState } from "react";
import { Save, Satellite,X } from "lucide-react";

import { createSatellite } from "../../api/satellite";

interface TLEUploadProps {
    onClose: () => void;
}

export default function TLEUpload({
        onClose,
    }: TLEUploadProps) {

    const [name, setName] = useState("");
    const [line1, setLine1] = useState("");
    const [line2, setLine2] = useState("");

    const [loading, setLoading] = useState(false);

    const [message, setMessage] =
        useState<string | null>(null);

    const [error, setError] =
        useState<string | null>(null);


    async function handleSubmit(
        event: React.FormEvent
    ) {

        event.preventDefault();

        setMessage(null);
        setError(null);


        if (!name.trim()) {
            setError("Satellite name is required.");
            return;
        }

        if (!line1.trim() || !line2.trim()) {
            setError("Both TLE lines are required.");
            return;
        }


        if (!line1.trim().startsWith("1 ")) {
            setError("TLE line 1 must begin with '1 '.");
            return;
        }

        if (!line2.trim().startsWith("2 ")) {
            setError("TLE line 2 must begin with '2 '.");
            return;
        }


        setLoading(true);

        try {

            await createSatellite({
                name: name.trim(),
                line1: line1.trim(),
                line2: line2.trim(),
            });

            setMessage(
                `${name.trim()} saved successfully.`
            );

            setName("");
            setLine1("");
            setLine2("");

        } catch (error) {

            if (error instanceof Error) {
                setError(error.message);
            } else {
                setError(
                    "Unable to save satellite."
                );
            }

        } finally {
            setLoading(false);
        }
    }


    return (
        <div
            className="
                rounded-xl
                border border-slate-800
                bg-slate-900
                p-5
            "
        >

            {/* Header */}
            <div className="mb-5 flex items-center justify-between">

                <div className="flex items-center gap-3">

                    <div
                        className="
                            flex
                            h-9
                            w-9
                            items-center
                            justify-center
                            rounded-lg
                            bg-violet-500/10
                        "
                    >
                        <Satellite
                            size={18}
                            className="text-violet-400"
                        />
                    </div>

                    <div>
                        <h2 className="font-semibold text-slate-100">
                            Add Satellite TLE
                        </h2>

                        <p className="text-xs text-slate-500">
                            Store orbital elements for future tracking
                        </p>
                    </div>

                </div>


                <button
                    type="button"
                    onClick={onClose}
                    className="
                        rounded-lg
                        p-2
                        text-slate-500
                        transition
                        hover:bg-slate-800
                        hover:text-slate-200
                    "
                >
                    <X size={18} />
                </button>

            </div>


            <form
                onSubmit={handleSubmit}
                className="space-y-4"
            >

                {/* Satellite Name */}
                <div>

                    <label
                        className="
                            mb-1.5
                            block
                            text-xs
                            font-medium
                            uppercase
                            tracking-wide
                            text-slate-500
                        "
                    >
                        Satellite Name
                    </label>

                    <input
                        type="text"
                        value={name}
                        onChange={(event) =>
                            setName(event.target.value)
                        }
                        placeholder="e.g. ISS (ZARYA)"
                        className="
                            w-full
                            rounded-lg
                            border border-slate-700
                            bg-slate-950
                            px-3 py-2
                            text-sm
                            text-slate-200
                            outline-none
                            transition
                            placeholder:text-slate-600
                            focus:border-violet-500
                            focus:ring-2
                            focus:ring-violet-500/20
                        "
                    />

                </div>


                {/* TLE Line 1 */}
                <div>

                    <label
                        className="
                            mb-1.5
                            block
                            text-xs
                            font-medium
                            uppercase
                            tracking-wide
                            text-slate-500
                        "
                    >
                        TLE Line 1
                    </label>

                    <input
                        type="text"
                        value={line1}
                        onChange={(event) =>
                            setLine1(event.target.value)
                        }
                        placeholder="1 25544U 98067A ..."
                        className="
                            w-full
                            rounded-lg
                            border border-slate-700
                            bg-slate-950
                            px-3 py-2
                            font-mono
                            text-sm
                            text-slate-200
                            outline-none
                            transition
                            placeholder:text-slate-600
                            focus:border-violet-500
                            focus:ring-2
                            focus:ring-violet-500/20
                        "
                    />

                </div>


                {/* TLE Line 2 */}
                <div>

                    <label
                        className="
                            mb-1.5
                            block
                            text-xs
                            font-medium
                            uppercase
                            tracking-wide
                            text-slate-500
                        "
                    >
                        TLE Line 2
                    </label>

                    <input
                        type="text"
                        value={line2}
                        onChange={(event) =>
                            setLine2(event.target.value)
                        }
                        placeholder="2 25544 51.6400 ..."
                        className="
                            w-full
                            rounded-lg
                            border border-slate-700
                            bg-slate-950
                            px-3 py-2
                            font-mono
                            text-sm
                            text-slate-200
                            outline-none
                            transition
                            placeholder:text-slate-600
                            focus:border-violet-500
                            focus:ring-2
                            focus:ring-violet-500/20
                        "
                    />

                </div>


                {/* Bottom Row */}
                <div className="flex items-center justify-between pt-1">

                    <div>

                        {error && (
                            <p className="text-sm text-red-400">
                                {error}
                            </p>
                        )}

                        {message && (
                            <p className="text-sm text-green-400">
                                {message}
                            </p>
                        )}

                    </div>


                    <button
                        type="submit"
                        disabled={loading}
                        className="
                            flex
                            items-center
                            gap-2
                            rounded-lg
                            bg-violet-600
                            px-4 py-2.5
                            text-sm
                            font-medium
                            text-white
                            transition
                            hover:bg-violet-500
                            disabled:cursor-not-allowed
                            disabled:opacity-50
                        "
                    >
                        <Save size={16} />

                        {loading
                            ? "Saving..."
                            : "Save Satellite"}
                    </button>

                </div>

            </form>

        </div>
    );
}