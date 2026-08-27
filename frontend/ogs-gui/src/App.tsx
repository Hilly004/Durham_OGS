import {
    BrowserRouter,
    Routes,
    Route,
} from "react-router-dom";

import {
    ObservatoryStatusProvider,
} from "./context/ObservatoryStatusProvider";

import Layout from "./components/Layout/Layout";

import Home from "./pages/Home";
import MountPage from "./pages/MountPage";
import DomePage from "./pages/DomePage";
import WeatherPage from "./pages/WeatherPage";
import SatellitePage from "./pages/SatellitePage";
import SettingsPage from "./pages/SettingsPage";
import CameraPage from "./pages/CameraPage";


export default function App() {

    return (
        <ObservatoryStatusProvider>

            <BrowserRouter>

                <Routes>

                    <Route
                        path="/"
                        element={<Layout />}
                    >

                        <Route
                            index
                            element={<Home />}
                        />

                        <Route
                            path="mount"
                            element={<MountPage />}
                        />

                        <Route
                            path="dome"
                            element={<DomePage />}
                        />

                        <Route
                            path="camera"
                            element={<CameraPage />}
                        />

                        <Route
                            path="weather"
                            element={<WeatherPage />}
                        />

                        <Route
                            path="tracking"
                            element={<SatellitePage />}
                        />

                        <Route
                            path="settings"
                            element={<SettingsPage />}
                        />

                    </Route>

                </Routes>

            </BrowserRouter>

        </ObservatoryStatusProvider>
    );
}