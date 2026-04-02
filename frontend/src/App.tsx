import { HashRouter as Router, Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import Subject from './pages/Subject';

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gray-50 text-gray-900">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/subject/:id" element={<Subject />} />
          <Route path="/subject/:id/:questionId" element={<Subject />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
