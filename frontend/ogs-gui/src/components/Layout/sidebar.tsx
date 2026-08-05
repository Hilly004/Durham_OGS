import { Link } from "react-router-dom";
import { Settings } from 'lucide-react';

export default function Sidebar() {
    return (
        <nav className='
        w-40
        h-screen
        bg-slate-900
        text-white
        p-6
        flex
        flex-col
        '
        >
            <div className='flex flex-col gap-4'>

                <Link 
                    className="
                    px-4
                    py-4
                    rounded-lg
                    hover:bg-slate-700
                    "
                to='/'>
                    Dashboard
                </Link>
                <Link className="
                    px-4
                    py-4
                    rounded-lg
                    hover:bg-slate-700
                    "
                to='/mount'>
                    Mount
                </Link>
                <Link className="
                    px-4
                    py-4
                    rounded-lg
                    hover:bg-slate-700
                    "
                to='/dome'>
                    Dome
                </Link>

                <Link className="
                    px-4
                    py-4
                    rounded-lg
                    hover:bg-slate-700
                    "
                to='/camera'>
                    Camera
                </Link>

                <Link className="
                    px-4
                    py-4
                    rounded-lg
                    hover:bg-slate-700
                    "
                to='/weather'>
                    Weather
                </Link>
            </div>

            <Link className="
                mt-auto
                "
            to='/settings'>
                <Settings size={24}/>
            </Link>
            
        </nav>
    );
}
