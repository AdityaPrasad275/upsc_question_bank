import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';

interface Subject {
  id: string;
  name: string;
  count: number;
}

const Home = () => {
  const [subjects, setSubjects] = useState<Subject[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('data/subjects.json')
      .then(res => res.json())
      .then(data => {
        setSubjects(data);
        setLoading(false);
      })
      .catch(err => {
        console.error("Error fetching subjects:", err);
        setLoading(false);
      });
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto px-4 py-12">
      <header className="mb-12 text-center">
        <h1 className="text-4xl font-extrabold text-gray-900 mb-4 tracking-tight">
          UPSC Question Bank
        </h1>
        <p className="text-xl text-gray-600">
          A collection of high-quality UPSC practice questions with detailed research and explanations.
        </p>
      </header>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {subjects.map(subject => (
          <Link 
            key={subject.id} 
            to={`/subject/${subject.id}`}
            className="group block p-8 bg-white rounded-2xl border border-gray-200 shadow-sm hover:shadow-xl hover:border-blue-300 transition-all duration-300 transform hover:-translate-y-1"
          >
            <div className="flex justify-between items-start mb-4">
              <h2 className="text-2xl font-bold text-gray-800 group-hover:text-blue-600 transition-colors">
                {subject.name}
              </h2>
              <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                {subject.count} Questions
              </span>
            </div>
            <p className="text-gray-600">
              Practice questions for {subject.name} with deep insights and analysis.
            </p>
            <div className="mt-6 flex items-center text-blue-600 font-semibold">
              Explore Questions
              <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 ml-2 group-hover:translate-x-1 transition-transform" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M14 5l7 7m0 0l-7 7m7-7H3" />
              </svg>
            </div>
          </Link>
        ))}
      </div>
      
      {subjects.length === 0 && !loading && (
        <div className="text-center p-12 bg-white rounded-2xl border border-dashed border-gray-300">
          <p className="text-gray-500 text-lg">No subjects found. Please run the data generator.</p>
        </div>
      )}
    </div>
  );
};

export default Home;
