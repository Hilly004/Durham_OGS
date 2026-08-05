import MountStatusWidget from "../components/Mount/MountStatus";
import DomeStatusWidget from "../components/Dome/DomeStatus";
import WeatherStatusWidget from "../components/Weather/WeatherStatus";

export default function Home(){
    return (
        <div>
            <h1 className='
            text-3xl
            font-bold
            mb-6
            '>
                Observatory Dashboard
            </h1>

            <div className='
            grid
            grid-cols-3
            gap-6
            '>
                <MountStatusWidget />
                <DomeStatusWidget />
                <WeatherStatusWidget />
            </div>  
        </div>
    );
}
