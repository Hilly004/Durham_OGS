import MountControls from "../components/Mount/MountControls";
import MountStatus from "../components/Mount/MountStatus";

export default function App() {
    return (
        <div
        className='
        grid
        grid-rows
        gap-3'
        >
            <h1>Mount Page</h1>

            <MountStatus />
            <MountControls />
        </div>
    );
}