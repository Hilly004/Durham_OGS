import {
  BrowserRouter,
  Routes,
  Route
} from "react-router-dom"

import Layout from "./components/Layout/Layout";

import Home from "./pages/Home";
import Mount from "./pages/MountPage";
import Dome from "./pages/DomePage";

export default function App() {
  return (

    <BrowserRouter>

      <Routes>

        <Route 
          path='/'
          element={<Layout />}
        >
          <Route 
            path='/'
            element={<Home />}
          />

          <Route 
            path='/mount'
            element={<Mount />}
          />

          <Route 
            path='/dome'
            element={<Dome />}
          />

        </Route>

      </Routes>

    </BrowserRouter>

  );
}