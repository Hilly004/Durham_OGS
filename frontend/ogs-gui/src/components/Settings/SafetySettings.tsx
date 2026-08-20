import type { ObservatorySettings } from "../../api/settings";

interface Props { settings: ObservatorySettings; onChange: (key: keyof ObservatorySettings, value: string | number | boolean) => void; }

export default function SafetySettings({ settings, onChange }: Props) {
    const input = "mt-1 w-full rounded-lg border border-slate-700 bg-slate-800 px-3 py-2 text-slate-100";
    return (
        <section className="rounded-xl border border-slate-800 bg-slate-900/40 p-5">
            <h2 className="mb-4 text-lg font-semibold text-slate-100">Safety</h2>
            <div className="grid gap-4 md:grid-cols-3">
                <label className="text-sm text-slate-300">Max wind speed<input type="number" className={input} value={settings.max_wind_speed} onChange={e => onChange("max_wind_speed", Number(e.target.value))} /></label>
                <label className="text-sm text-slate-300">Max humidity (%)<input type="number" className={input} value={settings.max_humidity} onChange={e => onChange("max_humidity", Number(e.target.value))} /></label>
                <label className="text-sm text-slate-300">Weather timeout (s)<input type="number" className={input} value={settings.weather_timeout_seconds} onChange={e => onChange("weather_timeout_seconds", Number(e.target.value))} /></label>
            </div>
            <label className="mt-4 flex items-center gap-3 text-sm text-slate-300">
                <input type="checkbox" checked={settings.automatic_shutdown_enabled} onChange={e => onChange("automatic_shutdown_enabled", e.target.checked)} />
                Automatically perform safe shutdown when conditions become unsafe
            </label>
        </section>
    );
}