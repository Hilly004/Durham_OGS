import type { ObservatorySettings } from "../../api/settings";
import Card from '../Common/Card'

interface Props { settings: ObservatorySettings; onChange: (key: keyof ObservatorySettings, value: string | number | boolean) => void; }
export default function SystemSettings({ settings, onChange }: Props) {
    return (
        <Card
            as="section"
            variant="soft"
            className="space-y-5"
        >
            <h2 className="mb-4 text-lg font-semibold text-slate-100">Defaults & System</h2>
            <div className="grid gap-4 md:grid-cols-3">
                <label className="text-sm text-slate-300">Default nudge (arcsec)<input type="number" className="mt-1 w-full rounded-lg border border-slate-700 bg-slate-800 px-3 py-2" value={settings.default_nudge_arcsec} onChange={e => onChange("default_nudge_arcsec", Number(e.target.value))} /></label>
                <label className="text-sm text-slate-300">Default prediction window (min)<input type="number" className="mt-1 w-full rounded-lg border border-slate-700 bg-slate-800 px-3 py-2" value={settings.default_prediction_minutes} onChange={e => onChange("default_prediction_minutes", Number(e.target.value))} /></label>
                <label className="text-sm text-slate-300">Activity log max entries<input type="number" className="mt-1 w-full rounded-lg border border-slate-700 bg-slate-800 px-3 py-2" value={settings.activity_log_max_entries} onChange={e => onChange("activity_log_max_entries", Number(e.target.value))} /></label>
            </div>
        </Card>
    );
}