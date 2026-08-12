import Sidebar from "./sidebar";
import { Outlet } from "react-router-dom";

export default function Layout() {
    return (
        <div className="flex h-screen overflow-hidden">

            {/* Sidebar */}

            <Sidebar />

            {/* Main content */}

            <main className="
                flex-1
                min-w-0
                min-h-0
                bg-slate-950
                overflow-hidden
            ">
                <Outlet />
            </main>

        </div>
    );
}