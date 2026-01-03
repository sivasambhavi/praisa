import React, { useEffect, useState } from 'react';

const MatchResults = ({ sourcePatient, targetPatient, matchData, onHistoryClick }) => {
    const [score, setScore] = useState(0);

    // Animate score on mount
    useEffect(() => {
        if (matchData?.match_score) {
            const target = matchData.match_score;
            let current = 0;
            const timer = setInterval(() => {
                current += 1;
                if (current >= target) {
                    current = target;
                    clearInterval(timer);
                }
                setScore(current);
            }, 10);
            return () => clearInterval(timer);
        }
    }, [matchData]);

    if (!sourcePatient || !targetPatient || !matchData) return null;

    const getScoreColor = (s) => {
        if (s >= 80) return 'text-green-600';
        if (s >= 60) return 'text-yellow-600';
        return 'text-red-600';
    };

    const getProgressColor = (s) => {
        if (s >= 80) return 'stroke-green-500';
        if (s >= 60) return 'stroke-yellow-500';
        return 'stroke-red-500';
    };

    return (
        <div className="bg-white p-6 rounded-lg shadow-lg border-2 border-blue-100 animate-fade-in">
            <h2 className="text-2xl font-bold mb-6 text-center text-gray-800">Match Analysis</h2>

            <div className="flex flex-col md:flex-row justify-between items-center gap-8">
                {/* Source Patient */}
                <div className="flex-1 bg-blue-50 p-4 rounded-lg w-full">
                    <div className="text-sm text-blue-600 font-bold mb-2">HOSPITAL A</div>
                    <div className="text-xl font-semibold">{sourcePatient.name}</div>
                    <div className="text-gray-600">ID: {sourcePatient.id}</div>
                    <div className="text-gray-600">ABHA: {sourcePatient.abha_number}</div>
                    <div className="text-gray-600">DOB: {sourcePatient.dob}</div>
                </div>

                {/* Match Score */}
                <div className="flex flex-col items-center justify-center p-4">
                    <div className="relative w-32 h-32">
                        <svg className="w-full h-full" viewBox="0 0 36 36">
                            <path
                                d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                                fill="none"
                                stroke="#eee"
                                strokeWidth="3"
                            />
                            <path
                                d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                                fill="none"
                                className={`transition-all duration-1000 ease-out ${getProgressColor(score)}`}
                                strokeWidth="3"
                                strokeDasharray={`${score}, 100`}
                            />
                        </svg>
                        <div className={`absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 text-2xl font-bold ${getScoreColor(score)}`}>
                            {score}%
                        </div>
                    </div>
                    <div className="mt-2 font-semibold text-gray-700">Confidence: HIGH</div>
                    <div className="text-xs text-gray-500 uppercase tracking-wide mt-1">
                        {matchData.method || "Phonetic Match"}
                    </div>
                </div>

                {/* Target Patient */}
                <div className="flex-1 bg-green-50 p-4 rounded-lg w-full">
                    <div className="text-sm text-green-600 font-bold mb-2">HOSPITAL B</div>
                    <div className="text-xl font-semibold">
                        {targetPatient.name.split('').map((char, i) => (
                            // Simple highlighting for demo purposes if names differ
                            sourcePatient.name[i] !== char ? <span key={i} className="text-red-500 font-bold bg-yellow-100">{char}</span> : char
                        ))}
                    </div>
                    <div className="text-gray-600">ID: {targetPatient.id}</div>
                    <div className="text-gray-600">ABHA: {targetPatient.abha_number}</div>
                    <div className="text-gray-600">DOB: {targetPatient.dob}</div>
                </div>
            </div>

            <div className="mt-8 text-center">
                <button
                    onClick={onHistoryClick}
                    className="bg-indigo-600 text-white px-8 py-3 rounded-full text-lg font-bold shadow-lg hover:bg-indigo-700 transform hover:scale-105 transition-all"
                >
                    View Unified History
                </button>
            </div>
        </div>
    );
};

export default MatchResults;
