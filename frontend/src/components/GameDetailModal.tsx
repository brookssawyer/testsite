'use client';

import React, { useState, useEffect } from 'react';
import TrendsView from './TrendsView';

interface GameDetailModalProps {
  gameId: string;
  gameTitle?: string;
  onClose: () => void;
}

interface AISummary {
  summary: string;
  recommendation: string;
  reasoning: string;
  timestamp: string;
}

export default function GameDetailModal({ gameId, gameTitle, onClose }: GameDetailModalProps) {
  const [aiSummary, setAiSummary] = useState<AISummary | null>(null);
  const [loadingAI, setLoadingAI] = useState(false);
  const [aiError, setAiError] = useState<string | null>(null);

  // Close on Escape key
  useEffect(() => {
    const handleEscape = (e: KeyboardEvent) => {
      if (e.key === 'Escape') onClose();
    };
    window.addEventListener('keydown', handleEscape);
    return () => window.removeEventListener('keydown', handleEscape);
  }, [onClose]);

  // Prevent body scroll when modal is open
  useEffect(() => {
    document.body.style.overflow = 'hidden';
    return () => {
      document.body.style.overflow = 'unset';
    };
  }, []);

  // Fetch AI Summary
  const fetchAISummary = async () => {
    setLoadingAI(true);
    setAiError(null);

    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
      const response = await fetch(`${apiUrl}/api/games/${gameId}/ai-summary`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        throw new Error(`Failed to generate AI summary: ${response.statusText}`);
      }

      const data = await response.json();
      setAiSummary(data);
    } catch (error) {
      console.error('Error fetching AI summary:', error);
      setAiError(error instanceof Error ? error.message : 'Failed to generate AI summary');
    } finally {
      setLoadingAI(false);
    }
  };

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-sm"
      onClick={onClose}
    >
      <div
        className="bg-gray-800 rounded-lg shadow-2xl border-2 border-gray-700 w-full max-w-7xl max-h-[90vh] overflow-y-auto"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className="sticky top-0 bg-gray-800 border-b border-gray-700 px-6 py-4 flex justify-between items-center z-10">
          <h2 className="text-xl font-bold text-white">
            {gameTitle || 'Game Details'}
          </h2>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-white transition-colors text-2xl font-bold px-3 py-1 hover:bg-gray-700 rounded"
            aria-label="Close modal"
          >
            ×
          </button>
        </div>

        {/* Content */}
        <div className="p-6 space-y-6">
          {/* AI Betting Summary Section */}
          <div className="bg-gray-900 rounded-lg p-6 border border-gray-700">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-bold text-white flex items-center">
                <svg className="w-6 h-6 mr-2 text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                </svg>
                AI Betting Analysis
              </h3>
              <button
                onClick={fetchAISummary}
                disabled={loadingAI}
                className="px-4 py-2 bg-purple-600 hover:bg-purple-700 disabled:bg-gray-600 text-white rounded-lg font-medium transition-colors flex items-center"
              >
                {loadingAI ? (
                  <>
                    <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-white" fill="none" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    Generating...
                  </>
                ) : (
                  <>
                    <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                    </svg>
                    Generate Summary
                  </>
                )}
              </button>
            </div>

            {aiError && (
              <div className="bg-red-900/50 border border-red-700 rounded-lg p-4 text-red-200 mb-4">
                <p className="font-medium">Error generating AI summary</p>
                <p className="text-sm mt-1">{aiError}</p>
              </div>
            )}

            {aiSummary ? (
              <div className="space-y-4">
                <div className="prose prose-invert max-w-none">
                  <div className="bg-gray-800 rounded-lg p-4 whitespace-pre-wrap text-gray-200">
                    {aiSummary.summary}
                  </div>
                </div>
                <div className="text-xs text-gray-400 text-right">
                  Generated {new Date(aiSummary.timestamp).toLocaleString()}
                </div>
              </div>
            ) : (
              <div className="text-gray-400 text-center py-8">
                <svg className="w-16 h-16 mx-auto mb-4 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                </svg>
                <p className="text-lg">Click Generate Summary to get AI-powered betting analysis</p>
                <p className="text-sm mt-2">Analyzes game state, team metrics, and betting situation to provide intelligent recommendations</p>
              </div>
            )}
          </div>

          {/* Trends View */}
          <TrendsView preSelectedGameId={gameId} hideSelector={true} />
        </div>
      </div>
    </div>
  );
}
