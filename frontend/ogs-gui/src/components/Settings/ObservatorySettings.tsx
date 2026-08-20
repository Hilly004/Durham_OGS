import type { ObservatorySettings } from "../../api/settings";

interface Props {
    settings: ObservatorySettings;
    onChange: (key: keyof ObservatorySettings, value: string | number | boolean) => void;
}

export default function ObservatorySettingsSection({ settings, onChange }: Props) {
    return (
        <section className="rounded-xl border border-slate-800 bg-slate-900/40 p-5">
            <h2 className="mb-4 text-lg font-semibold text-slate-100">Observatory</h2>
            <div className="grid gap-4 md:grid-cols-2">
                <label className="text-sm text-slate-300">Site name
                    <input className="mt-1 w-full rounded-lg border border-slate-700 bg-slate-800 px-3 py-2" value={settings.site_name} onChange={e => onChange("site_name", e.target.value)} />
                </label>
                <label className="text-sm text-slate-300">Elevation (m)
                    <input type="number" className="mt-1 w-full rounded-lg border border-slate-700 bg-slate-800 px-3 py-2" value={settings.elevation_m} onChange={e => onChange("elevation_m", Number(e.target.value))} />
                </label>
                <label className="text-sm text-slate-300">Latitude
                    <input type="number" step="0.000001" className="mt-1 w-full rounded-lg border border-slate-700 bg-slate-800 px-3 py-2" value={settings.latitude} onChange={e => onChange("latitude", Number(e.target.value))} />
                </label>
                <label className="text-sm text-slate-300">Longitude
                    <input type="number" step="0.000001" className="mt-1 w-full rounded-lg border border-slate-700 bg-slate-800 px-3 py-2" value={settings.longitude} onChange={e => onChange("longitude", Number(e.target.value))} />
                </label>
            </div>
        </section>
    );
}