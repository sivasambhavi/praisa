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

    return (
        <div className="bg-white/90 backdrop-blur-xl p-8 rounded-3xl shadow-2xl border border-white/50 animate-fade-in-up">
            <div className="text-center mb-10">
                <span className="bg-green-100 text-green-800 text-xs font-bold px-3 py-1 rounded-full uppercase tracking-widest border border-green-200">
                    AI Match Found
                </span>
                <h2 className="text-3xl font-extrabold mt-4 text-gray-900">Patient Identity Match</h2>
            </div>

            <div className="flex flex-col lg:flex-row justify-center items-stretch gap-8 relative">

                {/* Source Patient Card */}
                <div className="flex-1 bg-gradient-to-br from-blue-50 to-white p-6 rounded-2xl border border-blue-100 shadow-sm relative overflow-hidden group hover:shadow-md transition-all">
                    <div className="absolute top-0 right-0 p-4 opacity-10 group-hover:opacity-20 transition-opacity">
                        <svg className="w-24 h-24 text-blue-600" fill="currentColor" viewBox="0 0 24 24"><path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-7 3c1.93 0 3.5 1.57 3.5 3.5S13.93 13 12 13s-3.5-1.57-3.5-3.5S10.07 6 12 6zm7 13H5v-.23c0-.62.28-1.2.76-1.58C7.47 15.82 9.64 15 12 15s4.53.82 6.24 2.19c.48.38.76.97.76 1.58V19z" /></svg>
                    </div>
                    <div className="text-xs font-bold text-blue-600 uppercase tracking-widest mb-1">Source Record</div>
                    <div className="text-2xl font-bold text-gray-900 mb-4">{sourcePatient.name}</div>

                    <div className="space-y-3">
                        <div className="flex justify-between border-b border-blue-100 pb-2">
                            <span className="text-gray-500 text-sm">Hospital ID</span>
                            <span className="font-mono font-medium text-gray-700 bg-white px-2 rounded border border-gray-100">{sourcePatient.id}</span>
                        </div>
                        <div className="flex justify-between border-b border-blue-100 pb-2">
                            <span className="text-gray-500 text-sm">ABHA No</span>
                            <span className="font-mono font-medium text-gray-700">{sourcePatient.abha_number}</span>
                        </div>
                        <div className="flex justify-between pb-2">
                            <span className="text-gray-500 text-sm">DOB</span>
                            <span className="font-medium text-gray-700">{sourcePatient.dob}</span>
                        </div>
                    </div>
                    <div className="mt-6 flex items-center gap-2 text-blue-700 bg-blue-100/50 p-2 rounded-lg">
                        <div className="w-2 h-2 rounded-full bg-blue-500"></div>
                        <span className="text-xs font-semibold">Hospital A (Apollo)</span>
                    </div>
                </div>

                {/* Match Score Center */}
                <div className="flex flex-col items-center justify-center min-w-[200px] z-10">
                    <div className="relative w-40 h-40">
                        {/* Outer Glow */}
                        <div className={`absolute inset-0 rounded-full blur-xl opacity-20 ${score >= 90 ? 'bg-green-500' : 'bg-yellow-500'}`}></div>

                        <svg className="w-full h-full transform -rotate-90 drop-shadow-lg" viewBox="0 0 100 100">
                            <circle cx="50" cy="50" r="45" fill="none" stroke="#f1f5f9" strokeWidth="8" />
                            <circle
                                cx="50" cy="50" r="45"
                                fill="none"
                                stroke="url(#gradient)"
                                strokeWidth="8"
                                strokeDasharray={`${score * 2.827} 282.7`}
                                strokeLinecap="round"
                                className="transition-all duration-[1500ms] ease-out"
                            />
                            <defs>
                                <linearGradient id="gradient" x1="0%" y1="0%" x2="100%" y2="0%">
                                    <stop offset="0%" stopColor="#3b82f6" />
                                    <stop offset="100%" stopColor="#10b981" />
                                </linearGradient>
                            </defs>
                        </svg>
                        <div className="absolute inset-0 flex flex-col items-center justify-center">
                            <span className="text-4xl font-black text-gray-800 tracking-tighter">{score}%</span>
                            <span className="text-[10px] font-bold text-gray-400 uppercase tracking-widest mt-1">Match Score</span>
                        </div>
                    </div>
                    <div className="mt-4 text-center">
                        <div className="text-sm font-bold text-gray-600 bg-white px-4 py-1 rounded-full shadow-sm border border-gray-100 inline-block">
                            {matchData.method || "Phonetic Analysis"}
                        </div>
                    </div>
                </div>

                {/* Target Patient Card */}
                <div className="flex-1 bg-gradient-to-br from-green-50 to-white p-6 rounded-2xl border border-green-100 shadow-sm relative overflow-hidden group hover:shadow-md transition-all">
                    <div className="absolute top-0 right-0 p-4 opacity-10 group-hover:opacity-20 transition-opacity">
                        <svg className="w-24 h-24 text-green-600" fill="currentColor" viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 3c1.66 0 3 1.34 3 3s-1.34 3-3 3-3-1.34-3-3 1.34-3 3-3zm0 14.2c-2.5 0-4.71-1.28-6-3.22.03-1.99 4-3.08 6-3.08 1.99 0 5.97 1.09 6 3.08-1.29 1.94-3.5 3.22-6 3.22z" /></svg>
                    </div>
                    <div className="text-xs font-bold text-green-600 uppercase tracking-widest mb-1">Target Record</div>
                    <div className="text-2xl font-bold text-gray-900 mb-4">
                        {targetPatient.name.split('').map((char, i) => (
                            sourcePatient.name[i] !== char ? <span key={i} className="text-red-500 bg-red-50">{char}</span> : char
                        ))}
                    </div>

                    <div className="space-y-3">
                        <div className="flex justify-between border-b border-green-100 pb-2">
                            <span className="text-gray-500 text-sm">Hospital ID</span>
                            <span className="font-mono font-medium text-gray-700 bg-white px-2 rounded border border-gray-100">{targetPatient.id}</span>
                        </div>
                        <div className="flex justify-between border-b border-green-100 pb-2">
                            <span className="text-gray-500 text-sm">ABHA No</span>
                            <span className="font-mono font-medium text-gray-700">{targetPatient.abha_number}</span>
                        </div>
                        <div className="flex justify-between pb-2">
                            <span className="text-gray-500 text-sm">DOB</span>
                            <span className="font-medium text-gray-700">{targetPatient.dob}</span>
                        </div>
                    </div>
                    <div className="mt-6 flex items-center gap-2 text-green-700 bg-green-100/50 p-2 rounded-lg">
                        <div className="w-2 h-2 rounded-full bg-green-500"></div>
                        <span className="text-xs font-semibold">Hospital B (Max)</span>
                    </div>
                </div>
            </div>

            <div className="mt-12 flex justify-center">
                <button
                    onClick={onHistoryClick}
                    className="group relative bg-gray-900 text-white px-10 py-4 rounded-xl text-lg font-bold shadow-xl hover:shadow-2xl hover:-translate-y-1 transition-all overflow-hidden"
                >
                    <span className="relative z-10 flex items-center gap-3">
                        View Unified Medical History
                        <svg className="w-5 h-5 group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M14 5l7 7m0 0l-7 7m7-7H3"></path></svg>
                    </span>
                    <div className="absolute inset-0 bg-gradient-to-r from-blue-600 to-indigo-600 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
                </button>
            </div>
        </div>
    );
};

export default MatchResults;
