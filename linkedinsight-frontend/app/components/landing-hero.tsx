/**
 * Landing Page Hero Section
 */

import { Button } from '@/components/ui/button';
import { ArrowRight, Sparkles, Target, TrendingUp } from 'lucide-react';
import Link from 'next/link';

export function LandingHero() {
  return (
    <section className="relative overflow-hidden bg-gradient-to-b from-white via-blue-50/30 to-white py-20 md:py-32">
      <div className="container mx-auto px-4">
        <div className="mx-auto max-w-3xl text-center">
          <div className="mb-6 inline-flex items-center gap-2 rounded-full border border-blue-200 bg-white px-4 py-2 text-sm shadow-sm">
            <Sparkles className="h-4 w-4 text-[#0077B5]" />
            <span className="text-gray-600 font-medium">AI-powered career navigation</span>
          </div>
          
          <h1 className="mb-6 text-4xl font-bold tracking-tight text-gray-900 sm:text-5xl md:text-6xl lg:text-7xl">
            AI-powered career path &{' '}
            <span className="text-[#0077B5]">
              skills navigator
            </span>
          </h1>
          
          <p className="mb-8 text-lg text-gray-600 sm:text-xl md:text-2xl max-w-2xl mx-auto">
            Discover your ideal career path, identify skill gaps, and get personalized
            learning roadmaps powered by AI and real-time job market data.
          </p>
          
          <div className="flex flex-col gap-4 sm:flex-row sm:justify-center">
            <Button 
              asChild 
              size="lg" 
              className="text-lg bg-[#0077B5] hover:bg-[#004182] text-white font-semibold px-8 py-6 rounded-full shadow-lg hover:shadow-xl transition-all"
            >
              <Link href="/dashboard">
                Get Started
                <ArrowRight className="ml-2 h-5 w-5" />
              </Link>
            </Button>
            <Button 
              asChild 
              variant="outline" 
              size="lg" 
              className="text-lg border-2 border-[#0077B5] text-[#0077B5] hover:bg-[#0077B5] hover:text-white font-semibold px-8 py-6 rounded-full transition-all"
            >
              <Link href="#features">Learn More</Link>
            </Button>
          </div>
        </div>
      </div>
    </section>
  );
}

