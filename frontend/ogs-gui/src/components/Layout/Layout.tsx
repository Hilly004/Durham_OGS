import Sidebar from "./sidebar";
import { Outlet } from "react-router-dom";

export default function Layout() {
    return (
        <div className='flex h-screen'>

            <Sidebar />

            <main className='flex-1 p-6'>
                <Outlet />
            </main>

        </div>
    );
}
