import MountStatusWidget from "../components/Mount/MountStatus";
import DomeStatusWidget from "../components/Dome/DomeStatus";
import WeatherStatusWidget from "../components/Weather/WeatherStatus";
import CameraWidget from '../components/Camera/CameraWidget';
import ActivityLog from '../components/Activity/ActivityWidget'


export default function Home(){
    return (
        <div>

            <div className='
            grid
            grid-cols-4
            gap-6
            '>
            
    <div className="col-span-2">
        <MountStatusWidget />
    </div>

    <div className="col-span-1">
        <DomeStatusWidget />
    </div>

    <div className="col-span-1">
        <WeatherStatusWidget />
    </div>

    <div className="col-span-2">
        <ActivityLog />
    </div>

    <div className="col-span-2">
        <CameraWidget />
    </div>

            </div>  

        </div>
    );
}
