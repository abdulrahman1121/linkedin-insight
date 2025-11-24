/**
 * Landing Page Hero Section
 */

import { Button } from '@/components/ui/button';
import { ArrowRight, Sparkles, Target, TrendingUp } from 'lucide-react';
import Link from 'next/link';

export function LandingHero() {
  return (
    <section className="relative overflow-hidden bg-gradient-to-b from-background to-muted/20 py-20 md:py-32">
      <div className="container mx-auto px-4">
        <div className="mx-auto max-w-3xl text-center">
          <div className="mb-6 inline-flex items-center gap-2 rounded-full border bg-background px-4 py-2 text-sm">
            <Sparkles className="h-4 w-4 text-primary" />
            <span className="text-muted-foreground">AI-powered career navigation</span>
          </div>
          
          <h1 className="mb-6 text-4xl font-bold tracking-tight sm:text-5xl md:text-6xl lg:text-7xl">
            AI-powered career path &{' '}
            <span className="bg-gradient-to-r from-primary to-primary/60 bg-clip-text text-transparent">
              skills navigator
            </span>
          </h1>
          
          <p className="mb-8 text-lg text-muted-foreground sm:text-xl md:text-2xl">
            Discover your ideal career path, identify skill gaps, and get personalized
            learning roadmaps powered by AI and real-time job market data.
          </p>
          
          <div className="flex flex-col gap-4 sm:flex-row sm:justify-center">
            <Button asChild size="lg" className="text-lg">
              <Link href="/dashboard">
                Get Started
                <ArrowRight className="ml-2 h-5 w-5" />
              </Link>
            </Button>
            <Button asChild variant="outline" size="lg" className="text-lg">
              <Link href="#features">Learn More</Link>
            </Button>
          </div>
        </div>
      </div>
    </section>
  );
}

