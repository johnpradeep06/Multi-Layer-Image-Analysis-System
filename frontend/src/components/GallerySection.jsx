import { useState, useEffect } from 'react';
import axios from 'axios';
import clsx from 'clsx';
import { RefreshCw } from 'lucide-react';

export default function GallerySection({ refreshTrigger }) {
    const [tab, setTab] = useState('real'); // 'real' | 'review'
    const [images, setImages] = useState([]);
    const [loading, setLoading] = useState(false);

    const fetchImages = async () => {
        setLoading(true);
        try {
            const endpoint = tab === 'real' ? '/gallery/real' : '/gallery/review';
            const response = await axios.get(`https://ai-image-detector-backend-3c7f.onrender.com${endpoint}`);
            setImages(response.data);
        } catch (err) {
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchImages();
    }, [tab, refreshTrigger]);

    return (
        <div className="w-full max-w-6xl mx-auto p-6">
            <div className="flex justify-between items-center mb-6">
                <h2 className="text-3xl font-bold text-white flex items-center gap-3">
                    <span className="text-terminal-green">#</span> Public Gallery
                </h2>
                <button onClick={fetchImages} className="p-2 hover:bg-gray-800 rounded-full transition-colors">
                    <RefreshCw className={clsx("w-5 h-5", loading && "animate-spin")} />
                </button>
            </div>

            {/* Tabs */}
            <div className="flex gap-4 mb-8 border-b border-gray-700 pb-1">
                <button
                    onClick={() => setTab('real')}
                    className={clsx(
                        "px-4 py-2 font-mono text-lg transition-colors border-b-2",
                        tab === 'real' ? "text-terminal-green border-terminal-green" : "text-gray-500 border-transparent hover:text-gray-300"
                    )}
                >
                    VERIFIED REAL
                </button>
                <button
                    onClick={() => setTab('review')}
                    className={clsx(
                        "px-4 py-2 font-mono text-lg transition-colors border-b-2",
                        tab === 'review' ? "text-warning-yellow border-warning-yellow" : "text-gray-500 border-transparent hover:text-gray-300"
                    )}
                >
                    UNDER REVIEW
                </button>
            </div>

            {/* Grid */}
            {/* Loading State */}
            {loading ? (
                <div className="flex justify-center items-center h-64">
                    <div className="relative">
                        <div className="w-16 h-16 border-4 border-gray-800 border-t-terminal-green rounded-full animate-spin"></div>
                        <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 text-terminal-green text-xs font-mono">
                            LOAD
                        </div>
                    </div>
                </div>
            ) : (
                <>
                    {/* Grid */}
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                        {images.map((img) => (
                            <div key={img.id} className="bg-crime-gray border border-gray-800 rounded-lg overflow-hidden hover:border-gray-600 transition-all group">
                                <div className="relative aspect-video bg-black overflow-hidden">
                                    <img
                                        src={`https://ai-image-detector-backend-3c7f.onrender.com/uploads/${img.filename}`}
                                        alt={img.filename}
                                        className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-500"
                                    />
                                    {/* Overlay info */}
                                    <div className="absolute inset-0 bg-gradient-to-t from-black/80 to-transparent opacity-0 group-hover:opacity-100 transition-opacity flex items-end p-4">
                                        <p className="text-xs text-gray-300 font-mono line-clamp-2">
                                            {img.forensic_summary}
                                        </p>
                                    </div>
                                </div>
                                <div className="p-4 flex justify-between items-center">
                                    <span className="text-sm font-mono text-gray-400 truncate max-w-[150px]">{img.filename}</span>
                                    <span className={clsx(
                                        "text-xs font-bold px-2 py-1 rounded",
                                        img.final_result === "Real" ? "bg-green-900/30 text-green-400" : "bg-yellow-900/30 text-yellow-400"
                                    )}>
                                        {img.final_result.toUpperCase()}
                                    </span>
                                </div>
                            </div>
                        ))}
                    </div>

                    {images.length === 0 && (
                        <div className="text-center py-20 text-gray-600">
                            No images found in this category.
                        </div>
                    )}
                </>
            )}
        </div>
    );
}
