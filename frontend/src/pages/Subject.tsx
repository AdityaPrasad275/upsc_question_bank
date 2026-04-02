import { useEffect, useState } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';

interface QuestionSummary {
  id: string | number;
  short_text: string;
  file: string;
}

interface Source {
  title: string;
  url: string;
  whyUsed: string;
}

interface QuestionDetails {
  id: number;
  subject: string;
  year: number;
  theme: string;
  question_short_text: string;
  text: string;
  options: string[];
  answerIndex: number;
  answerText: string;
  explanation: string;
  research: {
    summary: string;
    facts: string[];
    sources: Source[];
  };
}

const Subject = () => {
  const { id, questionId } = useParams();
  const navigate = useNavigate();
  const [manifest, setManifest] = useState<QuestionSummary[]>([]);
  const [subjectName, setSubjectName] = useState<string>('');
  const [currentQuestion, setCurrentQuestion] = useState<QuestionDetails | null>(null);
  const [loading, setLoading] = useState(true);
  const [questionLoading, setQuestionLoading] = useState(false);
  const [showAnswer, setShowAnswer] = useState(false);
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);

  useEffect(() => {
    setLoading(true);
    fetch(`data/${id}/manifest.json`)
      .then(res => res.json())
      .then(data => {
        setManifest(data.questions);
        setSubjectName(data.name);
        setLoading(false);
        // If no questionId is in URL, navigate to the first question
        if (!questionId && data.questions.length > 0) {
          navigate(`/subject/${id}/${data.questions[0].id}`, { replace: true });
        }
      })
      .catch(err => {
        console.error("Error fetching subject manifest:", err);
        setLoading(false);
      });
  }, [id]);

  useEffect(() => {
    if (questionId && manifest.length > 0) {
      const qSummary = manifest.find(q => String(q.id) === String(questionId));
      if (qSummary) {
        setQuestionLoading(true);
        setShowAnswer(false);
        fetch(`data/${id}/${qSummary.file}`)
          .then(res => res.json())
          .then(data => {
            setCurrentQuestion(data);
            setQuestionLoading(false);
            window.scrollTo(0, 0);
          })
          .catch(err => {
            console.error("Error fetching question details:", err);
            setQuestionLoading(false);
          });
      }
    }
  }, [id, questionId, manifest]);

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  const toggleSidebar = () => setIsSidebarOpen(!isSidebarOpen);

  return (
    <div className="flex flex-col h-screen md:flex-row bg-white overflow-hidden">
      {/* Mobile Header */}
      <div className="md:hidden flex items-center justify-between p-4 border-b bg-white z-20">
        <Link to="/" className="text-blue-600 font-bold">← Home</Link>
        <span className="font-bold text-gray-800 truncate px-2">
          {subjectName}
        </span>
        <button 
          onClick={toggleSidebar}
          className="p-2 rounded-lg bg-gray-100 text-gray-600 focus:outline-none"
        >
          <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
          </svg>
        </button>
      </div>

      {/* Sidebar - Desktop and Mobile Overlay */}
      <aside className={`
        fixed inset-y-0 left-0 z-30 w-72 bg-gray-50 border-r transform transition-transform duration-300 ease-in-out
        md:relative md:translate-x-0
        ${isSidebarOpen ? 'translate-x-0' : '-translate-x-full'}
      `}>
        <div className="flex flex-col h-full">
          <div className="p-6 border-b bg-white hidden md:block">
            <Link to="/" className="text-blue-600 hover:text-blue-800 font-medium mb-4 inline-block flex items-center">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4 mr-1" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M9.707 16.707a1 1 0 01-1.414 0l-6-6a1 1 0 010-1.414l6-6a1 1 0 011.414 1.414L5.414 9H17a1 1 0 110 2H5.414l4.293 4.293a1 1 0 010 1.414z" clipRule="evenodd" />
              </svg>
              Back to Home
            </Link>
            <h2 className="text-xl font-bold text-gray-900 truncate">
              {subjectName}
            </h2>
            <p className="text-sm text-gray-500 mt-1">{manifest.length} Questions</p>
          </div>
          <div className="flex-1 overflow-y-auto p-4 space-y-1 custom-scrollbar">
            {manifest.map((q) => (
              <Link
                key={q.id}
                to={`/subject/${id}/${q.id}`}
                onClick={() => setIsSidebarOpen(false)}
                className={`
                  block p-3 rounded-lg text-sm transition-all duration-200
                  ${String(questionId) === String(q.id)
                    ? 'bg-blue-600 text-white shadow-md'
                    : 'text-gray-700 hover:bg-gray-200'}
                `}
              >
                <div className="font-semibold mb-1">Question {q.id}</div>
                <div className={`text-xs ${String(questionId) === String(q.id) ? 'text-blue-100' : 'text-gray-500'} line-clamp-2`}>
                  {q.short_text}
                </div>
              </Link>
            ))}
          </div>
        </div>
      </aside>

      {/* Backdrop for mobile sidebar */}
      {isSidebarOpen && (
        <div 
          className="fixed inset-0 bg-black bg-opacity-50 z-20 md:hidden"
          onClick={toggleSidebar}
        ></div>
      )}

      {/* Main Content Area */}
      <main className="flex-1 overflow-y-auto bg-white">
        <div className="max-w-3xl mx-auto px-6 py-8 md:py-12">
          {questionLoading ? (
            <div className="flex flex-col items-center justify-center h-64">
              <div className="animate-spin rounded-full h-10 w-10 border-b-2 border-blue-600 mb-4"></div>
              <p className="text-gray-500">Loading question content...</p>
            </div>
          ) : currentQuestion ? (
            <article className="space-y-8 animate-fadeIn">
              <header className="border-b pb-6">
                <div className="flex items-center space-x-2 text-sm text-blue-600 font-semibold mb-2">
                  <span className="bg-blue-50 px-2 py-1 rounded">{currentQuestion.subject}</span>
                  <span className="bg-gray-50 text-gray-600 px-2 py-1 rounded">{currentQuestion.year}</span>
                </div>
                <h1 className="text-2xl md:text-3xl font-bold text-gray-900 leading-tight">
                  {currentQuestion.theme}
                </h1>
              </header>

              <section className="bg-gray-50 p-6 rounded-2xl border border-gray-100 shadow-inner">
                <div className="text-lg text-gray-800 whitespace-pre-line leading-relaxed">
                  {currentQuestion.text}
                </div>
              </section>

              <section className="space-y-3">
                <h3 className="text-sm font-bold text-gray-400 uppercase tracking-wider mb-4">Select an Option</h3>
                <div className="grid grid-cols-1 gap-3">
                  {currentQuestion.options.map((option, idx) => (
                    <div 
                      key={idx}
                      className={`
                        p-4 rounded-xl border-2 transition-all cursor-pointer
                        ${showAnswer && idx === currentQuestion.answerIndex 
                          ? 'border-green-500 bg-green-50' 
                          : showAnswer 
                            ? 'border-gray-200 bg-white opacity-60' 
                            : 'border-gray-200 hover:border-blue-300 hover:bg-blue-50 bg-white'}
                      `}
                      onClick={() => !showAnswer && setShowAnswer(true)}
                    >
                      <div className="flex items-start">
                        <span className={`
                          flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center mr-4 font-bold
                          ${showAnswer && idx === currentQuestion.answerIndex 
                            ? 'bg-green-500 text-white' 
                            : 'bg-gray-100 text-gray-500'}
                        `}>
                          {String.fromCharCode(97 + idx)}
                        </span>
                        <span className="text-gray-700 font-medium pt-1">{option}</span>
                      </div>
                    </div>
                  ))}
                </div>
              </section>

              {!showAnswer ? (
                <div className="flex justify-center pt-6">
                  <button 
                    onClick={() => setShowAnswer(true)}
                    className="px-8 py-4 bg-blue-600 text-white rounded-xl font-bold shadow-lg hover:bg-blue-700 transition-all transform hover:scale-105"
                  >
                    Check Answer
                  </button>
                </div>
              ) : (
                <div className="space-y-10 pt-6 animate-fadeIn">
                  <div className="bg-green-50 border-l-4 border-green-500 p-6 rounded-r-xl">
                    <h3 className="text-green-800 font-bold text-lg mb-2 flex items-center">
                      <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                      </svg>
                      Correct Answer: {currentQuestion.answerText}
                    </h3>
                    <p className="text-green-700 leading-relaxed">
                      {currentQuestion.explanation}
                    </p>
                  </div>

                  <div className="space-y-6">
                    <h2 className="text-2xl font-bold text-gray-900 border-b pb-4">Deep Research</h2>
                    
                    <div className="prose prose-blue max-w-none text-gray-700 leading-relaxed">
                      <p className="whitespace-pre-line">{currentQuestion.research.summary}</p>
                    </div>

                    <div className="bg-gray-50 p-6 rounded-2xl border border-gray-100">
                      <h3 className="font-bold text-gray-900 mb-4 flex items-center">
                        <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-2 text-blue-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                        Key Facts
                      </h3>
                      <ul className="space-y-3">
                        {currentQuestion.research.facts.map((fact, idx) => (
                          <li key={idx} className="flex items-start">
                            <span className="text-blue-500 mr-2">•</span>
                            <span className="text-gray-700 text-sm">{fact}</span>
                          </li>
                        ))}
                      </ul>
                    </div>

                    <div className="space-y-4">
                      <h3 className="font-bold text-gray-900 flex items-center">
                        <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-2 text-blue-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
                        </svg>
                        Sources & Further Reading
                      </h3>
                      <div className="grid grid-cols-1 gap-3">
                        {currentQuestion.research.sources.map((source, idx) => (
                          <a 
                            key={idx}
                            href={source.url}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="block p-4 rounded-xl border border-gray-200 hover:border-blue-300 hover:bg-blue-50 transition-all group"
                          >
                            <div className="font-bold text-gray-900 group-hover:text-blue-600">{source.title}</div>
                            <div className="text-sm text-gray-500 mt-1">{source.whyUsed}</div>
                            <div className="text-xs text-blue-500 mt-2 truncate underline">{source.url}</div>
                          </a>
                        ))}
                      </div>
                    </div>
                  </div>
                </div>
              )}
            </article>
          ) : (
            <div className="text-center py-20">
              <h2 className="text-2xl font-bold text-gray-400">Question not found</h2>
              <Link to="/" className="text-blue-600 mt-4 inline-block">Return to Home</Link>
            </div>
          )}
        </div>
      </main>
    </div>
  );
};

export default Subject;
