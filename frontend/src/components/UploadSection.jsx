import { useState, useEffect } from 'react';
import axios from 'axios';
import { motion, AnimatePresence } from 'framer-motion';
import { Upload, AlertTriangle, CheckCircle, ShieldAlert, Loader2 } from 'lucide-react';
import clsx from 'clsx';

const ANALYSIS_STEPS = [
    "Analyzing Pixels...",
    "Analyzing Metadata...",
    "Testing File Integrity...",
    "Analyzing CFA Pattern...",
    "Cross-Referencing GenAI Models...",
    "Finalizing Verdict..."
];

export default function UploadSection({ onUploadSuccess }) {
    const [file, setFile] = useState(null);
    const [isAnalyzing, setIsAnalyzing] = useState(false);
    const [analysisStep, setAnalysisStep] = useState(0);
    const [result, setResult] = useState(null);
    const [error, setError] = useState(null);

    useEffect(() => {
        let interval;
        if (isAnalyzing && analysisStep < ANALYSIS_STEPS.length - 1) {
            interval = setInterval(() => {
                setAnalysisStep((prev) => (prev + 1) % ANALYSIS_STEPS.length);
            }, 800);
        }
        return () => clearInterval(interval);
    }, [isAnalyzing, analysisStep]);

    const handleFileChange = (e) => {
        if (e.target.files && e.target.files[0]) {
            setFile(e.target.files[0]);
            setResult(null);
            setError(null);
        }
    };

    const handleAnalyze = async () => {
        if (!file) return;

        setIsAnalyzing(true);
        setAnalysisStep(0);
        setResult(null);
        setError(null);

        const formData = new FormData();
        formData.append('file', file);

        try {
            // Simulate at least a few seconds of "analysis" for the UX
            const minTime = new Promise(resolve => setTimeout(resolve, 3000));
            const request = axios.post('http://localhost:8000/analyze', formData, {
                headers: { 'Content-Type': 'multipart/form-data' }
            });

            const [_, response] = await Promise.all([minTime, request]);
            setResult(response.data);
            if (onUploadSuccess) onUploadSuccess();
        } catch (err) {
            console.error(err);
            setError("Analysis failed. Please try again.");
        } finally {
            setIsAnalyzing(false);
        }
    };

    const statusColor = result?.db_entry?.final_result === "Real" ? "text-terminal-green border-terminal-green" :
        result?.db_entry?.final_result === "AI Edited" ? "text-warning-yellow border-warning-yellow" :
            "text-alert-red border-alert-red";

    return (
        <div className="w-full max-w-2xl mx-auto p-6 bg-crime-gray rounded-lg border border-gray-700 shadow-xl">
            <h2 className="text-2xl font-bold mb-4 text-center border-b border-gray-700 pb-2">
                AI Image Analysis
            </h2>

            {/* File Input */}
            <div className="flex flex-col items-center justify-center w-full mb-6">
                <label htmlFor="dropzone-file" className="flex flex-col items-center justify-center w-full h-64 border-2 border-gray-600 border-dashed rounded-lg cursor-pointer bg-gray-800 hover:bg-gray-700 transition-colors">
                    <div className="flex flex-col items-center justify-center pt-5 pb-6">
                        {file ? (
                            <div className="text-center">
                                <p className="mb-2 text-sm text-gray-400">Selected File:</p>
                                <p className="text-lg font-semibold text-white">{file.name}</p>
                            </div>
                        ) : (
                            <>
                                <Upload className="w-10 h-10 mb-3 text-gray-400" />
                                <p className="mb-2 text-sm text-gray-400"><span className="font-semibold">Click to upload</span> or drag and drop</p>
                                <p className="text-xs text-gray-500">SVG, PNG, JPG or GIF</p>
                            </>
                        )}
                    </div>
                    <input id="dropzone-file" type="file" className="hidden" onChange={handleFileChange} accept="image/*" />
                </label>
            </div>

            {/* Analyze Button */}
            <div className="flex justify-center mb-6">
                <button
                    onClick={handleAnalyze}
                    disabled={!file || isAnalyzing}
                    className={clsx(
                        "px-6 py-3 rounded font-bold text-black transition-all transform hover:scale-105",
                        isAnalyzing ? "bg-gray-500 cursor-not-allowed" : "bg-terminal-green hover:bg-green-400 shadow-[0_0_10px_rgba(0,255,0,0.5)]"
                    )}
                >
                    {isAnalyzing ? (
                        <span className="flex items-center gap-2">
                            <Loader2 className="animate-spin" /> Analyzing...
                        </span>
                    ) : "Start Analysis"}
                </button>
            </div>

            {/* Analysis status text */}
            <AnimatePresence mode="wait">
                {isAnalyzing && (
                    <motion.div
                        key="analyzing-text"
                        initial={{ opacity: 0, y: 10 }}
                        animate={{ opacity: 1, y: 0 }}
                        exit={{ opacity: 0, y: -10 }}
                        className="text-center font-mono text-terminal-green mb-4"
                    >
                        {`> ${ANALYSIS_STEPS[analysisStep]}`}
                    </motion.div>
                )}
            </AnimatePresence>

            {/* Results: Error Case */}
            {result && (result.status === 'error' || !result.db_entry) && (
                <div className="p-4 bg-red-900/50 border border-red-500 text-red-200 rounded text-center">
                    <h3 className="font-bold text-lg mb-2">Analysis Error</h3>
                    <p>{result.message || "Unknown error occurred during analysis"}</p>
                    {result.raw && (
                        <div className="mt-2 text-left">
                            <p className="text-xs text-gray-400 mb-1">Raw Output:</p>
                            <pre className="text-xs bg-black p-2 overflow-auto max-h-40 whitespace-pre-wrap">{result.raw}</pre>
                        </div>
                    )}
                </div>
            )}

            {/* Results: Success Case */}
            {result && result.status === 'success' && result.db_entry && (
                <motion.div
                    initial={{ opacity: 0, scale: 0.9 }}
                    animate={{ opacity: 1, scale: 1 }}
                    className={clsx("p-6 rounded-lg border-2 text-center", statusColor)}
                >
                    <div className="flex justify-center mb-4">
                        {result.db_entry.final_result === "Real" ? <CheckCircle className="w-16 h-16" /> :
                            result.db_entry.final_result === "AI Edited" ? <AlertTriangle className="w-16 h-16" /> :
                                <ShieldAlert className="w-16 h-16" />}
                    </div>

                    <h3 className="text-3xl font-black uppercase mb-2">
                        {result.db_entry.final_result === "AI Generated" ? "UPLOAD BLOCKED" :
                            result.db_entry.final_result === "AI Edited" ? "UNDER REVIEW" :
                                "UPLOAD SUCCESSFUL"}
                    </h3>

                    <p className="text-xl mb-4 text-white">
                        Verdict: <span className="font-bold">{result.db_entry.final_result}</span>
                    </p>

                    <div className="text-left bg-black p-4 rounded text-sm font-mono text-gray-300">
                        <p><span className="text-gray-500">AI Score:</span> {(result.db_entry.ai_generated_score * 100).toFixed(1)}%</p>
                        <p className="mt-2"><span className="text-gray-500">Reasoning:</span> {result.db_entry.forensic_summary}</p>
                    </div>
                </motion.div>
            )}

            {error && (
                <div className="p-4 bg-red-900/50 border border-red-500 text-red-200 rounded text-center">
                    {error}
                </div>
            )}
        </div>
    );
}
