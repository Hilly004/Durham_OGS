<div className="flex items-center gap-3">

    <button
        onClick={handleConnection}
        disabled={loading}
        className="
            rounded-lg
            border
            border-violet-500/30
            bg-violet-500/10
            px-4
            py-2
            text-sm
            font-medium
            text-violet-300
            hover:bg-violet-500/20
        "
    >
        {status?.connected
            ? "Disconnect"
            : "Connect"}
    </button>

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
            className={`
                h-2.5
                w-2.5
                rounded-full
                ${
                    status?.connected
                        ? "bg-green-500"
                        : "bg-red-500"
                }
            `}
        />

        <span className="text-sm text-slate-300">
            {status?.connected
                ? "Connected"
                : "Disconnected"}
        </span>
    </div>

</div>