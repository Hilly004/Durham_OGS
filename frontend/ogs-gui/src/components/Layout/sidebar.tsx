import { Link } from "react-router-dom";

export default function Sidebar() {
    return (
        <nav className='
        w-64
        min-h-screen
        bg-slate-900
        text-white
        p-6
        '
        >
            <h2 className='text-xl font-bold mb-6'>
                Durham OGS</h2>

            <div className='space-y-3'>

                <Link to='/'>
                    Dashboard
                </Link>
                <Link to='/mount'>
                    Mount
                </Link>
                <Link to='/dome'>
                    Dome
                </Link>
            </div>
        </nav>
    );
}
