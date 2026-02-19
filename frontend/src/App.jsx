import { useState } from 'react';
import { Coffee } from 'lucide-react';
import UploadSection from './components/UploadSection';
import GallerySection from './components/GallerySection';

function App() {
  const [refreshGallery, setRefreshGallery] = useState(0);

  const handleUploadSuccess = () => {
    // Trigger gallery refresh after successful upload (if it was Real or Review)
    setRefreshGallery(prev => prev + 1);
  };

  return (
    <div className="min-h-screen bg-crime-black text-gray-200 overflow-x-hidden">
      {/* Header */}
      <header className="border-b border-gray-800 p-6 bg-black/50 backdrop-blur sticky top-0 z-50">
        <div className="max-w-6xl mx-auto flex items-center justify-between">
          <h1 className="text-2xl font-mono font-bold tracking-tighter text-white">
            <Coffee className="text-terminal-green mr-2 w-8 h-8" />
            CHAI<span className="text-gray-500">.AI</span>
          </h1>
          <div className="flex gap-4 text-xs font-mono text-gray-500">
            <span>SYS.STATUS: ONLINE</span>
            <span>SEC.LEVEL: HIGH</span>
          </div>
        </div>
      </header>

      <main className="py-12 px-4 gap-12 flex flex-col">
        {/* Hero / Upload Section */}
        <section className="w-full">
          <UploadSection onUploadSuccess={handleUploadSuccess} />
        </section>

        {/* Gallery Section */}
        <section className="w-full bg-black/20 py-10 rounded-3xl border-t border-gray-900">
          <GallerySection refreshTrigger={refreshGallery} />
        </section>
      </main>

      <footer className="border-t border-gray-900 py-8 text-center text-gray-600 font-mono text-sm">
        <p>SECURE IMAGE ANALYSIS SYSTEM v1.0</p>
      </footer>
    </div>
  );
}

export default App;
