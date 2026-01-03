import React, { useState } from 'react';
import SearchForm from './components/SearchForm';
import MatchResults from './components/MatchResults';
import UnifiedHistory from './components/UnifiedHistory';

function App() {
    const [step, setStep] = useState('search'); // search, match, history
    const [searchData, setSearchData] = useState(null);

    // Mock Data for Demo
    const mockComputations = {
        source: {
            id: "HA001",
            name: "Ramesh Singh",
            dob: "1985-03-15",
            abha_number: "12-3456-7890-1234"
        },
        target: {
            id: "HB001",
            name: "Ramehs Singh",
            dob: "1985-03-15",
            abha_number: "12-3456-7890-1234"
        },
        match: {
            match_score: 90,
            method: "Phonetic Match (Indian Names)"
        },
        history: [
            {
                date: "2025-12-28",
                hospital: "B",
                type: "Emergency",
                diagnosis: "Chest Pain",
                doctor: "Suresh Reddy",
                department: "Cardiology",
                notes: "Patient presented with chest pain..."
            },
            {
                date: "2025-10-15",
                hospital: "A",
                type: "OPD",
                diagnosis: "Diabetes Follow-up",
                doctor: "Anjali Mehta",
                department: "Endocrinology",
                notes: "Blood sugar levels stable..."
            },
            {
                date: "2025-10-01",
                hospital: "A",
                type: "OPD",
                diagnosis: "Type 2 Diabetes Mellitus",
                doctor: "Anjali Mehta",
                department: "General Medicine",
                notes: "Initial diagnosis. Prescribed Metformin."
            }
        ]
    };

    const handleSearch = (data) => {
        setSearchData(data);
        // In a real app, we would transition based on API result
        // For demo, if matches mock data or blank, we show the result table
    };

    const handleMatchClick = () => {
        setStep('match');
    };

    const handleHistoryClick = () => {
        setStep('history');
    };

    return (
        <div className="min-h-screen bg-gray-100 p-8 font-sans">
            <div className="max-w-4xl mx-auto">
                <header className="mb-8 text-center animate-fade-in-down">
                    <h1 className="text-4xl font-extrabold text-blue-800 tracking-tight">PRAISA</h1>
                    <p className="text-gray-600 text-lg">AI-Powered Healthcare Interoperability Platform</p>
                </header>

                {step === 'search' && (
                    <div className="animate-fade-in-up">
                        <SearchForm onSearch={handleSearch} />
                        {searchData && (
                            <div className="bg-white p-6 rounded-lg shadow-md mt-6 animate-fade-in">
                                <h3 className="text-lg font-bold mb-4 text-gray-800">Search Results</h3>
                                <div className="overflow-x-auto">
                                    <table className="w-full text-left border-collapse">
                                        <thead className="bg-gray-50 text-gray-600 uppercase text-xs">
                                            <tr>
                                                <th className="p-3 border-b">ID</th>
                                                <th className="p-3 border-b">Name</th>
                                                <th className="p-3 border-b">DOB</th>
                                                <th className="p-3 border-b">Action</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            <tr className="hover:bg-gray-50 transition-colors">
                                                <td className="p-3 border-b">HA001</td>
                                                <td className="p-3 border-b font-medium text-gray-900">Ramesh Singh</td>
                                                <td className="p-3 border-b">1985-03-15</td>
                                                <td className="p-3 border-b">
                                                    <button
                                                        onClick={handleMatchClick}
                                                        className="bg-green-600 text-white px-4 py-2 rounded shadow hover:bg-green-700 transition transform hover:scale-105"
                                                    >
                                                        Match with Hospital B
                                                    </button>
                                                </td>
                                            </tr>
                                        </tbody>
                                    </table>
                                </div>
                            </div>
                        )}
                    </div>
                )}

                {(step === 'match' || step === 'history') && (
                    <div className="animate-fade-in">
                        <MatchResults
                            sourcePatient={mockComputations.source}
                            targetPatient={mockComputations.target}
                            matchData={mockComputations.match}
                            onHistoryClick={handleHistoryClick}
                        />
                    </div>
                )}

                {step === 'history' && (
                    <div className="animate-slide-in-bottom">
                        <UnifiedHistory history={mockComputations.history} />
                    </div>
                )}

                {step !== 'search' && (
                    <div className="mt-12 text-center pb-8">
                        <button
                            onClick={() => { setStep('search'); setSearchData(null); }}
                            className="text-gray-500 hover:text-blue-600 underline transition-colors"
                        >
                            Start New Search
                        </button>
                    </div>
                )}
            </div>
        </div>
    );
}

export default App;
