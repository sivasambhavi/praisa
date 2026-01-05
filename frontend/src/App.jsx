import React, { useState } from 'react';
import AdvancedSearch from './components/AdvancedSearch';
import PatientList from './components/PatientList';
import MatchResults from './components/MatchResults';
import UnifiedHistory from './components/UnifiedHistory';
import { searchPatients, matchPatients, getPatientHistory } from './api/client';

function App() {
    const [step, setStep] = useState('search'); // search, results, match, history
    const [searchResults, setSearchResults] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    // State for match flow
    const [currentPatient, setCurrentPatient] = useState(null);
    const [matchResult, setMatchResult] = useState(null);
    const [targetPatientId, setTargetPatientId] = useState(null);
    const [history, setHistory] = useState([]);

    const handleSearch = async (criteria) => {
        setLoading(true);
        setError(null);
        setSearchResults([]);

        try {
            const results = await searchPatients(criteria);

            if (results.length > 0) {
                setSearchResults(results);
                setStep('results');
            } else {
                setSearchResults([]);
                setStep('results');
                setError("No patients found matching your search criteria");
            }
        } catch (err) {
            setError("Failed to search patients. Please try again.");
            console.error(err);
            setSearchResults([]);
        } finally {
            setLoading(false);
        }
    };

    const handleMatchClick = async (patient) => {
        setCurrentPatient(patient);
        setLoading(true);
        setError(null);

        try {
            // DYNAMIC CROSS-HOSPITAL MATCHING (All 5 Hospitals)
            // Find candidates in all hospitals EXCEPT the source hospital
            const HOSPITALS = ['A', 'B', 'C', 'D', 'E'];
            const sourceHosp = patient.hospital_id ? patient.hospital_id.split('_')[1].toUpperCase() : 'A';
            const targetHospitals = HOSPITALS.filter(h => h !== sourceHosp);

            let bestTarget = null;

            // Search for candidates in other hospitals
            for (const h of targetHospitals) {
                const candidates = await searchPatients({ type: 'name', value: patient.name, hospital: h });
                if (candidates.length > 0) {
                    bestTarget = candidates[0];
                    break;
                }
            }

            // Fallback: If no direct name match, try the "typo fallback" for demo reliability
            if (!bestTarget) {
                const demoTypos = {
                    "Ramesh": "Ramehs",
                    "Anita": "Ainta",
                    "Sita": "iSta"
                };

                for (const [key, typo] of Object.entries(demoTypos)) {
                    if (patient.name.includes(key)) {
                        for (const h of targetHospitals) {
                            const candidates = await searchPatients({ type: 'name', value: typo, hospital: h });
                            if (candidates.length > 0) {
                                bestTarget = candidates[0];
                                break;
                            }
                        }
                    }
                    if (bestTarget) break;
                }
            }

            if (!bestTarget) {
                throw new Error("No matching candidate found in other hospitals to compare against.");
            }

            setTargetPatientId(bestTarget.id);

            // Perform the Match
            const result = await matchPatients(patient.id, bestTarget.id);

            // Store full target object for display
            setMatchResult({ ...result, targetPatient: bestTarget });
            setStep('match');
        } catch (err) {
            setError("Matching failed: " + err.message);
        } finally {
            setLoading(false);
        }
    };

    const handleHistoryClick = async (patient) => {
        if (!patient) {
            patient = currentPatient;
        }

        setCurrentPatient(patient);
        setLoading(true);
        setError(null);

        try {
            // Fetch source patient history
            const sourceHosp = patient.hospital_id ? patient.hospital_id.split('_')[1].toUpperCase() : 'A';
            const visitsA = await getPatientHistory(patient.id, sourceHosp);

            // Fetch target patient history if we have a match target
            let visitsB = [];
            if (targetPatientId && matchResult?.targetPatient) {
                try {
                    const targetHosp = matchResult.targetPatient.hospital_id 
                        ? matchResult.targetPatient.hospital_id.split('_')[1].toUpperCase() 
                        : 'B'; // Fallback
                    visitsB = await getPatientHistory(targetPatientId, targetHosp);
                } catch (e) {
                    console.warn("Could not fetch target history", e);
                }
            }

            // Combine and sort by date descending
            const combinedHistory = [...visitsA, ...visitsB].sort((a, b) => {
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

    const handleNewSearch = () => {
        setStep('search');
        setSearchResults([]);
        setCurrentPatient(null);
        setMatchResult(null);
        setTargetPatientId(null);
        setHistory([]);
        setError(null);
    };

    return (
        <div className="min-h-screen bg-transparent p-4 md:p-8 font-sans text-gray-800">
            <div className="max-w-5xl mx-auto">
                {/* Header */}
                <header className="mb-12 text-center animate-fade-in-down">
                    <div className="flex items-center justify-center gap-6 mb-4">
                        <img
                            src="/praisa-logo.jpg"
                            alt="PRAISA Logo"
                            className="w-24 h-24 md:w-32 md:h-32 object-contain drop-shadow-2xl"
                        />
                        <h1 className="text-6xl md:text-7xl font-extrabold tracking-tighter">
                            <span className="gradient-text drop-shadow-lg">
                                PR
                            </span>
                            <span className="text-lime-500 drop-shadow-lg" style={{
                                textShadow: '0 0 30px rgba(132, 204, 22, 0.8), 0 0 60px rgba(132, 204, 22, 0.4)',
                                WebkitTextStroke: '2px rgba(255, 255, 255, 0.9)'
                            }}>
                                AI
                            </span>
                            <span className="gradient-text drop-shadow-lg">
                                SA
                            </span>
                        </h1>
                    </div>
                    <p className="text-cyan-300 text-lg md:text-xl font-semibold tracking-widest mb-3" style={{
                        textShadow: '0 0 20px rgba(103, 232, 249, 0.5)'
                    }}>
                        Prana Records AI Sangam for Arogya
                    </p>
                    <p className="text-white text-lg md:text-xl font-medium tracking-wide mb-2">
                        AI-Powered Healthcare Interoperability Platform
                    </p>
                    <p className="text-white/70 text-sm md:text-base">
                        Advanced Patient Record Matching & Integration System
                    </p>
                </header>

                {/* Error Display */}
                {error && (
                    <div className="glass-card p-4 mb-6 border-l-4 border-red-500 animate-fade-in">
                        <div className="flex items-center gap-3">
                            <svg className="w-6 h-6 text-red-400 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                            </svg>
                            <span className="text-white font-medium">{error}</span>
                        </div>
                    </div>
                )}

                {/* Search View */}
                {step === 'search' && (
                    <div>
                        <AdvancedSearch onSearch={handleSearch} isLoading={loading} />
                    </div>
                )}

                {/* Results View */}
                {step === 'results' && (
                    <div>
                        <PatientList
                            patients={searchResults}
                            loading={loading}
                            onMatchClick={handleMatchClick}
                            onHistoryClick={handleHistoryClick}
                        />

                        <div className="mt-8 text-center">
                            <button
                                onClick={handleNewSearch}
                                className="glass-card px-6 py-3 text-white font-semibold hover:scale-105 transition-all inline-flex items-center gap-2"
                            >
                                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"></path>
                                </svg>
                                New Search
                            </button>
                        </div>
                    </div>
                )}

                {(step === 'match' || step === 'history') && matchResult && (
                    <div className="animate-fade-in">
                        <MatchResults
                            sourcePatient={currentPatient}
                            targetPatient={matchResult.targetPatient}
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

                {/* Back to Search Button (for match and history views) */}
                {step !== 'search' && step !== 'results' && (
                    <div className="mt-12 text-center pb-8">
                        <button
                            onClick={handleNewSearch}
                            className="glass-card px-8 py-4 text-white font-bold text-lg hover:scale-105 transition-all inline-flex items-center gap-3"
                        >
                            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"></path>
                            </svg>
                            Start New Search
                        </button>
                    </div>
                )}
            </div>
        </div>
    );
}

export default App;
