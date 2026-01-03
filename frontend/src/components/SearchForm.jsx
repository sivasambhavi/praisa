import React, { useState } from 'react';

const SearchForm = ({ onSearch }) => {
    const [name, setName] = useState('');
    const [hospital, setHospital] = useState('A');

    const handleSubmit = (e) => {
        e.preventDefault();
        onSearch({ name, hospital });
    };

    return (
        <div className="bg-white p-6 rounded-lg shadow-md mb-8">
            <h2 className="text-xl font-semibold mb-4 text-gray-800">Search Patients</h2>
            <form onSubmit={handleSubmit} className="flex gap-4 items-end">
                <div className="flex-1">
                    <label className="block text-sm font-medium text-gray-700 mb-1">Patient Name</label>
                    <input
                        type="text"
                        className="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                        placeholder="e.g. Ramesh Singh"
                        value={name}
                        onChange={(e) => setName(e.target.value)}
                        required
                    />
                </div>
                <div className="w-48">
                    <label className="block text-sm font-medium text-gray-700 mb-1">Hospital</label>
                    <select
                        className="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                        value={hospital}
                        onChange={(e) => setHospital(e.target.value)}
                    >
                        <option value="A">Hospital A</option>
                        <option value="B">Hospital B</option>
                    </select>
                </div>
                <button
                    type="submit"
                    className="bg-blue-600 text-white px-6 py-2 rounded-md hover:bg-blue-700 transition-colors font-medium"
                >
                    Search
                </button>
            </form>
        </div>
    );
};

export default SearchForm;
