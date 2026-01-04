import React, { useState } from 'react';
import SearchForm from './components/SearchForm';
import MatchResults from './components/MatchResults';
import UnifiedHistory from './components/UnifiedHistory';
import { searchPatients, matchPatients, getPatientHistory } from './api/client';

function App() {
    const [step, setStep] = useState('search'); // search, match, history
    const [searchData, setSearchData] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    // State for match flow
    const [currentPatient, setCurrentPatient] = useState(null);
    const [matchResult, setMatchResult] = useState(null);
    const [targetPatientId, setTargetPatientId] = useState(null); // The ID to match against
    const [history, setHistory] = useState([]);

    const handleSearch = async (criteria) => {
        setLoading(true);
        setError(null);
        try {
            const results = await searchPatients(criteria);
            // Just take the first result for simplicity in this demo flow if multiple returned
            // Or pass list to a selection view. For now, let's assume specific search.
            if (results.length > 0) {
                setSearchData(results[0]);
                setCurrentPatient(results[0]);
            } else {
                setSearchData(null);
                setCurrentPatient(null);
                setError("No patient found");
            }
        } catch (err) {
            setError("Failed to search patients");
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    const handleMatchClick = async () => {
        if (!currentPatient) return;
        setLoading(true);
        setError(null);

        try {
            // Hardcoded target selection for Demo Flow as per guide (Select HB001)
            // In a real app, this would be a selection from a list of candidates.
            const targetId = "HB001";
            setTargetPatientId(targetId);

            const result = await matchPatients(currentPatient.id, targetId);
            setMatchResult(result);
            setStep('match');
        } catch (err) {
            setError("Matching failed: " + err.message);
        } finally {
            setLoading(false);
        }
    };

    const handleHistoryClick = async () => {
        if (!currentPatient) return;
        setLoading(true);
        setError(null);

        try {
            // Fetch source patient history (Hospital A)
            const visitsA = await getPatientHistory(currentPatient.id, 'A');

            // Fetch target patient history (Hospital B) if we have a match target
            let visitsB = [];
            if (targetPatientId) {
                try {
                    visitsB = await getPatientHistory(targetPatientId, 'B');
                } catch (e) {
                    console.warn("Could not fetch target history", e);
                    // Continue even if B fails, just show A
                }
            }

            // Combine and sort by date descending
            const combinedHistory = [...visitsA, ...visitsB].sort((a, b) => {
                // Date strings might be empty if invalid
                const dateA = a.date ? new Date(a.date) : new Date(0);
                const dateB = b.date ? new Date(b.date) : new Date(0);
                return dateB - dateA;
            });

            setHistory(combinedHistory);
            setStep('history');
        } catch (err) {
            setError("Failed to load history");
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    // Derived state for MatchResults component
    // It expects sourcePatient, targetPatient, matchData
    // We have currentPatient (source). We need targetPatient object.
    // matchResult contains details but maybe not full patient object?
    // Let's modify MatchResults if needed or fetch target patient details.

    // Actually, matchResult from backend returns:
    // { match_score, ... details: { ... } }
    // It doesn't return the full patient objects B.
    // But we fetched them in `matchPatients` client method!
    // We might need to store them.

    // Simplified for now: We pass what we have.
    // Ideally we should update MatchResults to accept the structure we have.

    return (
        <div className="min-h-screen bg-transparent p-4 md:p-8 font-sans text-gray-800">
            <div className="max-w-5xl mx-auto">
                <header className="mb-12 text-center animate-fade-in-down">
                    <h1 className="text-6xl font-extrabold tracking-tighter mb-2">
                        <span className="bg-clip-text text-transparent bg-gradient-to-r from-blue-600 to-indigo-600 drop-shadow-sm">
                            PRAISA
                        </span>
                    </h1>
                    <p className="text-slate-600 text-xl font-medium tracking-wide">AI-Powered Healthcare Interoperability Platform</p>
                </header>

                {error && (
                    <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative mb-4" role="alert">
                        <span className="block sm:inline">{error}</span>
                    </div>
                )}

                {step === 'search' && (
                    <div className="animate-fade-in-up">
                        <SearchForm onSearch={handleSearch} isLoading={loading} />

                        {loading && <div className="text-center mt-4">Loading...</div>}

                        {!loading && searchData && (
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
                                                <td className="p-3 border-b">{searchData.id}</td>
                                                <td className="p-3 border-b font-medium text-gray-900">{searchData.name}</td>
                                                <td className="p-3 border-b">{searchData.dob}</td>
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

                {(step === 'match' || step === 'history') && matchResult && (
                    <div className="animate-fade-in">
                        <MatchResults
                            sourcePatient={currentPatient}
                            targetPatient={{ id: "HB001", name: "Ramehs Singh", dob: "1985-03-15", abha_number: currentPatient.abha_number }} // Mock target for display
                            matchData={matchResult}
                            onHistoryClick={handleHistoryClick}
                        />
                    </div>
                )}

                {step === 'history' && (
                    <div className="animate-slide-in-bottom">
                        <UnifiedHistory history={history} />
                    </div>
                )}

                {step !== 'search' && (
                    <div className="mt-12 text-center pb-8">
                        <button
                            onClick={() => { setStep('search'); setSearchData(null); setCurrentPatient(null); setMatchResult(null); }}
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
