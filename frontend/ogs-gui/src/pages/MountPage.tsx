import MountControls from "../components/Mount/MountControls";
import MountStatus from "../components/Mount/MountStatus";

export default function App() {
    return (
        <div>
            <h1>Mount Page</h1>

            <MountStatus />
            <MountControls />
        </div>
    );
}