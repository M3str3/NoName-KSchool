import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Database from './pages/Database/Database';
import RegDetails from './pages/RegDetails/RegDetails';
import Domain from './pages/Domain/Domain';
import Main from './pages/Main/Main';
import Yara from './components/Yara';

function App() {
  return (
    <div className='content'>
      <Router>
        <Routes>
          <Route path="/" element={<Main />} />
          <Route path="/database" element={<Database />} />
          <Route path="/database/yara/:hostId" element={<Yara />} />
          <Route path="/database/domain/:requestdomain" element={<Domain />} />
          <Route path="/database/reg/:requestId" element={<RegDetails />} />
        </Routes>
      </Router>
    </div>
  );
}

export default App;
