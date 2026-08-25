import { useState } from "react";
import { testDomeConnection, testMountConnection, testWeatherConnection, type ObservatorySettings } from "../../api/settings";

interface Props {
    settings: ObservatorySettings;
    onChange: (key: keyof ObservatorySettings, value: string | number | boolean) => void;
}

export default function ConnectionSettings({ settings, onChange }: Props) {
    const [message, setMessage] = useState<string | null>(null);
    const [testing, setTesting] = useState<string | null>(null);

    async function run(name: string, action: () => Promise<string>) {
        setTesting(name); setMessage(null);
        try { setMessage(await action()); }
        catch (error) { setMessage(error instanceof Error ? error.message : "Connection test failed"); }
        finally { setTesting(null); }
    }

    const input = "mt-1 w-full rounded-lg border border-slate-700 bg-slate-800 px-3 py-2 text-slate-100";
    const button = "rounded-lg border border-violet-500/30 bg-violet-500/10 px-3 py-2 text-sm text-violet-300 hover:bg-violet-500/20 disabled:opacity-50";

    return (
        <section className="space-y-5 rounded-xl border border-slate-800 bg-slate-900/40 p-5">
            <h2 className="text-lg font-semibold text-slate-100">Connections</h2>
            <div>
                <h3 className="mb-3 font-medium text-slate-200">Mount</h3>
                <div className="grid gap-3 md:grid-cols-[1fr_160px_auto]">
                    <label className="text-sm text-slate-300">Host / IP<input className={input} value={settings.mount_host} onChange={e => onChange("mount_host", e.target.value)} /></label>
                    <label className="text-sm text-slate-300">TCP port<input type="number" className={input} value={settings.mount_port} onChange={e => onChange("mount_port", Number(e.target.value))} /></label>
                    <button className={`${button} self-end`} disabled={testing !== null} onClick={() => run("mount", () => testMountConnection(settings.mount_host, settings.mount_port))}>{testing === "mount" ? "Testing..." : "Test"}</button>
                </div>
            </div>
            <div>
                <h3 className="mb-3 font-medium text-slate-200">Dome</h3>
                <div className="grid gap-3 md:grid-cols-[1fr_160px_auto]">
                    <label className="text-sm text-slate-300">Host / IP<input className={input} value={settings.dome_host} onChange={e => onChange("dome_host", e.target.value)} /></label>
                    <label className="text-sm text-slate-300">TCP port<input type="number" className={input} value={settings.dome_port} onChange={e => onChange("dome_port", Number(e.target.value))} /></label>
                    <button className={`${button} self-end`} disabled={testing !== null} onClick={() => run("dome", () => testDomeConnection(settings.dome_host, settings.dome_port))}>{testing === "dome" ? "Testing..." : "Test"}</button>
                </div>
            </div>
            <div>
                <h3 className="mb-3 font-medium text-slate-200">Weather</h3>
                <div className="grid gap-3 md:grid-cols-[1fr_160px_auto]">
                    <label className="text-sm text-slate-300">Serial port<input className={input} value={settings.weather_port} onChange={e => onChange("weather_port", e.target.value)} /></label>
                    <label className="text-sm text-slate-300">Baud rate<input type="number" className={input} value={settings.weather_baudrate} onChange={e => onChange("weather_baudrate", Number(e.target.value))} /></label>
                    <button className={`${button} self-end`} disabled={testing !== null} onClick={() => run("weather", () => testWeatherConnection(settings.weather_port, settings.weather_baudrate))}>{testing === "weather" ? "Testing..." : "Test"}</button>
                </div>
            </div>
            <label>Camera Type</label>

                <select
                    value={settings.camera_type}
                    onChange={(event) =>
                        onChange(
                            "camera_type",
                            event.target.value
                        )
                    }
                >
                    <option value="allied">
                        Allied Vision
                    </option>

                    <option value="zwo">
                        ZWO ASI
                    </option>
                </select>
            <label>Camera ID</label>

                <input
                    value={settings.camera_id}
                    onChange={(event) =>
                        onChange(
                            "camera_id",
                            event.target.value
                        )
                    }
                    placeholder={
                        settings.camera_type === "zwo"
                            ? "ZWO camera index, e.g. 0"
                            : "Vimba camera ID"
                    }
                />
            {message && <div className="rounded-lg border border-slate-700 bg-slate-800 px-3 py-2 text-sm text-slate-300">{message}</div>}
            <p className="text-xs text-slate-500">Disconnect a device before saving a changed live connection address.</p>
        </section>
    );
}
