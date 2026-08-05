import Sidebar from "./sidebar";
import { Outlet } from "react-router-dom";

export default function Layout() {
    return (
        <div style={{ display: "flex" }}>

            <Sidebar />

            <main style={{ padding: '20px'}}>
                <Outlet />
            </main>

        </div>
    );
}
