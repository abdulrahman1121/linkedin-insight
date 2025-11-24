/**
 * Landing Page Features Section
 */

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Brain, Network, Target } from 'lucide-react';

const features = [
  {
    icon: Brain,
    title: 'AI-Powered Insights',
    description: 'Get personalized career recommendations and skill gap analysis powered by advanced AI models.',
  },
  {
    icon: Network,
    title: 'Skills Graph',
    description: 'Visualize skill prerequisites and dependencies to plan your learning journey effectively.',
  },
  {
    icon: Target,
    title: 'Learning Roadmaps',
    description: 'Receive detailed 4-week learning plans tailored to your career goals and current skills.',
  },
];

export function LandingFeatures() {
  return (
    <section id="features" className="py-20 md:py-32 bg-gray-50">
      <div className="container mx-auto px-4">
        <div className="mx-auto max-w-2xl text-center mb-12">
          <h2 className="text-3xl font-bold tracking-tight text-gray-900 sm:text-4xl mb-4">
            Everything you need to advance your career
          </h2>
          <p className="text-lg text-gray-600">
            Powerful tools to help you navigate your career path and achieve your professional goals.
          </p>
        </div>
        
        <div className="grid gap-6 md:grid-cols-3">
          {features.map((feature) => {
            const Icon = feature.icon;
            return (
              <Card 
                key={feature.title} 
                className="border border-gray-200 hover:border-[#0077B5] hover:shadow-lg transition-all bg-white"
              >
                <CardHeader>
                  <div className="mb-4 flex h-12 w-12 items-center justify-center rounded-lg bg-[#0077B5]/10">
                    <Icon className="h-6 w-6 text-[#0077B5]" />
                  </div>
                  <CardTitle className="text-gray-900">{feature.title}</CardTitle>
                </CardHeader>
                <CardContent>
                  <CardDescription className="text-base text-gray-600">
                    {feature.description}
                  </CardDescription>
                </CardContent>
              </Card>
            );
          })}
        </div>
      </div>
    </section>
  );
}

